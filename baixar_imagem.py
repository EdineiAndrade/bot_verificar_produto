import requests

def baixar_imagem(imagem_produto,id_produto):
    try:
        caminho_arquivo = f'C:\\Users\\inec\\Documents\\_projetos\\freelas\\scraping_sites_estevao\\site_01\\imagens\\{id_produto}.jpg'
        # Faz a solicitação GET para obter o conteúdo da imagem
        resposta = requests.get(imagem_produto)
        # Verifica se a solicitação foi bem-sucedida
        if resposta.status_code == 200:
            # Abre um arquivo no modo de escrita binária
            with open(caminho_arquivo, 'wb') as arquivo:
                # Escreve o conteúdo da imagem no arquivo
                arquivo.write(resposta.content)
            print(f"Imagem baixada com sucesso e salva em {caminho_arquivo}")
        else:
            print(f"Falha ao baixar a imagem. Status code: {resposta.status_code}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")