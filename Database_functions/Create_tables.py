import psycopg2
from config import host, user, password, db_name


try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    with connection.cursor() as cursor:
        cursor.execute(
            '''CREATE TABLE serials
            (id_serial serial PRIMARY KEY,
            name_ru varchar(75) NOT NULL,
            name_en varchar(75) UNIQUE,
            description text NOT NULL);'''
        )
        print('[Инфо]Создана таблица "serials"')

    with connection.cursor() as cursor:
        cursor.execute(
            '''CREATE TABLE countries
            (id_country serial PRIMARY KEY,
            name_country varchar(75) UNIQUE);'''
        )
        print('[Инфо]Создана таблица "countries"')

    with connection.cursor() as cursor:
        cursor.execute(
            '''CREATE TABLE genres
            (id_genre serial PRIMARY KEY,
            name_genre varchar(30) UNIQUE);'''
        )
        print('[Инфо]Создана таблица "genres"')
    with connection.cursor() as cursor:
        cursor.execute(
            '''CREATE TABLE genre_series
            (id_serial integer REFERENCES serials (id_serial) ON DELETE CASCADE,
            id_genre integer REFERENCES genres (id_genre) ON DELETE CASCADE);'''
        )
        print('[Инфо]Создана таблица "genre_series"')
    with connection.cursor() as cursor:
        cursor.execute(
            '''CREATE TABLE country_series
            (id_serial integer REFERENCES serials (id_serial) ON DELETE CASCADE,
            id_country integer REFERENCES countries (id_country) ON DELETE CASCADE); '''
        )
        print('[Инфо]Создана таблица "country_series"')

    with connection.cursor() as cursor:
        cursor.execute(
            '''CREATE TABLE output_series
            (id_serial integer REFERENCES serials (id_serial) ON DELETE CASCADE,
             number_serial varchar(10) NOT NULL,
             release text NOT NULL);'''
        )
        print('[Инфо]Создана таблица "output_series"')

except Exception as ex:
    print('Ошибка', ex)
finally:
    if connection:
        connection.close()
        print('Закрыто')