import task_manager as tm

def test_pridat_ukol_pozitivni(conn, monkeypatch):
    inputs = iter(["nazev_ukolu", "popis_ukolu"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    tm.pridat_ukol(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT nazev, popis, stav FROM ukoly WHERE nazev = %s", ("nazev_ukolu",))
    row = cursor.fetchone()
    cursor.close()

    assert row is not None
    assert row[0] == "nazev_ukolu"
    assert row[1] == "popis_ukolu"
    assert row[2] == "nezahájeno"

def test_pridat_ukol_negativni(conn, monkeypatch, capsys):
    inputs = iter(["", "", "OK_nazev_ukolu", "OK_popis_ukolu"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    tm.pridat_ukol(conn)

    out = capsys.readouterr().out

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ukoly")
    count = cursor.fetchone()[0]
    cursor.close()

    assert "Musí být zadaný název i popis úkolu" in out
    assert count == 1