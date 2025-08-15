import pytest


@pytest.mark.unit
@pytest.mark.asyncio
async def test_fallback_wikipedia_success(monkeypatch):
    from app.services.search_service import fallback_search_service

    class FakeResponse:
        status = 200

        async def json(self):
            return {
                "title": "India",
                "extract": "India is a country...",
                "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/India"}},
            }

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

    class FakeSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        def get(self, *args, **kwargs):
            return FakeResponse()

    import sys, types
    fake_aiohttp = types.SimpleNamespace(ClientSession=lambda: FakeSession())
    monkeypatch.setitem(sys.modules, "aiohttp", fake_aiohttp)

    result = await fallback_search_service.search_with_wikipedia("India")

    assert result["success"] is True
    assert result["query"] == "India"
    assert result["source"] == "wikipedia_api"
    assert result["results"][0]["url"].startswith("https://en.wikipedia.org/")


@pytest.mark.unit
@pytest.mark.asyncio
async def test_fallback_basic_when_wikipedia_fails(monkeypatch):
    from app.services.search_service import fallback_search_service

    class FakeResponse:
        status = 500

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

    class FakeSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        def get(self, *args, **kwargs):
            return FakeResponse()

    import sys, types
    fake_aiohttp = types.SimpleNamespace(ClientSession=lambda: FakeSession())
    monkeypatch.setitem(sys.modules, "aiohttp", fake_aiohttp)

    result = await fallback_search_service.search_with_wikipedia("India")

    assert result["success"] is True
    assert result["source"] == "fallback_service"


