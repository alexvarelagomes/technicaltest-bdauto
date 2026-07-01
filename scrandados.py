import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
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

    element_json = driver.find_element(By.XPATH, '//script[@type="application/json"]')
    conteudo_json = json.loads(element_json.get_attribute('innerHTML'))
    lista_categorias = conteudo_json['props']['available_categories']
    
    # Dicionário para armazenar os dados extraídos.
    produtos_extraidos = {'data': []}

    script_js = """
        var categoria = arguments[0];
        var pagina = arguments[1];
        var callback = arguments[arguments.length - 1];
        fetch('https://teste-tecnico-dados.hubbi.app/?application=' + encodeURIComponent(categoria) + '&page=' + pagina, {
            headers: { 'Accept': 'application/json' }
        })
        .then(response => response.json())
        .then(data => callback(data))
        .catch(error => callback({error: error.message}));
        """
    
    for categoria_atual in lista_categorias:
        print(f"\nIniciando coleta da categoria: {categoria_atual}")
        
        # Mapeia a primeira página para saber o limite de paginação desta categoria específica
        primeira_resposta = driver.execute_async_script(script_js, categoria_atual, 1)
        
        if 'error' in primeira_resposta:
            print(f"Erro na categoria {categoria_atual}: {primeira_resposta['error']}")
            continue
        else:
            produtos_extraidos['data'].extend(primeira_resposta['data'])
            ultima_pagina = primeira_resposta['meta']['last_page']
    
        # Itera sobre as páginas para coletar os dados.
        for pagina_atual in range(1, ultima_pagina + 1):
            print(f"Coletando {categoria_atual} - Página {pagina_atual} de {ultima_pagina}...")
            
            # Executa o script js para coletar os dados de cada página.
            resposta = driver.execute_async_script(script_js, categoria_atual, pagina_atual)
            
            if 'error' not in resposta:
                produtos_extraidos['data'].extend(resposta['data'])
                
            time.sleep(0.5) 

    print("\nColeta finalizada.")
    print(f"Total de registros: {len(produtos_extraidos['data'])}")
    
    driver.quit()

    # Repassa para o Pandas
    return produtos_extraidos

if __name__ == "__main__":
    dados = extrair_dados()