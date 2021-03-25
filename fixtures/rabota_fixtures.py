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
def get_description_for_first_vacancy():
    """
    Returns description for first vacancy
    """
    return RabotaByParser.get_description_for_first_vacancy()


@pytest.fixture
def amount_of_vacancies_founded_for_python():
    """
    Returns amount of vacancies founded from query
    """
    return RabotaByParser.amount_of_vacancies_founded('python')


@pytest.fixture
def amount_vacancies_on_one_page():
    """
    Returns amount of vacancies founded from query on one page
    """
    return RabotaByParser.amount_vacancies_on_one_page()


@pytest.fixture
def avg_occurrences_for_word_python():
    return RabotaByParser.get_avg_occurrences_for_words()[0]


@pytest.fixture
def avg_occurrences_for_word_linux():
    return RabotaByParser.get_avg_occurrences_for_words()[1]


@pytest.fixture
def avg_occurrences_for_word_flask():
    return RabotaByParser.get_avg_occurrences_for_words()[2]
