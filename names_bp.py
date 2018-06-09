# Naimportuje sqlite3 modul, abychom mohli pracovat s SQLite
import sqlite3
# Z flasku naimportuje spoustu různých funkcí, které budeme potřebovat
from flask import Blueprint, request, g, url_for, render_template, redirect
from jinja2 import exceptions

# Vytvoří nový blueprint s názvem "names_bp" a uloží ho to proměnné blueprint
blueprint = Blueprint('names_bp', __name__)

# Pomocná funkce, která se připojí k databázi, pokud je potřeba a vrátí nám
# jako výsledek objekt, který obsahuje ono spojení, nad kterém potom můžeme
# spouštět SQL dotazy
def get_db():
    if not hasattr(g, 'sqlite_db'):
        con = sqlite3.connect('mydb.sqlite')
        con.row_factory = sqlite3.Row
        g.sqlite_db = con
    return g.sqlite_db

# Zaregistruje funkci show() jako funkci, kterou má Flask zavolat, když uživatel
# otevře v prohlížeči stránku "/" (tedy úvodní stránku)
@blueprint.route('/')
def show():
    # Získá připojení na databázi
    db = get_db()
    # Pošle databázi "SELECT ..." SQL dotaz a výsledek uloží do proměnné cur
    cur = db.execute("SELECT id, name, date FROM mytable ORDER BY date DESC")
    # Načte všechny řádky z výsledku toho SQL dotazu a uloží je do proměnné entries
    entries = cur.fetchall()

    # Pro každý řádek z výsledku udělej...
    for row in entries:
        # ... tenhle print(). V proměnné row je uložený seznam, který odpovídá
        # jednotlivým sloupečkům z SQL tabulky "mytable", na které jsme spustili
        # ten SQL dotaz - když se podíváš nahoru na ten SELECT dotaz, tak vidíš,
        # že jsme chtěli 3 sloupečky: id, name a date. Tady v chceme vypsat do
        # konzole jenom jméno a datum, takže vypíěeme row[1] a row[2] - v row[0]
        # je to id
        print("Name: " + row[1] + ", date: " + row[2])

    # Zavolá funkci render_template(), která vezme template names.html, nahradí 
    # v něm "names" za to, co je v proměnné "entries" a vygeneruje výsledné HTML,
    # které vrátí jako výsledek z téhle funkce zpátky do Fasku, a ten ji pošle
    # k uživateli do prohlížeče.
    try:
        return render_template('names.html', names=entries)
    except exceptions.TemplateSyntaxError as e:
        return "Template error: " + e.filename + " on line " + str(e.lineno)


# Zaregistruje funkci remove_name() jako funkci, kterou má Flask zavolat, když
# uživatel otevře v prohlížeči stránku "/remove_name/<id>", kde místo <id> bude
# nějaké číslo nebo text. Flask vezme to id, a předá nám ho do té funkce
# remove_name() jako parametr (argument), takže s tí můžeme pracovat
@blueprint.route('/remove_name/<id>')
def remove_name(id):
    # Získá připojení na databázi
    db = get_db()
    # Pošle databází "DELTE FROM ...". Otázníček se nahradí za hodnotu, které
    # je v té proměnné "id" - tohle je lepší, než ručně skládat ten SQL dotaz
    # dohromady (něco jako "DELETE FROM mytable WHERE id = " + str(id)), protože
    # je to bezpečnější
    cur = db.execute("DELETE FROM mytable WHERE id = ?", (id, ))
    # Uloží tu změnu do databáze (tj nenávratně ten záznam smaže z té databáze
    # a uloží ty změny na pevný disk
    db.commit()
    # Takhle funkce nám získá adresu (URL) pro funkci show() v tomhle blueprintu
    # tzn v tomhle konkrétním případě na adresu "/"
    showUrl = url_for('names_bp.show')
    # Přesměuje uživatelův prohlížeč na adresu v showUrl, takže prohlížeč znovu
    # načte tu úvodní stránku (tzn. že se znovu zavolá funkce show() výše), a ta
    # znovu vypíše všechny záznamy z databáze, tentokrát ale už bez toho záznamu,
    # který jsme smazali
    return redirect(showUrl)

# Zaregistruje funkci add_name() jako funkci, kterou má Flask zavolat, když
# uživatel odešle (to je to methods=["POST"]) z prohlížeče formulář (tj klikne na
# to tlačítko "Přidat" na té úvodní stránce na adresu "/add_name".
@blueprint.route('/add_name', methods=['POST'])
def add_name():
    # Získá připojení k databází
    db = get_db()
    # request je proměnná, kterou nám dá Flask. request.form se odkazuje na
    # ten formulář, který nám uživatel odeslal z prohlížeče, a 'user_name' je název
    # toho vstupního pole v tom formuláři, do kterého uživatel zadal jméno. Ve
    # výsledku nám tedy request.form['user_name'] vrátí to jméno, které uživatel zadal
    # do toho formuláře na webu - a my si to jméno uložíme do proměnné "name"
    name = request.form['user_name']
    # Pošle databází "INSERT INTO ..." SQL dotaz. Otazníček se zase nahradí za
    # hodnotu v proměnné "name". datetime('now') je speciální funkce SQLite, která
    # do tabulky vloží aktuální datum a čas
    db.execute("INSERT INTO mytable (name, date) VALUES(?, datetime('now'))", (name, ))
    # Uloží tu změnu do databáze (tj opravdu ten záznam uloží do té databáze
    # a uloží ty změny na pevný disk
    db.commit()
    # Takhle funkce nám získá adresu (URL) pro funkci show() v tomhle blueprintu
    # tzn v tomhle konkrétním případě na adresu "/"
    showUrl = url_for('names_bp.show')
    # Přesměuje uživatelův prohlížeč na adresu v showUrl, takže prohlížeč znovu
    # načte tu úvodní stránku (tzn. že se znovu zavolá funkce show() výše), a ta
    # znovu vypíše všechny záznamy z databáze, tentokrát i s tím záznamem, který
    # jsme tam pravě vložili
    return redirect(showUrl)
