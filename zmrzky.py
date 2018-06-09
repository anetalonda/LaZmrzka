# Naimportuje sqlite3 modul, abychom mohli pracovat s SQLite
import sqlite3
# Z flasku naimportuje spoustu různých funkcí, které budeme potřebovat
from flask import Blueprint, request, g, url_for, render_template, redirect
from jinja2 import exceptions

# Vytvoří nový blueprint s názvem "zmrzky_bp" a uloží ho to proměnné blueprint
blueprint = Blueprint('zmrzky_bp', __name__)

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

    # SELECT .............
    # .....
    zmrzky = [ 'Jahodova', 'Oriskova', 'Cokoladova']

    return render_template("zmrzky.html", zmrzky = zmrzky, startDate = startDate, endDate = endDate)