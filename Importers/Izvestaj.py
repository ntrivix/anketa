# -*- coding: utf-8 -*-
import pymysql
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate



ANKETA_ID = 2

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


def prosZaSvaPitanja(cur, anketa_id):
    query = "SELECT TEKST, COUNT(*) AS ukupno, FLOOR(SUM(CASE WHEN OCENA=1 THEN 1 ELSE 0 END)) AS jedinice,  SUM(CASE WHEN OCENA=2 THEN 1 ELSE 0 END) as dvojke, SUM(CASE WHEN OCENA=3 THEN 1 ELSE 0 END) as trojke, SUM(CASE WHEN OCENA=4 THEN 1 ELSE 0 END) AS cetvorke, SUM(CASE WHEN OCENA=5 THEN 1 ELSE 0 END) AS petice, concat(floor((SUM(CASE WHEN OCENA=1 THEN 1 ELSE 0 END) / COUNT(*)) * 100), '%') AS procenatJedinica, concat(floor((SUM(CASE WHEN OCENA=2 THEN 1 ELSE 0 END) / COUNT(*)) * 100), '%') AS procenatDvojki, concat(floor((SUM(CASE WHEN OCENA=3 THEN 1 ELSE 0 END) / COUNT(*)) * 100), '%') AS procenatTrojki, concat(floor((SUM(CASE WHEN OCENA=4 THEN 1 ELSE 0 END) / COUNT(*)) * 100), '%') AS procenatCetvorki, concat(floor((SUM(CASE WHEN OCENA=5 THEN 1 ELSE 0 END) / COUNT(*)) * 100), '%') AS procenatPetica FROM ODGOVOR LEFT JOIN PITANJE ON ODGOVOR.ID_PITANJA=PITANJE.ID_PITANJA WHERE  ODGOVOR.ID_ANKETE=%S AND ODGOVOR.OCENA IS NOT NULL GROUP BY PITANJE.id_pitanja"
    cur.execute(query, anketa_id)
    result = cur.fetchall()
    return result


def prosekPoPredmetima(cur, anketa_id):
    query = 'SELECT PREDMET.IME, AVG(ODGOVOR.OCENA) as prosek FROM ODGOVOR LEFT JOIN CAS ON CAS.ID_CAS=ODGOVOR.ID_CAS LEFT JOIN PREDMET ON PREDMET.ID_PREDMET = CAS.ID_PREDMET WHERE ODGOVOR.ID_ANKETE=%s AND OCENA IS NOT NULL GROUP BY CAS.ID_PREDMET'
    cur.execute(query, anketa_id)
    result = cur.fetchall()
    return result


def prosekPredmetu(cur, anketa_id, predmet_id):
    query = 'SELECT PREDMET.IME, AVG(ODGOVOR.OCENA) as prosek FROM ODGOVOR LEFT JOIN CAS ON CAS.ID_CAS=ODGOVOR.ID_CAS LEFT JOIN PREDMET ON PREDMET.ID_PREDMET = CAS.ID_PREDMET WHERE ODGOVOR.ID_ANKETE=%s AND OCENA IS NOT NULL AND CAS.ID_PREDMET=%s'
    cur.execute(query, (anketa_id, predmet_id))
    result = cur.fetchall()
    return result


def prosekPredavacaNaCasu(cur, ankete_id):
    query = "SELECT PREDAVAC.IME, PREDAVAC.PREZIME, CAS.TIP_CASA, PREDMET.IME, AVG(ODGOVOR.OCENA) as prosek FROM ODGOVOR LEFT JOIN CAS ON CAS.ID_CAS=ODGOVOR.ID_CAS LEFT JOIN PREDMET ON PREDMET.ID_PREDMET = CAS.ID_PREDMET LEFT JOIN PREDAVAC ON CAS.ID_PREDAVAC = PREDAVAC.ID_PREDAVAC WHERE ODGOVOR.ID_ANKETE=%S AND OCENA IS NOT NULL GROUP BY CAS.ID_CAS"
    cur.execute(query, ankete_id)
    result = cur.fetchall()
    return result

def prosekPredavaca(cur, id_predavac, anketa_id):
    query = "SELECT PREDAVAC.IME, PREDAVAC.PREZIME, AVG(ODGOVOR.OCENA) as prosek FROM ODGOVOR LEFT JOIN CAS ON CAS.ID_CAS=ODGOVOR.ID_CAS RIGHT JOIN PREDAVAC ON PREDAVAC.ID_PREDAVAC =%s WHERE ODGOVOR.ID_ANKETE=%s  AND OCENA IS NOT NULL GROUP BY PREDAVAC.ID_PREDAVAC"
    cur.execute(query, (id_predavac, anketa_id))
    result = cur.fetchall()
    return result

conn = pymysql.connect(host='192.168.10.10', user='homestead', passwd='secret', db='skript', autocommit=True)
cur = conn.cursor()

ukupnoLjudi = brLjudiKojiSuPopuniliAnketu(cur, ANKETA_ID)
print(ukupnoLjudi)


cur.close()
conn.close()