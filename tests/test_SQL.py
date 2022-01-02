import mysql.connector as mysql
from algo_config import HOST, DATABASE, USER, PASSWORD


def test_connection():
    db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    assert db_connection.is_connected()
