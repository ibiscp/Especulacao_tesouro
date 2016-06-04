__author__ = 'Ibis'

import database2
from math import floor
import matplotlib.pyplot as plt
from _datetime import datetime

# Realiza o arredondamento de ma número em n casas decimais
def roundFloor(number, places):
    return floor(number * (10**places)) / float(10**places)

# Calcula a percentagem atual da carteira
def calculaPercentagemCarteira(quantTítulos, quantidade, venda, valorTotalCarteira):
    for j in range(0,quantTítulos):
        percentagemAtual[j] = roundFloor(quantidade[j]*venda[j][i], 2)/valorTotalCarteira*100
    return percentagemAtual

# Calcula a diferença das percentagens entre o desejado e o atual
def calculaDiffPercentagem(percentagemAtual, percentagemCarteira):
    diffPercentagem = [l1 - l2 for l1, l2 in zip(percentagemAtual, percentagemCarteira)]
    return diffPercentagem

# Calcula o valor total da carteira
def calculaValorCarteira(quantTítulos,quantidade,venda):
    valorTotalCarteira = 0
    for j in range(0,quantTítulos):
        valorTotalCarteira = valorTotalCarteira + quantidade[j]*venda[j][i]
    return valorTotalCarteira

# Esse arquivo serve para fazer uma simulação negociando somente com o Tesouro para obter ganhos maiores.
# Será estipulado os títulos a serem negociados e a percentagem em cada um, então será feita simulação para:
# 1%, 2%, 3%, 4%, 5%, 6%, 7%, 8%, 9% e 10%

diferenca = 4                                               # Diferença em percentagem para a realocação
dInicio = '2013/01/01'                                      # Data inicial
dFim = '2015/10/31'                                         # Data Final
titulos = ['NTNBP 150824', 'LFT 070317', 'LTN 010116']      # Títulos a serem utilizados na simulação
percentagemCarteira = [20, 20, 60]                          # Percentagem desejada na carteira
montanteInicial = 10000                                     # Montange inicial investido
aporteMensal = 100                                          # Aporte mensal
aplicacaoMinima = 30                                        # Aplicação mínima do tesouro é de R$ 30

# Pega os dados de compra, venda e datas para cada título do banco de dados
compra = []
venda = []
datas = []
for i in titulos:
    compra.append(database2.getCompra(i, dInicio, dFim))
    venda.append(database2.getVenda(i, dInicio, dFim))
for i in database2.getDates(titulos[0],dInicio,dFim):
    date_object = datetime.strptime(i[0], '%Y/%m/%d')       # Transforma as datas de string para strptime
    datas.append(date_object)

# Ordena dados de maior preço de venda para menor
indexes = sorted(range(len(compra)), key=lambda k: compra[k], reverse=True)
compra = [compra[i] for i in indexes]
venda = [venda[i] for i in indexes]
percentagemCarteira = [percentagemCarteira[i] for i in indexes]
titulos = [titulos[i] for i in indexes]

# Matrizes para salvar os dados a cada iteração
carteira = [[0 for x in range(len(compra[0]))] for x in range(len(titulos)+1)]          # Valor da carteira para cada título e o resto
quantidade = [0 for x in range(len(titulos))]                                           # Quantidade de títulos
quantidadeTitulos = [[0 for x in range(len(compra[0]))] for x in range(len(titulos))]   # Quantidade de títulos
resto = 0                                                                               # Dinheiro não investido em títulos
mes = 0                                                                                 # Mês atual
percentagemAtual = [0 for x in range(len(titulos))]                                     # Alocação atual
numeroRealocacoes = 0                                                                   # Número de realocações feitas

# Salva em um vetor a quantidade de cada título e o dinheiro restante na carteira
for i in range(0,len(titulos)):
    quantidade[i]=roundFloor(((montanteInicial*percentagemCarteira[i]/100+resto)/compra[i][0]), 2)
    resto = roundFloor(resto+montanteInicial*percentagemCarteira[i]/100-quantidade[i]*compra[i][0],2)

# Lógica principal, simula a carteira com o tempo
for i in range(0,len(compra[0])):

    if i == 108:
        print('')

    # Aporte Mensal
    if datas[i].month != mes:# and aporteMensal != 0:   # Executado quando muda o mês
        mes = datas[i].month

        valorTotalCarteira = calculaValorCarteira(len(titulos), quantidade, venda)
        percentagemAtual = calculaPercentagemCarteira(len(titulos),quantidade,venda,valorTotalCarteira)
        diffPercentagem = calculaDiffPercentagem(percentagemAtual, percentagemCarteira)

        # Vetor com a diferença entre o desejado e o atual
        realDiferenca = [0 for x in range(len(titulos))]
        aporteIndividual = [0 for x in range(len(titulos))]
        for j in range(0,len(carteira)-1):
            realDiferenca[j] = valorTotalCarteira*percentagemCarteira[j]/100-quantidade[j]*venda[j][i]
            aporteIndividual[j] = round(aporteMensal*percentagemCarteira[j]/100+realDiferenca[j],2)

        if round(sum(aporteIndividual))>0:
            for j in range(0,len(carteira)-1):
                aporteIndividual1 = aporteIndividual[j] + resto
                diffquant = roundFloor(aporteIndividual1/compra[j][i],2)
                quantidade[j] = roundFloor(quantidade[j]+diffquant,2)
                resto = roundFloor(aporteIndividual1 - diffquant*compra[j][i],2)

    valorTotalCarteira = calculaValorCarteira(len(titulos), quantidade, venda)
    percentagemAtual = calculaPercentagemCarteira(len(titulos),quantidade,venda,valorTotalCarteira)
    diffPercentagem = calculaDiffPercentagem(percentagemAtual, percentagemCarteira)

    # Rebalanceia a carteira, caso o balanço saia das percentagens estipuladas
    if max(diffPercentagem)>diferenca or abs(min(diffPercentagem))>diferenca:

        numeroRealocacoes += 1
        indexMax = diffPercentagem.index(max(diffPercentagem))   # Acha qual valor tem a máxima percentagem

        diffquant = roundFloor(diffPercentagem[indexMax]*valorTotalCarteira/(venda[indexMax][i]*100),2)  # Diferença em quantidade de títulos
        quantidade[indexMax] = roundFloor(quantidade[indexMax]-diffquant, 2) # Subtrai a quantia de títulos da matriz
        resto = resto + roundFloor(diffquant*venda[indexMax][i],2) # Adiciona o dinheiro dos títulos vendidos a carteira

        indexMin = diffPercentagem.index(min(diffPercentagem))   # Acha qual valor tem a mínima percentagem

        for l in range(indexMin,len(titulos)):
            quantidade[l] = roundFloor(quantidade[l]+(resto/compra[l][i]), 2) # Adiciona a quantia de títulos da matriz
            resto = roundFloor(resto - roundFloor((resto/compra[l][i]), 2)*compra[l][i],2) # Subtrai o dinheiro dos títulos comprados da carteira

    # Caso o preço do título de menor valor baixe e com o dinheiro do resto seja possível comprar mais 0.01, faz a compra
    if compra[2][i]*0.01 <= resto and resto > aplicacaoMinima:
        quantidade[2] = roundFloor(quantidade[2]+(resto/compra[2][i]), 2) # Adiciona a quantia de títulos da matriz
        resto = roundFloor(resto - roundFloor((resto/compra[2][i]), 2)*compra[2][i],2) # Subtrai o dinheiro dos títulos comprados da carteira

    # Adiciona as quantidades na matriz de quantidades
    for j in range(0,len(titulos)):
        quantidadeTitulos[j][i] = quantidade[j]

    # Calcula o valor da carteira para cada título
    for j in range(0,len(titulos)):
        carteira[j][i] = roundFloor(quantidade[j]*venda[j][i], 2)
    carteira[3][i] = resto

# Quatro plots na mesma imagem
f, axarr = plt.subplots(2, 2)

#Plota a carteira
axarr[0, 1].plot(datas, carteira[3])
axarr[0, 1].set_title('Dinheiro restante na carteira')

# Plota o gráfico com a composição da carteira
# f, axarr = plt.subplots(2, sharex=True)
for i in range(0, len(titulos)):
    axarr[0, 0].plot(datas, carteira[i])
    plt.hold(True)
axarr[0, 0].legend(titulos, loc = 'upper left')
axarr[0, 0].set_title('Dinheiro de cada título')

# Soma a carteira
carteiraTot = [roundFloor(sum(row),2) for row in zip(*carteira)]
axarr[1, 0].plot(datas,carteiraTot)

axarr[1, 0].text(0.95, 0.01, 'R$ ' + str(roundFloor(valorTotalCarteira,2)),
        verticalalignment='bottom', horizontalalignment='right',
        transform=axarr[1, 0].transAxes,
        color='black', fontsize=15)
axarr[1, 0].set_title('Dinheiro total na carteira')

# Plota o gráfico com a composição da em títulos
for i in range(0, len(titulos)):
    axarr[1, 1].plot(datas, quantidadeTitulos[i])
    plt.hold(True)
axarr[1, 1].set_title('Quantidade de cada título')
f.autofmt_xdate()   # Formata as datas no eixo X

plt.show()

print('Número de realocações: ' + str(numeroRealocacoes))