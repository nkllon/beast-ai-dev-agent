"""
Beast AI Development Agent

Platform-agnostic AI development agents for cloud platforms.
"""

__version__ = "0.1.0"

from .common.models import (
    KiroAgentInterface,
    KiroRequest,
    KiroResponse,
    KiroMetrics,
    KiroAgentFactory,
)
from .cloudrun.agent import CloudRunKiroAgent
from .gke.agent import GKEKiroAgent
from .cloud_functions.agent import CloudFunctionsKiroAgent

__all__ = [
    "KiroAgentInterface",
    "KiroRequest",
    "KiroResponse",
    "KiroMetrics",
    "KiroAgentFactory",
    "CloudRunKiroAgent",
    "GKEKiroAgent",
    "CloudFunctionsKiroAgent",
]

