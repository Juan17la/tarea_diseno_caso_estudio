"""Traceability package for Pecibalto.

Provides a small, structured logging layer to track UI events and errors.
"""

from .logger import TraceLogger, get_trace_logger

__all__ = ["TraceLogger", "get_trace_logger"]
