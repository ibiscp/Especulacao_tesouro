__author__ = 'Ibis'

import sqlite3
import statistics

# Arquivo contendo as operações do banco de dados.

def insertData(table, date, vc, vv):
    conn = sqlite3.connect('Titulos.db')
    c = conn.cursor()

    # Insert a row of data
    str = 'INSERT INTO table VALUES (?,?,?,?,?)'
    str = str.replace('table', "'" + table + "'")
    c.execute(str, (date, vc, vv))

    conn.commit()
    conn.close()
    return

def insertMany(table, data):

    conn = sqlite3.connect('Titulos.db')
    c = conn.cursor()

    str = 'INSERT INTO table VALUES (?,?,?,?,?)'
    str = str.replace('table', "'" + table + "'")
    c.executemany(str, data)

    conn.commit()
    conn.close()

    return

'''def printData(table, date):
    conn = sqlite3.connect('titulos.db')
    c = conn.cursor()

    # Do this instead
    c.execute("SELECT * FROM 'LFT 210104' WHERE Date=?", (date,))
    print (c.fetchone())

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

    return'''

def createTable(table):
    conn = sqlite3.connect('Titulos.db')
    c = conn.cursor()

    str = '''CREATE TABLE titulo (
    'Date'	TEXT NOT NULL UNIQUE,
    'Taxa Compra' NUMERIC,
    'Taxa Venda' NUMERIC,
    'Compra'	NUMERIC,
    'Venda'	NUMERIC,
    PRIMARY KEY(Date))'''

    str = str.replace('titulo', "'" + table + "'")

    try:
        # Create table
        c.execute(str)

        # Save (commit) the changes
        conn.commit()

        succeed = 1
    except:
        succeed = 0

    conn.close()

    return succeed

def risco(table, inicialDate, finalDate):

    conn = sqlite3.connect('Titulos.db')
    c = conn.cursor()

    str = 'select * from titulo where Date\
        between inicialDate and finalDate\
        ORDER BY Date'
    str = str.replace('titulo', "'" + table + "'")\
        .replace('inicialDate', "'" + inicialDate + "'")\
        .replace('finalDate', "'" + finalDate + "'")
    c.execute(str)
    dados = c.fetchall()

    conn.close()

    return

def getLastDate(table):

    conn = sqlite3.connect('Titulos.db')
    c = conn.cursor()

    str = 'select max(Date) from titulo'
    str = str.replace('titulo', "'" + table + "'")

    c.execute(str)

    a=c.fetchall()

    lastDate = ''.join(a[0])

    # if len(a)>0:
    #     lastDate = ''.join(a[0])
    # else:
    #     lastDate = '0001/01/01'

    conn.close()

    return lastDate

def getData(table, date):

    conn = sqlite3.connect('Titulos.db')
    c = conn.cursor()

    str = 'select * from titulo\
        where Date >= date\
        ORDER BY Date'
    str = str.replace('titulo', "'" + table + "'")\
        .replace('date', "'" + date + "'")
    c.execute(str)

    dados = c.fetchall()

    conn.close()

    return dados

def getPreçoVenda(table, date):

    conn = sqlite3.connect('Titulos.db')
    c = conn.cursor()

    str = 'select Date, Venda from titulo\
        where Date >= date\
        ORDER BY Date'
    str = str.replace('titulo', "'" + table + "'")\
        .replace('date', "'" + date + "'")
    c.execute(str)

    dados = c.fetchall()

    conn.close()

    return dados

# Pega o preço de compra entre duas datas
def getCompra(table, inicio, fim):

    conn = sqlite3.connect('Titulos.db')
    c = conn.cursor()

    str = 'SELECT Compra FROM titulo\
        WHERE (Date BETWEEN dateinic AND datefim)\
        ORDER BY Date'
    str = str.replace('titulo', "'" + table + "'")\
        .replace('dateinic', "'" + inicio + "'").replace('datefim', "'" + fim + "'")
    c.execute(str)

    dados = c.fetchall()

    conn.close()

    compra = [float(i[0]) for i in dados]

    return compra

# Pega o preço de venda entre duas datas
def getVenda(table, inicio, fim):

    conn = sqlite3.connect('Titulos.db')
    c = conn.cursor()

    str = 'SELECT Venda FROM titulo\
        WHERE (Date BETWEEN dateinic AND datefim)\
        ORDER BY Date'
    str = str.replace('titulo', "'" + table + "'")\
        .replace('dateinic', "'" + inicio + "'").replace('datefim', "'" + fim + "'")
    c.execute(str)

    dados = c.fetchall()

    conn.close()

    venda = [float(i[0]) for i in dados]

    return venda

# Pega o preço de venda em uma data
def getVendaUnico(table, date):

    conn = sqlite3.connect('Titulos.db')
    c = conn.cursor()

    str = 'SELECT Venda FROM titulo\
        WHERE Date = date'

    str = str.replace('titulo', "'" + table + "'")\
        .replace('date', "'" + date + "'")
    c.execute(str)

    dado = c.fetchone()

    conn.close()

    return float(dado)

# Pega a lista de datas entre as duas datas
def getDates(table, inicio, fim):

    conn = sqlite3.connect('Titulos.db')
    c = conn.cursor()

    str = 'SELECT Date FROM titulo\
        WHERE (Date BETWEEN dateinic AND datefim)'
    str = str.replace('titulo', "'" + table + "'")\
        .replace('dateinic', "'" + inicio + "'").replace('datefim', "'" + fim + "'")
    c.execute(str)

    dates = c.fetchall()

    conn.close()

    return dates