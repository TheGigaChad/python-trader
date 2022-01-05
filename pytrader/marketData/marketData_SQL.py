import mysql.connector as mysql
import json

from typing import Optional

from pytrader.config import SQL_SERVER_HOST, SQL_SERVER_DATABASE, SQL_SERVER_USER, SQL_SERVER_PASSWORD, \
    SQL_SERVER_WINDOWS_TABLE


def SQLToJson(sql_response: list, column_names: list) -> json:
    """
    Converts SQL responses to JSON format
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


def getSQLWindowDataAsJson(ticker_name: Optional[str] = "%") -> json:
    """
    Returns the windows used for analysis as a JSON object. \n
    :param ticker_name: name of specific ticker you want data for, else will return all.
    :return: window data for all
    """
    db_connection = mysql.connect(host=SQL_SERVER_HOST, database=SQL_SERVER_DATABASE, user=SQL_SERVER_USER,
                                  password=SQL_SERVER_PASSWORD)
    cursor = db_connection.cursor()
    sql_command = f"SELECT * FROM {SQL_SERVER_WINDOWS_TABLE} WHERE `NAME` LIKE '{ticker_name}'"
    cursor.execute(sql_command)
    response = cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    cursor.close()
    return SQLToJson(response, field_names)


def updateWindowData(file_name: Optional[str] = "algo_windows.json"):
    """
    Updates the file with JSON data
    :param file_name: (str) overrides the input json file to write data to
    """
    json_window_data = getSQLWindowDataAsJson()

    # empty the data
    open(file_name, 'w').close()

    # write new data
    with open(file_name, "w") as outfile:
        assert outfile.writable()
        outfile.write(json_window_data)
        outfile.close()

