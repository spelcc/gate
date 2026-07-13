#!/usr/bin/env python3

import json
import time
from urllib.request import urlopen


NGROK_API_URL = "http://127.0.0.1:4040/api/tunnels"


def extract_https_url(payload: dict) -> str | None:
    for tunnel in payload.get("tunnels", []):
        public_url = tunnel.get("public_url", "")
        if public_url.startswith("https://"):
            return public_url.rstrip("/")
    return None


def discover_ngrok_url(timeout: float = 20, interval: float = 0.5) -> str:
    deadline = time.monotonic() + timeout
    last_error: Exception | None = None

    while time.monotonic() < deadline:
        try:
            with urlopen(NGROK_API_URL, timeout=2) as response:
                public_url = extract_https_url(json.load(response))
                if public_url:
                    return public_url
        except Exception as exc:
            last_error = exc

        time.sleep(interval)

    detail = f": {last_error}" if last_error else ""
    raise RuntimeError(f"No HTTPS ngrok tunnel found within {timeout}s{detail}")


if __name__ == "__main__":
    print(discover_ngrok_url())
