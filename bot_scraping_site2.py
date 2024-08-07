from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from enviar_email import send_email
from dotenv import load_dotenv
from termcolor import colored
from datetime import datetime
import pandas as pd
import schedule
import locale
import time
import os

print(colored("\n========================| BOT verificar_produto INICIADO |======================\n",'green'))

def config_driver():
    print(colored("====>> Carregando navegador e buscando informações do produto...",'green'))
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=500,500', '--incognito'] #,'--headless'
    for argument in arguments:
        chrome_options.add_argument(argument)
        # inicializando o webdriver
    chrome_options.add_experimental_option('prefs', {
    # Desabilitar notificações
    'profile.default_content_setting_values.notifications': 2
    })
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-cookies")
    chrome_options.add_argument("--disable-session-crashed-bubble")
    chrome_options.add_argument("--disable-prompt-on-repost")
    driver = webdriver.Chrome(options=chrome_options)
    # Maximiza a janela
    driver.maximize_window()

    # Obter o tamanho da janela maximizada
    window_size = driver.get_window_size()

    # Define o tamanho padrão desejado (por exemplo, 1280x720)
    desired_width = 1463
    desired_height = 784

    # Verifica se o tamanho atual é menor do que o desejado
    if window_size['width'] > desired_width or window_size['height'] > desired_height:
        # Define o tamanho da janela para o tamanho desejado
        driver.set_window_size(desired_width, desired_height)
    return driver
def scrape_product_info():    
    # id do produto (substitua pela ID real no arquivo txt)
    with open("./id_produto.txt", 'r') as file:
        id_produto = file.read().strip()
    driver = config_driver()
    url = f"https://cemstoretec.com.br/"
    driver.get(url)
    
    print(colored("====>> Informações do produto:",'green'))
    # Exemplo de extração de dados (substitua pelos seletores corretos)
    time.sleep(.3)
    poup_01 = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "wt-cli-accept-all-btn")))
    poup_01.click()
    time.sleep(.3)
    try:
        poup_02 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dismiss-button")))
        poup_02.click()
    except Exception as e:
        print(f"")  
        # Seleciona todos os elementos com o atributo data-slick-index
    slick_slides = driver.find_elements(By.CSS_SELECTOR, '[data-slick-index]')

    # Itera sobre cada elemento encontrado
    for slide in slick_slides:
        # Obtém o valor do atributo data-slick-index
        slick_index = slide.get_attribute('data-slick-index')        
        # Aqui você pode realizar operações com cada slide
        link_elements = driver.find_element(By.XPATH,f'//*[@class="slick-list draggable"]/div/div[@tabindex={slick_index}]/div/a')
        link = link_elements.get_attribute('href')
        driver.get(link)
        #formatar valor    
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        # Função lambda para formatar a string
        valor = valor.replace('R$ ', '').replace('.', '').replace(',', '.')
        valor = float(valor)
        print(colored(f"===| Valor: {valor}",'green'))
        # Obter a data e hora atuais
        data_hora_atual = datetime.now()
        # Formatar a data e hora
        data_hora_formatada = data_hora_atual.strftime("%Y-%m-%d %H:%M:%S")
        # Encontrar o elemento usando XPath
        element = driver.find_element(By.XPATH,"//div[@class='sc-dcJsrY hmLryf']/div/ul/li/a")
        # Pegar o atributo href
        href_produto = element.get_attribute('href')
        driver.get(href_produto)
        url_produto = driver.current_url

    product_info = {
        'Produto': poup_01,
        'Data-hora_consulta': data_hora_formatada,
        'Valor': valor,
        'Link_produto': url_produto
    }
    df_produto = pd.DataFrame([product_info])

    driver.quit()
    return product_info, df_produto

def update_excel_file(product_info):
    
    #Atualiza o arquivo Excel com as informações do produto na próxima linha disponível.
    file_name = "dados_produto.xlsx"
    #Criar o arquivo se ainda não existe
    if not os.path.exists(file_name):
        create_excel_file(file_name)    
    # Carregar o arquivo existente
    print(colored("====>> Atualizando as informações do arqiovo Excel",'green'))
    df = pd.read_excel(file_name)    
    # Adicionar a nova linha de informações
    df = pd.concat([df, product_info], ignore_index=True)    
    # Salvar as atualizações
    df.to_excel(file_name, index=False)
    # Ordenar o DataFrame pela coluna datetime em ordem decrescente
    df = df.sort_values(by='Data-hora_consulta', ascending=False)
    #total de linhas
    # Caminho absoluto do arquivo
    path_file = os.path.abspath(file_name)
    print(colored(f'====>> Arquivo "{file_name}" atualizado com sucesso!\n','green'))
    return path_file
def create_excel_file(file_name):
    print(colored(f"====>> Criando arquivo excel {file_name}",'green'))
    #Cria um arquivo Excel com colunas especificadas.    
    columns = ['Categoria','Produto', 'Valor', 'Data-hora_consulta', 'Link_produto','Link_imagem_produto']
    df = pd.DataFrame(columns=columns)
    df.to_excel(file_name, index=False)

def tarefa_programada():
    df_produto,product_info = scrape_product_info()
    path_file = update_excel_file(product_info)
    send_email(df_produto,product_info,path_file)
    print(colored("====>> Busca atual finalizada!!",'green'))
# Agendar a tarefa para ser executada
schedule.every(.1).minutes.do(tarefa_programada)

# Loop para manter o script em execução e verificar o agendamento
while True:
    schedule.run_pending()
    time.sleep(1)