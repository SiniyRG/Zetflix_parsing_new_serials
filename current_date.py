from datetime import date

# День и месяц для url - адреса Zetflix
current_date = date.today()
dt_string = current_date.strftime('%d-%b-%Y')
dt_string = dt_string.lower().split('-')
current_date = str(int(dt_string[0]))+dt_string[1]