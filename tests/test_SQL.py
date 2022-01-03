import mysql.connector as mysql
import pytest

from algo_config import HOST, DATABASE, USER, PASSWORD


@pytest.mark.xfail
def test_connection():
    db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    assert db_connection.is_connected()
