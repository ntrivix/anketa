# -*- coding: utf-8 -*-
# !/usr/bin/env python
from __future__ import print_function
import pymysql
import csv


def getTipCasa(s):
    if "Predavanja i vezbe" in s:
        return "PV"
    if "Laboratorijske vezbe" in s:
        return "LV"
    if "Vezbe" in s:
        return "V"
    return "P"

def getPredavaci(s):
    predavaci = [x.strip() for x in s.split(',')]
    res = [];
    for predavac in predavaci:
        p = {}
        p["prezime"] = predavac[:predavac.rfind(" ")]
        p["ime"] = predavac[predavac.rfind(" ") + 1:]
        mail = p["ime"] + p["prezime"] + "1@raf.rs"
        mail = mail.lower()
        mail = mail.replace("-", "")
        p["mail"] = mail
        res.append(p)
    return res

conn = pymysql.connect(host='192.168.10.10', user='homestead', passwd='secret', db='skript', autocommit=True, charset='utf8')
cur = conn.cursor()

sviPredmeti = {}
sveGrupe = {}
sviCasovi = {}
sviPredavaci = {}
casoviGrupe = {}

with open('raspored.csv', newline='', encoding="utf8") as csvfile:
    rasporedreader = csv.reader(csvfile)
    for row in rasporedreader:
        predmet = row[0]
        predavaci = getPredavaci(row[2])
        tipCasa = getTipCasa(row[1])
        grupe = [x.strip() for x in row[3].split(',')]

        if not predmet in sviPredmeti:
            query = "INSERT INTO `PREDMET`(`IME`) VALUES (%s)"
            cur.execute(query, predmet)
            predmetId = cur.lastrowid
            sviPredmeti[predmet] = predmetId

        for predavac in predavaci:
            if not predavac["mail"] in sviPredavaci:
                query = "INSERT INTO `PREDAVAC`(`IME`, `PREZIME`, `MAIL`) VALUES (%s,%s,%s)"
                cur.execute(query, (predavac["ime"], predavac["prezime"], predavac["mail"]))
                predavacId = cur.lastrowid
                sviPredavaci[predavac["mail"]] = predavacId

        for g in grupe:
            if (not g in sveGrupe):
                query = "INSERT INTO `GRUPA` (`IME`,`AKTIVNA_OD`, `AKTIVNA_DO`, `GODINA`) VALUES (%s,'2017-02-01','2017-08-30',%S)"
                god = g[0]
                if g[0] == 'P':
                    god = 5
                cur.execute(query, g, god)
                grupaId = cur.lastrowid
                sveGrupe[g] = grupaId
                casoviGrupe[grupaId] = []
            for predavac in predavaci:
                if not predmet+"_"+predavac["mail"]+"_"+tipCasa in sviCasovi:
                    query = "INSERT INTO `CAS`(`ID_PREDMET`, `ID_PREDAVAC`, `TIP_CASA`) VALUES (%s,%s,%s)"
                    cur.execute(query, (sviPredmeti[predmet], sviPredavaci[predavac["mail"]], tipCasa))
                    casId = cur.lastrowid
                    sviCasovi[predmet+"_"+predavac["mail"]+"_"+tipCasa] = casId
                if (not sviCasovi[predmet+"_"+predavac["mail"]+"_"+tipCasa] in casoviGrupe[sveGrupe[g]]):
                    query = "INSERT INTO `GRUPE_NA_CASU`(`ID_CAS`, `ID_GRUPA`) VALUES (%s,%s)"
                    cur.execute(query, (sviCasovi[predmet+"_"+predavac["mail"]+"_"+tipCasa], sveGrupe[g]))
                    casoviGrupe[sveGrupe[g]].append(sviCasovi[predmet+"_"+predavac["mail"]+"_"+tipCasa])


cur.close()
conn.close()
