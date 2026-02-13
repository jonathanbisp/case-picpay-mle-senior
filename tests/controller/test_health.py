from fastapi.testclient import TestClient


async def test_health_check(mocked_api_client: TestClient) -> None:
    response = mocked_api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
