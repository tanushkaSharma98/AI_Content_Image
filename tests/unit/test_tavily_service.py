import pytest
from types import SimpleNamespace


@pytest.mark.unit
@pytest.mark.asyncio
async def test_tavily_service_success(monkeypatch):
    """Direct Tavily API returns results and uses Bearer auth header."""
    from app.services import tavily_service as mod

    captured_headers = {}

    class FakeResponse:
        status = 200

        async def json(self):
            return {
                "answer": "Test answer",
                "results": [
                    {"title": "A", "url": "https://a", "content": "alpha"},
                    {"title": "B", "url": "https://b", "content": "beta"},
                ],
            }

        async def text(self):  # pragma: no cover
            return ""

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

    class FakeSession:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        def post(self, url, headers=None, json=None):
            nonlocal captured_headers
            captured_headers = headers or {}
            return FakeResponse()

    monkeypatch.setattr(mod, "aiohttp", SimpleNamespace(ClientSession=FakeSession))

    result = await mod.tavily_service.search("what is ai")

    assert result["success"] is True
    assert result["query"] == "what is ai"
    assert isinstance(result["results"], list) and len(result["results"]) == 2
    # Verify Authorization Bearer header is used
    assert "Authorization" in captured_headers
    assert captured_headers["Authorization"].startswith("Bearer ")


@pytest.mark.unit
@pytest.mark.asyncio
async def test_tavily_service_401_raises(monkeypatch):
    """Direct Tavily API 401 should raise a clear exception."""
    from app.services import tavily_service as mod

    class FakeResponse:
        status = 401

        async def text(self):
            return '{"detail": {"error": "Unauthorized"}}'

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

    class FakeSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        def post(self, *args, **kwargs):
            return FakeResponse()

    monkeypatch.setattr(mod, "aiohttp", SimpleNamespace(ClientSession=FakeSession))

    with pytest.raises(Exception) as exc:
        await mod.tavily_service.search("test")

    assert "Tavily API error: 401" in str(exc.value)


