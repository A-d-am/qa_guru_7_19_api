import requests
from qa_guru_7_19_api.utils import load_schema
from qa_guru_7_19_api import response_validation
import allure

base_url = 'https://catfact.ninja'


def test_get_breeds():
    schema = load_schema('cat_facts', 'get_breeds.json')

    with allure.step('Отправляем GET /breeds'):
        response = requests.get(url=base_url + '/breeds')

    response_validation.check_status_code(200, response)
    response_validation.check_response_json_schema(schema, response)


def test_get_fact():
    schema = load_schema('cat_facts', 'get_fact.json')

    with allure.step('Отправляем GET /fact'):
        response = requests.get(url=base_url + '/fact')

    response_validation.check_status_code(200, response)
    response_validation.check_response_json_schema(schema, response)


def test_get_facts():
    schema = load_schema('cat_facts', 'get_facts.json')

    with allure.step('Отправляем GET /facts'):
        response = requests.get(url=base_url + '/facts')

    response_validation.check_status_code(200, response)
    response_validation.check_response_json_schema(schema, response)
