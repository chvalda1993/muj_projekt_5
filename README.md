# Task Manager (Python + MySQL + pytest)

## Popis projektu

Tento projekt je jednoduchá konzolová aplikace pro správu úkolů vytvořená v Pythonu.  
Úkoly jsou ukládány do databáze MySQL a aplikace umožňuje jejich přidávání, zobrazení, aktualizaci a odstranění.

Projekt je rozdělen na dvě části:
- aplikační logiku
- databázovou vrstvu

Součástí projektu jsou také automatické testy pomocí knihovny **pytest**.

---

## Použité technologie

- Python
- MySQL
- mysql-connector-python
- pytest
- python-dotenv

---

## Požadavky

Pro spuštění projektu je potřeba:

- Python 3.x
- MySQL server
- pip (Python package manager)

---

## Instalace závislostí

Nainstalujte potřebné knihovny:
pip install mysql-connector-python pytest python-dotenv

---

## Nastavení databáze

Projekt používá konfigurační soubor `.env` pro uložení přihlašovacích údajů k databázi.

1. Vytvořte soubor `.env`
2. Nastavte proměnné podle souboru `.env.example`

Příklad konfigurace:
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=task_manager
TEST_DB_NAME=task_manager_test

Databáze i tabulka se při spuštění programu vytvoří automaticky, pokud ještě neexistují.

---

## Spuštění programu

Program spustíte příkazem:
python task_manager.py


Po spuštění se zobrazí menu, ve kterém lze:

1. přidat nový úkol  
2. zobrazit úkoly  
3. aktualizovat stav úkolu  
4. odstranit úkol  
5. ukončit program  

---

## Spuštění testů

Testy lze spustit pomocí pytest:
pytest


Testy používají samostatnou **testovací databázi**, která je vytvořena automaticky při spuštění testů.

---

## Struktura projektu
project/
│
├─ task_manager.py # aplikační logika programu
├─ db.py # databázová vrstva (SQL operace)
├─ config.py # načítání konfiguračních proměnných
├─ .env.example # ukázka konfigurace
│
└─ tests/
├─ init.py
├─ conftest.py # fixture pro testovací databázi
└─ test_*.py # testy funkcí

---

## Funkcionalita programu

Aplikace umožňuje:

- přidání nového úkolu
- zobrazení aktivních úkolů
- změnu stavu úkolu
- odstranění úkolu

Úkoly mohou mít následující stavy:

- nezahájeno
- probíhá
- hotovo

---

## Autor

Klára Chvalinová
Projekt byl vytvořen jako studijní projekt akademie Tester s Pythonem.