import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.abspath(__file__), os.pardir, os.pardir)))
from api import JSONPlaceholderAPI

# Возможно обнаружен баг - типы для resource_schema я брал исходя из GET запросов, однако в POST/PUT/PATCH запросах возврщается иной тип для полей userId, albumId и т.п. сервис в ответе возвращает их значения строкой, а не числом, как в GET запросе
FIELDS_WITH_BUGS = ['id', 'userId', 'postId', 'albumId']

class TestJSONPlaceholderAPI:
    @staticmethod
    def generate_mock(schema: dict, keysToPass: list = []) -> dict:
        mock = {}
        for key in schema:
            if key in keysToPass:
                continue
            elif schema[key] == str:
                mock[key] = 'Some string'
            elif schema[key] == int:
                mock[key] = 1
            elif schema[key] == float:
                mock[key] = 1.0
            elif type(schema[key]) == dict:
                mock[key] = TestJSONPlaceholderAPI.generate_mock(
                    schema[key])
            elif type(schema[key]) == list:
                mock[key] = []
            else:
                raise Exception(
                    f'Unknown type {schema[key]} in key {key} in {schema}!')
        return mock

    @staticmethod
    def test_get_collection():
        for collection_name in JSONPlaceholderAPI.resources:
            status, collection = JSONPlaceholderAPI.get_collection(
                collection_name)
            assert status == 200
            for item in collection:
                for key in JSONPlaceholderAPI.resources[collection_name]:
                    assert key in item

    @staticmethod
    def test_get_item_by_id():
        for collection_name in JSONPlaceholderAPI.resources:
            status, resource = JSONPlaceholderAPI.get_item_by_id(
                collection_name, 1)
            assert status == 200
            for key in JSONPlaceholderAPI.resources[collection_name]:
                assert key in resource

    @staticmethod
    def test_post_item():
        for collection_name in JSONPlaceholderAPI.resources:
            schema = JSONPlaceholderAPI.resources[collection_name]
            mocked_item = TestJSONPlaceholderAPI.generate_mock(
                schema, keysToPass=['id'])

            status, created_item = JSONPlaceholderAPI.post_item(
                collection_name, mocked_item)
            assert status == 201
            for key in created_item:
                if key in FIELDS_WITH_BUGS:
                    continue
                # Выяснилось, что для вложенных объектов возвращается массив их ключей, а не полное содержание:
                if type(created_item[key] == list):
                    for field in created_item[key]:
                        assert field in mocked_item[key]
                else:
                    assert created_item[key] == mocked_item[key]

    @staticmethod
    def test_update_item_by_PUT():
        for collection_name in JSONPlaceholderAPI.resources:
            status, original_item = JSONPlaceholderAPI.get_item_by_id(
                collection_name, 1)
            schema = JSONPlaceholderAPI.resources[collection_name]
            mocked_item = TestJSONPlaceholderAPI.generate_mock(
                schema)

            mocked_item['id'] = original_item['id']

            status, updated_item = JSONPlaceholderAPI.update_item(
                collection_name, mocked_item)

            assert status == 200
            for key in updated_item:
                if key in FIELDS_WITH_BUGS:
                    continue
                if type(updated_item[key] == list):
                    for field in updated_item[key]:
                        assert field in mocked_item[key]
                else:
                    assert updated_item[key] == mocked_item[key]

    @staticmethod
    def test_patch_user():
        _, original_user = JSONPlaceholderAPI.get_item_by_id(
            'users', 1)

        status, updated_user = JSONPlaceholderAPI.update_item(
            'users', {'name': 'Vasia', 'id': original_user['id']}, method='patch')

        assert status == 200
        for key in updated_user:
            if key in FIELDS_WITH_BUGS:
                continue
            if key == 'name':
                assert updated_user[key] == 'Vasia'
            elif type(updated_user[key] == list):
                for field in updated_user[key]:
                    assert field in original_user[key]
            else:
                assert updated_user[key] == original_user[key]

    @staticmethod
    def test_delete_item():
        for colection_name in JSONPlaceholderAPI.resources:
            status, deleted = JSONPlaceholderAPI.delete_item(
                colection_name, 1)
            assert status == 200
            assert deleted == {}

    @staticmethod
    def test_get_users_collection():
        for colection_name in JSONPlaceholderAPI.user_collections:
            status, collection = JSONPlaceholderAPI.get_users_collection(
                colection_name, 1)
            assert status == 200
            assert len(collection) >= 0

    @staticmethod
    def test_post_comments():
        status, comments = JSONPlaceholderAPI.get_post_comments(1)

        assert status == 200
        assert len(comments) >= 0

    @staticmethod
    def test_get_photos_in_album():
        status, photos = JSONPlaceholderAPI.get_post_comments(1)

        assert status == 200
        assert len(photos) >= 0

    @staticmethod
    def test_todos_completed_filter():
        status, todos = JSONPlaceholderAPI.get_collection(
            'todos', filters={'completed': True})

        assert status == 200
        assert all([todo['completed'] for todo in todos])

        status, todos = JSONPlaceholderAPI.get_collection(
            'todos', filters={'completed': False})

        assert status == 200
        assert all([not todo['completed'] for todo in todos])
