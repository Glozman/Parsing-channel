import requests
from bs4 import BeautifulSoup
import csv

FILENAME = "telemetr.csv"

category = input('Введите категорию:')

URL = f'https://telemetr.me/channels/cat/{category}/?page=1'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }


def get_site(url, params=None):
    site = requests.get(url, headers=HEADERS, params=params)
    return site


def get_pages_count(link):
    soup = BeautifulSoup(link, 'html.parser')
    pagination = soup.find_all('a', class_='btn-light')
    return int(pagination[-1].text)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items_even = soup.find_all('tr', class_='tr_even')
    items_odd = soup.find_all('tr', class_='tr_odd')
    items_even = items_even[::2]
    items_odd = items_odd[::2]
    i = 0
    for item in items_odd:
        items_even.insert(i + 1, item)
        i += 2
    items = items_even
    channel = []
    for item in items:
        channel.append({
            'link': item.find('a', class_='kt-ch-title').get('href'),
            'Name': item.find('a', class_='kt-ch-title').get_text()
        })
    return channel

def save_file(items, path=None):
    with open(FILENAME, "w", encoding='utf-8', newline="") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Название", "Ссылка"])
        for item in items:
            writer.writerow([item['Name'], item['link']])

def parse():
    site = get_site(URL)
    if site.status_code == 200:
        channel = []
        pages = get_pages_count(site.text)
        for page in range(1, pages + 1):
            print(f'Парсинг {page} из {pages}...')
            site = get_site(URL, params={'page': page})
            channel.extend(get_content(site.content))
        save_file(channel, FILENAME)
        for i in range(len(channel)):
            print(f'№{i+1}.{channel[i]["Name"]}-->{channel[i]["link"]}')
    else:
        print('error')


parse()
