import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from dotenv import load_dotenv
from termcolor import colored
import os

# Configure sua chave do Google (colocar o código de vocês no arquivo)

# Utilizando Senhas de app do Google (Tem que habilitar verificação em duas etapas antes)-> 
# //https://myaccount.google.com/apppasswords
def send_email(product_info, df_produto, file_path):
    print(colored("====>> Carregando informações no Email:", 'green'))
    load_dotenv()
    smtp_password = os.getenv('SMTP_PASSWORD')
    # Data e hora atual
    data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Configuração do e-mail
    msg = MIMEMultipart()
    msg['Subject'] = f"Busca Preço | Magalu - {data_hora_atual}"
    msg['From'] = '"Última Busca" <dney.dev@gmail.com>'
    msg['To'] = os.getenv('TO')

    # Corpo do email com cores da Magalu e imagem
    if len(df_produto) > 2:
        df_produto = df_produto.head(2)
    body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>Consula de preço do produto:</h2>
        {df_produto.to_html(index=False)}
        <div style="background-color: #0078d7; padding: 10px; text-align: center;">
          <img src="https://marcasmais.com.br/wp-content/uploads/2020/08/magalu.jpg" alt="Magalu" style="width: 150px;">
        </div>
        <div style="padding: 20px;">
          <p></p>
        </div>
      </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    print(colored("====>> Anexando arquivo no Email:", 'green'))
    # Anexar o arquivo Excel
    with open(file_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(file_path)}")
        msg.attach(part)

    # Configurações do servidor SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    smtp_user = os.getenv('SMTP_USER')

    # Enviar o e-mail
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            print(colored("====>> Email enviado com sucesso!!", 'green'))
    except Exception as e:
        print(colored(f"====>> Falha ao enviar email: {e}", 'red'))