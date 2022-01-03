import json

import mysql.connector as mysql
import marketData_SQL

from algo_config import SQL_SERVER_HOST, SQL_SERVER_DATABASE, SQL_SERVER_USER, SQL_SERVER_PASSWORD, \
    SQL_SERVER_WINDOWS_TABLE


def test_connection():
    db_connection = mysql.connect(host=SQL_SERVER_HOST, database=SQL_SERVER_DATABASE, user=SQL_SERVER_USER,
                                  password=SQL_SERVER_PASSWORD)
    assert db_connection.is_connected()


def test_sql_get_algo_windows():
    db_connection = mysql.connect(host=SQL_SERVER_HOST, database=SQL_SERVER_DATABASE, user=SQL_SERVER_USER,
                                  password=SQL_SERVER_PASSWORD)
    cursor = db_connection.cursor()
    sql_command = f"SELECT * FROM {SQL_SERVER_WINDOWS_TABLE} WHERE 1"
    cursor.execute(sql_command)
    response = cursor.fetchall()
    cursor.close()
    assert len(response) > 0


def is_json(item):
    try:
        json_object = json.dumps(item)
    except ValueError as e:
        return False
    return True


def test_sql_window_data_to_json():
    json_data = marketData_SQL.getSQLWindowDataAsJson()
    assert is_json(json_data)


def test_sql_save_window_data():
    json_file = "test_algo_windows.json"

    # empty the data
    open(json_file, 'w').close()

    # make sure data is gone
    with open(json_file, "r") as infile:
        assert infile.readable()
        assert len(infile.readlines()) == 0
        infile.close()

    marketData_SQL.updateWindowData(file_name=json_file)

    # make sure data is written
    with open(json_file, "r") as infile:
        assert infile.readable()
        assert len(infile.readlines()) > 0
        infile.close()



