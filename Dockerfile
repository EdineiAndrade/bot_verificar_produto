# Use uma imagem base Ubuntu 20.04
FROM ubuntu:20.04

# Defina variáveis de ambiente
ENV DEBIAN_FRONTEND=noninteractive

# Atualize e instale dependências necessárias
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    python3 \
    python3-pip \
    --no-install-recommends

# Baixe e adicione a chave GPG do Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adicione o repositório do Google Chrome
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Atualize os repositórios e instale o Google Chrome
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends

# Limpe a instalação e remova os arquivos temporários
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/apt/* && \
    rm -rf /tmp/*

# Copie o arquivo requirements.txt e instale as dependências Python
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# Copie os scripts Python para o contêiner
COPY buscar_produto.py /app/buscar_produto.py
COPY enviar_email.py /app/enviar_email.py
COPY enviar_email.py /app/id_produto.txt

# Defina o diretório de trabalho
WORKDIR /app

# Comando para executar o script Python
CMD ["python3", "buscar_produto.py"]
