"""
Module contains fixtures for rabota_by_tests.py
"""
import re
import math
import pytest

from clients.http_client import HTTPClient
from models.parser_jobs_tut_by import RabotaByParser


@pytest.fixture
def get_response():
    """
    Getting response for 'python' query
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/webkit-version (KHTML, like Gecko) '
                      'Silk / browser - version like Chrome / chrome - version Safari / webkit - version'}
    url = 'https://rabota.by/search/' \
          'vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=python&page=0'
    return HTTPClient.get(url, headers=headers)


@pytest.fixture
def get_response_from_wrong_url():
    """
    Getting response for incorrect url
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/webkit-version (KHTML, like Gecko) '
                      'Silk / browser - version like Chrome / chrome - version Safari / webkit - version'}
    wrong_url = 'https://rabota.by/search/vacncy?clusters=true&' \
                'area=16&enable_snippets=true&salary=&st=searchVacancy&text=python'
    return HTTPClient.get(wrong_url, headers=headers)


@pytest.fixture
def get_query_shotgun():
    """
    Getting response for 'shotgun' query
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/webkit-version (KHTML, like Gecko) '
                      'Silk / browser - version like Chrome / chrome - version Safari / webkit - version'}
    url_shotgun = 'https://rabota.by/search/' \
                  'vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=shotgun'
    return HTTPClient.get(url_shotgun, headers=headers)


@pytest.fixture
def id_for_first_vacancy(get_response):
    """
    Returns id for first vacancy
    """
    lxml_text = RabotaByParser.get_lxml(get_response.text)
    list_id = RabotaByParser.get_list_of_vacancy_id(lxml_text)
    return list_id[0]


@pytest.fixture
def get_response_for_first_vacancy_by_id(id_for_first_vacancy):
    """
    Getting response for first vacancy of 'python' query
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/webkit-version (KHTML, like Gecko) '
                      'Silk / browser - version like Chrome / chrome - version Safari / webkit - version'}
    return HTTPClient.get(f'https://rabota.by/vacancy/{id_for_first_vacancy}', headers=headers)


@pytest.fixture
def description_for_first_vacancy(get_response_for_first_vacancy_by_id):
    """
    Returns description for first vacancy in query 'python'
    """
    return RabotaByParser.find_vacancy_description(get_response_for_first_vacancy_by_id.text).text.lower()


@pytest.fixture
def occur_python_on_first_vacancy(description_for_first_vacancy):
    """
    Returns amount of occurrences for the word 'python' on the first vacancy
    """
    return RabotaByParser.count_word('python', description_for_first_vacancy)


@pytest.fixture
def occur_linux_on_first_vacancy(description_for_first_vacancy):
    """
    Returns amount of occurrences for the word 'linux' on the first vacancy
    """
    return RabotaByParser.count_word('linux', description_for_first_vacancy)


@pytest.fixture
def occur_flask_on_first_vacancy(description_for_first_vacancy):
    """
    Returns amount of occurrences for the word 'flask' on the first vacancy
    """
    return RabotaByParser.count_word('flask', description_for_first_vacancy)


@pytest.fixture
def avg_occur_for_python(get_response):
    """
    Returns average amount of occurrences for word python
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/webkit-version (KHTML, like Gecko) '
                      'Silk / browser - version like Chrome / chrome - version Safari / webkit - version'}
    url_for_page = 'https://rabota.by/search/' \
                   'vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=python&page='
    pages = RabotaByParser.amount_of_pages(get_response.text)
    page = 0
    all_urls_list = []
    while page <= int(pages) - 1:
        response = HTTPClient.get(f'{url_for_page}{page}', headers=headers).text
        lxml_text = RabotaByParser.get_lxml(response)
        list_id = RabotaByParser.get_list_of_vacancy_id(lxml_text)
        list_urls_for_one_page = RabotaByParser.get_list_of_url_of_vacancies_pages_by_id(list_id)
        all_urls_list += list_urls_for_one_page
        page += 1
    counter_for_word = 0
    for ur in all_urls_list:
        response = HTTPClient.get(ur, headers=headers).text
        description = RabotaByParser.find_vacancy_description(response)
        description = description.text.lower()
        counter_for_word_on_one_page = RabotaByParser.count_word('python', description)
        counter_for_word += counter_for_word_on_one_page
    avg_word = counter_for_word // len(all_urls_list)
    return avg_word


@pytest.fixture
def avg_occur_for_linux(get_response):
    """
    Returns average amount of occurrences for word linux
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/webkit-version (KHTML, like Gecko) '
                      'Silk / browser - version like Chrome / chrome - version Safari / webkit - version'}
    url_for_page = 'https://rabota.by/search/' \
                   'vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=python&page='
    pages = RabotaByParser.amount_of_pages(get_response.text)
    page = 0
    all_urls_list = []
    while page <= int(pages) - 1:
        response = HTTPClient.get(f'{url_for_page}{page}', headers=headers).text
        lxml_text = RabotaByParser.get_lxml(response)
        list_id = RabotaByParser.get_list_of_vacancy_id(lxml_text)
        list_urls_for_one_page = RabotaByParser.get_list_of_url_of_vacancies_pages_by_id(list_id)
        all_urls_list += list_urls_for_one_page
        page += 1
    counter_for_word = 0
    for ur in all_urls_list:
        response = HTTPClient.get(ur, headers=headers).text
        description = RabotaByParser.find_vacancy_description(response)
        description = description.text.lower()
        counter_for_word_on_one_page = RabotaByParser.count_word('linux', description)
        counter_for_word += counter_for_word_on_one_page
    avg_word = counter_for_word // len(all_urls_list)
    return avg_word


@pytest.fixture
def avg_occur_for_flask(get_response):
    """
    Returns average amount of occurrences for word flask
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/webkit-version (KHTML, like Gecko) '
                      'Silk / browser - version like Chrome / chrome - version Safari / webkit - version'}
    url_for_page = 'https://rabota.by/search/' \
                   'vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=python&page='
    pages = RabotaByParser.amount_of_pages(get_response.text)
    page = 0
    all_urls_list = []
    while page <= int(pages) - 1:
        response = HTTPClient.get(f'{url_for_page}{page}', headers=headers).text
        lxml_text = RabotaByParser.get_lxml(response)
        list_id = RabotaByParser.get_list_of_vacancy_id(lxml_text)
        list_urls_for_one_page = RabotaByParser.get_list_of_url_of_vacancies_pages_by_id(list_id)
        all_urls_list += list_urls_for_one_page
        page += 1
    counter_for_word = 0
    for ur in all_urls_list:
        response = HTTPClient.get(ur, headers=headers).text
        description = RabotaByParser.find_vacancy_description(response)
        description = description.text.lower()
        counter_for_word_on_one_page = RabotaByParser.count_word('flask', description)
        counter_for_word += counter_for_word_on_one_page
    avg_word = counter_for_word // len(all_urls_list)
    return avg_word


@pytest.fixture
def amount_of_vacancies_founded_for_python(get_response):
    """
    Returns amount of vacancies founded from query
    """
    lxml_text = RabotaByParser.get_lxml(get_response.text)
    h1_text = lxml_text.find('h1', class_='bloko-header-1').text
    pattern = '\d+'
    return int(re.findall(pattern, h1_text)[0])


@pytest.fixture
def amount_vacancies_on_one_page(get_response):
    """
    Returns amount of vacancies founded from query on one page
    """
    lxml_text = RabotaByParser.get_lxml(get_response.text)
    list_id = RabotaByParser.get_list_of_vacancy_id(lxml_text)
    return len(list_id)


@pytest.fixture
def estimated_number_of_pages(get_response, amount_vacancies_on_one_page, amount_of_vacancies_founded_for_python):
    """
    Returns estimated number of pages for query
    """
    return math.ceil(amount_of_vacancies_founded_for_python / amount_vacancies_on_one_page)


@pytest.fixture
def amount_of_pages(get_response):
    """
    Returns actual number of pages for query
    """
    return int(RabotaByParser.amount_of_pages(get_response.text))
