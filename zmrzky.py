# Naimportuje sqlite3 modul, abychom mohli pracovat s SQLite
import mysql.connector
import zmrzlinovac
# Z flasku naimportuje spoustu různých funkcí, které budeme potřebovat
from flask import Blueprint, request, g, url_for, render_template, redirect
from jinja2 import exceptions

# Vytvoří nový blueprint s názvem "zmrzky_bp" a uloží ho to proměnné blueprint
blueprint = Blueprint('zmrzky_bp', __name__)

def get_db():
    if not hasattr(g, 'mysql_db'):
        conn = mysql.connector.connect(host='localhost',user='root',password='Digizmrzka876', database='LaZmrzka')
        g.mysql_db = conn
    return g.mysql_db

@blueprint.route("/zmrzka")
def show():
    # Velmi chytry kod ktery najde v databazi nejzassi den,
    # pro ktery ma vygenerovanou zmrzlinu
    minDatum = '2018-06-09'

    return render_template("index.html", minDatum = minDatum)

@blueprint.route("/zmrzka/generuj", methods = ['POST'])
def generuj():
    # Datum ve formatu YYYY-MM-DD
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    
    return generuj_den(startDate, endDate)


@blueprint.route("/zmrzka/generuj/:dnesstr/:konecstr")
def generuj_den(dnesstr, konecstr):
    dnes = datetime.datetime.strptime(dnesstr, "%Y-%m-%d").date()
    konec = datetime.datetime.strptime(konecstr, "%Y-%m-%d").date()
    kombo = zmrzlinovac.zmrzlinuj(dnes, get_db())
    if len(kombo) == 0:
        # TODO: vypis error
        return "error"
    return render_template("potvrzeni.html", dnesstr = dnesstr, konecstr = konecstr, kombo = kombo)

@blueprint.route("/zmrzka/uloz/:dnesstr/:konecstr", methods=["POST"])
def uloz(dnesstr, konecstr):
    kombo = request.form['kombo'].split(",")
    conn = get_db()
    with conn.cursor() as cursor:
        for i in kombo:
            cursor.execute('INSERT into Produkce (Datum, Priznak_Plan_vs_Skut, Druh_Kod) values (%s, %s, %s)', [dnesstr, 'Plan', i])
    conn.commit()
    dnes = datetime.datetime.strptime(dnesstr, "%Y-%m-%d").date()
    zitra = dnes + timedelta(days = 1)
    if dnesstr == konecstr:
        return show()
    else:
        return generuj_den(zitra.strftime("%Y-%m-%d"), konecstr)

