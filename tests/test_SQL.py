import mysql.connector as mysql
import pytest

from algo_config import SQL_SERVER_HOST, SQL_SERVER_DATABASE, SQL_SERVER_USER, SQL_SERVER_PASSWORD


@pytest.mark.xfail
def test_connection():
    db_connection = mysql.connect(host=SQL_SERVER_HOST, database=SQL_SERVER_DATABASE, user=SQL_SERVER_USER, password=SQL_SERVER_PASSWORD)
    assert db_connection.is_connected()
