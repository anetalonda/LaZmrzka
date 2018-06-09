import sys
import random
import datetime
from datetime import date, timedelta
import itertools

def zmrzlinuj(dnes, teplota_dnes, db):
    cursor = db.cursor()
    nazev_dne = dnes.weekday()

    data1 = [] #druhy zmrzlin
    data2 = []
    data3 = []
    data4 = []
    fin1 = [] #finanční náročnosti
    fin2 = []
    fin3 = []
    fin4 = []
    obl1 = [] #oblibenosti
    obl2 = []
    obl3 = []
    obl4 = []
    ing1data1 = [] #ingredience č.1 pro zmrzliny ze selectu 1
    ing2data1 = [] #ingredience č.2 pro zmrzliny ze selectu 1 atd.
    ing3data1 = []
    ing4data1 = []
    ing1data2 = [] #ingredience č.1 pro zmrzliny ze selectu 2
    ing2data2 = []
    ing3data2 = []
    ing4data2 = []
    ing1data3 = []
    ing2data3 = []
    ing3data3 = []
    ing4data3 = []
    ing1data4 = []
    ing2data4 = []
    ing3data4 = []
    ing4data4 = []


    select1 = ("select Pk.Druh_Kod, Pk.Fin_Kod, Ing1.Ingredience, Ing2.Ingredience, Ing3.Ingredience, Ing4.Ingredience, Pk.Obl_Kod " \
        "from Produktovy_katalog Pk " \
        "left join Ingredience Ing1 on Pk.Druh_Kod = Ing1.Druh_Kod and Ing1.Ingredience_poradi = 1 " \
        "left join Ingredience Ing2 on Pk.Druh_Kod = Ing2.Druh_Kod and Ing2.Ingredience_poradi = 2 " \
        "left join Ingredience Ing3 on Pk.Druh_Kod = Ing3.Druh_Kod and Ing3.Ingredience_poradi = 3 " \
        "left join Ingredience Ing4 on Pk.Druh_Kod = Ing4.Druh_Kod and Ing4.Ingredience_poradi = 4 " \
        "where Pk.Kategorie_Kod = 'Cerv_sor' and " \
        "Ing1.Ingredience not in (select Ingr1.Ingredience from Ingredience Ingr1 " \
        "left join Produkce P on Ingr1.Druh_Kod = P.Druh_Kod and Ingr1.Ingredience_poradi = 1 " \
        "where P.Datum > (select date_sub(max(Datum), interval 3 day) from Produkce)) and " \
        "Ing1.Ingredience not in (select Ingr1.Ingredience from Ingredience Ingr1 " \
        "left join Produkce P on Ingr1.Druh_Kod = P.Druh_Kod and Ingr1.Ingredience_poradi = 2 " \
        "where P.Datum > (select date_sub(max(Datum), interval 3 day) from Produkce)) and " \
        "Ing2.Ingredience not in (select Ingr2.Ingredience from Ingredience Ingr2 " \
        "left join Produkce P on Ingr2.Druh_Kod = P.Druh_Kod and Ingr2.Ingredience_poradi = 2 " \
        "where P.Datum > (select date_sub(max(Datum), interval 2 day) from Produkce)) and " \
        "Ing2.Ingredience not in (select Ingr2.Ingredience from Ingredience Ingr2 " \
        "left join Produkce P on Ingr2.Druh_Kod = P.Druh_Kod and Ingr2.Ingredience_poradi = 1 " \
        "where P.Datum > (select date_sub(max(Datum), interval 2 day) from Produkce)) and " \
        "(case when ((%(mesic)s between 4 and 10) and (%(teplota)s > 23)) then Pk.Fin_Kod < '4' else Pk.Fin_Kod > '0' end) and " \
        "(case when ((%(mesic)s between 4 and 10) and (%(teplota)s < 23)) then Pk.Obl_Kod < '4' else Pk.Obl_Kod > '0' end) and " \
        "Pk.Sezonnost_Kod in " \
        "(select S.Sezonnost_Kod " \
        "from Sezonnost S " \
        "where S.Sezonnost_Mesic = %(mesic)s " \
        ") "\
        "order by rand() ")
    cursor.execute(select1, {"mesic": dnes.month, "teplota": teplota_dnes})

    for row in cursor.fetchall():
        data1.append(row[0])
        fin1.append(int(row[1]))
        ing1data1.append(row[2])
        ing2data1.append(row[3])
        ing3data1.append(row[4])
        ing4data1.append(row[5])
        obl1.append(int(row[6]))

    #zmrzka1 = data1[0]
    #print(zmrzka1)
    #ingredience_zmrzky1 = [ing1data1[0], ing2data1[0], ing3data1[0], ing4data1[0]]
    #print(ingredience_zmrzky1)

    select2 = ("select Pk.Druh_Kod, Pk.Fin_Kod, Ing1.Ingredience, Ing2.Ingredience, Ing3.Ingredience, Ing4.Ingredience, Pk.Obl_Kod " \
        "from Produktovy_katalog Pk " \
        "left join Ingredience Ing1 on Pk.Druh_Kod = Ing1.Druh_Kod and Ing1.Ingredience_poradi = 1 " \
        "left join Ingredience Ing2 on Pk.Druh_Kod = Ing2.Druh_Kod and Ing2.Ingredience_poradi = 2 " \
        "left join Ingredience Ing3 on Pk.Druh_Kod = Ing3.Druh_Kod and Ing3.Ingredience_poradi = 3 " \
        "left join Ingredience Ing4 on Pk.Druh_Kod = Ing4.Druh_Kod and Ing4.Ingredience_poradi = 4 " \
        "where Pk.Kategorie_Kod = 'Ost_sor' and " \
        "Ing1.Ingredience not in (select Ingr1.Ingredience from Ingredience Ingr1 " \
        "left join Produkce P on Ingr1.Druh_Kod = P.Druh_Kod and Ingr1.Ingredience_poradi = 1 " \
        "where P.Datum > (select date_sub(max(Datum), interval 3 day) from Produkce)) and " \
        "Ing1.Ingredience not in (select Ingr1.Ingredience from Ingredience Ingr1 " \
        "left join Produkce P on Ingr1.Druh_Kod = P.Druh_Kod and Ingr1.Ingredience_poradi = 2 " \
        "where P.Datum > (select date_sub(max(Datum), interval 3 day) from Produkce)) and " \
        "Ing2.Ingredience not in (select Ingr2.Ingredience from Ingredience Ingr2 " \
        "left join Produkce P on Ingr2.Druh_Kod = P.Druh_Kod and Ingr2.Ingredience_poradi = 2 " \
        "where P.Datum > (select date_sub(max(Datum), interval 2 day) from Produkce)) and " \
        "Ing2.Ingredience not in (select Ingr2.Ingredience from Ingredience Ingr2 " \
        "left join Produkce P on Ingr2.Druh_Kod = P.Druh_Kod and Ingr2.Ingredience_poradi = 2 " \
        "where P.Datum > (select date_sub(max(Datum), interval 2 day) from Produkce)) and " \
        "(case when ((%(mesic)s between 4 and 10) and (%(teplota)s > 23)) then Pk.Fin_Kod < '4' else Pk.Fin_Kod > '0' end) and " \
        "(case when ((%(mesic)s between 4 and 10) and (%(teplota)s < 23)) then Pk.Obl_Kod < '4' else Pk.Obl_Kod > '0' end) and " \
        "Pk.Sezonnost_Kod in " \
        "(select S.Sezonnost_Kod " \
        "from Sezonnost S " \
        "where S.Sezonnost_Mesic = %(mesic)s " \
        ") "
        "order by rand() ")
    cursor.execute(select2, {"mesic": dnes.month, "teplota": teplota_dnes})
    for row in cursor.fetchall():
        data2.append(row[0])
        fin2.append(int(row[1]))
        ing1data2.append(row[2])
        ing2data2.append(row[3])
        ing3data2.append(row[4])
        ing4data2.append(row[5])
        obl2.append(int(row[6]))

    #zmrzka2 = data2[0]
    #print(zmrzka2)
    #ingredience_zmrzky2 = [ing1data2[0], ing2data2[0], ing3data2[0], ing4data2[0]]
    #print(ingredience_zmrzky2)


    select3 = ("select Pk.Druh_Kod, Pk.Fin_Kod, Ing1.Ingredience, Ing2.Ingredience, Ing3.Ingredience, Ing4.Ingredience, Pk.Obl_Kod " \
        "from Produktovy_katalog Pk " \
        "left join Ingredience Ing1 on Pk.Druh_Kod = Ing1.Druh_Kod and Ing1.Ingredience_poradi = 1 " \
        "left join Ingredience Ing2 on Pk.Druh_Kod = Ing2.Druh_Kod and Ing2.Ingredience_poradi = 2 " \
        "left join Ingredience Ing3 on Pk.Druh_Kod = Ing3.Druh_Kod and Ing3.Ingredience_poradi = 3 " \
        "left join Ingredience Ing4 on Pk.Druh_Kod = Ing4.Druh_Kod and Ing4.Ingredience_poradi = 4 " \
        "where (Pk.Kategorie_Kod = 'Ml_ovo' or Pk.Kategorie_Kod = 'Ml_sv') and " \
        "Ing1.Ingredience not in (select Ingr1.Ingredience from Ingredience Ingr1 " \
        "left join Produkce P on Ingr1.Druh_Kod = P.Druh_Kod and Ingr1.Ingredience_poradi = 1 " \
        "where P.Datum > (select date_sub(max(Datum), interval 3 day) from Produkce)) and " \
        "Ing1.Ingredience not in (select Ingr1.Ingredience from Ingredience Ingr1 " \
        "left join Produkce P on Ingr1.Druh_Kod = P.Druh_Kod and Ingr1.Ingredience_poradi = 2 " \
        "where P.Datum > (select date_sub(max(Datum), interval 3 day) from Produkce)) and " \
        "Ing2.Ingredience not in (select Ingr2.Ingredience from Ingredience Ingr2 " \
        "left join Produkce P on Ingr2.Druh_Kod = P.Druh_Kod and Ingr2.Ingredience_poradi = 2 " \
        "where P.Datum > (select date_sub(max(Datum), interval 2 day) from Produkce)) and " \
        "Ing2.Ingredience not in (select Ingr2.Ingredience from Ingredience Ingr2 " \
        "left join Produkce P on Ingr2.Druh_Kod = P.Druh_Kod and Ingr2.Ingredience_poradi = 1 " \
        "where P.Datum > (select date_sub(max(Datum), interval 2 day) from Produkce)) and " \
        "(case when ((%(mesic)s between 4 and 10) and (%(teplota)s > 23)) then Pk.Fin_Kod < '4' else Pk.Fin_Kod > '0' end) and " \
        "(case when ((%(mesic)s between 4 and 10) and (%(teplota)s < 23)) then Pk.Obl_Kod < '4' else Pk.Obl_Kod > '0' end) and " \
        "Pk.Sezonnost_Kod in " \
        "(select S.Sezonnost_Kod " \
        "from Sezonnost S " \
        "where S.Sezonnost_Mesic = %(mesic)s " \
        ") " \
        "order by rand() ")
    cursor.execute(select3, {"mesic": dnes.month, "teplota": teplota_dnes})
    for row in cursor.fetchall():
        data3.append(row[0])
        fin3.append(int(row[1]))
        ing1data3.append(row[2])
        ing2data3.append(row[3])
        ing3data3.append(row[4])
        ing4data3.append(row[5])
        obl3.append(int(row[6]))

    #zmrzka3 = data3[0]
    #print(zmrzka3)
    #ingredience_zmrzky3 = [ing1data3[0], ing2data3[0], ing3data3[0], ing4data3[0]]
    #print(ingredience_zmrzky3)

    select4 = ("select Pk.Druh_Kod, Pk.Fin_Kod, Ing1.Ingredience, Ing2.Ingredience, Ing3.Ingredience, Ing4.Ingredience, Pk.Obl_Kod " \
        "from Produktovy_katalog Pk " \
        "left join Ingredience Ing1 on Pk.Druh_Kod = Ing1.Druh_Kod and Ing1.Ingredience_poradi = 1 " \
        "left join Ingredience Ing2 on Pk.Druh_Kod = Ing2.Druh_Kod and Ing2.Ingredience_poradi = 2 " \
        "left join Ingredience Ing3 on Pk.Druh_Kod = Ing3.Druh_Kod and Ing3.Ingredience_poradi = 3 " \
        "left join Ingredience Ing4 on Pk.Druh_Kod = Ing4.Druh_Kod and Ing4.Ingredience_poradi = 4 " \
        "where (Pk.Kategorie_Kod = 'Ml_tm' or Pk.Kategorie_Kod = 'Ml_or' or Pk.Kategorie_Kod = 'Alk' or Pk.Kategorie_Kod = 'Ve') and " \
        "Ing1.Ingredience not in (select Ingr1.Ingredience from Ingredience Ingr1 " \
        "left join Produkce P on Ingr1.Druh_Kod = P.Druh_Kod and Ingr1.Ingredience_poradi = 1 " \
        "where P.Datum > (select date_sub(max(Datum), interval 2 day) from Produkce)) and " \
        "Ing1.Ingredience not in (select Ingr1.Ingredience from Ingredience Ingr1 " \
        "left join Produkce P on Ingr1.Druh_Kod = P.Druh_Kod and Ingr1.Ingredience_poradi = 2 " \
        "where P.Datum > (select date_sub(max(Datum), interval 2 day) from Produkce)) and " \
        "Ing2.Ingredience not in (select Ingr2.Ingredience from Ingredience Ingr2 " \
        "left join Produkce P on Ingr2.Druh_Kod = P.Druh_Kod and Ingr2.Ingredience_poradi = 2 " \
        "where P.Datum > (select date_sub(max(Datum), interval 1 day) from Produkce)) and " \
        "Ing2.Ingredience not in (select Ingr2.Ingredience from Ingredience Ingr2 " \
        "left join Produkce P on Ingr2.Druh_Kod = P.Druh_Kod and Ingr2.Ingredience_poradi = 1 " \
        "where P.Datum > (select date_sub(max(Datum), interval 1 day) from Produkce)) and " \
        "Pk.Kategorie_Kod not in " \
        "(select Pk.Kategorie_Kod from Produkce P " \
        "left join Produktovy_katalog Pk on P.Druh_Kod = Pk.Druh_Kod where Pk.Kategorie_Kod = 'Ml_or' and " \
        "P.Datum > (select date_sub(max(Datum), interval 7 day) from Produkce)) and " \
        "Pk.Kategorie_Kod not in " \
        "(select Pk.Kategorie_Kod from Produkce P " \
        "left join Produktovy_katalog Pk on P.Druh_Kod = Pk.Druh_Kod where Pk.Kategorie_Kod = 'Alk' and " \
        "P.Datum > (select date_sub(max(Datum), interval 14 day) from Produkce)) and " \
        "Pk.Kategorie_Kod not in " \
        "(select Pk.Kategorie_Kod from Produkce P " \
        "left join Produktovy_katalog Pk on P.Druh_Kod = Pk.Druh_Kod where Pk.Kategorie_Kod = 'Ve' and " \
        "P.Datum > (select date_sub(max(Datum), interval 14 day) from Produkce)) and " \
        "(case when ((%(mesic)s between 4 and 10) and (%(teplota)s > 23)) then Pk.Fin_Kod < '4' else Pk.Fin_Kod > '0' end) and " \
        "(case when ((%(mesic)s between 4 and 10) and (%(teplota)s < 23)) then Pk.Obl_Kod < '4' else Pk.Obl_Kod > '0' end) and " \
        "Pk.Sezonnost_Kod in " \
        "(select S.Sezonnost_Kod " \
        "from Sezonnost S " \
        "where S.Sezonnost_Mesic = %(mesic)s " \
        ") and "\
        "(case when ((%(den)s = 5) or (%(den)s = 6)) then (Pk.Kategorie_Kod = 'Ml_tm' or Pk.Kategorie_Kod = 'Ml_or' or Pk.Kategorie_Kod = 'Ve') else (Pk.Kategorie_Kod = 'Ml_tm' or Pk.Kategorie_Kod = 'Ml_or' or Pk.Kategorie_Kod = 'Alk' or Pk.Kategorie_Kod = 'Ve') end) "\
        "order by rand() ")
    cursor.execute(select4, {"mesic": dnes.month, "teplota": teplota_dnes, "den": nazev_dne})
    for row in cursor.fetchall():
        data4.append(row[0])
        fin4.append(int(row[1]))
        ing1data4.append(row[2])
        ing2data4.append(row[3])
        ing3data4.append(row[4])
        ing4data4.append(row[5])
        obl4.append(int(row[6]))


    #zmrzka4 = data4[0]
    #print(zmrzka4)
    #ingredience_zmrzky4 = [ing1data4[0], ing2data4[0], ing3data4[0], ing4data4[0]]
    #print(ingredience_zmrzky4)

    kombinace = [data1, data2, data3, data4]
    seznam_komb = list(itertools.product(*kombinace))
    print(kombinace)
 
    #print(len(seznam_komb))
    #seznam_komb = [z for z in seznam_komb_spinavy if len(z) == 4]
    #seznam_komb = list(itertools.combinations(kombinace, 4))
    #print(len(seznam_komb))

    print("První kombinace: ", seznam_komb[0])

    rand_kombo = random.choice(seznam_komb)

    print('Random kombo: ', rand_kombo)

    #tento postup dělám pro to, aby se častěji generovaly oblíbenější zmrzky

    oblibenost = [obl1[data1.index(rand_kombo[0])], obl2[data2.index(rand_kombo[1])], obl3[data3.index(rand_kombo[2])], obl4[data4.index(rand_kombo[3])]]
    oblibenost_ref = sum(oblibenost)+1
    print("Oblíbenost: ", oblibenost)
    print("Referenční oblíbenost kombinace:", oblibenost_ref)

    fin_nar = [fin1[data1.index(rand_kombo[0])], fin2[data2.index(rand_kombo[1])], fin3[data3.index(rand_kombo[2])], fin4[data4.index(rand_kombo[3])]]
    fin_nar_ref = sum(fin_nar)+1
    print("Finanční náročnost: ", fin_nar)
    print("Referenční fin. náročnost kombinace:", fin_nar_ref)

    print("Počítám zmrzliny pro den: ", dnes)
    random.shuffle(seznam_komb)
    #print (start + datetime.timedelta(days=i))
    for kombo in seznam_komb:
        obl_temp = []
        obl_temp.append(obl1[data1.index(kombo[0])])
        obl_temp.append(obl2[data2.index(kombo[1])])
        obl_temp.append(obl3[data3.index(kombo[2])])
        obl_temp.append(obl4[data4.index(kombo[3])])

        obl_komba = int(sum(obl_temp))
        if oblibenost_ref < obl_komba:
            continue
        else:
            fin_temp = []
            fin_temp.append(fin1[data1.index(kombo[0])])
            fin_temp.append(fin2[data2.index(kombo[1])])
            fin_temp.append(fin3[data3.index(kombo[2])])
            fin_temp.append(fin4[data4.index(kombo[3])])


            fin_nar_komba = int(sum(fin_temp))
            if fin_nar_ref < fin_nar_komba:
                continue
            else:
                if ((fin_temp.count(5) > 1) or (fin_temp.count(4) > 1) or (fin_temp.count(5) == 1 and fin_temp.count(4) == 1)):
                    continue
                else:
                    ingr_temp = []
                    ingr_temp.append(ing1data1[data1.index(kombo[0])])
                    ingr_temp.append(ing2data1[data1.index(kombo[0])])
                    ingr_temp.append(ing3data1[data1.index(kombo[0])])
                    ingr_temp.append(ing4data1[data1.index(kombo[0])])

                    ingr_temp.append(ing1data2[data2.index(kombo[1])])
                    ingr_temp.append(ing2data2[data2.index(kombo[1])])
                    ingr_temp.append(ing3data2[data2.index(kombo[1])])
                    ingr_temp.append(ing4data2[data2.index(kombo[1])])

                    ingr_temp.append(ing1data3[data3.index(kombo[2])])
                    ingr_temp.append(ing2data3[data3.index(kombo[2])])
                    ingr_temp.append(ing3data3[data3.index(kombo[2])])
                    ingr_temp.append(ing4data3[data3.index(kombo[2])])

                    ingr_temp.append(ing1data4[data4.index(kombo[3])])
                    ingr_temp.append(ing2data4[data4.index(kombo[3])])
                    ingr_temp.append(ing3data4[data4.index(kombo[3])])
                    ingr_temp.append(ing4data4[data4.index(kombo[3])])

                    #print(ingr_temp)

                    ingr_temp_c = [s for s in ingr_temp if s is not None]

                    #print(ingr_temp_c)
                    #print(len(ingr_temp))
                    #print(len(set(ingr_temp)))

                    if len(ingr_temp_c) != len(set(ingr_temp_c)):
                        continue
                    else:
                        return kombo
    return []