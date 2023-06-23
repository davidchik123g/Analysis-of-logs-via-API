import re
import datetime
import mysql.connector
import click
import datetime
import argparse
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

# Создание таблицы для хранения данных
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS access_logs (id INT AUTO_INCREMENT PRIMARY KEY, ip VARCHAR(255), date DATETIME, user_agent VARCHAR(1000), status_code INT)")

# Парсинг логов и сохранение данных в БД
log_file = "C:/Users/Пользователь/Downloads/proekt/access.log"
log_pattern = r'(\d+\.\d+\.\d+\.\d+)\s-\s-\s\[(.*?)\]\s\"(.*?)\"\s(\d+)'

with open(log_file, 'r') as file:
    for line in file:
        match = re.search(log_pattern, line)
        if match:
            ip = match.group(1)
            date_str = match.group(2)
            user_agent = match.group(3)
            status_code = match.group(4)
            
            date = datetime.datetime.strptime(date_str, "%d/%b/%Y:%H:%M:%S %z")
            
            # Сохранение данных в БД
            sql = "INSERT INTO access_logs (ip, date, user_agent, status_code) VALUES (%s, %s, %s, %s)"
            values = (ip, date, user_agent, status_code)
            cursor.execute(sql, values)

db.commit()

def view_logs(ip=None, start_date=None, end_date=None, log_path=None, log_file_mask=None):
    # Формируем SQL-запрос в соответствии с переданными параметрами
    sql_query = 'SELECT * FROM access_logs'
    conditions = []

    if ip:
        conditions.append(f"ip = '{ip}'")
    if start_date and end_date:
        conditions.append(f"date BETWEEN '{start_date}' AND '{end_date}'")
    elif start_date:
        conditions.append(f"date >= '{start_date}'")
    elif end_date:
        conditions.append(f"date <= '{end_date}'")

    if conditions:
        sql_query += " WHERE " + " AND ".join(conditions)

    # Выполняем SQL-запрос
    cursor.execute(sql_query)

    # Извлекаем результаты запроса и выводим на экран
    result = cursor.fetchall()
    for r in result:
        print(r)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter logs by IP and/or date')
    parser.add_argument('--ip', type=str, help='Filter logs by IP')
    parser.add_argument('--start-date', type=str, help='Start date for date range filter (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, help='End date for date range filter (YYYY-MM-DD)')
    parser.add_argument('--config-file', type=str, help='Path to the config file')

    args = parser.parse_args()

    if args.config_file:
        config = load_config(args.config_file)
        db = connect_to_database(config)
        view_logs(args.ip, args.start_date, args.end_date)
    else:
        view_logs(args.ip, args.start_date, args.end_date)

db.close()
