import mysql.connector as mysql
import json

from config import SQL_SERVER_HOST, SQL_SERVER_DATABASE, SQL_SERVER_USER, SQL_SERVER_PASSWORD, \
    SQL_SERVER_WINDOWS_TABLE


def SQLToJson(sql_response, column_names):
    """
    Converts SQL responses to JSON format
    """
    sql_data_list = []
    for row in sql_response:
        window_json_item = {}
        for i in range(len(column_names)):
            window_json_item[column_names[i]] = row[i]
        sql_data_list.append(window_json_item)
    return json.dumps(sql_data_list, indent=1)


def getSQLWindowDataAsJson(ticker_name="%"):
    """
    Returns the windows used for analysis as a JSON object. \n
    :param ticker_name: (str) name of specific ticker you want data for, else will return all.
    :return: (JSON) window data for all
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


def updateWindowData(file_name="algo_windows.json"):
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

