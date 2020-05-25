import requests
import time
import sys
from base_doc import busca_doc
from base_doc import disponiveis
from analise_demon import balanco_gerencial


def animation():                                                                #funcao pronta stackoverflow para animacao durante o download
    print("Buscando arquivo:")
    #animation = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
    animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
    for i in range(len(animation)):
        time.sleep(3)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()
    print("\n")



def escreve_arquivo(ticker,ano,demon,dados):                                    #salva a saida de dados no arquivo csv com nome ticker_ano_demon.csv
    try:
        f = (open(ticker+'_'+ano+'_'+demon+'.csv', "x"))
        f.write(dados)
        return True
    except:
        return False



def demonstrativo(token, doc):                                                  #Funcao para iniciar o projeto ParseHub
    doc = str(doc)                                                              #Faz um POST Request para a api do ParseHub conforme a documentacao oferecida pelo site
    params = {
      "api_key": "t14QhaR-0UJq",
      "start_url": "https://www.rad.cvm.gov.br/ENETCONSULTA/frmGerenciaPaginaFRE.aspx?NumeroSequencialDocumento="+doc+"&CodigoTipoInstituicao=2",
    }
    r = requests.post('https://www.parsehub.com/api/v2/projects/'+token+'/run', data=params)
    run_token = str(r.text[15:27])                                              #salva o token do processo gerado ao executar o projeto
    print()
    print("Importando os dados...")
    print("(Aproximadamente 30 segundos)")
    print()
    animation()
    #time.sleep(30)

    params = {                                                                  #GET Request para pegar raw data do projeto iniciado anteriormente
      "api_key": "t14QhaR-0UJq",                                                #passa o token gerado anteriormente como parametro para buscar os dados gerados pela execucao do processo anterior
      "format": "csv",
    }
    demo = requests.get('https://www.parsehub.com/api/v2/runs/'+run_token+'/data', params=params)
    #print(demo.text)
    dados = demo.text
    return dados



def body(ticker, ano, demon, token):                #funcao base para buscar um demonstrativo e salvar em .csv
    doc = busca_doc(ticker, ano)
    if doc == 0:
        print('Demonstrativo nao encontrado')
        return
    dados = demonstrativo(token, doc)
    aux = escreve_arquivo(ticker,ano,demon,dados)
    if aux == True:
        print('Arquivo '+ticker+'_'+ano+'_'+demon+'.csv'' gerado com sucesso!!!')
    else:
        print("Falha na cópia do arquivo!!! / Arquivo ja existente")



def busca_demon(ticker, ano, demon):                    #Busca de um relatorio a partir de ticker + ano + demonstrativo
    if demon == 'dr' or demon == 'DR':
        body(ticker, ano, demon, 'tUgYN4_k8zKU')        #gera DR --> passa como parametro o codigo para execucao do projeto DR (tUgYN4_k8zKU)

    elif demon == 'bpa' or demon == 'BPA':
        body(ticker, ano, demon, 'tStJKRY4WWN_')        #gera BPA

    elif demon == 'bpp' or demon == 'BPP':
        body(ticker, ano, demon, 't3fX3x4OODkW')        #gera BPP

    elif demon == 'dfc' or demon == 'DFC':
        body(ticker, ano, demon, 'tD1m6nCLOBRu')        #gera DFC

    else:
        print('Demonstrativo nao encontrado...')
        print('Digite: DR para Demonstracao dos Resultados')
        print('Digite: BPA para Balanco Patrimonial Ativo')
        print('Digite: BPP para Balanco Patrimonial Passivo')
        print('Digite: DFC para Demonstração de Fluxos de Caixa')
        return



def conj_demon(ticker, ano_ini, ano_fim):                                 #Busca conjunto de demonstrativos, executando a busca individual para todos demons de 2015 a 2019
    for ano in range(ano_ini, ano_fim+1, 1):
        ano = str(ano)
        body(ticker, ano, 'DR', 'tUgYN4_k8zKU')
        body(ticker, ano, 'BPA', 'tStJKRY4WWN_')
        body(ticker, ano, 'BPP', 't3fX3x4OODkW')
        body(ticker, ano, 'DFC', 'tD1m6nCLOBRu')


def main():

    print("_________________________________________________________________________________")
    print("                          DEMONSTRATIVOS FINANCEIROS B3                          ")
    print("_________________________________________________________________________________")
    print()
    while True:
        print("__________________________ DOWNLOAD DE DEMONSTRATIVOS ___________________________")
        print()
        print('1- Demonstrativo individual por ano')
        print('2- Conjunto de demonstrativos (DR + BPA + BPP + DFC (2015-2019))')
        print()
        print("________________________________ OUTRAS FUNCOES _________________________________")
        print()
        print('3- Listar empresas disponíveis para consulta')
        print('4- Compilar demonstrativos')
        print('5- Sair do programa')
        print("_________________________________________________________________________________")
        print()
        modo = int(input('Opção:'))
        print()
        if modo == 1:
            while True:
                ticker = input("\nTicker: ")
                if len(ticker) < 1: break
                ano = input("Ano: ")
                demon = input("Demonstrativo: ")
                busca_demon(ticker,ano,demon)

        elif modo == 2:
            ticker = input('Ticker:')
            print('Periodo:')
            ano_ini = int(input('\tAno incial:'))
            ano_fim = int(input('\tAno final:'))
            conj_demon(ticker, ano_ini, ano_fim)
            print("Todos os demonstrativos foram baixados!!!")
            print("Encerrando o programa...")
            exit()

        elif modo == 3:
            disponiveis()
            print('\n\n')

        elif modo == 4:
            ticker = input('Ticker: ')
            print('Periodo:')
            ano_ini = int(input('\tAno Inicial: '))
            ano_fim = int(input('\tAno final: '))
            balanco_gerencial(ticker, ano_ini, ano_fim)

        elif modo == 5:
            print('Encerrando o programa...')
            exit()

        else:
            print('Opção Invalida')
            exit()

    print("_________________________________________________________________________________")
main()