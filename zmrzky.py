# Naimportovat moduly
import mysql.connector
import zmrzlinovac
import jmenovac
import datetime
import heslo
import pocasi
from datetime import date, timedelta
from darksky import forecast #nezapomenout nainstalovat darksky i ve virtualnim prostredi

# Z flasku naimportuje spoustu různých funkcí, které budeme potřebovat
from flask import Blueprint, request, g, url_for, render_template, redirect
from jinja2 import exceptions

# Vytvoří nový blueprint s názvem "zmrzky_bp" a uloží ho to proměnné blueprint
blueprint = Blueprint('zmrzky_bp', __name__)

def get_db():
    if not hasattr(g, 'mysql_db'):
        conn = mysql.connector.connect(host='localhost',user='root',password=heslo.pasw, database='LaZmrzka')
        g.mysql_db = conn
    return g.mysql_db

@blueprint.route("/zmrzka")
def show():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("select max(Datum) from Produkce")
    data = cursor.fetchall()
    for row in data:
        maxDatum = row[0]
        minDatum = maxDatum + timedelta(days = 1)
    return render_template("index.html", minDatum = minDatum)

@blueprint.route("/zmrzka/generuj", methods = ['POST'])
def generuj():
    # Datum ve formatu YYYY-MM-DD
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    return generuj_den(startDate, endDate)

@blueprint.route("/zmrzka/generuj/<dnesstr>/<konecstr>")
def generuj_den(dnesstr, konecstr):
    dnes = datetime.datetime.strptime(dnesstr, "%Y-%m-%d").date()
    konec = datetime.datetime.strptime(konecstr, "%Y-%m-%d").date()
    
    praha = forecast(pocasi.klic, 50.0464, 14.3038)
    teplota = int(praha.temperature)

    kombo = zmrzlinovac.zmrzlinuj(dnes, teplota, get_db())

    conn = get_db()
    cursor = conn.cursor()
    kombo_nazev1 = []
    for x in kombo:
        cursor.execute("SELECT Druh_Nazev FROM Druh_Zmrzliny WHERE Druh_Kod = %(kod)s", { "kod": x })
        for row in cursor.fetchall():
            vysledek = row[0]
            kombo_nazev1.append(vysledek)
            kombo_nazev = (tuple(kombo_nazev1))
    return kombo_nazev

    #if len(kombo) == 0:
        # TODO: vypis error
        #return "error"

    return render_template("potvrzeni.html", dnesstr = dnesstr, konecstr = konecstr, kombo_nazev = kombo_nazev, teplotastr = teplota)

@blueprint.route("/zmrzka/uloz/<dnesstr>/<konecstr>", methods=["POST"])
def uloz(dnesstr, konecstr):
    dnes = datetime.datetime.strptime(dnesstr, "%Y-%m-%d").date()
    konec = datetime.datetime.strptime(konecstr, "%Y-%m-%d").date()
    
    praha = forecast(pocasi.klic, 50.0464, 14.3038)
    teplota = int(praha.temperature)
    kombo = zmrzlinovac.zmrzlinuj(dnes, teplota, get_db())
    kombo = request.form['kombo'].split(",")
    conn = get_db()
    cursor = conn.cursor()
    for i in kombo:
        cursor.execute('INSERT into Produkce (Datum, Priznak_Plan_vs_Skut, Druh_Kod) values (%s, %s, %s)', [dnesstr, 'Plan', i])
    conn.commit()
    dnes = datetime.datetime.strptime(dnesstr, "%Y-%m-%d").date()
    zitra = dnes + datetime.timedelta(days = 1)
    if dnesstr == konecstr:
        return show()
    else:
        return generuj_den(zitra.strftime("%Y-%m-%d"), konecstr)
'''
#<!--zde se snazim vytvorit stranku, kde bude seznam s vygenerovanymi druhy zmrzlin (pro ty data, ktera byla zadana ve formulari) -->
@blueprint.route("/seznam")
def seznam():
    dnesstr = request.form.get('dnesstr')
    kombo = request.form.get('kombo')
    return render_template('seznam.html', dnesstr=dnesstr, kombo=kombo)

    try:
        return render_template('seznam.html')
    except exceptions.TemplateSyntaxError as e:
        return "Template error: " + e.filename + " on line " + str(e.lineno)
'''