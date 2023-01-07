import mysql.connector
from mysql.connector import Error
from datetime import date

import data


def connect_to_db(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")

    except Error as err:
        print(f'Error: {err}')

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f'Error: {err}')


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f'Error: "{err}"')


def insert_func_into_table(connection, table, func, col_name):
    test_query = f"SELECT COUNT(DISTINCT {col_name}) FROM job"
    query_count = (read_query(connection, test_query)[0][0])
    ifupdate_query = "SELECT date FROM lastupdate"
    ifupdate_value = read_query(connection, ifupdate_query)[0][0]
    if int(query_count) < 2:
        for elems in table:
            result = func(elems)
            if str(result).isdigit():
                query = f'Update Job SET {col_name} = {result} WHERE language = "{elems}"'
            else:
                query = f'Update Job SET {col_name} = "{result}" WHERE language = "{elems}"'
            execute_query(connection, query)
    elif str(ifupdate_value) != str(date.today()):
        execute_query(connection, f"Update job SET {col_name} = NULL")
        for elems in table:
            result = func(elems)
            query = f'Update Job SET {col_name} = {result} WHERE language = "{elems}"'
            execute_query(connection, query)

    update_query = f'UPDATE lastupdate SET date="{date.today()}" WHERE id=1'
    execute_query(connection, update_query)


def check_table_exists(connection, tablename):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if cursor.fetchone()[0] == 1:
        cursor.close()
        return True

    cursor.close()
    return False


def create_tables(connection):
    if check_table_exists(connection, "lastupdate") and check_table_exists(connection, "job"):
        print("All tables exist already")
        return
    if not check_table_exists(connection, "lastupdate"):
        query = "CREATE TABLE lastupdate (date DATE NOT NULL, id INT NOT NULL)"
        execute_query(connection, query)
    if not check_table_exists(connection, "job"):
        query = "CREATE TABLE job (language TEXT NOT NULL , number_of_speakers INT, number_of_hours INT, job_offers INT, family_of_language TEXT)"
        execute_query(connection, query)
        for lang in data.all_languages:
            query = f"INSERT INTO job (language) VALUES ('{lang}')"
            execute_query(connection, query)
    print("All tables created successfully")
