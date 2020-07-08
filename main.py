import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


# Форматируем строку с рейтингом.
def refined(s):
    r = s.split(' ')[1]
    return r


def write_csv(data):
    with open('cmc.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow([
            data['name'],
            data['symbol'],
            data['link'],
            data['price']
        ])


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('tbody').find_all('tr')  # В tbody находим все tr.
    for tr in trs:
        tds = tr.find_all('td')  # Получаем список ТДсок.
        name = tds[1].find('a').text  # Тэг 'a' второго элемента списка содержит имя валюты.
        symbol = refined(tds[5].text)
        link = 'https://coinmarketcap.com' + tds[1].find('a').get('href')
        price = tds[3].find('a').text
        data = {
            'name': name,
            'symbol': symbol,
            'link': link,
            'price': price
        }

        write_csv(data)


def main():
    url = 'https://coinmarketcap.com'
    get_page_data(get_html(url))


if __name__ == '__main__':
    main()
