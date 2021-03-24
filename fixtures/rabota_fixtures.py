import re

import pytest

from clients.http_client import HTTPClient
from models.parser_jobs_tut_by import RabotaByParser

url = 'https://rabota.by/search/' \
      'vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=python&page=0'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/webkit-version (KHTML, like Gecko) '
                  'Silk / browser - version like Chrome / chrome - version Safari / webkit - version'}


@pytest.fixture
def get_response():
    return HTTPClient.get(url, headers=HEADERS)


@pytest.fixture
def get_response_from_wrong_url():
    wrong_url = 'https://rabota.by/search/vacncy?clusters=true&' \
                'area=16&enable_snippets=true&salary=&st=searchVacancy&text=python'
    return HTTPClient.get(wrong_url, headers=HEADERS)


@pytest.fixture
def get_query_shotgun():
    url_shotgun = 'https://rabota.by/search/' \
                  'vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=shotgun'
    return HTTPClient.get(url_shotgun, headers=HEADERS)


@pytest.fixture
def get_description_for_first_vacancy():
    response = HTTPClient.get(url, headers=HEADERS).text
    lxml_text = RabotaByParser.get_lxml(response)
    list_id = RabotaByParser.get_list_of_vacancy_id(lxml_text)
    first_vacancy_id = list_id[0]
    response_for_first_vacancy = HTTPClient.get(f'https://rabota.by/vacancy/{first_vacancy_id}?query=python',
                                                headers=HEADERS).text
    description = RabotaByParser.find_vacancy_description(response_for_first_vacancy)
    return description.text.lower()


@pytest.fixture
def get_avg_occurrences_for_words():
    url_for_page = 'https://rabota.by/search/' \
                   'vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=python&page='

    response = HTTPClient.get(url, headers=HEADERS).text
    pages = RabotaByParser.amount_of_pages(response)
    page = 0
    all_urls_list = []
    while page <= int(pages) - 1:
        response = HTTPClient.get(f'{url_for_page}{page}', headers=HEADERS).text
        lxml_text = RabotaByParser.get_lxml(response)
        list_id = RabotaByParser.get_list_of_vacancy_id(lxml_text)
        list_urls_for_one_page = RabotaByParser.get_list_of_url_of_vacancies_pages_by_id(list_id)
        all_urls_list += list_urls_for_one_page
        page += 1
    dictionary = {}
    number = 1
    python = 0
    linux = 0
    flask = 0
    for ur in all_urls_list:
        response = HTTPClient.get(ur, headers=HEADERS).text
        description = RabotaByParser.find_vacancy_description(response)
        description = description.text.lower()
        count_python = RabotaByParser.count_word('python', description)
        count_linux = RabotaByParser.count_word('linux', description)
        count_flask = RabotaByParser.count_word('flask', description)
        dictionary[f'{number} vacancy'] = {'python': count_python, 'linux': count_linux, 'flask': count_flask}
        python += count_python
        linux += count_linux
        flask += count_flask
        number += 1
    avg_python = python // len(all_urls_list)
    avg_linux = linux // len(all_urls_list)
    avg_flask = flask // len(all_urls_list)
    return avg_python, avg_linux, avg_flask


@pytest.fixture
def amount_of_vacancies_founded():
    response = HTTPClient.get(url, headers=HEADERS).text
    lxml_text = RabotaByParser.get_lxml(response)
    h1_text = lxml_text.find('h1', class_='bloko-header-1').text
    pattern = '\d+'
    return int(re.findall(pattern, h1_text)[0])


@pytest.fixture
def amount_vacancies_on_one_page(get_response):
    lxml_text = RabotaByParser.get_lxml(get_response.text)
    list_id = RabotaByParser.get_list_of_vacancy_id(lxml_text)
    return len(list_id)
