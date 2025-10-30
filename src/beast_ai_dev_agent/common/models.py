#!/usr/bin/env python3
"""
Common interface for Kiro agents across GKE and Cloud Run platforms.
Ensures stateless design and platform compatibility.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class KiroRequest:
    """Common request structure for all platforms"""

    data: Dict[str, Any]
    headers: Dict[str, str]
    method: str
    path: str
    query_params: Dict[str, str]
    timestamp: str


@dataclass
class KiroResponse:
    """Common response structure for all platforms"""

    status_code: int
    data: Dict[str, Any]
    headers: Dict[str, str]
    timestamp: str


@dataclass
class KiroMetrics:
    """Common metrics structure"""

    platform: str
    instance_id: str
    timestamp: str
    request_count: int
    error_count: int
    avg_response_time: float
    memory_usage: float
    cpu_usage: float


class KiroAgentInterface(ABC):
    """Common interface for Kiro agents across platforms"""

    def __init__(self, platform: str):
        self.platform = platform
        self.request_count = 0
        self.error_count = 0
        self.response_times = []
        self.logger = logging.getLogger(f"{__name__}.{platform}")

    @abstractmethod
    def process_request(self, request: KiroRequest) -> KiroResponse:
        """Process a Kiro agent request - must be implemented by platform"""
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Health check endpoint - platform specific"""
        pass

    @abstractmethod
    def get_metrics(self) -> KiroMetrics:
        """Get agent metrics - platform specific"""
        pass

    def analyze_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Core analysis logic - shared across platforms"""
        try:
            self.logger.info(f"Processing analysis request on {self.platform}")

            # Core Kiro agent analysis logic
            result = {
                "analysis_id": self._generate_analysis_id(),
                "platform": self.platform,
                "timestamp": datetime.utcnow().isoformat(),
                "input_data": data,
                "analysis_result": self._perform_analysis(data),
                "metadata": {"processing_time": self._get_processing_time(), "data_size": len(str(data))},
            }

            self.logger.info(f"Analysis completed successfully on {self.platform}")
            return result

        except Exception as e:
            self.logger.error(f"Analysis failed on {self.platform}: {e}")
            raise

    def _generate_analysis_id(self) -> str:
        """Generate unique analysis ID"""
        import uuid

        return f"kiro_{self.platform}_{uuid.uuid4().hex[:8]}"

    def _perform_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform the actual analysis - implement your logic here"""
        # This is where you implement your specific Kiro agent analysis
        # For now, returning a placeholder
        return {"status": "analyzed", "confidence": 0.95, "categories": ["example_category"], "insights": ["Example insight from analysis"]}

    def _get_processing_time(self) -> float:
        """Get processing time in seconds"""
        # Placeholder - implement actual timing logic
        return 0.1

    def validate_request(self, request: KiroRequest) -> bool:
        """Validate incoming request"""
        try:
            # Basic validation
            if not request.data:
                self.logger.warning("Empty request data")
                return False

            if request.method not in ["GET", "POST", "PUT", "DELETE"]:
                self.logger.warning(f"Invalid method: {request.method}")
                return False

            return True

        except Exception as e:
            self.logger.error(f"Request validation failed: {e}")
            return False

    def create_error_response(self, error_message: str, status_code: int = 500) -> KiroResponse:
        """Create standardized error response"""
        self.error_count += 1

        return KiroResponse(
            status_code=status_code,
            data={"status": "error", "message": error_message, "platform": self.platform, "timestamp": datetime.utcnow().isoformat()},
            headers={"Content-Type": "application/json"},
            timestamp=datetime.utcnow().isoformat(),
        )

    def create_success_response(self, data: Dict[str, Any], status_code: int = 200) -> KiroResponse:
        """Create standardized success response"""
        self.request_count += 1

        return KiroResponse(
            status_code=status_code,
            data={"status": "success", "platform": self.platform, "timestamp": datetime.utcnow().isoformat(), "result": data},
            headers={"Content-Type": "application/json"},
            timestamp=datetime.utcnow().isoformat(),
        )

    def get_platform_info(self) -> Dict[str, Any]:
        """Get platform-specific information"""
        return {"platform": self.platform, "version": "1.0.0", "capabilities": self._get_platform_capabilities(), "constraints": self._get_platform_constraints()}

    def _get_platform_capabilities(self) -> List[str]:
        """Get platform-specific capabilities"""
        if self.platform == "gke":
            return ["persistent_volumes", "stateful_sets", "node_affinity", "custom_networking", "advanced_scaling"]
        elif self.platform == "cloudrun":
            return ["auto_scaling", "pay_per_use", "serverless", "http_triggers", "event_triggers"]
        else:
            return ["basic_http"]

    def _get_platform_constraints(self) -> List[str]:
        """Get platform-specific constraints"""
        if self.platform == "gke":
            return ["stateless_only", "no_persistent_volumes", "no_stateful_sets", "no_node_affinity"]
        elif self.platform == "cloudrun":
            return ["15_minute_timeout", "http_only", "stateless_only", "ephemeral_storage"]
        else:
            return ["basic_constraints"]


class KiroAgentFactory:
    """Factory for creating platform-specific Kiro agents"""

    @staticmethod
    def create_agent(platform: str) -> KiroAgentInterface:
        """Create a platform-specific Kiro agent"""
        if platform == "gke":
            from ..gke.agent import GKEKiroAgent

            return GKEKiroAgent()
        elif platform == "cloudrun":
            from ..cloudrun.agent import CloudRunKiroAgent

            return CloudRunKiroAgent()
        else:
            raise ValueError(f"Unknown platform: {platform}")

    @staticmethod
    def get_available_platforms() -> List[str]:
        """Get list of available platforms"""
        return ["gke", "cloudrun"]

    @staticmethod
    def validate_platform(platform: str) -> bool:
        """Validate if platform is supported"""
        return platform in KiroAgentFactory.get_available_platforms()


# Utility functions for common operations
def create_kiro_request_from_flask(request) -> KiroRequest:
    """Create KiroRequest from Flask request object"""
    return KiroRequest(data=request.get_json() or {}, headers=dict(request.headers), method=request.method, path=request.path, query_params=dict(request.args), timestamp=datetime.utcnow().isoformat())


def create_flask_response_from_kiro(kiro_response: KiroResponse):
    """Create Flask response from KiroResponse"""
    from flask import jsonify

    return jsonify(kiro_response.data), kiro_response.status_code, kiro_response.headers


def log_request(platform: str, request: KiroRequest, response: KiroResponse):
    """Log request/response for monitoring"""
    logger.info(f"[{platform}] {request.method} {request.path} -> {response.status_code}")


def validate_stateless_constraints(platform: str) -> bool:
    """Validate that platform meets stateless constraints"""
    if platform == "gke":
        # Check for forbidden resources
        import subprocess

        try:
            # Check for PersistentVolumeClaims
            result = subprocess.run(["kubectl", "get", "pvc", "-n", "kiro-agents"], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                logger.error("❌ FORBIDDEN: PersistentVolumeClaims found")
                return False

            # Check for StatefulSets
            result = subprocess.run(["kubectl", "get", "statefulset", "-n", "kiro-agents"], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                logger.error("❌ FORBIDDEN: StatefulSets found")
                return False

            logger.info("✅ GKE stateless constraints validated")
            return True

        except Exception as e:
            logger.error(f"Failed to validate GKE constraints: {e}")
            return False

    elif platform == "cloudrun":
        # Cloud Run is inherently stateless
        logger.info("✅ Cloud Run stateless constraints validated")
        return True

    else:
        logger.error(f"Unknown platform: {platform}")
        return False
