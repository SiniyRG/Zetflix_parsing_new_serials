from Parsing.Parsing_zetflix import parsing
from config import host, user, password, db_name
import psycopg2

parsing_values = parsing()
try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )
        print(f"Версия {cursor.fetchone()}")
    # Обнуление счетчиков авто-инкремента
    all_tables = ['serials', 'countries', 'genres']
    for table in all_tables:
        with connection.cursor() as cursor:
            cursor.execute(
                f'''TRUNCATE TABLE {table} RESTART IDENTITY CASCADE'''
            )
    # Таблица сериалов


    for parsing_value in parsing_values:
        # Добавление данных в таблицу сериалов
        with connection.cursor() as cursor:
            cursor.execute(
                f'''INSERT INTO serials
                (name_ru, name_en, description)
                VALUES('{(parsing_value['Имя_ру'])}','{parsing_value['Имя_англ']}', '{(parsing_value['Описание'])}') 
                ON CONFLICT (name_en) DO UPDATE
                SET name_ru = '{(parsing_value['Имя_ру'])}', name_en = '{(parsing_value['Имя_англ'])}',
                description = '{(parsing_value['Описание'])}';'''
            )
            print('[Инфо]Данные добавлены в таблицу "serials"')
        # Добавление данных в таблицу страны
        with connection.cursor() as cursor:
            for country in parsing_value['Страна']:
                cursor.execute(
                    f'''INSERT INTO countries
                    (name_country)
                    VALUES('{country}') ON CONFLICT(name_country) do nothing;'''
                )
            print('[Инфо]Данные добавлены в таблицу "countries"')
        # Добавление данных в таблицу жанры
        with connection.cursor() as cursor:
            for genre in parsing_value['Жанр']:
                cursor.execute(
                    f'''INSERT INTO genres
                    (name_genre)
                    VALUES ('{genre}') on conflict(name_genre) do nothing;'''
                )
        # Добавление данных в таблицу жанры сериала
        with connection.cursor() as cursor:
            name_serial = parsing_value['Имя_ру']
            for genre in parsing_value['Жанр']:
                cursor.execute(
                    f'''with get_name as
                    (select id_serial from serials
                    where name_ru = '{name_serial}'),
                    get_genre as
                    (select id_genre from genres
                    where name_genre = '{genre}')
                    INSERT INTO genre_series
                    select * from get_name, get_genre;
                    '''
                )
        # Добавление данных в таблицу страны сериала
        with connection.cursor() as cursor:
            name_serial = parsing_value['Имя_ру']
            for country in parsing_value['Страна']:
                country = country.strip(' ')
                cursor.execute(
                    f'''with get_name as
                    (select id_serial from serials
                    where name_ru = '{name_serial}'),
                    get_country as
                    (select id_country from countries
                    where name_country = '{country}')
                    INSERT INTO country_series
                    select * from get_name, get_country;
                    '''
                )
        # Добавление данных в таблицу даты выхода сериала
        with connection.cursor() as cursor:
            name_serial = parsing_value['Имя_ру']
            for num, release in enumerate(parsing_value['Дата выхода'], 1):
                cursor.execute(
                    f'''with get_name as
                    (select id_serial, '{release}' as cl2, '{parsing_value['Дата выхода'][release]}' as cl3 from serials
                    where name_ru = '{name_serial}')
                    INSERT INTO output_series
                    select * from get_name;
                    '''
                )
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         '''DROP TABLE genre_series'''
    #     )
    #     print('[Инфо]Таблица удалена')
except Exception as ex:
    print('Ошибка', ex)
finally:
    if connection:
        connection.close()
        print('Закрыто')
