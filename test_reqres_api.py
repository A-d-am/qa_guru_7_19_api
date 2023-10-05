import requests
import jsonschema
from utils import load_schema


def test_ok_status_code():
    response = requests.get(url='https://reqres.in/api/users/2')

    assert response.status_code == 200


def test_get_users():
    schema = load_schema('get_users.json')
    response = requests.get(url='https://reqres.in/api/users?page=2')

    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)


def test_get_user():
    schema = load_schema('get_single_user.json')
    response = requests.get(url='https://reqres.in/api/users/2')

    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)


def test_get_user_not_found():
    response = requests.get(url='https://reqres.in/api/users/?page=2')
    total_users = response.json()['total']

    response_with_404 = requests.get(url=f'https://reqres.in/api/users/{int(total_users) + 2}')
    assert response_with_404.status_code == 404


def test_create_user():
    schema = load_schema('create_user.json')
    response = requests.post(
        url='https://reqres.in/api/users',
        json={
            "name": "Vova",
            "job": "QA"
        }
    )
    assert response.status_code == 201
    jsonschema.validate(response.json(), schema)


def test_put_user():
    schema = load_schema('put_user.json')
    name = "morpheus"
    job = "zion resisdent"

    response = requests.put(
        url='https://reqres.in/api/users/2',
        json={
            "name": name,
            "job": job
        }
    )
    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)


def test_post_successful_login():
    schema = load_schema('post_success_login.json')
    response = requests.post(
        url='https://reqres.in/api/login',
        json={
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        }
    )
    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)


def test_post_unsuccessful_login():
    response = requests.post(
        url='https://reqres.in/api/login',
        json={
            "email": "peter@klaven"
        }
    )
    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'


def test_post_successful_registration():
    schema = load_schema('post_register_user.json')
    response = requests.post(
        url='https://reqres.in/api/register',
        json={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
    )
    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)


def test_post_unsuccessful_registration():
    response = requests.post(
        url='https://reqres.in/api/register',
        json={
            "email": "sydney@fife"
        }
    )
    assert response.status_code == 400
    assert response.json()['error'] == "Missing password"
