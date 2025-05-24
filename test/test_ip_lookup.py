from src.ip_lookup import get_ip_info

def test_ip_response():
    result = get_ip_info("8.8.8.8")
    assert result["IP"] == "8.8.8.8"
    assert "País" in result
