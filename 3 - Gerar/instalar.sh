#!/bin/bash
# Script criado para realizar a instalação das dependencias e aplicações necessárias para utilização do ler_nuemro2.py
# Apenas execute e seja feliz!
echo
echo "----- Para instalação e utilização do script, algums dependencias e aplicativos devem ser instalados -----"
echo
echo "Aqui vamos fazer de maneira automática para agilizar a utilização do script"
echo
echo "----- Instalando os modulos contidos no requeriments.txt -----"
echo
echo
sleep 2
apt-get -y install python3-pip
pip3 install -r requirements.txt
sleep 2
echo
echo
echo "Instalação dos modulos concluida"
echo
echo
echo "Instalação concluida agora é só utilizar o ./gerar.py"
chmod +x gerar_csv_numero3.py 2>/dev/null
