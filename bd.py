import mysql.connector
import configparser
import json

def load_config(config_file):
    # Загрузка настроек из файла JSON
    with open(config_file, 'r') as f:
        config_data = json.load(f)
    return config_data

def connect_to_database(config):
    # Подключение к БД
    db = mysql.connector.connect(
        host=config['database']['host'],
        user=config['database']['user'],
        password=config['database']['password'],
        database=config['database']['name']
    )
    return db

# Загрузка настроек из файла JSON
config = load_config('config.json')

# Подключение к БД
db = connect_to_database(config)

# Функция для просмотра данных с фильтрацией
def view_logs(filter_ip=None, filter_start_date=None, filter_end_date=None):
    cursor = db.cursor()
    sql = "SELECT * FROM access_logs"
    conditions = []

    if filter_ip:
        conditions.append("ip = %s")
    if filter_start_date:
        conditions.append("date >= %s")
    if filter_end_date:
        conditions.append("date <= %s")

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    values = []
    if filter_ip:
        values.append(filter_ip)
    if filter_start_date:
        values.append(filter_start_date)
    if filter_end_date:
        values.append(filter_end_date)

    cursor.execute(sql, tuple(values))
    result = cursor.fetchall()

    for row in result:
        print(row)

# Примеры вызова функции для просмотра данных с различными фильтрами
# Фильтрация по IP адресу
view_logs(filter_ip='127.0.0.1')

# Фильтрация по промежутку дат
view_logs(filter_start_date='2023-01-01', filter_end_date='2023-12-31')

# Фильтрация по IP адресу и промежутку дат
view_logs(filter_ip='127.0.0.1', filter_start_date='2023-01-01', filter_end_date='2023-12-31')

db.close()
