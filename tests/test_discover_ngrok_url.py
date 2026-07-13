from scripts.discover_ngrok_url import extract_https_url


def test_extract_https_url_prefers_https_tunnel():
    payload = {
        "tunnels": [
            {"public_url": "http://example.ngrok-free.dev"},
            {"public_url": "https://example.ngrok-free.dev/"},
        ]
    }

    assert extract_https_url(payload) == "https://example.ngrok-free.dev"


def test_extract_https_url_returns_none_without_tunnel():
    assert extract_https_url({"tunnels": []}) is None
