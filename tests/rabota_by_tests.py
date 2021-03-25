import math

from models.parser_jobs_tut_by import RabotaByParser


def test_connection(get_response):
    assert get_response.status_code == 200, 'Connection error'


def test_shotgun_not_found(get_query_shotgun):
    assert 'По запросу «shotgun» ничего не найдено' in get_query_shotgun.text, 'Query give responses'


def test_occurrence_of_the_words(get_description_for_first_vacancy, avg_occurrences_for_word_python,
                                 avg_occurrences_for_word_linux, avg_occurrences_for_word_flask):
    description = get_description_for_first_vacancy
    count_python = RabotaByParser.count_word('python', description)
    count_linux = RabotaByParser.count_word('linux', description)
    count_flask = RabotaByParser.count_word('flask', description)
    assert count_python in range(avg_occurrences_for_word_python[0] - 1, avg_occurrences_for_word_python[0] + 2)
    assert count_linux in range(avg_occurrences_for_word_linux[1] - 1, avg_occurrences_for_word_linux[1] + 2)
    assert count_flask in range(avg_occurrences_for_word_flask[2] - 1, avg_occurrences_for_word_flask[2] + 2)


def test_amount_vacancies_on_one_page(amount_vacancies_on_one_page):
    assert amount_vacancies_on_one_page == 50, 'Incorrect amount of vacancies on one page'


def test_accordance_amount_pages_for_amount_of_vacancies(amount_of_vacancies_founded_for_python,
                                                         amount_vacancies_on_one_page,
                                                         get_response):
    actual_number_of_pages = RabotaByParser.amount_of_pages(get_response.text)
    estimated_number_of_pages = math.ceil(amount_of_vacancies_founded_for_python / amount_vacancies_on_one_page)
    assert estimated_number_of_pages == int(actual_number_of_pages), 'Incorrect amount of pages'


def test_wrong_url(get_response_from_wrong_url):
    assert get_response_from_wrong_url.status_code == 404, 'Correct url entered'
