# fixture pro napojení DB, vytvoření tabulky, vymazání tabulky po testu a uzavření databáze
import pytest
import mysql.connector

@pytest.fixture
def conn():
    connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="task_manager_test")
    cursor = connection.cursor()
    sql = ("""
        CREATE TABLE IF NOT EXISTS ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(255) NOT NULL,
            popis TEXT NOT NULL,
            stav ENUM ('nezahájeno','probíhá','hotovo') NOT NULL DEFAULT 'nezahájeno',
            datum_vytvoreni TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute(sql)
    connection.commit()
    cursor.close()

    yield connection
    cursor = connection.cursor()
    sql = "DELETE FROM ukoly"
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()