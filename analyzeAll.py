__author__ = 'Ibis'

from os import listdir
from os.path import isfile, join
import xlrd
from _datetime import datetime
import xlsxwriter
import database2
import re
import Download_Files

# Script utilizado apra analizar os arquivos baixados do site do tesouro e atualizar o banco de dados.

def filterFilesByYear(lastYear, titlefiles, titulo):

    files = list();

    lastYearTitulo = int(titulo[-2:])+2000

    for i in titlefiles:
        # Separa apenas o ano do nome do arquivo.
        regex = re.compile(r'\d+')
        fileYear = int(regex.findall(i)[0])

        if fileYear >= lastYear and fileYear <= lastYearTitulo:
            files.append(i)

    return files

def updateBD():

    Download_Files.downloadFiles()

    folderName = 'Titulos/'
    titles = ['LFT', 'LTN', 'NTNB', 'NTNBPrincipal', 'NTNC', 'NTNF']

    # List of all files inside the folder
    files = [ f for f in listdir(folderName) if isfile(join(folderName,f)) ]

    # For each title that exists
    for t in titles:

        titlefiles = list()

        # De todos os arquivos da pasta separa aqueles que são o mesmo tipo de título
        for f in files:
            if f.__contains__(t + "_"):
                titlefiles.append(f)

        titleSheets = list();

        # for each file get all the sheets (todos os títulos de cada categoria)
        for f in titlefiles:
            TeamPointWorkbook = xlrd.open_workbook(folderName + f)
            sheets = TeamPointWorkbook.sheet_names()

            # Add all titles in list if not there yet
            for s in sheets:
                if s.replace('-','').replace(' Principal','P') not in titleSheets:
                    titleSheets.append(s.replace('-','').replace(' Principal','P'))

        # # Ordena os títulos
        # titleSheets.sort(s, key=lambda x: int(x[-2]))

        # Trata cada título
        for title in titleSheets:

            # Cria a tabela no banco de dados
            succeed = database2.createTable(title)

            if succeed:
                tableExists = 0
                lastYear = 1
            else:
                tableExists = 1
                lastDate = database2.getLastDate(title)
                lastYear = int(lastDate[:4])

            dados = list(list())

            # Filtra a lista de arquivos dependendo da data
            filteredTitleFiles = filterFilesByYear(lastYear, titlefiles, title)

            # Para cada título dentro do arquivo
            for file in filteredTitleFiles:
                TeamPointWorkbook = xlrd.open_workbook(folderName + file)
                sheets = TeamPointWorkbook.sheet_names()
                sheets = [w.replace('-', '').replace(' Principal','P') for w in sheets]

                # Se existir o título dentro do arquivo coleta os dados
                if title in sheets:

                    index = sheets.index(title)
                    sheet = TeamPointWorkbook.sheet_by_index(index)

                    for row in range(2,sheet.nrows):
                        if sheet.cell_value(row,4) != '':
                            if sheet.cell_type(row,0) == 3:
                                dateT = xlrd.xldate_as_tuple(sheet.cell_value(row,0), TeamPointWorkbook.datemode)
                                date = datetime(*dateT)
                            else:
                                date = sheet.cell_value(row,0)
                                date = datetime.strptime(date,'%d/%m/%Y')

                            date = date.strftime("%Y/%m/%d")

                            # Se já houver a tabela no banco de dados deve verificar a data antes de adicionar
                            # Se não, apenas adiciona os dados no banco
                            add = 0
                            if tableExists:
                                if date>lastDate:
                                    add = 1
                            else:
                                add = 1

                            if add == 1:
                                taxaCompra = sheet.cell_value(row,1)
                                taxaVenda = sheet.cell_value(row,2)
                                valorCompra = sheet.cell_value(row,3)
                                valorVenda = sheet.cell_value(row,4)
                                #base = sheet.cell_value(row,5)

                                dados.append((date,taxaCompra,taxaVenda,valorCompra,valorVenda))

            # Adiciona ao banco de dados apenas se houver algo para adicionar
            if len(dados) > 0:
                database2.insertMany(title,dados)

                # Imprime o nome do título que está sendo analisado
                if tableExists:
                    print(title + ' atualizado com ' + str(len(dados)) + ' entradas')
                else:
                    print(title + ' adicionado com ' + str(len(dados)) + ' entradas')