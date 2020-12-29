import email
from termcolor import colored
from email import policy
from email.parser import BytesParser
import glob
from pathlib import Path
import sys
import os
import os.path
from email.parser import Parser
import patoolib

# Script para enumeração e extração de anexos em arquivos EML. Funciona de maneira simples e rápida, logando os erros em um arquivo de texto, para verificação posterior
# Versões
# v1.1 -> Extraindo anexos .zip e .rar e loop das pastas melhorado

# Interação com o usuário
if len(sys.argv) <= 2:
	print()
	print(colored("Attach - Script para extração de texto e anexos em arquivos eml","red"))
	print(colored('Sintaxe para correta utilização: ./attach.py <PASTA ONDE SE ENCONTRAM AS CAIXAS DE E-MAIL> <PASTA PARA QUAIS ELAS DEVEM SER EXTRAÍDAS>', 'red'))
	print()
	print(colored("O primeiro argumento DEVE ser a pasta em que AS CAIXAS DE EMAIL ESTÃO!","blue"))
	print()
	print(colored('Recomendo fortemente ler o código para melhores resultados', 'magenta'))
	print()
	sys.exit()


# Cria a lista de pastas, se no caso de cada conta de e-mail vier com uma pasta, e dentro dela todos os arquivos emls
pastas = []
path = os.path.abspath(sys.argv[1])
pastas_geral = [os.path.join(path, fname) for fname in os.listdir(path)]
for p in pastas_geral:
	if os.path.isdir(p):
		pastas.append(p)

# Criando a pasta onde será armazenado todo o conteúdo extraído
pasta_gravar_extraidos = os.path.abspath(sys.argv[2])

try:
	os.mkdir(pasta_gravar_extraidos)
except:
	print("Caminho incorreto para esse pasta que está querendo criar")


# Cria a lista de arquivos eml que não foi possível extração
arquivos_corrompidos = []

# Cria a lista de arquivos eml
documentos = []

# Função para encontrar todos os arquivos EML em todas as pastas e subpastas
def enumerar_eml(pasta):
	# Aqui ele limpa a lista para não ser contaminada com os emls da pasta anterior
	documentos.clear()
	# Aqui ele vai novamente encher a lista com os eml da pasta que ta sendo varrida
	for path in Path(pasta).rglob("*.eml"):
		local = str(path)
		local = os.path.abspath(local)
		documentos.append(local)
	print()
	print(colored("Terminamos a enumeração da pasta","red"),pasta)
	print(colored("Todos emls foram enumerados, um total de:","red"),len(documentos))
	print()

# Função para ler o conteúdo do texto e salvar ele um arquivo .txt

# Aqui ele somente grava o conteudo em texto do e-mail, o que foi digitado no corpo da mensagem e vai salvar na pasta criada por caixa de email

# --- NÃO SALVA OS METADADOS, COMO POR EXEMPLO E-MAIL QUE FORAM ENVIADOS E TUDO MAIS, SALVA SOMENTE O CORPO DO TEXTO ---
def ler_texto_email(str):
        with open(str, 'rb') as fp:
                msg = BytesParser(policy=policy.default).parse(fp)
                fnm = output_dir + '/email_texto.txt'
                txt = msg.get_body(preferencelist=('plain')).get_content()
                with open(fnm, 'w') as f:
                        print(txt, file = f)


# -------- Aqui se inicia as funções que são utilizadas para  extrair os anexos ----------

# Aqui ele parsea o email pra ficar legível pra função extrair corretamente
def parse_message(filename):
   try:
     with open(filename) as f:
        return Parser().parse(f)
   except:
     return

# Aqui é a função de encontrar os anexos
def find_attachments(message):
    found = []
    for part in message.walk():
        if 'content-disposition' not in part:
            continue
        cdisp = part['content-disposition'].split(';')
        cdisp = [x.strip() for x in cdisp]
        if cdisp[0].lower() != 'attachment' and cdisp[0].lower() != 'inline':
            print('Attachment nao encontrado')
            continue
        parsed = {}
        for kv in cdisp[1:]:
          if 'filename="=' in kv:
            kv = kv.replace('filename="=','filename=')
          if "\n\tfilename=" in kv:
            kv = kv.replace("\n\tfilename=","filename=")
          if "filename*=" in kv:
            kv = kv.replace("filename*=","filename=")
          if "filename*0*=" in kv:
            kv = kv.replace("filename*0*=","filename=")

          if "''" in kv:
            kv = kv.replace("''",'')
          try:
            key, val = kv.split('name=')
            if val.startswith('"'):
                val = val.strip('"')
            elif val.startswith("'"):
                val = val.strip("'")
            if val.endswith('"'):
                val = val.replace('"','')
            parsed[key] = val
          except:
            pass
        found.append((parsed, part))
    return found

# Aqui é função que realiza a extração, deve vir com dois parâmetros, o arquivo eml e a pasta de output que serão passados no loop for logo a baixo
def run(eml_filename, output_dir):

    print(colored("Vamos iniciar a extração do eml","red"),eml_filename)
    msg = parse_message(eml_filename)
    attachments = find_attachments(msg)
    print (colored("Encontramos um total de {0} attachments...","blue").format(len(attachments)))
    for cdisp, part in attachments:
        cdisp_filename = os.path.normpath(cdisp['file'])
        if os.path.isabs(cdisp_filename):
            cdisp_filename = os.path.basename(cdisp_filename)
        towrite = os.path.join(output_dir, cdisp_filename)
        try:
          with open(towrite, "wb") as fp:
            data = part.get_payload(decode=True)
            fp.write(data)
        except:
          print ("Erro ao extrair o anexo")
          with open('erros.txt','a+') as erro:
            erro.write(output_dir+'\r\n')
          pass
    print(colored("Extração terminada! Vamos para o próximo","cyan"))
    print()

for pasta in pastas:
	# Aqui ele vai carregar todos os emls que existem em cada pasta e jogar pra lista chamada documentos
	enumerar_eml(pasta)

	# Aqui eu crio a subpasta para cada email
	output_dir = pasta_gravar_extraidos+"/"+pasta.split("/")[-1]+"_extraido"


	# Torno ela em caminho absoluto
	output_dir = os.path.abspath(output_dir)

	# Crio ela
	try:
		os.mkdir(output_dir)
	except:
		print("A pasta",output_dir,"já existe!",colored("Você já rodou o script antes, apague todas as pastas criadas, por que senão vai dar conflito","red"))
		sys.exit()


	# Seto uma variável como sendo a pasta original para retornar no final do loop de extração
	original_inicio = os.getcwd() # Pasta raiz /root/emails

	# Criamos a variável para contar a quantidade de pastas
	contar_pasta = 1

	# Aqui eu entro na pasta criada
	os.chdir(output_dir)

	# Seto uma variável como sendo a pasta do email (_extraido)
	original_email = os.getcwd()

	# Aqui vamos começar a iterar dentro de cada email
	for eml_filename in documentos:
	# Aqui deve-se tomar cuidado pra correta criação das pastas, o script deve ser executado na mesma pasta onde estão todos os emails

			# Criamos a pasta do numero do email
			os.mkdir(str(contar_pasta))

			# Entramos na pasta criada (numeração)
			os.chdir(str(contar_pasta))

			# Seto ele como a variável de extração da função
			output_dir = os.getcwd()
			print(colored("Vamos extrair os arquivos do eml:","red"),eml_filename)
			print(colored("Os arquivos serão salvos em:","blue"),output_dir)

			# Extraimos todo o conteudo
			try:
				run(eml_filename,output_dir) # Chamada da função pra extrair attachments
				ler_texto_email(eml_filename) # Chamada da função para extrair o corpo do texto

				# Aqui vai extrair os .rar se tiver como anexo ao email
				compactados_rar = []

				# Primeiro devemos pesquisar pra ver se tem algum arquivo .rar e adicionar ele a lista de compactados
				for path in Path(output_dir).glob("*.rar"):
					compactado = str(path)
					compactado = os.path.abspath(compactado)
					compactados_rar.append(compactado)

					# Aqui vamos ver se algum foi adicionado, se for positivo ele vai executar o bloco de código e descompactar ele
					if len(compactados_rar) != "0":
						print(colored("ENCONTRAMOS ARQUIVOS COMPACTADOS, VAMOS DESCOMPACTAR","red"))
						for compac in compactados_rar:
							patoolib.extract_archive(compac, outdir=output_dir)

						compactados_rar.clear()

					# Caso não encontre nenhum, vai prosseguir normalmente
					else:
						continue

                # Aqui vai extrair os .zip se tiver como anexo ao email
				compactados_zip = []

                # Primeiro devemos pesquisar pra ver se tem algum arquivo .zip e adicionar ele a lista de compactados
				for path in Path(output_dir).glob("*.zip"):
					compactado = str(path)
					compactado = os.path.abspath(compactado)
					compactados_zip.append(compactado)

                                        # Aqui vamos ver se algum foi adicionado, se for positivo ele vai executar o bloco de código e descompactar ele
					if len(compactados_zip) != "0":
						print(colored("ENCONTRAMOS ARQUIVOS COMPACTADOS, VAMOS DESCOMPACTAR","red"))
						for compac in compactados_zip:
							patoolib.extract_archive(compac, outdir=output_dir)

						compactados_zip.clear()

                    # Caso não encontre nenhum, vai prosseguir normalmente
					else:
						continue

			except KeyboardInterrupt:
				print()
				print(colored("Já que você insiste em sair, vamos sair. Todo o processo será perdido","blue"))
				print()
				sys.exit()

			except:
				print()
				print(colored("Encontramos um arquivo eml com ERRO","yellow"))
				print(colored("O arquivo é o:","blue"),eml_filename)
				print(colored("O arquivo foi salvo para verificação posterior... Vamos prosseguir","yellow"))
				print()
				arquivos_corrompidos.append(eml_filename)
			finally:

				# Retornamos para o path anterior
				os.chdir(original_email)

				# Incrementamos o marcador
				contar_pasta += 1

	# Retorno para o path original, para dar inicio a proxima caixa de email
	os.chdir(original_inicio)

# Abrindo o arquivo que foi utilizado salvar os emls corrompidos ou com algm erro
with open('/dev/shm/corrompidos.txt', 'w') as f:
	for item in arquivos_corrompidos:
		f.write("%s\n" % item)

# Fechando ele após terminar de gravar os arquivos corrompidos
f.close()

# Extração concluída!
print(colored("Extração concluida!","red"))
print()

# Caso tenha ocorrido algum arquivo com erro, isso será printado na tela
if len(arquivos_corrompidos) != 0:
	print(colored("Arquivos Corrompidos detectados!","cyan"))
	print(colored("Todos foram salvos em:","red"),colored("/dev/shm/corrompidos.txt","blue"),colored("Verifique eles manualmente","red"))
	print()

else:
	print()
	print(colored("Pronto. Tudo Finalizado!","blue"))
	print()
