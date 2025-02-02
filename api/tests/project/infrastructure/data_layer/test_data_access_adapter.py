
import pytest
from project.infrastructure.constants.mongo_collections import Collections
from project.infrastructure.data_layer.data_access_adapter import MongoDataLayer

from dotenv import load_dotenv

load_dotenv()

async def create_mongo_object(input_object: dict):
    data_layer = MongoDataLayer(Collections.general_collection)
    result = await data_layer.save(input_object)
    return result


def test_data_layer_instance():
    data_layer = MongoDataLayer(Collections.general_collection)
    assert data_layer


@pytest.mark.asyncio
async def test_data_layer_creation():
    input_object = {"key": "value"}
    document = await create_mongo_object(input_object)
    assert document == input_object


@pytest.mark.asyncio
async def test_data_layer_update():

    input_object = {"key": "value"}
    document = await create_mongo_object(input_object)

    criteria = {"_id": document["_id"]}
    data_layer = MongoDataLayer(Collections.general_collection)
    result = await data_layer.update(criteria, {"key": "value2"})

    assert result.raw_result == {'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}


@pytest.mark.asyncio
async def test_data_layer_delete():

    input_object = {"key": "value"}
    document = await create_mongo_object(input_object)

    criteria = {"_id": document["_id"]}
    data_layer = MongoDataLayer(Collections.general_collection)
    result = await data_layer.delete(criteria)

    assert result.raw_result == {'n': 1, 'ok': 1.0}


@pytest.mark.asyncio
async def test_data_layer_get_by_id():

    input_object = {"key": "value"}
    document = await create_mongo_object(input_object)

    data_layer = MongoDataLayer(Collections.general_collection)
    result = await data_layer.get_by_id(document["_id"])

    assert result == document


@pytest.mark.asyncio
async def test_data_layer_get_by_filter():

    custom_filter = {}
    data_layer = MongoDataLayer(Collections.general_collection)
    result = await data_layer.get_by_filter(custom_filter)

    assert len(result) >= 2
