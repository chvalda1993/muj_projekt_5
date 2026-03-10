from db import pripojeni_db, vytvoreni_tabulky, pridat_ukol_do_db, ziskat_aktivni_ukoly, overit_id_aktivniho_ukolu, aktualizovat_stav_ukolu_v_db, ziskat_vsechny_ukoly, overit_id_ukolu, odstranit_ukol_z_db, vytvoreni_databaze


def pridat_ukol(conn):
    """
    Přidá nový úkol do databáze.

    Uživatel zadává název a popis úkolu.
    Funkce kontroluje, že vstupy nejsou prázdné.
    Každý vstup je kontrolován samostatně.

    Parametry:
        conn: aktivní připojení k databázi.
    """
    while True:
        nazev_ukolu = input("Zadejte název úkolu: ").strip()
        if nazev_ukolu:
            break
        print("Název úkolu nesmí být prázdný.")

    while True:
        popis_ukolu = input("Zadejte popis úkolu: ").strip()
        if popis_ukolu:
            break
        print("Popis úkolu nesmí být prázdný.")

    if pridat_ukol_do_db(conn, nazev_ukolu, popis_ukolu):
        print("Úkol byl úspěšně přidán.")

def zobrazit_ukoly(conn):
    """
    Zobrazí všechny aktivní úkoly (nezahájeno, probíhá).

    Parametry:
        conn: aktivní připojení k databázi.
    """
    
    rows = ziskat_aktivni_ukoly(conn)
        
    if not rows:
        print("Seznam úkolů je prázdný.")
    else:
        for id_ukolu, nazev, popis, stav in rows:
            print(f"{id_ukolu}. {nazev} - {popis} ({stav})")

def aktualizovat_ukol(conn):
    """
    Umožní uživateli změnit stav ybraného aktivního úkolu.
    Uživatel nejprvě vybere úkol podle ID a poté zadá nový stav.
    Parametry:
        conn: aktivní připojení k databázi.
    """
    rows = ziskat_aktivni_ukoly(conn)

    if not rows:
        print("Nejsou žádné úkoly k aktualizaci.")
        return
    else:
        for id_ukolu, nazev, popis, stav in rows:
            print(f"{id_ukolu}. {nazev} - {stav}")
    

    while True:
        try:
            id_ukolu = int(input("Zadejte ID úkolu, který chcete aktualizovat: ").strip())
        except ValueError:
            print("Zadejte platné číslo.")
            continue

        if not overit_id_aktivniho_ukolu(conn, id_ukolu):
            print(f"Aktivní úkol s ID {id_ukolu} neexistuje.")
            continue
        else:
            break

    while True:
        novy_stav = input("Zadejte nový stav úkolu ('probíhá' nebo 'hotovo'): ").strip().lower()

        if novy_stav not in ("probíhá", "hotovo"):
            print("Neplatný stav. Zadejte 'probíhá' nebo 'hotovo'.")
            continue
        else:
            break

    aktualizovat_stav_ukolu_v_db(conn, id_ukolu, novy_stav)
    print("Úkol byl úspěšně aktualizován.")
    

def odstranit_ukol(conn):
    """
    Umožní uživateli odstranit úkol podle ID.
    Parametry:
        conn: aktivní připojení k databázi.
    """
    rows = ziskat_vsechny_ukoly(conn)

    if not rows:
        print("Nejsou žádné úkoly k odstranění.")
        return
    else:
        for id_ukolu, nazev, popis, stav in rows:
            print(f"{id_ukolu}. {nazev} - {popis} ({stav})")

    while True:
        try:
            id_ukolu = int(input("Zadejte ID úkolu, který chcete odstranit: ").strip())
        except ValueError:
            print("Zadejte platné číslo.")
            continue

        if not overit_id_ukolu(conn, id_ukolu):
            print(f"Úkol s ID {id_ukolu} neexistuje.")
            continue
        else:
            break
    
    odstranit_ukol_z_db(conn, id_ukolu)
    print("Úkol byl úspěšně odstraněn.")

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
    if not vytvoreni_databaze():
        return
    
    conn = pripojeni_db()

    if conn is None:
        return

    try:
        if not vytvoreni_tabulky(conn):
            return

        hlavni_menu(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
