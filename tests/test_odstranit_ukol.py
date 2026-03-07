import task_manager_db as tm

def test_odstranit_ukol_pozitivni(conn, monkeypatch):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)", ("nazev_ukolu", "popis_ukolu", "nezahájeno"))
    id_ukolu = cursor.lastrowid
    conn.commit()
    cursor.close()

    inputs = iter([str(id_ukolu)])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    tm.odstranit_ukol(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT nazev FROM ukoly WHERE id = %s", (id_ukolu,))
    row = cursor.fetchone()
    cursor.close()

    assert row is None

def test_odstranit_ukol_negativni(conn, monkeypatch, capsys):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)", ("nazev_ukolu", "popis_ukolu", "nezahájeno"))
    id_ukolu = cursor.lastrowid
    conn.commit()
    cursor.close()

    inputs = iter(["999", str(id_ukolu)])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    tm.odstranit_ukol(conn)
    out = capsys.readouterr().out

    cursor = conn.cursor()
    cursor.execute("SELECT nazev FROM ukoly WHERE id = %s", (id_ukolu,))
    row = cursor.fetchone()
    cursor.close()

    assert "Úkol s ID" in out
    assert row is None