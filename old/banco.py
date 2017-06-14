
import psycopg2

con = psycopg2.connect(host='192.168.122.13', user='postgres', password='postgres',dbname='inmtroLog')

bd = con.cursor()

sql = "INSERT INTO log (id_medidor,leitura)VALUES ('leitura','ts')"


bd.execute(sql)

con.commit()


print ("ok")
"""
from pyPgSQL import PgSQL
"""
