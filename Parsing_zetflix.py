import requests
from bs4 import BeautifulSoup as bs
import time


def connection(url, name='', referer='https://31aug.zetflix-online.net/serials/ochen-strannye-dela/date/'):
    sess = requests.Session()
    sess.trust_env = False
    sess.headers.update({
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_ym_d=1660662814; _ym_uid=1660662814163144663; _ga=GA1.2.373018146.1660995655; PHPSESSID=5e7hpa41ed0kqepj847pq3fbit; _ym_isad=1; _ym_visorc=w; viewed_ids=16039,17353,915,18029,17305',
        'referer': referer,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 OPR/89.0.4447.104',
    })
    try:
        r = sess.get(url)
        r.raise_for_status()
    except Exception as err:
        print(f"Ошибка поключения: {err} - {name}")
    else:
        print(f"Подключение прошло успешно - {name}")
        soup = bs(r.text, 'lxml')
        return soup


# Парсинг сериалов по стариницам
def parsing():
    now_webpage = ''
    return_num = []
    for now_page in range(2, 3):
        soup = connection(f'https://31aug.zetflix-online.net/serials/new_serial/' + now_webpage)
        for tag in soup.find_all('a', class_='vi-img img-resp-h'):
            time.sleep(1)
            return_num.append(parsing_page(tag['href'], tag['alt']))

        now_webpage = f'page/{now_page}/'
    return return_num


# Обработка сериала
def parsing_page(url, name):
    dict_serials = {'Имя_англ': '', 'Имя_ру': '', 'Жанр': '', 'Страна': '', 'Описание': ''}
    soup = connection(url, name=name)
    # Общая информация сериала
    for tag in soup.find_all('ul', class_='finfo'):
        new_str = (tag.text.strip('\n').split('\n'))
        dict_serials['Имя_англ'] = new_str[0][10:].replace("'", "''")
        dict_serials['Имя_ру'] = name
        dict_serials['Жанр'] = (new_str[1][6:].split(','))
        dict_serials['Страна'] = (new_str[2][8:-1].split(','))

    for tag in soup.find_all('div', attrs={'id': 'serial-kratko'}):
        dict_serials['Описание'] = tag.text.replace('\t', '').strip('\n')

    soup = connection(url + 'date/', referer='https://31aug.zetflix-online.net/serials/ochen-strannye-dela/')

    release_date = {}
    new_arr = []
    # Дата выхода каждой серии
    num_block = (len(soup.find_all('table')))
    for tag in soup.find_all('div', attrs={'id': f'dateblock_{num_block}'}):
        for new_tag in tag.find_all('tr', attrs={'class': 'epscape_tr'}):
            new_arr.append(new_tag.text.strip('\n'))

        for num, arr in enumerate(new_arr[::-1], 1):
            num_series = f"Серия {num}"
            if '*' in arr:
                release_date[num_series] = 'Вышла'
            else:
                new_date = arr.split('\n')[2].split(',')[0]
                release_date[num_series] = f'Выйдет {new_date}'

    dict_serials['Дата выхода'] = release_date
    return dict_serials


if __name__ == '__main__':
    parsing()
