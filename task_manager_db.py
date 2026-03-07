import mysql.connector

def pripojeni_db():
    """
    Vytvoří připojení k databázi MySQL.

    Návratová hodnota:
        conn: Objekt připojení k databázi, pokud je připojení úspěšné.
        None: Pokud připojení selže.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="task_manager"
        )
        print("Připojení k databázi bylo úspěšné.")
        return conn

    except mysql.connector.Error as err:
        print(f"Chyba připojení k databázi: {err}")
        return None


def vytvoreni_tabulky(conn):
    """
    Vytvoří tabulku 'ukoly', pokud v databázi ještě neexistuje.

    Parametry:
        conn: aktivní připojení k databázi
    """
    try:
        cursor = conn.cursor()
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
        conn.commit()
        cursor.close()
        print("Tabulka 'ukoly' byla vytvořena nebo už existuje.")

    except mysql.connector.Error as err:
        print(f"Chyba při vytvoření tabulky: {err}")
        return None

def pridat_ukol(conn):
    """
    Přidá nový úkol do databáze.

    Uživatel zadává název a popis úkolu.
    Funkce kontroluje, že vstupy nejsou prázdné.

    Parametry:
        conn: aktivní připojení k databázi.
    """
    while True:
        nazev_ukolu = input("Zadejte název úkolu: ").strip()
        popis_ukolu = input("Zadejte popis úkolu: ").strip()

        if not nazev_ukolu or not popis_ukolu:
            print("Musí být zadaný název i popis úkolu. Zadejte oba dva údaje.")
            continue
            
        cursor = None

        try:
            cursor = conn.cursor()
            sql = "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)"
            cursor.execute(sql, (nazev_ukolu, popis_ukolu))
            conn.commit()
            print("Úkol byl úspěšně přidán.")
            break

        except mysql.connector.Error as err:
            print(f"Chyba při vytvoření úkolu: {err}")
            
        finally:
            if cursor is not None:
                cursor.close()

def zobrazit_ukoly(conn):
    """
    Zobrazí všechny aktivní úkoly (nezahájeno, probíhá).

    Parametry:
        conn: aktivní připojení k databázi.
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
        rows = cursor.fetchall()
        
        if not rows:
            print("Seznam úkolů je prázdný.")
        else:
            for id_ukolu, nazev, popis, stav in rows:
                print(f"{id_ukolu}. {nazev} - {popis} ({stav})")

    except mysql.connector.Error as err:
        print(f"Chyba při zobrazení úkolů: {err}")
        
    finally:
        if cursor is not None:
            cursor.close()

def aktualizovat_ukol(conn):
    """
    Umožní uživateli změnit stav vybraného úkolu.

    Úkol se vybírá podle ID.
    Stav lze změnit pouze na 'probíhá' nebo 'hotovo'.

    Parametry:
        conn: aktivní připojení k databázi
    """
    cursor = None

    try:
        cursor = conn.cursor()
        sql = """
        SELECT id, nazev, stav
        FROM ukoly
        WHERE stav IN ('nezahájeno','probíhá')
        ORDER BY id
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        if not rows:
            print("Nejsou žádné úkoly k aktualizaci.")
            return
        else:
            for id_ukolu, nazev, stav in rows:
                print(f"{id_ukolu}. {nazev} - {stav}")
    except mysql.connector.Error as err:
        print(f"Chyba při zobrazení úkolů: {err}")
        return
    finally:
        if cursor is not None:
            cursor.close()

    while True:
        try:
            id_ukolu = int(input("Zadejte ID úkolu, který chcete aktualizovat: ").strip())
        except ValueError:
            print("Zadejte platné číslo.")
            continue

        try:
            cursor = conn.cursor()
            sql = "SELECT id FROM ukoly WHERE id = %s"
            cursor.execute(sql, (id_ukolu,))
            row = cursor.fetchone()
        
            if row is None:
                print(f"Úkol s ID {id_ukolu} neexistuje.")
                continue 
            else:
                break
        except mysql.connector.Error as err:
            print(f"Chyba při zadávání ID úkolu: {err}")
        finally:
            if cursor is not None:
                cursor.close()

    while True:
        novy_stav = input("Zadejte nový stav úkolu ('probíhá' nebo 'hotovo'): ").strip().lower()

        if novy_stav not in ("probíhá", "hotovo"):
            print("Neplatný stav. Zadejte 'probíhá' nebo 'hotovo'.")
            continue
        else:
            break

    
    try:
        cursor = conn.cursor()
        sql = """
            UPDATE ukoly
            SET stav = %s
            WHERE id = %s
            """
        cursor.execute(sql, (novy_stav, id_ukolu))
        conn.commit()
        print("Úkol byl úspěšně aktualizován.")
    except mysql.connector.Error as err:
        print(f"Chyba při aktualizaci úkolu: {err}")
    finally:
        if cursor is not None:
            cursor.close()
    

def odstranit_ukol(conn):
    """
    Odstraní vybraný úkol z databáze podle jeho ID.

    Parametry:
        conn: aktivní připojení k databázi.
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
        rows = cursor.fetchall()
        
        if not rows:
            print("Nejsou žádné úkoly k odstranění.")
            return
        else:
            for id_ukolu, nazev, popis, stav in rows:
                print(f"{id_ukolu}. {nazev} - {popis} ({stav})")

    except mysql.connector.Error as err:
        print(f"Chyba při zobrazení úkolu: {err}")
        return
    finally:
        if cursor is not None:
            cursor.close()

    while True:
        try:
            id_ukolu = int(input("Zadejte ID úkolu, který chcete odstranit: ").strip())
        except ValueError:
            print("Zadejte platné číslo.")
            continue

        try:
            cursor = conn.cursor()
            sql = "SELECT id FROM ukoly WHERE id = %s"
            cursor.execute(sql, (id_ukolu,))
            row = cursor.fetchone()
        
            if row is None:
                print(f"Úkol s ID {id_ukolu} neexistuje.")
                continue 
            else:
                break
        except mysql.connector.Error as err:
            print(f"Chyba při zadávání ID úkolu: {err}")
            continue
        finally:
            if cursor is not None:
                cursor.close()
    
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM ukoly WHERE id = %s"
        cursor.execute(sql, (id_ukolu,))
        conn.commit()
        print("Úkol byl úspěšně odstraněn.")
    except mysql.connector.Error as err:
        print(f"Chyba při odstraňování úkolu: {err}")
    finally:
        if cursor is not None:
            cursor.close()

def hlavni_menu(conn):
    """
    Zobrazí hlavní menu programu a umožní uživateli
    vybrat požadovanou operaci.

    Parametry:
        conn: aktivní připojení k databázi.
    """
    while True:
        print("Správce úkolů - Hlavní menu",
            "1. Přidat nový úkol",
            "2. Zobrazit úkoly",
            "3. Aktualizovat úkol",
            "4. Odstranit úkol",
            "5. Konec programu",
            sep="\n")
        cislo_funkce = input("Vyberte možnost (1-5):").strip()

        if cislo_funkce == "1":
            pridat_ukol(conn)
        elif cislo_funkce == "2":
            zobrazit_ukoly(conn)
        elif cislo_funkce == "3":
            aktualizovat_ukol(conn)
        elif cislo_funkce == "4":
            odstranit_ukol(conn)
        elif cislo_funkce == "5":
            print("Ukončuji program.")
            break
        else:
            print("Zadejte platné číslo funkce, kterou chcete vykonat (1–5).")

def main():
    """
    Hlavní vstupní bod programu.

    Zajišťuje připojení k databázi, vytvoření tabulky
    a spuštění hlavního menu.
    """
    conn = pripojeni_db()

    if conn is None:
        return

    try:
        vytvoreni_tabulky(conn)
        hlavni_menu(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
