from qa_guru_7_19_api.utils import load_schema
from qa_guru_7_19_api import response_validation
from allure_commons.types import AttachmentType
from requests import sessions
from curlify import to_curl
import allure
import json


def catfact_api(method, url, **kwargs):
    args = kwargs
    base_url = 'https://catfact.ninja'
    new_url = base_url + url
    method = method.upper()
    with allure.step(f'Отправляем запрос {method} {url} {args if len(args) != 0 else ''}'):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            message = to_curl(response.request)
            allure.attach(body=message.encode('utf8'), name='Curl', attachment_type=AttachmentType.TEXT,
                          extension='txt')
            allure.attach(body=json.dumps(response.json(), indent=4).encode("utf8"), name="Response Json",
                          attachment_type=AttachmentType.JSON, extension='json')
    return response


def test_get_breeds():
    schema = load_schema('cat_facts', 'get_breeds.json')

    response = catfact_api('get', '/breeds')

    response_validation.check_status_code(200, response)
    response_validation.check_response_json_schema(schema, response)


def test_get_fact():
    schema = load_schema('cat_facts', 'get_fact.json')

    response = catfact_api('get', '/fact')

    response_validation.check_status_code(200, response)
    response_validation.check_response_json_schema(schema, response)


def test_get_facts():
    schema = load_schema('cat_facts', 'get_facts.json')

    response = catfact_api('get', '/facts')

    response_validation.check_status_code(200, response)
    response_validation.check_response_json_schema(schema, response)
