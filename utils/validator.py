"""Validador de URLs para plataformas soportadas."""
import re
from typing import Optional, Tuple

from core.contracts import IURLValidator


class URLValidator(IURLValidator):
    """Valida URLs de redes sociales soportadas."""

    _PATTERNS = {
        "youtube": re.compile(
            r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+"
        ),
        "twitter": re.compile(r"(https?://)?(www\.)?(twitter|x)\.com/.+"),
        "instagram": re.compile(r"(https?://)?(www\.)?instagram\.com/.+"),
    }

    def validate(self, url: str) -> Tuple[bool, Optional[str]]:
        if not isinstance(url, str) or not url.strip():
            return False, "La URL está vacía."

        url = url.strip()
        for _platform, pattern in self._PATTERNS.items():
            if pattern.match(url):
                return True, None

        return False, "URL no soportada. Usa enlaces de YouTube, X/Twitter o Instagram."
