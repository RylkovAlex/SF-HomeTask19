"""Модуль 19 Итоговое практическое задание"""
import json
from typing import Tuple
import requests


class JSONPlaceholderAPI:
    """API for JSONPlaceholder - Free Fake REST API"""
    resources = {
        'posts': {
            "userId": int,
            "id": int,
            "title": str,
            "body": str
        },
        'comments': {
            "postId": int,
            "id": int,
            "name": str,
            "email": str,
            "body": str
        },
        'albums': {
            "userId": int,
            "id": int,
            "title": str
        },
        'photos': {
            "albumId": int,
            "id": int,
            "title": str,
            "url": str,
            "thumbnailUrl": str
        },
        'todos': {
            "userId": int,
            "id": int,
            "title": str,
        },
        'users': {
            "id": int,
            "name": str,
            "username": str,
            "email": str,
            "address": {
                "street": str,
                "suite": str,
                "city": str,
                "zipcode": str,
                "geo": {
                    "lat": str,
                    "lng": str
                }
            },
            "phone": str,
            "website": str,
            "company": {
                "name": str,
                "catchPhrase": str,
                "bs": str
            }
        }
    }
    user_collections = ['posts', 'comments', 'photos', 'todos', 'todos']
    base_url = "https://jsonplaceholder.typicode.com"

    @staticmethod
    def validate(instance, model_schema):
        for key in instance:
            if key not in model_schema:
                raise Exception(
                    f'Key {key} not exist in model schema for {instance}')
            elif type(model_schema[key]) == dict:
                JSONPlaceholderAPI.validate(instance[key], model_schema[key])
            elif model_schema[key] != type(instance[key]):
                raise Exception(
                    f'{instance} in not valid, check {key}')
            else:
                return True

    @ staticmethod
    def get_collection(colection_name: str, filters: dict = {}) -> Tuple[int, list] or Tuple[int, str]:
        """GET запрос на получение коллекции ресурса"""
        if colection_name not in JSONPlaceholderAPI.resources.keys():
            raise Exception(f'Resource {colection_name} not Exist!')
        res = requests.get(
            f'{JSONPlaceholderAPI.base_url}/{colection_name}', params=filters)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @ staticmethod
    def get_item_by_id(colection_name: str, id: int, filters: dict = {}) -> Tuple[int, dict] or Tuple[int, str]:
        """GET запрос на получение сущности из коллекции по идентификатору"""
        if colection_name not in JSONPlaceholderAPI.resources.keys():
            raise Exception(f'Resource {colection_name} not Exist!')
        res = requests.get(
            f'{JSONPlaceholderAPI.base_url}/{colection_name}/{id}', params=filters)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @ staticmethod
    def post_item(colection_name: str, item: dict) -> Tuple[int, dict] or Tuple[int, str]:
        """POST запрос на создание сущности в коллекции"""
        JSONPlaceholderAPI.validate(
            item, JSONPlaceholderAPI.resources[colection_name])

        res = requests.post(
            f'{JSONPlaceholderAPI.base_url}/{colection_name}', data=item)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @ staticmethod
    def update_item(colection_name: str, item: dict, method: str = 'put') -> Tuple[int, dict] or Tuple[int, str]:
        """PUT/PATCH запрос на обновление существующего ресурса"""
        JSONPlaceholderAPI.validate(
            item, JSONPlaceholderAPI.resources[colection_name])

        if not (method == 'put' or method == 'patch'):
            raise Exception(f'{method} is not REST update method')
        res = requests.__dict__[method](
            f'{JSONPlaceholderAPI.base_url}/{colection_name}/{item["id"]}', data=item)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @ staticmethod
    def delete_item(colection_name: str, resource_id: int) -> Tuple[int, dict] or Tuple[int, str]:
        """DELETE запрос на удаление ресурса"""
        if colection_name not in JSONPlaceholderAPI.resources.keys():
            raise Exception(f'Resource {colection_name} not Exist!')

        res = requests.delete(
            f'{JSONPlaceholderAPI.base_url}/{colection_name}/{resource_id}')
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @ staticmethod
    def get_users_collection(colection_name: str, user_id: int, filters: dict = {}) -> Tuple[int, list] or Tuple[int, str]:
        """GET запрос коллекции ресурсов определённого пользователя"""
        if colection_name not in JSONPlaceholderAPI.user_collections:
            raise Exception('Wrong resurce name!')
        res = requests.get(
            f'{JSONPlaceholderAPI.base_url}/users/{user_id}/{colection_name}', params=filters)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @ staticmethod
    def get_post_comments(post_id: int, filters: dict = {}) -> Tuple[int, list] or Tuple[int, str]:
        """GET запрос списка комментариев к определённому посту"""
        res = requests.get(
            f'{JSONPlaceholderAPI.base_url}/posts/{post_id}/comments', params=filters)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @ staticmethod
    def get_photos_in_album(album_id: int, filters: dict = {}) -> Tuple[int, list] or Tuple[int, str]:
        """GET запрос списка фотографий в определённом альбоме"""
        res = requests.get(
            f'{JSONPlaceholderAPI.base_url}/albums/{album_id}/photos', params=filters)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
