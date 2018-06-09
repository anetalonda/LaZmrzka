# Z modulu flask naimportuje "Flask" a "g" tak, abychom je mohli
# používat v tomto programu
from flask import Flask, g
# Naimportuje náš modul names_bp (names_bp.py), tak abychom z tohoto souboru
# používat proměnné a funkce, které jsou definované v names_bp.py
#import names_bp
# Stejně tak pro about_bp modul
#import about_bp

import zmrzky

# Vytvoří novou Flask aplikaci a uloží ji do proměnné "kateApp"
kateApp = Flask(__name__)
# Zaregistruje blueprint z names_bp do naší Flask aplikace - names_bp.blueprint
# odkazuje na proměnnou "blueprint", kterou jsme vytvořili v names_bp.py
#kateApp.register_blueprint(names_bp.blueprint)
# Stejně tak zaregistrujeme about_bp blueprint
#kateApp.register_blueprint(about_bp.blueprint)

kateApp.register_blueprint(zmrzky.blueprint)

# Zaregistruje funkci close_db() do naší aplikace jako funkci, která se má spustit,
# když se ukončuje naše aplikace
@kateApp.teardown_appcontext
def close_db(error):
    if hasattr(g, 'mysql_db'):
        # Bezpečně ukončí spojení s naší databází
        g.mysql_db.close()
