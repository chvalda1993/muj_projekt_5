import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def pripojeni_server():
    """
    Vytvoří připojení k MySQL serveru bez výběru konkrétní databáze.

    Návratová hodnota:
        conn: objekt připojení k serveru, pokud je připojení úspěšné.
        None: pokud připojení selže.
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Chyba při připojení k MySQL serveru: {err}")
        return None

def vytvoreni_databaze():
    """
    Vytvoří databázi, pokud ještě neexistuje.

    Návratová hodnota:
        True: pokud operace proběhla úspěšně.
        False: pokud nastala chyba.
    """
    conn = pripojeni_server()

    if conn is None:
        return False

    cursor = None

    try:
        cursor = conn.cursor()
        sql = f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
        cursor.execute(sql)
        return True

    except mysql.connector.Error as err:
        print(f"Chyba při vytváření databáze: {err}")
        return False

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

def pripojeni_db():
    """
    Vytvoří připojení k databázi MySQL.

    Návratová hodnota:
        conn: Objekt připojení k databázi, pokud je připojení úspěšné.
        None: Pokud připojení selže.
    """

    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Chyba při připojení k databázi: {e}")
        return None
    
def vytvoreni_tabulky(conn):
    """
    Vytvoří tabulku 'ukoly', pokud v databázi ještě neexistuje.

    Parametry:
        conn: aktivní připojení k databázi.
    """
    cursor = None
    try:
        cursor = conn.cursor()
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
        conn.commit()
        return True
    
    except mysql.connector.Error as err:
        print(f"Chyba při vytvoření tabulky: {err}")

    finally:
        if cursor is not None:
            cursor.close()

def pridat_ukol_do_db(conn, nazev_ukolu, popis_ukolu):
    """
    Přidá nový úkol do databáze.

    Parametry:
        conn: aktivní připojení k databázi.
        nazev_ukolu: název úkolu.
        popis_ukolu: popis úkolu.

    Návratová hodnota:
        True: pokud byl úkol úspěšně přidán.
        False: pokud nastala chyba.
    """
    cursor = None

    try:
        cursor = conn.cursor()
        sql = "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)"
        cursor.execute(sql, (nazev_ukolu, popis_ukolu))
        conn.commit()
        return True

    except mysql.connector.Error as err:
        print(f"Chyba při vytvoření úkolu: {err}")
        return False

    finally:
        if cursor is not None:
            cursor.close()

def ziskat_aktivni_ukoly(conn):
    """
    Načte všechny aktivní úkoly (nezahájeno, probíhá) z databáze.

    Parametry:
        conn: aktivní připojení k databázi.

    Návratová hodnota:
        list: seznam aktivních úkolů.
    """
    cursor = None
    try:
        cursor = conn.cursor()
        sql = """
        SELECT id, nazev, popis, stav
        FROM ukoly
        WHERE stav IN ('nezahájeno','probíhá')
        ORDER BY id
        """
        cursor.execute(sql)
        return cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Chyba při zobrazení úkolů: {err}")
        return []

    finally:
        if cursor is not None:
            cursor.close()

def overit_id_aktivniho_ukolu(conn, id_ukolu):
    """
    Ověří, zda existuje aktivní úkol se zadaným ID.

    Parametry:
        conn: aktivní připojení k databázi.
        id_ukolu: ID úkolu.

    Návratová hodnota:
        True: pokud aktivní úkol existuje.
        False: pokud aktivní úkol neexistuje.
    """
    cursor = None

    try:
        cursor = conn.cursor()
        sql = """
        SELECT id
        FROM ukoly
        WHERE id = %s AND stav IN ('nezahájeno', 'probíhá')
        """
        cursor.execute(sql, (id_ukolu,))
        row = cursor.fetchone()
        return row is not None

    except mysql.connector.Error as err:
        print(f"Chyba při ověřování ID úkolu: {err}")
        return False

    finally:
        if cursor is not None:
            cursor.close()

def aktualizovat_stav_ukolu_v_db(conn, id_ukolu, novy_stav):
    """
    Aktualizuje stav úkolu v databázi.

    Parametry:
        conn: aktivní připojení k databázi.
        id_ukolu: ID úkolu.
        novy_stav: nový stav úkolu.
    """
    cursor = None

    try:
        cursor = conn.cursor()
        sql = """
            UPDATE ukoly
            SET stav = %s
            WHERE id = %s
        """
        cursor.execute(sql, (novy_stav, id_ukolu))
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Chyba při aktualizaci úkolu: {err}")

    finally:
        if cursor is not None:
            cursor.close()

def ziskat_vsechny_ukoly(conn):
    """
    Načte všechny úkoly z databáze.

    Parametry:
        conn: aktivní připojení k databázi.

    Návratová hodnota:
        list: seznam všech úkolů.
    """
    cursor = None
    try:
        cursor = conn.cursor()
        sql = """
        SELECT id, nazev, popis, stav
        FROM ukoly
        ORDER BY id
        """
        cursor.execute(sql)
        return cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Chyba při zobrazení úkolů: {err}")
        return []

    finally:
        if cursor is not None:
            cursor.close()

def overit_id_ukolu(conn, id_ukolu):
    """
    Ověří, zda existuje úkol se zadaným ID.

    Parametry:
        conn: aktivní připojení k databázi.
        id_ukolu: ID úkolu.

    Návratová hodnota:
        True: pokud úkol existuje.
        False: pokud úkol neexistuje.
    """
    cursor = None

    try:
        cursor = conn.cursor()
        sql = "SELECT id FROM ukoly WHERE id = %s"
        cursor.execute(sql, (id_ukolu,))
        row = cursor.fetchone()
        return row is not None

    except mysql.connector.Error as err:
        print(f"Chyba při ověřování ID úkolu: {err}")
        return False

    finally:
        if cursor is not None:
            cursor.close()

def odstranit_ukol_z_db(conn, id_ukolu):
    """
    Odstraní úkol z databáze podle jeho ID.

    Parametry:
        conn: aktivní připojení k databázi.
        id_ukolu: ID úkolu, který se má odstranit.
    """
    cursor = None

    try:
        cursor = conn.cursor()
        sql = "DELETE FROM ukoly WHERE id = %s"
        cursor.execute(sql, (id_ukolu,))
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Chyba při odstraňování úkolu: {err}")

    finally:
        if cursor is not None:
            cursor.close()