import pytest

@pytest.fixture
def api_request(playwright):
    request = playwright.request.new_context(
        base_url="http://127.0.0.1:8000"
    )

    yield request
    request.dispose()