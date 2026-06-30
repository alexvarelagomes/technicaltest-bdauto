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
    var callback = arguments[arguments.length - 1];
    fetch('https://teste-tecnico-dados.hubbi.app/?application=Igni%C3%A7%C3%A3o', {
        headers: { 'Accept': 'application/json' }
    })
    .then(response => response.json())
    .then(data => callback(data))
    .catch(error => callback({error: error.message}));
    """
    
    # Executa o script de forma assíncrona e captura a resposta direto para o Python
    produtos_extraidos = driver.execute_async_script(script_js)
    
    if 'error' in produtos_extraidos:
        print(f"Erro capturado pelo JS: {produtos_extraidos['error']}")
        return

    print("Dados extraídos com sucesso.")
    print(f"Total de registros: ({len(produtos_extraidos)})")
    
    driver.quit()

    # Repassa para o Pandas
    return produtos_extraidos


if __name__ == "__main__":
    dados = extrair_dados()