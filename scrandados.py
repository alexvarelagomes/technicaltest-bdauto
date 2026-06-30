import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def extrair_dados():
    
    # Inicializa o Chrome sem flags de automação
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=149)
    
    print("Acessando a raiz do site para validação.")
    driver.get("https://teste-tecnico-dados.hubbi.app/")

    botao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[3]/div/div[2]/div[2]/button')))
    botao.click()
    
    time.sleep(15)

    script_js = """
        var pagina = arguments[0];
        var callback = arguments[arguments.length - 1];
        fetch('https://teste-tecnico-dados.hubbi.app/?application=Igni%C3%A7%C3%A3o&page=' + pagina, {
            headers: { 'Accept': 'application/json' }
        })
        .then(response => response.json())
        .then(data => callback(data))
        .catch(error => callback({error: error.message}));
        """
    
    # Dicionário para armazenar os dados extraídos.
    produtos_extraidos = {'data': []}
    
    print("Mapeando paginação...")
    primeira_resposta = driver.execute_async_script(script_js, 1)
    
    if 'error' in primeira_resposta:
        print(f"Erro capturado pelo JS: {primeira_resposta['error']}")
        driver.quit()
        return
        
    # Armazena os dados da primeira página e descobre o limite de paginação dinamicamente
    produtos_extraidos['data'].extend(primeira_resposta['data'])
    ultima_pagina = primeira_resposta['meta']['last_page']
    
    # Itera sobre as páginas para coletar os dados.
    for pagina_atual in range(ultima_pagina + 1):
        print(f"Coletando página {pagina_atual} de {ultima_pagina}...")
        
        # Executa o script js para coletar os dados de cada página.
        resposta = driver.execute_async_script(script_js, pagina_atual)
        
        if 'error' not in resposta:
            produtos_extraidos['data'].extend(resposta['data'])
        else:
            print(f"Falha ao extrair página {pagina_atual}: {resposta['error']}")
            
        time.sleep(0.5) 

    print("\nColeta finalizada.")
    print(f"Total de registros: {len(produtos_extraidos['data'])}")
    
    driver.quit()

    # Repassa para o Pandas
    return produtos_extraidos

if __name__ == "__main__":
    dados = extrair_dados()