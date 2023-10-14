import requests
import jsonschema
from qa_guru_7_19_api.utils import load_schema
import allure

base_url = 'https://reqres.in'


def get_total_users():
    response = requests.get(url=f'{base_url}/api/users/?page=2')
    total_users = response.json()['total']
    return total_users


def check_status_code(expected_code, response):
    with allure.step(f'Проверяем, что пришел status code = {expected_code}'):
        assert response.status_code == expected_code, \
            f'Пришел неверный статус код: ожидался {expected_code}, пришел {response.status_code}'


def check_response_json_schema(expected_schema, response):
    with allure.step('Проверяем содержание response.json'):
        jsonschema.validate(response.json(), expected_schema)


def test_ok_status_code():
    with allure.step('Отправляем запрос GET /api/users/2'):
        response = requests.get(url=f'{base_url}/api/users/2')
    check_status_code(200, response)


def test_get_users():
    schema = load_schema('get_users.json')
    with allure.step('Отправляем запрос GET /api/users?page=2'):
        response = requests.get(url=f'{base_url}/api/users?page=2')

    check_status_code(200, response)
    check_response_json_schema(schema, response)


def test_get_user():
    schema = load_schema('get_single_user.json')
    with allure.step('Отправляем запрос GET /api/users/2'):
        response = requests.get(url=f'{base_url}/api/users/2')

    check_status_code(200, response)
    check_response_json_schema(schema, response)


def test_get_user_not_found():
    total_users = int(get_total_users())
    more_than_expected_users_amount = total_users + 2

    with allure.step(f'Отправляем запрос GET /api/users/{more_than_expected_users_amount}'):
        response_with_404 = requests.get(url=f'{base_url}/api/users/{more_than_expected_users_amount}')

    check_status_code(404, response_with_404)


def test_create_user():
    schema = load_schema('create_user.json')

    with allure.step('Отправляем POST /api/users'):
        response = requests.post(
            url=f'{base_url}/api/users',
            json={
                "name": "Vova",
                "job": "QA"
            }
        )

    check_status_code(201, response)
    check_response_json_schema(schema, response)


def test_put_user():
    schema = load_schema('put_user.json')
    name = "morpheus"
    job = "zion resisdent"
    with allure.step(f'Отправляем PUT /api/users/2 c name={name}, job={job}'):
        response = requests.put(
            url=f'{base_url}/api/users/2',
            json={
                "name": name,
                "job": job
            }
        )
    check_status_code(200, response)
    check_response_json_schema(schema, response)


def test_post_successful_login():
    email = "eve.holt@reqres.in"
    password = "cityslicka"
    schema = load_schema('post_success_login.json')

    with allure.step(f'Отправляем запрос POST /api/login c email ={email}, password={password}'):
        response = requests.post(
            url=f'{base_url}/api/login',
            json={
                "email": email,
                "password": password
            }
        )

    check_status_code(200, response)
    check_response_json_schema(schema, response)


def test_post_unsuccessful_login():
    email = "peter@klaven"

    with allure.step(f'Отправляем запрос POST /api/login c email={email}'):
        response = requests.post(
            url=f'{base_url}/api/login',
            json={
                "email": email
            }
        )

    check_status_code(400, response)
    with allure.step('Проверяем, что пришла ошибка "Missing password"'):
        assert response.json()['error'] == 'Missing password'


def test_post_successful_registration():
    schema = load_schema('post_register_user.json')
    response = requests.post(
        url=f'{base_url}/api/register',
        json={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
    )
    check_status_code(200, response)
    check_response_json_schema(schema, response)


def test_post_unsuccessful_registration():
    email = "sydney@fife"

    with allure.step('Отправляем запрос POST /api/register'):
        response = requests.post(
            url=f'{base_url}/api/register',
            json={
                "email": email
            }
        )

    check_status_code(400, response)
    with allure.step('Проверяем, что пришла ошибка "Missing password"'):
        assert response.json()['error'] == "Missing password"
