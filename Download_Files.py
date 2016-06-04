__author__ = 'Ibis'

# Este script serve para baixar todos os arquivos .xls do site do tesouro.
# Os arquivos são baixados por ano de cada título.
# Os arquivos antigos do último ano já salvou na pasta são atualizados.

import os
from datetime import date
import urllib.request
import re

# Acha o ano do arquivo mais atual dado um título.
def findHigherYear(titulo, directory):

    year = 0

    # Para cada arquivo dentro da pasta.
    for i in os.listdir(directory):

        # Se o arquivo iniciar com o nome do título passado como argumento.
        if os.path.isfile(os.path.join(directory,i)) and titulo in i:

            # Separa apenas o ano do nome do arquivo.
            regex = re.compile(r'\d+')
            fileYear = int(regex.findall(i)[0])

            if fileYear > year:
                year = fileYear

    return year

def downloadFiles():
    # Lista de títulos do tesouro com as duas formas escritas encontradas no site e o ano de início.
    titulos = [['NTNC', 'NTN-C', 2002],
                ['NTNB', 'NTN-B', 2003],
                ['NTNF', 'NTN-F', 2004],
                ['NTNBPrincipal', 'NTN-B_Principal', 2005],
                ['LFT', 'LFT', 2002],
                ['LTN', 'LTN', 2002]]

    # Cria a pasta Titulos se ela ainda não existir.
    folderName = 'Titulos/';

    if not os.path.exists(folderName):
        os.makedirs(folderName)

    # Ano atual.
    year = date.today().year

    # Baixará para cada título da lista titulos.
    for t in titulos:

        higherYear = findHigherYear(t[0], folderName)

        # Para cada ano desde o ano inicial do título até o ano atual.
        for y in range(t[2],year+1):

            filename = "%s%s_%s.xls" % (folderName, t[0], y)

            # Baixa se o arquivo ainda não existir ou se estiver desatualizado
            if os.path.isfile(filename)==False or y>=higherYear:

                # Diferentes url's para antes e depois do ano 2011.
                if y <= 2011:
                    site = "http://www3.tesouro.gov.br/tesouro_direto/download/historico/%s/historico%s_%s.xls" % (y, t[0], y)
                else:
                    site = "http://www.tesouro.fazenda.gov.br/documents/10180/137713/%s_%s.xls" % (t[1], y)

                urllib.request.urlretrieve(site, filename)

                print("%s_%s.xls" % (t[0], y))