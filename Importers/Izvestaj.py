# -*- coding: utf-8 -*-
import pymysql
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


# za mail

def send_mail(send_from, send_to, subject, text, files=None,
              server="127.0.0.1", password=""):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

    smtp = smtplib.SMTP(server, 587)
    smtp.starttls()
    smtp.login(send_from, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


# vraca sve aktivne ankete
def sveAnkete(cur):
    query = "SELECT `id_ankete`, `ime` FROM `anketa` WHERE otvorena_od <= NOW() AND otvorena_do >= NOW()"
    cur.execute(query)
    result = cur.fetchall()
    return result

def brLjudiKojiSuPopuniliAnketu(cur, anketa_id):
    query = 'SELECT COUNT(ID_STUDENT) as broj FROM POPUNIO_ANKETU WHERE ID_ANKETE=%s'
    cur.execute(query, anketa_id)
    result = cur.fetchone()
    return result

def brLjidiKojiSuPopuniliAnketu(cur, anketa_id, godina):
    query = 'SELECT COUNT(ID_STUDENT) as broj FROM POPUNIO_ANKETU RIGHT JOIN STUDENT ON POPUNIO_ANKETU.ID_STUDENT = STUDENT.ID_STUDENT WHERE ID_ANKETE=%s AND STUDENT.ID_STUDENT=%s'
    cur.execute(query, anketa_id)
    result = cur.fetchone()
    return result

def brLjudiKojiSuPopuniliZaPredmet(cur, ankete_id, predmet_id):
    query = "SELECT COUNT(DISTINCT student_id_student) as broj FROM odgovor WHERE anketa_id_anketa IN " + ankete_id + " AND predmet_id_predmet =%s";
    cur.execute(query, predmet_id)
    result = cur.fetchone()
    return result


def brLjudiPoGodinama(anekte_id):
    query = 'SELECT godina,COUNT(DISTINCT odgovor.student_id_student) as broj FROM odgovor JOIN student_u_grupi ON odgovor.student_id_student=student_u_grupi.student_id_student JOIN grupa ON grupa_id_grupa=id_grupa WHERE anketa_id_anketa IN ' + anekte_id + ' GROUP BY godina'
    cur.execute(query)
    result = cur.fetchall()
    return result


# za svako pitanje vraca procenat svih odgovora
def procZaSvaPitanja(cur, anketa_id):
    query = "SELECT tekst, COUNT(*) AS ukupno, FLOOR(SUM(CASE WHEN odgovor=1 THEN 1 ELSE 0 END)) AS jedinice,  SUM(CASE WHEN odgovor=2 THEN 1 ELSE 0 END) as dvojke, SUM(CASE WHEN odgovor=3 THEN 1 ELSE 0 END) as trojke, SUM(CASE WHEN odgovor=4 THEN 1 ELSE 0 END) AS cetvorke, SUM(CASE WHEN odgovor=5 THEN 1 ELSE 0 END) AS petice, concat(floor((SUM(CASE WHEN odgovor=1 THEN 1 ELSE 0 END) / COUNT(*)) * 100), '%') AS procenatJedinica, concat(floor((SUM(CASE WHEN odgovor=2 THEN 1 ELSE 0 END) / COUNT(*)) * 100), '%') AS procenatDvojki, concat(floor((SUM(CASE WHEN odgovor=3 THEN 1 ELSE 0 END) / COUNT(*)) * 100), '%') AS procenatTrojki, concat(floor((SUM(CASE WHEN odgovor=4 THEN 1 ELSE 0 END) / COUNT(*)) * 100), '%') AS procenatCetvorki, concat(floor((SUM(CASE WHEN odgovor=5 THEN 1 ELSE 0 END) / COUNT(*)) * 100), '%') AS procenatPetica FROM odgovor JOIN pitanje ON pitanje_id_pitanje=id_pitanje WHERE anketa_id_anketa=" + str(
        anketa_id) + "  AND odgovor REGEXP '^-?[0-9]+$' GROUP BY pitanje_id_pitanje"
    cur.execute(query)
    result = cur.fetchall()
    return result


def prosekPoPredmetima(cur, anketa_id):
    query = 'SELECT naziv, AVG(odgovor) as prosek FROM odgovor JOIN predmet ON id_predmet=predmet_id_predmet WHERE `anketa_id_anketa`=' + str(
        anketa_id) + ' AND odgovor REGEXP "^-?[0-9]+$" GROUP BY predmet_id_predmet'
    cur.execute(query)
    result = cur.fetchall()
    return result


def prosek_za_o_predmetu(cur, anketa_id, predmet_id):
    query = 'SELECT AVG(odgovor) as prosek FROM odgovor WHERE `anketa_id_anketa`=' + str(
        anketa_id) + ' AND odgovor REGEXP "^-?[0-9]+$" AND predmet_id_predmet=' + str(predmet_id)
    cur.execute(query)
    result = cur.fetchall()
    return result


def prosekPredavaca(cur, ankete_id):
    query = "SELECT ime,prezime, naziv, AVG(odgovor) as prosek FROM odgovor JOIN predavac ON id_predavac = predavac_id_predavac JOIN predmet ON id_predmet = predmet_id_predmet WHERE predavac_id_predavac IS NOT NULL AND odgovor REGEXP '^-?[0-9]+$' AND anketa_id_anketa IN " + ankete_id + " GROUP BY predavac_id_predavac, predmet_id_predmet"
    cur.execute(query)
    result = cur.fetchall()
    return result

def predavac_na_predmetu_porosek_po_svim_pitanjima(cur, predmet_id):
    # query="SELECT concat(ime, ' ', prezime) as `ime`, naziv_tip_ankete, tekst, AVG(odgovor) as `prosek` FROM odgovor JOIN pitanje ON id_pitanje = pitanje_id_pitanje JOIN predmet ON predmet_id_predmet = id_predmet JOIN predavac ON predavac_id_predavac = id_predavac JOIN tip_ankete ON anketa_id_anketa = id_tip_ankete WHERE otvorena_od <= NOW() AND otvorena_do >= NOW() AND predmet_id_predmet ="+ str(predmet_id)+ "AND odgovor REGEXP '^-?[0-9]+$' GROUP BY pitanje_id_pitanje ORDER BY anketa_id_anketa ASC, prezime, ime"
    query = "SELECT concat(predavac.ime, ' ', prezime) as `ime`, naziv_tip_ankete, tekst, AVG(odgovor) as `prosek` FROM odgovor JOIN pitanje ON id_pitanje = pitanje_id_pitanje JOIN predmet ON predmet_id_predmet = id_predmet JOIN predavac ON predavac_id_predavac = id_predavac JOIN tip_ankete ON anketa_id_anketa = id_tip_ankete JOIN anketa ON id_anketa=anketa_id_anketa WHERE otvorena_od <= NOW() AND otvorena_do >= NOW() AND predmet_id_predmet =%s AND odgovor REGEXP '^-?[0-9]+$' GROUP BY pitanje_id_pitanje ORDER BY anketa_id_anketa ASC, prezime, ime"
    cur.execute(query, predmet_id)
    result = cur.fetchall()
    return result


def profesori_po_predmetu(cur, predmet_id):
    query = "SELECT `ime`,`prezime`,`mail` FROM `cas` JOIN predavac ON predavac_id_predavac=id_predavac WHERE `predmet_id`=%s AND tip_casa_id_tip_casa=3 GROUP BY `predavac_id_predavac`"
    cur.execute(query, predmet_id)
    result = cur.fetchall()
    return result


conn = pymysql.connect(host='192.168.10.10', user='homestead', passwd='secret', db='raf_najjaci', autocommit=True)
cur = conn.cursor()

# OVDE BROJ LJUDI KOJI
ukupnoLjudi = brLjudiKojiSuPopuniliNekuAnketu(cur, srtingic)
# print(ukupnoLjudi)

        text = 'Izvestaj o anketi se nalazi u prilogu'
        subject = 'Anketa izvestaj /' + predmet_ime

        ## Lista stringova, ukoliko se salje ka vise ljudi
        send_to = ['jovanakpd@hotmail.com']
        sned_to = [prof_mail]
        ## Moja mail adresa
        send_from = 'jovanakpd11@gmail.com'

        ## Fajlovi za attach -- lista

        files = [predmet_ime + '.txt']

        password = "???"
        if (predmet_ime == 'Dizajn i analiza algoritama'):
            print("USOOOOOOOOOOOOOOOOOOOOOOOOO")
            send_mail(send_from, send_to, \
                      subject, text, password=password, server=server, files=files)

cur.close()
conn.close()