#!/usr/bin/python3
import re
import glob
import textract
import pathlib
from pathlib import Path
import sys
from termcolor import colored
import os
from pdf2image import convert_from_path
import tempfile
import base64

# Interação com o usuário
if len(sys.argv) <= 1:
	print()
	print(colored("Ler - Script para extração de conteudo de todo tipo de arquivo","red"))
	print(colored('Sintaxe para correta utilização: ./ler.py <PASTA ONDE SE ENCONTRAM AS CAIXAS DE E-MAIL>', 'red'))
	print()
	print(colored("O primeiro argumento DEVE ser a pasta em que AS CAIXAS DE EMAIL ESTÃO! Fique tranquilo, ele é recursivo!","blue"))
	print()
	print(colored('Recomendo fortemente ler o código para melhores resultados', 'magenta'))
	print()
	sys.exit()

# Listar os formatos que ele faz a extração
formatos = ['txt','doc','pdf','odt','docx','pptx','xls','png','jpg','ppt','eml','gif','html','xlsx','rtf','tiff','csv','ps','msg','json','epub','odp','ods']

# Cria a lista de arquivos existentes
documentos = []

# Cria a lista de arquivos corrompidos ou com problemas
arquivos_corrompidos = []

# Realizar a coleta dos arquivos de modo recursivo
print(colored("Agora vamos coletar todos os arquivos nas pastas","magenta"))

# Aqui ele faz a coleta de todos os arquvios que tem em todas as pastas, checa se realmente é arquivo também
for path in Path(sys.argv[1]).rglob('*'):
    # Aqui tornamos ele caminho absoluto
    local = str(path.resolve())
    print(colored("Documento encontrado:","blue"),ascii(local))
    # Se ele for arquivo e não pasta
    if os.path.isfile(local):
        # Primeira verificação é por arquivos com \n\t no nome, alguns vem com isso ai não conseguimos extrair
        if re.search(r"\n\t",str(local)):
            try:
                for formato in formatos:
                    if re.search(formato+r'\?',str(local)):
                        # Aqui ele pega somente o caminho absoluto da pasta que está o arquivo
                        dst = pathlib.Path(local).parent.absolute()                        
                        # Aqui ele vai trocar o nome do arquivo pra um nome que o textract entenda, pra poder ser feita a extração corretamente
                        os.rename(str(local),str(dst)+"/arquivo_com_erro_renomeado."+formato)
                        local = str(dst)+"/arquivo_com_erro_renomeado."+formato
                        documentos.append(local)
            except:
                print("Continuando")
            else:
                print(colored("=*=*=*= NÃO CONSEGUI ENCONTRAR O FORMATO DO ARQUIVO, VOU DEIXAR COMO PDF E LOGAR O ERRO =*=*=*=*="))
                # Aqui ele pega somente o caminho absoluto da pasta que está o arquivo
                dst = pathlib.Path(local).parent.absolute() 
                # Aqui ele vai trocar o nome do arquivo pra um nome que o textract entenda, pra poder ser feita a extração corretamente
                os.rename(str(local),str(dst)+"/arquivo_com_erro_renomeado_possivel_extensao_errada."+"pdf")
                local = str(dst)+"/arquivo_com_erro_renomeado_possivel_extensao_errada."+"pdf"
                documentos.append(local)
                arquivos_corrompidos.append(local)
                continue


        # Aqui ele vai verificar se o nome dele ta errado, daquelEs que possuem a extensão no nome alguns vem assim
        if re.search("/?utf-8/?",str(local)):
            for formato in formatos:
                if re.search(formato+r'\?',str(local)):
                    # Aqui ele pega somente o caminho absoluto da pasta que está o arquivo
                    dst = pathlib.Path(local).parent.absolute()                        
                    # Aqui ele vai trocar o nome do arquivo pra um nome que o textract entenda, pra poder ser feita a extração corretamente
                    os.rename(str(local),str(dst)+"/arquivo_com_erro_renomeado."+formato)
                    local = str(dst)+"/arquivo_com_erro_renomeado."+formato
                    documentos.append(local)
                           
            # Aqui é caso ele não ache a extensão do arquivo no nome dele, ai tem que fazer uma maracutaia com base64
            if re.search("/?utf-8/?",str(local)):
                try:
                    # Aqui ele pega somente o caminho absoluto da pasta que está o arquivo
                    dst = pathlib.Path(local).parent.absolute()
                    local = str(local)                
                    # Aqui ele vai dividir o nome do arquivo por ?
                    lista_nome_arquivo = local.split("?")
                    # Aqui vai setar somente o base64
                    nome_base64 = lista_nome_arquivo[3]
                    # Decodificar o base64
                    nome_limpo = base64.b64decode(nome_base64)
                    # Converter pra string
                    nome_limpo = nome_limpo.decode("utf-8")                
                    # Renomear o arquivo com o nome dele mesmo
                    os.rename(str(local),str(dst)+"/"+nome_limpo)
                    local = str(dst)+"/"+nome_limpo
                    # Adicionar a lista
                    documentos.append(local)
                except:
                    arquivos_corrompidos.append(local)
            else:
                arquivos_corrompidos.append(local)
                continue
        # Aqui ele vai verificar os arquivos que vieram errado mas não tem a extensão no nome   
        if re.search("/?UTF-8/?",str(local)):
                for formato in formatos:
                    if re.search(formato+r'\?',str(local)):
                        # Aqui ele pega somente o caminho absoluto da pasta que está o arquivo
                        dst = pathlib.Path(local).parent.absolute()                        
                        # Aqui ele vai trocar o nome do arquivo pra um nome que o textract entenda, pra poder ser feita a extração corretamente
                        os.rename(str(local),str(dst)+"/arquivo_com_erro_renomeado."+formato)
                        local = str(dst)+"/arquivo_com_erro_renomeado."+formato
                        documentos.append(local)
                if re.search("/?UTF-8/?",str(local)):
                    try:
                        # Aqui ele pega somente o caminho absoluto da pasta que está o arquivo
                        dst = pathlib.Path(local).parent.absolute()
                        local = str(local)
                        # Aqui ele vai dividir o nome do arquivo por ?
                        lista_nome_arquivo = local.split("?")
                        # Aqui vai setar somente o base64
                        nome_base64 = lista_nome_arquivo[3]
                        # Decodificar o base64
                        nome_limpo = base64.b64decode(nome_base64)
                        # Converter pra string
                        nome_limpo = nome_limpo.decode("utf-8")
                        # Renomear o arquivo com o nome dele mesmo
                        os.rename(str(local),str(dst)+"/"+nome_limpo)
                        local = str(dst)+"/"+nome_limpo
                        # Adicionar a lista
                        documentos.append(local)
                    except:
                        arquivos_corrompidos.append(local)
                else:
                    arquivos_corrompidos.append(local)
                    continue
        else:
            documentos.append(local)
            continue
    else:
        continue
print("Foram coletados um total de:",len(documentos),"documentos")
total = len(documentos)
print(documentos)

cont = 0

print(colored("Agora vamos iniciar a extração do conteudo dos arquivos", "blue"))

# Aqui vai fazer a extração do conteúdo e o tratatmento de erro pra caso tenha algum arquivo corrompido
for arquivo in documentos:

    # Aqui vamos abrir o arquivo para gravação
    arquivo_texto = open(arquivo+"_extraido","wb")
    cont += 1
    print(colored("Extraindo tudo do arquivo:","yellow"),arquivo)
    print("Este é o arquivo número",cont,"de um total de",total)

	# Fazendo a extração de todos os arquivos
    try:
        # Primeiro ele vai testar pra ver se o comando tem response, se tiver vai pro finnaly e seguir o curso da aplicação
        text = textract.process(arquivo)
    except KeyboardInterrupt:
        print()
        print(colored("Já que você insiste em sair, vamos sair. Todo o processo será perdido","blue"))
        print()
        sys.exit()
    except:
			# Se por algum motivo der erro, ele vai executar esse bloco, ele vai avisar e vai logar o arquivo na relação de arquivos corrompidos
        print(colored("----- ATENÇÃO!!!!!! ARQUIVO CORROMPIDO OU COM PROBLEMAS!!!! ----","red"))
        print(colored("Caminho do arquivo:","blue"),arquivo,colored("É o arquivo de número:","blue"),cont)
        print(colored("----- SALVANDO EM UM ARQUIVO PRA VOCÊ VERIFICAR MANUALMENTE -----","red"))
			# Aqui adicionamos o arquivo que deu problema na lista de problemáticos
        arquivos_corrompidos.append(arquivo)
    else:
			# Sem exceções vai rodar isso aqui
		# Essa parte do if é para fazer OCR em pdf, coloquei como sendo tamanho menor que 60 pq dificilmente um documento vai ter mais de 60 páginas de foto, e cada foto ele conta como um byte, coloquei também pra somente procurar por pdf, pq percebi que nao colocasse especifico pra pdf ele ia pesquisar por odt tbm e ia dar ruim
        if len(text) < 60 and re.search('pdf'+r'$', arquivo):
				# Aqui vai salvar as fotos de cada página do pdf que está como foto
            with tempfile.TemporaryDirectory() as path:
                print(colored("Encontramos arquivos PDF com imagens, vamos fazer OCR, processamento do script vai demorar", "red"))
                images_from_path = convert_from_path(arquivo, output_folder="/tmp/", fmt="png")
					# Aqui vai pesquisar pelos arquivos que foram salvos e jogar dentro de uma lista
                for path in Path("/tmp/").glob("*.png"):
                    local = str(path)
                    fotos_ocr = []
                    fotos_ocr.append(local)
						# Pra cada item da lista, cada foto no caso, vai fazer ocr
                    for foto in fotos_ocr:
                        print("Extraindo da foto",foto,"do arquivo PDF",arquivo)
                        texto_foto = textract.process(foto)
                        arquivo_texto.write(texto_foto)
							# Apagando todas as imagens criadas do OCR no pdf pra não ficar muito arquivo depois de terminado o trabalho e pra não cair em loop de repetir a mesma imagem
                        os.system("rm "+foto)
                continue
			# Aqui ele apenas escreve no arquivo de texto, no caso de não ter ocr, ser arquivo normal
        arquivo_texto.write(text)
	# Fechando o arquivo apos terminar de escrever tudo nele
    print("Pronto, extraimos e gravamos tudo, vamos para o próximo")
    arquivo_texto.close()

# Criando o arquivo externo com o arquivos problemáticos
with open('/tmp/corrompidos.txt', 'w') as f:
	for item in arquivos_corrompidos:
		f.write("%s\n" % item)
# Fechando o arquivo após acabar a gravação
f.close()

print()
print(colored("EXTRAÇÃO FINALIZADA!!!!!"))
print()
print(colored("Todos os arquivos que eu não consegui extrair por algum motivo, estão salvos em:","red"),colored("/tmp/corrompidos.txt","blue"))
print()
print(colored("Veja eles manualmente!","yellow"))
print()