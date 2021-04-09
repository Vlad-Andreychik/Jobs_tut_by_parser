import pytest


def test_connection(get_response):
    assert get_response.status_code == 200, 'Connection error'


def test_shotgun_not_found(get_query_shotgun):
    assert 'По запросу «shotgun» ничего не найдено' in get_query_shotgun.text, 'Info message not found'


def test_occurrence_of_the_words(avg_occur_for_python, avg_occur_for_linux, avg_occur_for_flask,
                                 occur_python_on_first_vacancy, occur_linux_on_first_vacancy,
                                 occur_flask_on_first_vacancy):
    assert occur_python_on_first_vacancy in range(avg_occur_for_python - 1, avg_occur_for_python + 2),\
        f'Occurrence of word is out of boundaries avg +- 1'
    assert occur_linux_on_first_vacancy in range(avg_occur_for_linux - 1, avg_occur_for_linux + 2),\
        f'Occurrence of word is out of boundaries avg +- 1'
    assert occur_flask_on_first_vacancy in range(avg_occur_for_flask - 1, avg_occur_for_flask  + 2),\
        f'Occurrence of word is out of boundaries avg +- 1'


def test_amount_vacancies_on_one_page(amount_vacancies_on_one_page):
    assert amount_vacancies_on_one_page == 50, 'Incorrect amount of vacancies on one page'


def test_accordance_amount_pages_for_amount_of_vacancies(estimated_number_of_pages, amount_of_pages):
    assert estimated_number_of_pages == amount_of_pages, 'Incorrect amount of pages'


def test_wrong_url(get_response_from_wrong_url):
    assert get_response_from_wrong_url.status_code == 404, "Response didn't return 404 code"
