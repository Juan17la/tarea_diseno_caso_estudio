"""
Servicio de extracción de medios basado en yt-dlp.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Optional

import yt_dlp


ProgressCallback = Callable[[float, dict[str, Any]], None]


class ExtractorService:
    """Encapsula la lógica de extracción de información y descarga con yt-dlp."""

    def __init__(
        self,
        progress_callback: Optional[ProgressCallback] = None,
        ydl_options: Optional[dict[str, Any]] = None,
    ):
        self._progress_callback = progress_callback
        self._base_options: dict[str, Any] = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
        }
        if ydl_options:
            self._base_options.update(ydl_options)

    def set_progress_callback(
        self, progress_callback: Optional[ProgressCallback]
    ) -> None:
        """Actualiza el callback usado para reportar progreso."""
        self._progress_callback = progress_callback

    def fetch_info(self, url):
        """Obtiene metadatos sin descargar (extract_info con download=False)."""
        self._validate_url(url)

        options = dict(self._base_options)
        options.update(
            {
                "skip_download": True,
                "extract_flat": False,
            }
        )

        with yt_dlp.YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=False)

    def download(self, url, output_path, format_profile, progress_hook):
        """Ejecuta la descarga del medio."""
        self._validate_url(url)

        callback = progress_hook or self._progress_callback
        options = dict(self._base_options)
        options.update(self._build_download_options(output_path, format_profile))
        options["progress_hooks"] = [self._build_progress_hook(callback)]

        with yt_dlp.YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=True)

    def _validate_url(self, url):
        if not isinstance(url, str) or not url.strip():
            raise ValueError("Se requiere una URL válida para continuar.")

    def _build_download_options(self, output_path, format_profile):
        options: dict[str, Any] = {
            "outtmpl": self._build_output_template(output_path),
        }

        if isinstance(format_profile, dict):
            options.update(format_profile)
            return options

        profile = str(format_profile or "mp4").strip().lower()

        if profile in {"mp3", "audio"}:
            options.update(
                {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                }
            )
            return options

        if profile in {"mp4", "video"}:
            options.update(
                {
                    "format": "bv*+ba/b",
                    "merge_output_format": "mp4",
                }
            )
            return options

        options["format"] = profile
        return options

    def _build_output_template(self, output_path):
        if not output_path:
            return "%(title)s.%(ext)s"

        target = Path(output_path).expanduser()

        if target.exists() and target.is_file():
            return str(target)

        if target.suffix and not target.is_dir():
            return str(target)

        return str(target / "%(title)s.%(ext)s")

    def _build_progress_hook(self, callback):
        def _hook(progress_data):
            if not callback:
                return

            payload = self._normalize_progress_data(progress_data)
            callback(payload["progress"], payload)

        return _hook

    def _normalize_progress_data(self, progress_data):
        status = progress_data.get("status", "unknown")
        progress = self._extract_percentage(progress_data)

        if status == "finished":
            progress = 100.0

        payload = dict(progress_data)
        payload["progress"] = progress
        return payload

    def _extract_percentage(self, progress_data):
        downloaded = progress_data.get("downloaded_bytes") or 0
        total = (
            progress_data.get("total_bytes")
            or progress_data.get("total_bytes_estimate")
            or 0
        )

        if total:
            return self._clamp_percentage((float(downloaded) / float(total)) * 100.0)

        percent_text = progress_data.get("_percent_str")
        if isinstance(percent_text, str):
            try:
                return self._clamp_percentage(float(percent_text.strip().rstrip("%")))
            except ValueError:
                pass

        if progress_data.get("status") == "finished":
            return 100.0

        return 0.0

    def _clamp_percentage(self, value):
        if value < 0.0:
            return 0.0
        if value > 100.0:
            return 100.0
        return round(value, 2)
