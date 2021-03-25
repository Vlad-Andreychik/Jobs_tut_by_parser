import re

from bs4 import BeautifulSoup

from clients.http_client import HTTPClient


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

    @staticmethod
    def get_description_for_first_vacancy():
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/webkit-version (KHTML, like Gecko) '
                          'Silk / browser - version like Chrome / chrome - version Safari / webkit - version'}
        url = 'https://rabota.by/search/' \
              'vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=python&page=0'
        response = HTTPClient.get(url, headers=headers).text
        lxml_text = RabotaByParser.get_lxml(response)
        list_id = RabotaByParser.get_list_of_vacancy_id(lxml_text)
        first_vacancy_id = list_id[0]
        response_for_first_vacancy = HTTPClient.get(f'https://rabota.by/vacancy/{first_vacancy_id}?query=python',
                                                    headers=headers).text
        description = RabotaByParser.find_vacancy_description(response_for_first_vacancy)
        return description.text.lower()

    @staticmethod
    def get_avg_occurrences_for_words():
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/webkit-version (KHTML, like Gecko) '
                          'Silk / browser - version like Chrome / chrome - version Safari / webkit - version'}
        url_for_page = 'https://rabota.by/search/' \
                       'vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=python&page='
        url = 'https://rabota.by/search/' \
              'vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=python&page=0'
        response = HTTPClient.get(url, headers=headers).text
        pages = RabotaByParser.amount_of_pages(response)
        page = 0
        all_urls_list = []
        while page <= int(pages) - 1:
            response = HTTPClient.get(f'{url_for_page}{page}', headers=headers).text
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
            response = HTTPClient.get(ur, headers=headers).text
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

    @staticmethod
    def amount_of_vacancies_founded(query):
        """
        Returns amount of vacancies founded from query
        """
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/webkit-version (KHTML, like Gecko) '
                          'Silk / browser - version like Chrome / chrome - version Safari / webkit - version'}
        url = f'https://rabota.by/search/' \
              f'vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text={query}&page=0'
        response = HTTPClient.get(url, headers=headers).text
        lxml_text = RabotaByParser.get_lxml(response)
        h1_text = lxml_text.find('h1', class_='bloko-header-1').text
        pattern = '\d+'
        return int(re.findall(pattern, h1_text)[0])

    @staticmethod
    def amount_vacancies_on_one_page():
        """
        Returns amount of vacancies founded from query on one page
        """
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/webkit-version (KHTML, like Gecko) '
                          'Silk / browser - version like Chrome / chrome - version Safari / webkit - version'}
        url = 'https://rabota.by/search/' \
              'vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=python&page=0'
        response = HTTPClient.get(url, headers=headers)
        lxml_text = RabotaByParser.get_lxml(response.text)
        list_id = RabotaByParser.get_list_of_vacancy_id(lxml_text)
        return len(list_id)
