import pytest
from src.ip_lookup import get_ip_info

def test_ipinfo_fallback(monkeypatch):
    def mock_requests_get(url, timeout=5):
        class MockResponse:
            def __init__(self, url):
                self.url = url
                self.status_code = 200 if "ipinfo.io" in url else 403
            def json(self):
                if "ipinfo.io" in self.url:
                    return {
                        "ip": "1.1.1.1",
                        "city": "Sydney",
                        "region": "New South Wales",
                        "country": "AU",
                        "org": "APNIC",
                        "loc": "-33.8688,151.2093"
                    }
                return {"status": "fail", "message": "limit exceeded"}
        return MockResponse(url)

    monkeypatch.setattr("requests.get", mock_requests_get)
    result = get_ip_info("1.1.1.1")
    assert result["IP"] == "1.1.1.1"
    assert result["Ciudad"] == "Sydney"
    assert result["País"] == "AU"