== Soubory a složky v tomhle projektu ==

static - obsahuje statické dokumenty, které se nikdy nemění, jako obrázky, CSS 
         styly, JavaScripty atd.

templates - obsahuje HTML šablony, ze kterých se pak poskládá stránka, která se
            zobrazí uživateli

main.py - hlavní (spouštěcí) program našeho webíku - v něm se vytvoří Flask a
          zaregistrují se jednotlivé Blueprinty

names_bp.py - náš vlastní Blueprint pro stránku na zobrazování, vkládání a mazání
              jmen z databáze

about_bp.py - náš vlastní Blueprint pro stránku "O mně"

mydb.sqlite - SQLite datábáze, nad kterou spouštíme všechny naše SQL dotazy

schema.sql - popis, jak vytvořit v mydb.sqlite tu tabulku, kterou použiváme

__pycache__ - až ten program poprvé spustíš, tak se možná vytvoří složka __pycache__.
              Do té složky si Python a Flask ukládají některé kusy programu, aby
              je přístě mohli spustit rychleji. Tuhle složku můžeš klidně kdykoliv
              vymazat, Python si ji zase udělá sám znovu, až bude potřebovat

.gitignore - soubor se seznamem souborů, které má git ignorovat

== Instalace/spouštění ==

Nejprve ve složce s tímto projektem musíme vytvořit nové virtualní prostředí Pythonu.
Otevři terminál a pomocí příkazu "cd" se naviguj do složky, kde jsi tento projekt
rozbalila.

Nyní spusť

    python3 -m venv venv

Tím se vytvoří virtuální prostředí. Tento kroky už v budoucnu nebudeš muset opakovat,
pokud budeš chtít spustit tenhle program znovu.


Nyní aktivuj virtualní prostředí:

    source ./venv/bin/activate

Na Windows:

    venv\Scripts\activate.bat

Na začátku příkazové řádky by se ti mělo objevit "venv", což znamená, že jsi nyní
ve virtulálním prostředí našeho projektu. Tenhle krok musíš udělat vždycky, když
budeš chtít spustit tenhle program.

Nyní nainstaluj Flask, abychom ho mohli použivat:

    pip3 install flask

Tohle do našeho virtuálního prostředí nainstaluje Flask. Tenhle krok stačí udělat
jenom jednou, Flask zůstane v tomto prostředí nainstalovaný napořád.

A teď už můžeš spustit tuhle aplikaci:

    FLASK_DEBUG=1 FLASK_APP=main.py flask run

V terminálu by se mělo objevit něco jako:

 * Serving Flask app "main"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Teď můžeš v prohlížeči otevřít tu adresu (http://127.0.0.1:5000) a všechno by mělo
fungovat. Až budeš chtít aplikaci ukončit, tak zmáčnki Ctrl+C (myslím, že i na
Macku musíš fakt zmáčknout Ctrl+C, ne Command+C)
