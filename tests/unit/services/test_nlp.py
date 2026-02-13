from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from bson import ObjectId
from fastapi import HTTPException

from models import HistoryResponse
from services.nlp import NLPService


async def test_extract_entities(mocked_nlp_service: NLPService) -> None:
    mocked_nlp_service.load_model = AsyncMock(
        return_value=MagicMock(
            return_value=MagicMock(
                ents=[
                    MagicMock(label_="MONEY", text="45"),
                    MagicMock(label_="PERSON", text="Michael"),
                    MagicMock(label_="DATE", text="June 3"),
                ]
            )
        )
    )
    mocked_nlp_service.repository.write = AsyncMock(return_value=None)

    result = await mocked_nlp_service.extract_entities(
        model_name="test_model", text="Can you send $45 to Michael on June 3?"
    )
    assert result.money == 45
    assert result.person == "Michael"
    assert result.date == "June 3"


async def test_add_model(mocked_nlp_service: NLPService) -> None:
    mocked_nlp_service.repository.find = AsyncMock(return_value=None)
    mocked_nlp_service.repository.write = AsyncMock()
    mocked_nlp_service.load_model = AsyncMock()

    await mocked_nlp_service.add_model("test_model")

    mocked_nlp_service.repository.write.assert_awaited_once()
    mocked_nlp_service.load_model.assert_awaited_once()


async def test_add_model_exists(mocked_nlp_service: NLPService) -> None:
    mocked_nlp_service.repository.find = AsyncMock(return_value={"model": "test_model"})
    with pytest.raises(
        HTTPException, match="400: Model 'test_model' already exists in repository."
    ):
        await mocked_nlp_service.add_model(model_name="test_model")


async def test_load_model(mocked_nlp_service: NLPService) -> None:
    mocked_nlp_service.repository.find = AsyncMock(return_value={"model": "test_model"})
    model = MagicMock(pipe_names=["ner", "textcat"])
    mocked_nlp_service.models = {}
    with patch("services.nlp.is_package", return_value=False), patch(
        "services.nlp.download", return_value=None
    ), patch("services.nlp.load", return_value=model):
        result = await mocked_nlp_service.load_model(model_name="test_model")
        assert result == model


async def test_load_model_already_loaded(mocked_nlp_service: NLPService) -> None:
    mocked_nlp_service.repository.find = AsyncMock(return_value={"model": "test_model"})
    model = MagicMock(pipe_names=["ner", "textcat"])
    mocked_nlp_service.models = {"test_model": model}
    result = await mocked_nlp_service.load_model(model_name="test_model")
    assert result == model


async def test_load_model_not_found(mocked_nlp_service: NLPService) -> None:
    mocked_nlp_service.repository.find = AsyncMock(return_value=None)
    mocked_nlp_service.models = {"test_model": MagicMock(pipe_names=["ner", "textcat"])}
    with pytest.raises(
        HTTPException, match="404: Model 'test_model' not found in repository."
    ):
        await mocked_nlp_service.load_model(model_name="test_model")


async def test_load_model_download_failure(mocked_nlp_service: NLPService) -> None:
    mocked_nlp_service.repository.find = AsyncMock(return_value={"model": "test_model"})
    mocked_nlp_service.models = {}
    with patch("services.nlp.is_package", return_value=False), patch(
        "services.nlp.download", side_effect=SystemExit("Download failed")
    ):
        with pytest.raises(
            HTTPException,
            match="500: Failed to download model 'test_model': Download failed",
        ):
            await mocked_nlp_service.load_model(model_name="test_model")


async def test_get_models(mocked_nlp_service: NLPService) -> None:
    mocked_nlp_service.repository.list = AsyncMock(
        return_value=[{"model": "model1"}, {"model": "model2"}]
    )
    models = await mocked_nlp_service.get_models()
    assert models == ["model1", "model2"]


async def test_delete_model(mocked_nlp_service: NLPService) -> None:
    mocked_nlp_service.repository.find = AsyncMock(return_value={"model": "test_model"})
    mocked_nlp_service.repository.delete = AsyncMock(return_value=None)
    mocked_nlp_service.models = {"test_model": MagicMock(pipe_names=["ner"])}
    await mocked_nlp_service.delete_model(model_name="test_model")
    assert "test_model" not in mocked_nlp_service.models


async def test_delete_model_not_found(mocked_nlp_service: NLPService) -> None:
    mocked_nlp_service.repository.find = AsyncMock(return_value=None)
    with pytest.raises(
        HTTPException, match="404: Model 'test_model' not found in repository."
    ):
        await mocked_nlp_service.delete_model(model_name="test_model")


async def test_history(mocked_nlp_service: NLPService) -> None:
    mocked_nlp_service.repository.list = AsyncMock(
        return_value=[
            {
                "_id": ObjectId("698e2ed263b50e4d1efabc7b"),
                "model": "en_core_web_sm",
                "text": "Can you send $45 to Michael on June 3?",
                "entities": {"money": 45, "person": "Michael", "date": "June 3"},
                "timestamp": "2026-02-12T19:49:38.983Z",
            },
            {
                "_id": ObjectId("698e3aa266e979874081b8b2"),
                "model": "en_core_web_sm",
                "text": "Can you send $50 to John on May 4?",
                "entities": {"money": 50, "person": "John", "date": "May 4"},
                "timestamp": "2026-02-12T20:40:02.519Z",
            },
        ]
    )
    history = await mocked_nlp_service.history()
    assert history == HistoryResponse.model_validate(
        {
            "history": [
                {
                    "_id": ObjectId("698e2ed263b50e4d1efabc7b"),
                    "model": "en_core_web_sm",
                    "text": "Can you send $45 to Michael on June 3?",
                    "entities": {"money": 45, "person": "Michael", "date": "June 3"},
                    "timestamp": "2026-02-12T19:49:38.983Z",
                },
                {
                    "_id": ObjectId("698e3aa266e979874081b8b2"),
                    "model": "en_core_web_sm",
                    "text": "Can you send $50 to John on May 4?",
                    "entities": {"money": 50, "person": "John", "date": "May 4"},
                    "timestamp": "2026-02-12T20:40:02.519Z",
                },
            ]
        }
    )
