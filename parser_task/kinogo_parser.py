import os
import requests
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool
import sqlite3
import argparse


parser = argparse.ArgumentParser(description='Kinogo_parser')
parser.add_argument('page', type=int, help='Number of pages')
args = parser.parse_args()
PAGE = args.page+1


def get_html(url):
    r = requests.get(url)
    return r.text


def get_file(url):
    r = requests.get(url, stream=True)
    return r


def get_name_screen(url, title):
    name = url.split('/')[-1]
    folder = 'media/screens/' + title.split('/')[-1].split('.')[0]
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.abspath(folder)
    screen_name = path + '/' + name
    return screen_name


def get_name_poster(url):
    name = url.split('/')[-1]
    if not os.path.exists('media/poster'):
        os.makedirs('media/poster')
    path = os.path.abspath('media/poster')
    poster_name = path + '/' + name
    return poster_name


def save_image(name, file_object):
    with open(name, 'bw') as f:
        for chunk in file_object.iter_content(8192):
            f.write(chunk)


def write_data(data):
    inf, abs_poster, abs_screen = data
    conn = sqlite3.connect('db.sqlite3')
    with conn:
        cursor = conn.cursor()
        keys, values = zip(*inf.items())
        insert_str = "INSERT INTO kinogo_film (%s) values (%s)" % (
            ",".join(keys), ",".join(['?'] * len(keys)))
        cursor.execute(insert_str, values)
        last_id = cursor.lastrowid
        kinogo_poster = (abs_poster, last_id)
        cursor.execute("INSERT INTO kinogo_poster (abs_poster, films_id) values (?, ?)",
                       kinogo_poster)
        if not abs_screen == []:
            for screen in abs_screen:
                kinogo_screen = (screen, last_id)
                cursor.execute("INSERT INTO kinogo_screen (abs_screen, films_id) values (?, ?)",
                               kinogo_screen)


def get_page_data(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('div', class_="kino-title-full").find('span').text.split(' (')[0]
    inf = soup.find('div', class_='kino-text')
    poster = 'http://kinogo-net.org' + inf.find('img').get('src')
    duration = ' '.join(re.findall(r'\d{2}:\d{2}', inf.find(
        'ul', class_='kino-lines').text))

    try:
        desc = inf.find('div', class_='kino-desc').find('span').text.split("\n\t\t\t")[1]
    except IndexError:
        desc = ''

    try:
        genres = inf.find('ul', class_='kino-lines').find(
            'div', text=re.compile('Жанр')).parent.text.split(': ')[1]
    except AttributeError:
        genres = ''

    try:
        year = inf.find('ul', class_='kino-lines').find(
            'div', text=re.compile('Год выпуска')).parent.text.split(': ')[1]
    except AttributeError:
        year = ''

    screens = inf.find('div', class_='screens-section').find_all('a')
    abc_screens = []

    for screen in screens:
        screen_url = screen.get('href')
        abs_screen = get_name_screen(screen_url, url)
        save_image(abs_screen, get_file(screen_url))
        abc_screens.append(abs_screen)

    abs_poster = get_name_poster(poster)
    save_image(abs_poster, get_file(poster))

    data = {'title': title,
            'url': url,
            'year': year,
            'desc': desc,
            'duration': duration,
            'genres': genres,
            }

    return data, abs_poster, abc_screens


def get_all_urls(html):
    soup = BeautifulSoup(html, 'lxml')
    films = soup.find('div', class_='main-items').find_all('div', class_='kino-item')
    urls = []

    for film in films:
        url = film.find('a', class_='kino-h').get('href')
        urls.append(url)

    return urls


def make_all(url):
    data = get_page_data(url)
    write_data(data)


def main():
    base_url = 'http://kinogo-net.org/ru/page/'
    all_urls = []
    for i in range(1, PAGE):
        url_gen = base_url + str(i)
        urls = get_all_urls(get_html(url_gen))
        all_urls.extend(urls)

    with Pool(40) as p:
        p.map(make_all, all_urls)


if __name__ == '__main__':
    main()
