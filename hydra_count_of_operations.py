#!/usr/bin/python3

import configparser
import MySQLdb 					# Для работы с MySQL
import re 				        # Работаем с регулярками
import os 
import cx_Oracle  			        # Подключение к БД
import pandas as pd                             # работа с таблицами
import pretty_html_table                        # перевод DataFrame в HTML
import smtplib                                  # работа с SMTP сервером
from email.mime.multipart import MIMEMultipart  # создаём сообщение
from email.mime.text import MIMEText            # вёрстка письма
from datetime import date
from datetime import timedelta

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')

server = config.get('mail', 'server')
From = config.get('mail', 'From')
To = config.get('mail', 'To')
path_to_files =config.get('DB', 'path_to_sql_file')
ora_server = config.get('DB', 'ora_server')
ora_login = config.get('DB', 'ora_login')
ora_pass = config.get('DB', 'ora_pass')
mysql_db = config.get('DB', 'mysql_db')
mysql_server = config.get('DB', 'mysql_server')
mysql_login = config.get('DB', 'mysql_login')
mysql_pass = config.get('DB', 'mysql_pass')

# Вычесляем даты +1 день от даты выполнения, и неделю назад
current_date = date.today()

start_date = str(current_date-timedelta(7))
end_date = str(current_date+timedelta(1))
end_date_to_body_mail_report = str(current_date)

input_date = {
	'date1': start_date,
	'date2': end_date
	}

# Решение пробелмы с кодировкой из-за наличия руссикх символов в SQL запросе, в том числе даже в коментариях
os.environ["NLS_LANG"] = ".AL32UTF8" 

# Присоединение и выполнение SQL запроса к БД Oracle
connection = cx_Oracle.connect(ora_login, ora_pass, ora_server)
print("Database version:", connection.version)
print("Encoding:", connection.encoding)

cursor = connection.cursor()
query_from_file = open(path_to_files+'count_of_operations_hydra.sql')
sql_query = query_from_file.read()
df = pd.read_sql(sql_query, params = input_date, con=connection)


# Присоединение и выполнение SQL запроса к БД MySQL
connection_mysql=MySQLdb.connect(host=mysql_server, user=mysql_login, passwd=mysql_pass, db=mysql_db)
#print("Database version:", connection_mysql.version)
#print("Encoding:", connection_mysql.encoding)

mysql_query_from_file = open(path_to_files+'count_of_operations_potok.sql')
sql_query_mysql = mysql_query_from_file.read()
df_mysql = pd.read_sql(sql_query_mysql, params = input_date, con=connection_mysql)


# Обработка ошибок. Если нет данных в выборке SQL, то выдаёся сообщение начинающееся с Empty. Регулярками находим это. Если данные есть, то 
# выдаётся сообщение None. Рабочим оказался вариант сравнивать именно с None, т.к. если наоборот, то проблема с типами данных (не разобрался)
# Если обработку не делать, то тоже сваливается в ошибку из за отсутствия данных в выборке

result = re.match(r'Empty', str(df))
if str(result) == 'None':
    html_table = pretty_html_table.build_table(df, 'blue_light', 'x-small')
else:
    html_table = 'Нет данных'

result = re.match(r'Empty', str(df_mysql))
if str(result) == 'None':
    html_table_mysql = pretty_html_table.build_table(df_mysql, 'blue_light', 'x-small')
else:
    html_table_mysql = 'Нет данных'

# подключаемся к SMTP серверу
server = smtplib.SMTP(server)
#server.login('email_login', 'email_password')
 
# создаём письмо
msg = MIMEMultipart('mixed')
msg['Subject'] = 'Количество операций'
msg['From'] = From
msg['To'] = To
       
#добавляем в письмо текст и таблицу
html_table = MIMEText('<h2>Количество операций за период с '+start_date+' по '+end_date_to_body_mail_report+' </h2><h3>Hydra:</h3>'+html_table+'<h3>Поток:</h3>'+html_table_mysql, 'html')
 
msg.attach(html_table)
 
# отправляем письмо
server.send_message(msg)
 
# отключаемся от SMTP сервера
server.quit()




