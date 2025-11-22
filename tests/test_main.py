import pytest

@pytest.mark.asyncio
async def test_health_check(test_client):
    response = await test_client.get("/healthy")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
