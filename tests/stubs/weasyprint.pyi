from typing import Any, Callable, IO
from pathlib import Path

from ssl import SSLContext


def default_url_fetcher(url: str, timeout: int = 10,
                        ssl_context: SSLContext | None = None
                        ) -> dict[str, Any]:
    ...


class HTML:
    def __init__(self, guess: Any = None, filename: str | Path | None = None,
                 url: str | None = None, file_obj: IO | None = None,
                 string: str | None = None, encoding: str | None = None,
                 base_url: str | Path | None = None,
                 url_fetcher: Callable = default_url_fetcher,
                 media_type: str = 'print') -> None:
        ...

    def write_pdf(self, target: str | Path | IO | None = None,
                  zoom: float = 1.0, finisher: Callable | None = None,
                  font_config: Any = None, counter_style: dict | None = None,
                  **options: Any) -> bytes:
        ...
