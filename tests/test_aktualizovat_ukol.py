import task_manager as tm

def test_aktualizovat_ukol_pozitivni(conn, monkeypatch):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)", ("nazev_ukolu", "popis_ukolu", "nezahájeno"))
    id_ukolu = cursor.lastrowid
    conn.commit()
    cursor.close()

    inputs = iter([str(id_ukolu), "hotovo"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    tm.aktualizovat_ukol(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (id_ukolu,))
    row = cursor.fetchone()
    cursor.close()

    assert row[0] == "hotovo"

def test_aktualizovat_ukol_negativni(conn, monkeypatch, capsys):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)", ("nazev_ukolu", "popis_ukolu", "nezahájeno"))
    id_ukolu = cursor.lastrowid
    conn.commit()
    cursor.close()

    inputs = iter([str(id_ukolu), "téměř hotovo", "hotovo"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    tm.aktualizovat_ukol(conn)
    out = capsys.readouterr().out

    cursor = conn.cursor()
    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (id_ukolu,))
    row = cursor.fetchone()
    cursor.close()

    assert row[0] == "hotovo"
    assert "Neplatný stav" in out