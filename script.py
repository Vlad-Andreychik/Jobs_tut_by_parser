"""
Script finds info about occurrences of words 'python', 'linux', 'flask' in each vacancy for query 'python'
"""
from clients.http_client import HTTPClient
from models.parser_jobs_tut_by import RabotaByParser

# declare variables for headers and url
HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/webkit-version (KHTML, like Gecko) '
                  'Silk / browser - version like Chrome / chrome - version Safari / webkit - version'}
URL = 'https://rabota.by/search/' \
      'vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=python&page=0'
url_for_page = 'https://rabota.by/search/' \
               'vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=python&page='

# Get content of the response
response = HTTPClient.get(URL, headers=HEADERS).text
# Get amount of response pages
pages = RabotaByParser.amount_of_pages(response)
# Set page counter
page = 0
# Set list of vacancies urls
all_urls_list = []
# Loop for taking all vacancies urls from every response page
while page <= int(pages) - 1:
    # Get content of the response for defined page
    response = HTTPClient.get(f'{url_for_page}{page}', headers=HEADERS).text
    # Get lxml text for content of the response
    lxml_text = RabotaByParser.get_lxml(response)
    # Get list of vacancies id
    list_id = RabotaByParser.get_list_of_vacancy_id(lxml_text)
    # Get list of urls of vacancies
    list_urls_for_one_page = RabotaByParser.get_list_of_url_of_vacancies_pages_by_id(list_id)
    # Fill list of all urls
    all_urls_list += list_urls_for_one_page
    # Increment number of page
    page += 1
# Set a dictionary
dictionary = {}
# Set number of vacancy
number = 1
# Set counter for python word
python = 0
# Set counter for linux word
linux = 0
# Set counter for flask word
flask = 0
# Loop for counting defined words in vacancies description
for url in all_urls_list:
    # Get content of the response
    response = HTTPClient.get(url, headers=HEADERS).text
    # Get vacancy description from the response
    description = RabotaByParser.find_vacancy_description(response)
    # Take only text from description and make it in lowercase
    description = description.text.lower()
    # Count python in description
    count_python = RabotaByParser.count_word('python', description)
    # Count linux in description
    count_linux = RabotaByParser.count_word('linux', description)
    # Count flask in description
    count_flask = RabotaByParser.count_word('flask', description)
    # Fill dict with info about amount of mentioning for every defined word in every description
    dictionary[f'{number} vacancy'] = {'python': count_python, 'linux': count_linux, 'flask': count_flask}
    # Count all mentioning for python
    python += count_python
    # Count all mentioning for linux
    linux += count_linux
    # Count all mentioning for flask
    flask += count_flask
    # Increment number of vacancy
    number += 1
print(dictionary)
print(len(all_urls_list), python, linux, flask)
# Calculate average number of occurrence of python
avg_python = python / len(all_urls_list)
# Calculate average number of occurrence of linux
avg_linux = linux / len(all_urls_list)
# Calculate average number of occurrence of flask
avg_flask = flask / len(all_urls_list)
print(avg_python, avg_linux, avg_flask)

