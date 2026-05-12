"""Structured traceability logger.

This module wraps Python's built-in `logging` to provide:
- Stable event names (e.g. "ui.find_clicked")
- JSON log lines with context fields
- File + console handlers

No external dependencies.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional


class _JsonLineFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "func": record.funcName,
            "line": record.lineno,
        }

        # Optional structured fields
        event = getattr(record, "event", None)
        if event is not None:
            payload["event"] = event

        fields = getattr(record, "fields", None)
        if isinstance(fields, dict) and fields:
            payload["fields"] = fields

        if record.exc_info:
            payload["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": "".join(traceback.format_exception(*record.exc_info)),
            }

        return json.dumps(payload, ensure_ascii=False)


def _ensure_log_dir(path: str) -> None:
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)


def _build_base_logger(
    name: str,
    log_file: Optional[str],
    level: int,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Idempotent: avoid duplicate handlers if imported multiple times.
    if getattr(logger, "_pecibalto_configured", False):
        return logger

    formatter = _JsonLineFormatter()

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_file:
        try:
            _ensure_log_dir(log_file)
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except OSError:
            # If file can't be opened, we still have console logging.
            pass

    logger.propagate = False
    setattr(logger, "_pecibalto_configured", True)
    return logger


@dataclass(frozen=True)
class TraceLogger:
    """Small wrapper to log named events with fields."""

    _logger: logging.Logger

    def event(self, event: str, *, level: int = logging.INFO, **fields: Any) -> None:
        self._logger.log(level, event, extra={"event": event, "fields": fields})

    def warning(self, event: str, **fields: Any) -> None:
        self.event(event, level=logging.WARNING, **fields)

    def error(self, event: str, **fields: Any) -> None:
        self.event(event, level=logging.ERROR, **fields)

    def exception(self, event: str, **fields: Any) -> None:
        self._logger.error(event, exc_info=True, extra={"event": event, "fields": fields})


_TRACE_LOGGER: Optional[TraceLogger] = None


def get_trace_logger(
    *,
    name: str = "pecibalto",
    log_file: str = os.path.join("logs", "pecibalto.log"),
    level: int = logging.INFO,
    force_new: bool = False,
) -> TraceLogger:
    """Return a singleton trace logger.

    By default logs to:
    - console (stdout)
    - logs/pecibalto.log (relative to current working directory)
    """

    global _TRACE_LOGGER
    if _TRACE_LOGGER is None or force_new:
        base = _build_base_logger(name=name, log_file=log_file, level=level)
        _TRACE_LOGGER = TraceLogger(base)
    return _TRACE_LOGGER
