from qa_guru_7_19_api.utils import load_schema
from qa_guru_7_19_api import response_validation
from allure_commons.types import AttachmentType
from requests import sessions
from curlify import to_curl
import allure
import json


def reqres_api(method, url, **kwargs):
    args = kwargs
    base_url = "https://reqres.in"
    new_url = base_url + url
    method = method.upper()
    with allure.step(f'Отправляем запрос {method} {url} {args if len(args) != 0 else ''}'):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            message = to_curl(response.request)
            allure.attach(body=message.encode("utf8"), name="Curl", attachment_type=AttachmentType.TEXT,
                          extension='txt')
            allure.attach(body=json.dumps(response.json(), indent=4).encode("utf8"), name="Response Json",
                          attachment_type=AttachmentType.JSON, extension='json')
    return response


def get_total_users():
    response = reqres_api('get', '/api/users/?page=2')
    total_users = response.json()['total']
    return total_users


def test_ok_status_code():
    response = reqres_api('get', '/api/users/2')
    response_validation.check_status_code(200, response)


def test_get_users():
    schema = load_schema('reqres_api', 'get_users.json')

    response = reqres_api('get', '/api/users?page=2')

    response_validation.check_status_code(200, response)
    response_validation.check_response_json_schema(schema, response)


def test_get_user():
    schema = load_schema('reqres_api', 'get_single_user.json')

    response = reqres_api('get', '/api/users/2')

    response_validation.check_status_code(200, response)
    response_validation.check_response_json_schema(schema, response)


def test_get_user_not_found():
    total_users = int(get_total_users())
    more_than_expected_users_amount = total_users + 2

    response = reqres_api('get', f'/api/users/{more_than_expected_users_amount}')

    response_validation.check_status_code(404, response)


def test_create_user():
    schema = load_schema('reqres_api', 'create_user.json')

    response = reqres_api(
        'post',
        '/api/users',
        json={
            "name": "Vova",
            "job": "QA"
        }
    )

    response_validation.check_status_code(201, response)
    response_validation.check_response_json_schema(schema, response)


def test_put_user():
    schema = load_schema('reqres_api', 'put_user.json')
    name = "morpheus"
    job = "zion resisdent"

    response = reqres_api(
        'put',
        '/api/users/2',
        json={
            "name": name,
            "job": job
        }
    )

    response_validation.check_status_code(200, response)
    response_validation.check_response_json_schema(schema, response)


def test_post_successful_login():
    email = "eve.holt@reqres.in"
    password = "cityslicka"
    schema = load_schema('reqres_api', 'post_success_login.json')

    response = reqres_api(
        'post',
        '/api/login',
        json={
            "email": email,
            "password": password
        }
    )

    response_validation.check_status_code(200, response)
    response_validation.check_response_json_schema(schema, response)


def test_post_unsuccessful_login():
    email = "peter@klaven"

    response = reqres_api(
        'post',
        '/api/login',
        json={
            "email": email
        }
    )

    response_validation.check_status_code(400, response)
    with allure.step('Проверяем, что пришла ошибка "Missing password"'):
        assert response.json()['error'] == 'Missing password'


def test_post_successful_registration():
    email = "eve.holt@reqres.in"
    password = "pistol"
    schema = load_schema('reqres_api', 'post_register_user.json')

    response = reqres_api(
        'post',
        '/api/register',
        json={
            "email": email,
            "password": password
        }
    )

    response_validation.check_status_code(200, response)
    response_validation.check_response_json_schema(schema, response)


def test_post_unsuccessful_registration():
    email = "sydney@fife"

    response = reqres_api(
        'post',
        '/api/register',
        json={
            "email": email
        }
    )

    response_validation.check_status_code(400, response)
    with allure.step('Проверяем, что пришла ошибка "Missing password"'):
        assert response.json()['error'] == "Missing password"
