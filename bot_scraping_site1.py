from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from enviar_email import send_email
from baixar_imagem import baixar_imagem
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
    url = f"https://www.gruposhopmix.com/"
    driver.get(url)    
    print(colored("====>> Informações do produto:",'green'))
    # Exemplo de extração de dados (substitua pelos seletores corretos)
    time.sleep(2)
    categorias = driver.find_elements(By.XPATH, '(//*[@class="nivel-dois borda-alpha"])[1]/li/a')
    # Itera sobre cada elemento encontrado
    n = 0

    for categoria in categorias:      
        try:
            # Aqui você pode realizar operações 
            time.sleep(5)
            n = n + 1
            n2 = 0
            elemento_categoria = driver.find_element(By.XPATH,f'(//*[@class="nivel-dois borda-alpha"])[1]/li[{n}]/a')
            link_categoria = elemento_categoria.get_attribute('href')
            nome_categoria = elemento_categoria.get_attribute('title')
            print(f'Categoria: {nome_categoria} | {link_categoria}')
            time.sleep(1)
            driver.get(link_categoria)
            produtos = driver.find_elements(By.XPATH,'(//*[@id="listagemProdutos"])[3]/ul/li/div')
            for produt in produtos:
                try:
                    n2 = n2 + 1
                    produto = driver.find_element(By.XPATH,f'(//*[@id="listagemProdutos"])[3]/ul/li[{n2}]/div')
                    id_produto = produto.get_attribute('data-id')
                    nome_produto = produto.find_element(By.TAG_NAME,'a').get_attribute('title')
                    link_produto = produto.find_element(By.TAG_NAME,'a').get_attribute('href')
                    imagem_produto = produto.find_element(By.TAG_NAME,'div').find_element(By.TAG_NAME,'img').get_attribute('src')
                    #preco_produto_venda = driver.find_element(By.XPATH,f'(//*[@id="listagemProdutos"])[3]/ul/li[{n2}]/div/div[2]/div/div/div/strong').text
                    preco_produto_promo = produto.find_element(By.XPATH,'./div[2]/div/div/div/strong').text
                    #promocao_produto = produto.find_element(By.XPATH,'.//div/span').text
                    #formatar valor    
                    #locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
                    # Função lambda para formatar a string
                    #valor = valor.replace('R$ ', '').replace('.', '').replace(',', '.')
                    #valor = float(valor)
                    
                    baixar_imagem(imagem_produto,id_produto)   
                    product_info = {
                            'categoria': nome_categoria,
                            'id_produto': id_produto,
                            'nome_produto': nome_produto,
                            'preco_produto_venda': '',
                            'preco_produto_promo': preco_produto_promo,
                            'promocao_produto': '',
                            'link_produto': link_produto,
                            'imagem_produto': imagem_produto

                        }
                    print(colored(f"====>> Informações buscadas: categoria: {categoria} Produto: {nome_produto}",'green'))
                    df_produto = pd.DataFrame([product_info])            
                    update_excel_file(df_produto)
                except:
                        print("Reiniciado...")
        except:
            print("Erro mudar de categoria...")
            continue            
    #driver.quit()
def update_excel_file(df_produto):
    file_name = r"C:\Users\inec\Documents\_projetos\freelas\scraping_sites_estevao\site_01\lista_produtos_site_01.xlsx"
    df = pd.read_excel(file_name)
    # Carregar o arquivo existente
    print(colored("====>> Inserindo as informações do arqiovo Excel",'green'))
    # Adicionar a nova linha de informações
    df = pd.concat([df, df_produto], ignore_index=True)    
    # Salvar as atualizações
    df.to_excel(file_name, index=False)
    print(colored("====>> Informações inseridas!!",'green'))
def create_excel_file(file_name):
    print(colored(f"====>> Criando arquivo excel {file_name}",'green'))
    #Cria um arquivo Excel com colunas especificadas.    
    columns = ['Categoria','Produto', 'Valor', 'Data-hora_consulta', 'Link_produto','Link_imagem_produto']
    df = pd.DataFrame(columns=columns)
    df.to_excel(file_name, index=False)

def tarefa_programada():
    product_info = scrape_product_info()
    #update_excel_file(product_info)
    #send_email(product_info,path_file)
    print(colored("====>> Busca atual finalizada!!",'green'))
# Agendar a tarefa para ser executada
schedule.every(.1).minutes.do(tarefa_programada)

# Loop para manter o script em execução e verificar o agendamento
while True:
    schedule.run_pending()
    time.sleep(1)