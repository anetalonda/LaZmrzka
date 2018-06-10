#ZKOUŠKA POČASÍ

#ANET: stáhni si toto https://github.com/lukaskubis/darkskylib
#do příkaz. řádky napiš: python3 setup.py install
#"klic" v prom. praha nahraď klíčem, který ti pošlu zprávou :)

from darksky import forecast
from datetime import datetime
from numpy import rint

PRAHA = 50.0464, 14.3038

#t = datetime.today().replace(microsecond=0).isoformat()

t = datetime(2018, 6, 28, 12).isoformat()

praha = forecast('klic', *PRAHA, time=t, units='si')
teplota = int(rint(praha.temperature))
#funkce rint zaokrouhlí k nejbližšímu integeru
print(teplota)



