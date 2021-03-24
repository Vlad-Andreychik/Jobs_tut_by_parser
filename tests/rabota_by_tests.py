import math

from models.parser_jobs_tut_by import RabotaByParser


def test_connection(get_response):
    """
    test connection of the web site
    """
    assert get_response.status_code == 200


def test_shotgun_not_found(get_query_shotgun):
    """
    test that there are no search results for the word "shotgun"
    """
    assert 'По запросу «shotgun» ничего не найдено' in get_query_shotgun.text


def test_occurrence_of_the_words(get_description_for_first_vacancy, get_avg_occurrences_for_words):
    """
    test that the occurrence of words "python", "linux", "flask" is within boundaries avg +- 1
    """
    description = get_description_for_first_vacancy
    count_python = RabotaByParser.count_word('python', description)
    count_linux = RabotaByParser.count_word('linux', description)
    count_flask = RabotaByParser.count_word('flask', description)
    assert count_python in range(get_avg_occurrences_for_words[0] - 1, get_avg_occurrences_for_words[0] + 2)
    assert count_linux in range(get_avg_occurrences_for_words[1] - 1, get_avg_occurrences_for_words[1] + 2)
    assert count_flask in range(get_avg_occurrences_for_words[2] - 1, get_avg_occurrences_for_words[2] + 2)


def test_amount_vacancies_on_one_page(amount_vacancies_on_one_page):
    """
    test that amount vacancies on one page is equal to 50
    """
    assert amount_vacancies_on_one_page == 50


def test_accordance_amount_pages_for_amount_of_vacancies(amount_of_vacancies_founded, amount_vacancies_on_one_page,
                                                         get_response):
    """
    test that there is correct number of pages for our amount of vacancies
    """
    actual_number_of_pages = RabotaByParser.amount_of_pages(get_response.text)
    estimated_number_of_pages = math.ceil(amount_of_vacancies_founded / amount_vacancies_on_one_page)
    assert estimated_number_of_pages == int(actual_number_of_pages)


def test_wrong_url(get_response_from_wrong_url):
    """
    test connection with wrong url
    """
    assert get_response_from_wrong_url.status_code == 404
