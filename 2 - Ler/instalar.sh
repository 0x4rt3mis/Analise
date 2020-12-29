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
echo "----- Instalando as dependencias específicas do textract -----"
echo
echo
sleep 2
apt-get -y install python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr \
flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig libpulse-dev
sleep 2
apt-get install antiword
echo
echo
echo
echo
echo "Instalação concluida agora é só utilizar o ./ler_numero2.py"
chmod +x ler_numero2.py 2>/dev/null
