import os
import re
import subprocess
import glob
from pathlib import Path
import sys
from termcolor import colored

# Interação com o usuário
if len(sys.argv) <= 1:
	print()
	print(colored("Gerar - Script para geração de arquivo CSV.","red"))
	print(colored('Sintaxe para correta utilização: ./gerar.py <PASTA ONDE SE ENCONTRAM OS ARQUIVOS>', 'red'))
	print()
	print(colored("O primeiro argumento DEVE ser a pasta em que OS ARQUVIOS ESTÃO! Fique tranquilo, ele é recursivo!","blue"))
	print()
	print(colored('Recomendo fortemente ler o código para melhores resultados', 'magenta'))
	print()
	sys.exit()

def parse_message(filename):
    with open(filename) as f:
        return Parser().parse(f)

# Aqui vai as palavras que devem ser pesquisadas nos documentos

lista_peso_5 = ['palavra5']

lista_peso_10 = ['palavra10']

lista_peso_20 = ['palavra20']

lista_peso_30 = ['palavra30']

lista_peso_50 = ['palavra50']

lista_peso_60 = ['palavra60']

lista_peso_80 = ['palavra80']

lista_nova = lista_peso_5+lista_peso_10+lista_peso_20+lista_peso_30+lista_peso_50+lista_peso_60+lista_peso_80

# Este é o arquivo que será salvo, favor mudar a data
arquivo='./planilha_arquivos.csv'

# Aqui ele abre o arquivo pra poder gravar
file_total= open(arquivo,'w')
file_total.write('diretorio,')

# Aqui ele faz o loop em cada palavra e adiciona no cabeçalho do csv pra ficar mais fácil depois
for palavra in lista_nova:
       file_total.write(palavra)
       if palavra != lista_nova[-1]:
         file_total.write(',')
       else:
         file_total.write(',ÍNDICE')
         file_total.write('\n')
file_total.close()

# Aqui ele vai recursivamente dentro das pastas pra criar um listão com todas as pastas
lista_de_pastas = ([x[0] for x in os.walk(sys.argv[1])])

# =*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*

# Aqui tem que ter ATENÇÃO, a atual estrutura de pastas que esse script está programado para executar é pastas que terminam com número, caso queira mudar fique a vontade

# =*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*

# Agora aqui ele vai começar a ir pasta por pasta procurando as palavras chaves pra montar o csv
for lista in lista_de_pastas:
  if lista[-1].isdigit(): # Aqui onde ele faz o "grep" somente nas pastas que terminam por número, isso vai depender de como está estruturado o sistema de arquivos que deseja verificar

    contador = 0
    print()
    print(colored('Diretório: ',"red")+lista)
    with open(arquivo,'a+') as filetxt:
      filetxt.write(lista)

      # Aqui vamos computar as palavras com peso 5
      for palavra in lista_peso_5:
        atributo=''
        if len(palavra)<2:
          filetxt.write(',NA')
        else:
          try:
            atributo=subprocess.check_output('grep -iR "'+palavra+'" ./'+lista,shell=True)
            print(colored('=*=*=*=*=* PALAVRA CHAVE COM PESO 5 ENCONTRADA: ','yellow')+palavra)
            contador += 5
            filetxt.write(','+palavra)
          except:
            filetxt.write(',')
        if palavra == lista_nova[-1]:
          filetxt.write('\r\n')

      # Aqui vamos computar as palavras com peso 10
      for palavra in lista_peso_10:
        atributo=''
        if len(palavra)<2:
          filetxt.write(',NA')
        else:
          try:
            atributo=subprocess.check_output('grep -iR "'+palavra+'" ./'+lista,shell=True)
            print(colored('=*=*=*=*=* PALAVRA CHAVE COM PESO 10 ENCONTRADA: ','blue')+palavra)
            contador += 10
            filetxt.write(','+palavra)
          except:
            filetxt.write(',')
        if palavra == lista_nova[-1]:
          filetxt.write('\r\n')

      # Aqui vamos computar as palavras com peso 20
      for palavra in lista_peso_20:
        atributo=''
        if len(palavra)<2:
          filetxt.write(',NA')
        else:
          try:
            atributo=subprocess.check_output('grep -iR "'+palavra+'" ./'+lista,shell=True)
            print(colored('=*=*=*=*=* PALAVRA CHAVE COM PESO 20 ENCONTRADA: ','yellow')+palavra)
            contador += 20
            filetxt.write(','+palavra)
          except:
            filetxt.write(',')
        if palavra == lista_nova[-1]:
          filetxt.write('\r\n')

      # Aqui vamos computar as palavras com peso 30
      for palavra in lista_peso_30:
        atributo=''
        if len(palavra)<2:
          filetxt.write(',NA')
        else:
          try:
            atributo=subprocess.check_output('grep -iR "'+palavra+'" ./'+lista,shell=True)
            print(colored('=*=*=*=*=* PALAVRA CHAVE COM PESO 30 ENCONTRADA: ','blue')+palavra)
            contador += 30
            filetxt.write(','+palavra)
          except:
            filetxt.write(',')
        if palavra == lista_nova[-1]:
          filetxt.write('\r\n')

      # Aqui vamos computar as palavras com peso 50
      for palavra in lista_peso_50:
        atributo=''
        if len(palavra)<2:
          filetxt.write(',NA')
        else:
          try:
            atributo=subprocess.check_output('grep -iR "'+palavra+'" ./'+lista,shell=True)
            print(colored('=*=*=*=*=* PALAVRA CHAVE COM PESO 50 ENCONTRADA: ','yellow')+palavra)
            contador += 50
            filetxt.write(','+palavra)
          except:
            filetxt.write(',')
        if palavra == lista_nova[-1]:
          filetxt.write('\r\n')


      # Aqui vamos computar as palavras com peso 60
      for palavra in lista_peso_60:
        atributo=''
        if len(palavra)<2:
          filetxt.write(',NA')
        else:
          try:
            atributo=subprocess.check_output('grep -iR "'+palavra+'" ./'+lista,shell=True)
            print(colored('=*=*=*=*=* PALAVRA CHAVE COM PESO 60 ENCONTRADA: ','blue')+palavra)
            contador += 60
            filetxt.write(','+palavra)
          except:
            filetxt.write(',')
        if palavra == lista_nova[-1]:
          filetxt.write('\r\n')


      # Aqui vamos computar as palavras com peso 80
      for palavra in lista_peso_80:
        atributo=''
        if len(palavra)<2:
          filetxt.write(',NA')
        else:
          try:
            atributo=subprocess.check_output('grep -iR "'+palavra+'" ./'+lista,shell=True)
            print(colored('=*=*=*=*=* PALAVRA CHAVE COM PESO 80 ENCONTRADA: ','yellow')+palavra)
            contador += 80
            filetxt.write(','+palavra)
          except:
            filetxt.write(',')
        if palavra == lista_nova[-1]:
          # Aqui ele vai adicionar o valor do indice de importância das palavras
          filetxt.write(','+str(contador))
          filetxt.write('\r\n')

print()
print(colored("Terminamos de montar nosso arquivo CSV","red"))
print()
print(colored("Verifique ele em:","blue"))
print(colored("./planilha_arquivos.csv","yellow"))
print()
print(colored("Boa análise!","magenta"))
print()