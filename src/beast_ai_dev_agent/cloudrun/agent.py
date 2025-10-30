"""
Cloud Run Kiro Agent Implementation
Platform-specific implementation for Google Cloud Run
"""

import logging
import os
from typing import Dict, Any
from datetime import datetime

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import uvicorn

from ..common.models import (
    KiroAgentInterface,
    KiroRequest,
    KiroResponse,
    KiroMetrics,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CloudRunKiroAgent(KiroAgentInterface):
    """Cloud Run specific implementation of Kiro Agent"""

    def __init__(self):
        super().__init__(platform="cloudrun")
        self.app = FastAPI(title="Cloud Run Kiro Agent", version="0.1.0")
        self._setup_routes()
        self.port = int(os.getenv("PORT", "8080"))
        logger.info(f"CloudRunKiroAgent initialized on port {self.port}")

    def _setup_routes(self):
        """Setup FastAPI routes"""

        @self.app.get("/health")
        async def health():
            """Health check endpoint for Cloud Run"""
            return await self._health_check_handler()

        @self.app.post("/analyze")
        async def analyze(request: Request):
            """Analysis endpoint"""
            return await self._analyze_handler(request)

        @self.app.get("/metrics")
        async def metrics():
            """Metrics endpoint"""
            return await self._metrics_handler()

        @self.app.get("/")
        async def root():
            """Root endpoint"""
            return {
                "service": "Cloud Run Kiro Agent",
                "platform": "cloudrun",
                "version": "0.1.0",
                "status": "running",
            }

    async def _health_check_handler(self):
        """Handle health check requests"""
        health_data = self.health_check()
        return JSONResponse(content=health_data, status_code=200)

    async def _analyze_handler(self, request: Request):
        """Handle analysis requests"""
        try:
            # Parse request body
            body = await request.json()

            # Create KiroRequest
            kiro_request = KiroRequest(
                data=body,
                headers=dict(request.headers),
                method=request.method,
                path=str(request.url.path),
                query_params=dict(request.query_params),
                timestamp=datetime.utcnow().isoformat(),
            )

            # Process request
            kiro_response = self.process_request(kiro_request)

            # Return response
            return JSONResponse(
                content=kiro_response.data, status_code=kiro_response.status_code
            )

        except Exception as e:
            logger.error(f"Error processing analyze request: {e}")
            return JSONResponse(
                content={"error": str(e), "platform": "cloudrun"},
                status_code=500,
            )

    async def _metrics_handler(self):
        """Handle metrics requests"""
        metrics = self.get_metrics()
        return JSONResponse(
            content={
                "platform": metrics.platform,
                "request_count": metrics.request_count,
                "error_count": metrics.error_count,
                "avg_response_time": metrics.avg_response_time,
                "memory_usage": metrics.memory_usage,
                "cpu_usage": metrics.cpu_usage,
            }
        )

    def process_request(self, request: KiroRequest) -> KiroResponse:
        """Process a Kiro agent request on Cloud Run"""
        try:
            self.request_count += 1
            start_time = datetime.utcnow()

            # Perform analysis using parent class method
            result = self.analyze_data(request.data)

            # Calculate response time
            end_time = datetime.utcnow()
            response_time = (end_time - start_time).total_seconds()
            self.response_times.append(response_time)

            # Create response
            response = KiroResponse(
                data=result,
                status_code=200,
                headers={"X-Platform": "cloudrun", "X-Response-Time": str(response_time)},
                timestamp=end_time.isoformat(),
            )

            logger.info(f"Request processed successfully in {response_time}s")
            return response

        except Exception as e:
            self.error_count += 1
            logger.error(f"Error processing request: {e}")
            return KiroResponse(
                data={"error": str(e), "platform": "cloudrun"},
                status_code=500,
                headers={"X-Platform": "cloudrun"},
                timestamp=datetime.utcnow().isoformat(),
            )

    def health_check(self) -> Dict[str, Any]:
        """Cloud Run health check"""
        return {
            "status": "healthy",
            "platform": "cloudrun",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime": self._get_uptime(),
            "request_count": self.request_count,
            "error_count": self.error_count,
            "checks": {"redis": self._check_redis(), "disk": self._check_disk()},
        }

    def get_metrics(self) -> KiroMetrics:
        """Get Cloud Run specific metrics"""
        avg_response_time = (
            sum(self.response_times) / len(self.response_times)
            if self.response_times
            else 0.0
        )

        return KiroMetrics(
            platform="cloudrun",
            request_count=self.request_count,
            error_count=self.error_count,
            avg_response_time=avg_response_time,
            memory_usage=self._get_memory_usage(),
            cpu_usage=self._get_cpu_usage(),
        )

    def _get_uptime(self) -> float:
        """Get service uptime in seconds"""
        # Simplified - in production would track actual start time
        return 0.0

    def _check_redis(self) -> str:
        """Check Redis connection for Beast Mode"""
        # Optional - only if Beast Mode is enabled
        beast_mode_enabled = os.getenv("BEAST_MODE_ENABLED", "false").lower() == "true"
        if not beast_mode_enabled:
            return "disabled"

        try:
            # Would check actual Redis connection here
            return "healthy"
        except Exception:
            return "unhealthy"

    def _check_disk(self) -> str:
        """Check disk space"""
        # Simplified health check
        return "healthy"

    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            import psutil

            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # Convert to MB
        except ImportError:
            return 0.0

    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage"""
        try:
            import psutil

            return psutil.cpu_percent(interval=0.1)
        except ImportError:
            return 0.0

    def run(self, host: str = "0.0.0.0", port: int = None):
        """Run the Cloud Run agent"""
        if port is None:
            port = self.port

        logger.info(f"Starting Cloud Run Kiro Agent on {host}:{port}")
        uvicorn.run(self.app, host=host, port=port, log_level="info")


# Factory integration
def create_cloudrun_agent() -> CloudRunKiroAgent:
    """Factory function for creating Cloud Run agents"""
    return CloudRunKiroAgent()

