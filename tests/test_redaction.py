from src.logging_utils import redact_dict


def test_redacts_sensitive_keys():
    payload = {
        "access_token": "secret",
        "notes": "private",
        "nested": {"token": "hidden"},
        "list": [{"password": "pw"}],
    }
    redacted = redact_dict(payload)
    assert redacted["access_token"] == "[REDACTED]"
    assert redacted["notes"] == "[REDACTED]"
    assert redacted["nested"]["token"] == "[REDACTED]"
    assert redacted["list"][0]["password"] == "[REDACTED]"
