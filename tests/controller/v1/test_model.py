from unittest.mock import AsyncMock

from bson import ObjectId
from fastapi.testclient import TestClient

from models import HistoryResponse, PredicitionEntities, PredictionModel
from services import NLPService


def test_load_model(
    mocked_api_client: TestClient, mocked_nlp_service: NLPService
) -> None:
    mocked_nlp_service.add_model = AsyncMock(return_value=None)

    response = mocked_api_client.post("/v1/load", json={"model": "test_model"})

    assert response.status_code == 200
    assert response.json() == {"message": "Model loaded successfully"}
    mocked_nlp_service.add_model.assert_awaited_once_with(model_name="test_model")


def test_get_models(
    mocked_api_client: TestClient, mocked_nlp_service: NLPService
) -> None:
    mocked_nlp_service.get_models = AsyncMock(return_value=["model1", "model2"])

    response = mocked_api_client.get("/v1/models")

    assert response.status_code == 200
    assert response.json() == {"models": ["model1", "model2"]}
    mocked_nlp_service.get_models.assert_awaited_once()


def test_predict(mocked_api_client: TestClient, mocked_nlp_service: NLPService) -> None:
    mocked_nlp_service.extract_entities = AsyncMock(
        return_value=PredicitionEntities(
            money=100.4, person="John Doe", date="2024-01-01"
        )
    )

    response = mocked_api_client.post(
        "/v1/predict",
        json={"model": "test_model", "text": "This is a test."},
    )

    assert response.status_code == 200
    assert response.json() == {
        "date": "2024-01-01",
        "money": 100.4,
        "person": "John Doe",
    }
    mocked_nlp_service.extract_entities.assert_awaited_once_with(
        model_name="test_model", text="This is a test."
    )


def test_delete_model(
    mocked_api_client: TestClient, mocked_nlp_service: NLPService
) -> None:
    mocked_nlp_service.delete_model = AsyncMock(return_value=None)

    response = mocked_api_client.delete("/v1/models/test_model")

    assert response.status_code == 200
    assert response.json() == {"message": "Model deleted successfully"}
    mocked_nlp_service.delete_model.assert_awaited_once_with(model_name="test_model")


def test_list_predictions(
    mocked_api_client: TestClient, mocked_nlp_service: NLPService
) -> None:
    mocked_nlp_service.history = AsyncMock(
        return_value=HistoryResponse(
            history=[
                PredictionModel(
                    _id=ObjectId("656f1c2e9b1e8b3a2c4d5e6f"),
                    model="test_model",
                    text="This is a test.",
                    entities=PredicitionEntities(
                        money=100.4, person="John Doe", date="2024-01-01"
                    ),
                    timestamp="2024-01-01T00:00:00Z",
                )
            ]
        )
    )

    response = mocked_api_client.get("/v1/list")

    assert response.status_code == 200
    assert response.json() == {
        "history": [
            {
                "entities": {
                    "date": "2024-01-01",
                    "money": 100.4,
                    "person": "John Doe",
                },
                "model": "test_model",
                "text": "This is a test.",
                "timestamp": "2024-01-01T00:00:00Z",
            }
        ]
    }

    mocked_nlp_service.history.assert_awaited_once()
