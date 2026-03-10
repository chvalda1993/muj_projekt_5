# fixture pro napojení DB, vytvoření tabulky, vymazání tabulky po testu a uzavření databáze
import pytest
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, TEST_DB_NAME


@pytest.fixture
def conn():
    server_conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    server_cursor = server_conn.cursor()
    server_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {TEST_DB_NAME}")
    server_cursor.close()
    server_conn.close()

    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=TEST_DB_NAME
    )

    cursor = connection.cursor()
    sql = """
        CREATE TABLE IF NOT EXISTS ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(255) NOT NULL,
            popis TEXT NOT NULL,
            stav ENUM ('nezahájeno','probíhá','hotovo') NOT NULL DEFAULT 'nezahájeno',
            datum_vytvoreni TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """
    cursor.execute(sql)
    connection.commit()
    cursor.close()

    yield connection

    cursor = connection.cursor()
    cursor.execute("DELETE FROM ukoly")
    connection.commit()
    cursor.close()
    connection.close()