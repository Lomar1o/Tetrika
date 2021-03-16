import requests
import time
from bs4 import BeautifulSoup
from collections import defaultdict


class Parser:

    def __init__(self):
        self.url = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0' \
                   '%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D' \
                   '0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%' \
                   'D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
        self.data = defaultdict(int)
        self.response = None

    def get_response(self):
        response = requests.get(self.url, timeout=15)
        response = response.text
        self.response = BeautifulSoup(response, 'lxml')

    def get_name(self):
        links = self.response.find(class_='mw-category').find_all('a')
        for link in links:
            first_letter = link.text[0]
            self.data[first_letter] += 1
        return self.data

    def get_next_page(self):
        links = self.response.find(id='mw-pages').find_all('a')
        for link in links:
            if link.text == 'Следующая страница':
                self.url = 'https://ru.wikipedia.org/' + link.get('href')
                self.run()

    def run(self):
        self.get_response()
        self.get_name()
        self.get_next_page()
        return self.data


def main():
    start = time.time()
    parser = Parser()
    res = parser.run()
    print(time.time() - start)
    for key, value in res.items():
        print(key, value)


if __name__ == '__main__':
    main()
