import re

from bs4 import BeautifulSoup


class RabotaByParser:
    """
    Parser for jobs.tut.by
    """

    @staticmethod
    def get_lxml(source):
        """
        Getting lxml version of source text
        :param source: source text
        :type source: string
        :return: lxml version of source text
        :rtype: string
        """
        return BeautifulSoup(source, 'lxml')

    @staticmethod
    def get_amount_of_pages(source):
        soup = BeautifulSoup(source, 'lxml')
        span = soup.find('span', class_='pager-item-not-in-short-range')
        return span.text

    @staticmethod
    def get_list_of_vacancy_id(text):
        """
        Getting list of vacancies id from jobs.tut.by
        :param text: text of web page
        :type text: string
        :return: list of vacancies id
        :rtype: list
        """
        pattern = '"vacancyId": "\d{8}"'
        vacancies_list = re.findall(pattern, str(text))
        list_with_unique_id = set(vacancies_list)
        vacancies_id_list = []
        for vacancy_id in list_with_unique_id:
            pattern_id = '\d{8}'
            id = re.findall(pattern_id, vacancy_id)
            vacancies_id_list.append(id[0])
        return vacancies_id_list

    @staticmethod
    def get_list_of_url_of_vacancies_pages_by_id(list_of_id):
        """
        Getting list of vacancies urls by id
        :param list_of_id: list of vacancies id
        :type list_of_id: list
        :return: list of vacancies urls
        :rtype: list
        """
        list_of_url = []
        for id in list_of_id:
            list_of_url.append(f'https://rabota.by/vacancy/{id}?query=python')
        return list_of_url

    @staticmethod
    def find_vacancy_description(source):
        """
        Find vacancy description from source of the web page
        :param source: source of the web page
        :type source:
        :return: vacancy description
        :rtype: Bs4
        """
        soup = BeautifulSoup(source, 'lxml')
        return soup.find('div', class_='vacancy-description')

    @staticmethod
    def count_word(word, text):
        """
        Count number of mentioning word in the text
        :param word: defined word
        :type word: str
        :param text: text
        :type text: str
        :return: number of mentioning
        :rtype: int
        """
        return text.count(word)

    @staticmethod
    def amount_of_pages(query_content):
        """
        Get amount of pages for the response
        :param query_content: Content of query
        :type query_content:
        :return: amount of pages
        :rtype: str
        """
        soup = BeautifulSoup(query_content, 'lxml')
        pages = soup.findAll('a', class_='bloko-button HH-Pager-Control')
        return pages[-1].text



