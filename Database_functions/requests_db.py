from config import host, user, password, db_name
import psycopg2


def connection_db():
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
                '''SELECT version()'''
            )
            print(f"Версия {cursor.fetchone()}")
        return connection
    except Exception as ex:
        print(f'Ошибка: {ex}')


# Запрос на название сериалов(на русском)
def get_name_serials():
    connection = connection_db()
    with connection.cursor() as cursor:
        cursor.execute(
            '''SELECT name_ru from serials'''
        )
        name_serials = cursor.fetchall()

    connection.close()
    return name_serials


# Запрос сериала на даты выхода
def get_date_serial(name_ru):
    connection = connection_db()
    with connection.cursor() as cursor:
        cursor.execute(
            f'''
            with get_name as 
            (select id_serial from serials
            where name_ru = '{name_ru}')
            SELECT number_serial, release from output_series
            where id_serial = (select 1 from get_name)'''
        )
        date_serials = cursor.fetchall()

    connection.close()
    return date_serials


if __name__ == '__main__':
    date_serials = get_date_serial('Псы резервации')
    str_date = ''
    for serial in date_serials:
        str_date += f'{serial[0]:15}{serial[1]}\n'
    str_date = str_date.strip('\n')
    print(str_date)
