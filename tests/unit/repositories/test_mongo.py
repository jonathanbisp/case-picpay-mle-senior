from unittest.mock import AsyncMock, MagicMock

from repositories.mongo import MongoRepository


async def test_write(mocked_repository: MongoRepository) -> None:
    data = {"key": "value"}
    result = await mocked_repository.write(collection="test_collection", data=data)
    assert "_id" in result
    assert result["key"] == "value"


async def test_find(mocked_repository: MongoRepository) -> None:
    await mocked_repository.write(collection="test_collection", data={"key": "value"})
    document = await mocked_repository.find(
        collection="test_collection", query={"key": "value"}
    )
    assert document is not None
    assert document["key"] == "value"


async def test_update(mocked_repository: MongoRepository) -> None:
    await mocked_repository.write(collection="test_collection", data={"key": "value"})
    updated_document = await mocked_repository.update(
        collection="test_collection",
        query={"key": "value"},
        data={"key": "new_value"},
    )
    assert updated_document is not None
    assert updated_document["key"] == "new_value"


async def test_delete(mocked_repository: MongoRepository) -> None:
    await mocked_repository.write(collection="test_collection", data={"key": "value"})
    deleted_document = await mocked_repository.delete(
        collection="test_collection", query={"key": "value"}
    )
    assert deleted_document is not None
    assert deleted_document["key"] == "value"
    should_be_none = await mocked_repository.find(
        collection="test_collection", query={"key": "value"}
    )
    assert should_be_none is None


async def test_list(mocked_repository: MongoRepository) -> None:
    await mocked_repository.write(collection="test_collection", data={"key": "value1"})
    await mocked_repository.write(collection="test_collection", data={"key": "value2"})

    documents = await mocked_repository.list(collection="test_collection", query={})
    assert len(documents) == 2
    keys = {doc["key"] for doc in documents}
    assert keys == {"value1", "value2"}


async def test_is_healthy(mocked_repository: MongoRepository) -> None:
    is_healthy = await mocked_repository.is_healthy()
    assert is_healthy


async def test_is_not_healthy(mocked_repository: MongoRepository) -> None:
    mocked_repository.client.admin = MagicMock()
    mocked_repository.client.admin.command = AsyncMock(
        side_effect=Exception("Connection error")
    )

    is_healthy = await mocked_repository.is_healthy()

    assert not is_healthy
