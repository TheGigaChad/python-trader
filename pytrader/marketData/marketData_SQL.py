import json
from typing import Optional

import mysql.connector as mysql

from pytrader import cfg as cfg


def sql_to_json(sql_response: list, column_names: list) -> json:
    """
    Converts sql responses to JSON format
    :param sql_response: response data
    :param column_names: names of columns of table
    :return: Json string of data
    """
    sql_data_list = []
    for row in sql_response:
        window_json_item = {}
        for i in range(len(column_names)):
            window_json_item[column_names[i]] = row[i]
        sql_data_list.append(window_json_item)
    return json.dumps(sql_data_list, indent=1)


def get_sql_window_data_as_json(ticker_name: Optional[str] = "%") -> json:
    """
    Returns the windows used for analysis as a JSON object. \n
    :param ticker_name: name of specific ticker you want data for, else will return all.
    :return: window data for all
    """
    # TODO - tidy
    db_connection = mysql.connect(host=cfg.SQL_SERVER_HOST, database=cfg.SQL_SERVER_DATABASE, user=cfg.SQL_SERVER_USER,
                                  password=cfg.SQL_SERVER_PASSWORD)
    cursor = db_connection.cursor()
    sql_command = f"SELECT * FROM {cfg.SQL_SERVER_WINDOWS_TABLE} WHERE `NAME` LIKE '{ticker_name}'"
    cursor.execute(sql_command)
    response = cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    cursor.close()
    return sql_to_json(response, field_names)


def update_window_data(file_name: Optional[str] = "algo_windows.json"):
    """
    Updates the file with JSON data
    :param file_name: (str) overrides the input json file to write data to
    """
    json_window_data = get_sql_window_data_as_json()

    # empty the data
    open(file_name, 'w').close()

    # write new data
    with open(file_name, "w") as outfile:
        assert outfile.writable()
        outfile.write(json_window_data)
        outfile.close()

