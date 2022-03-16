from matplotlib import pyplot as plt
from alive_progress import alive_bar
from collections import Counter
import requests


def get_requests_and_parse(title: str):

    links, names, data_keys, data_count = (list() for _ in range(4))
    
    for job in title:
        data = []
        with alive_bar(len(data)) as bar:
            bar()
            for pages in range(0, 20):
                url = 'https://api.hh.ru/vacancies/'
                param = {'text': job, 'area': '113', 'page': pages}
                session = requests.get(url, params=param)
                assert session.status_code == 200
                json = session.json()
                data.append(json)

    with alive_bar(len(links)) as bar:
        for items in data:
            bar()
            for url_pages in range(0, 20):
                links.append(items['items'][url_pages]['url'])

    with alive_bar(len(names)) as bar:
        for urls in links:
            bar()
            response = requests.get(urls)
            assert response.status_code == 200
            dict_json = response.json()
            for links_pages in dict_json['key_skills']:
                names.append(links_pages['name'])
 
    count = dict(Counter(names))
    search_links = len(links)

    with alive_bar(len(data_keys)) as bar:
        for key in count:
            bar()
            if count[key] >= 40:
                if len(key) < 18:
                    data_keys.append(key)
                    data_count.append(count[key])

    plt.bar(range(len(data_keys)), data_count)
    plt.title(f'Количество совпадений значений на {search_links} вакансии: ')
    plt.xticks(range(len(data_keys)), data_keys)
    plt.grid(axis='y')
    plt.show()

    
if __name__ == '__main__':
    """ Example: QA Engineer and Тестировщик ПО """
    title = ['QA Engineer' and 'Тестировщик ПО']
    get_requests_and_parse(title)
