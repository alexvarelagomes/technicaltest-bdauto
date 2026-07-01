# Pipeline ETL Automotivo

### 1. Extração - `scrandados.py`
* **Bypass do Cloudflare:** Para burlar os bloqueios do site, utilizei o `undetected-chromedriver` fixando a versão do navegador. Isso evita que o scraper seja barrado logo na tela inicial pelo anti-bot.
* **Busca dinâmica de categorias:** Para o script não quebrar caso o layout do site mude (fugindo de XPaths frágeis), o código extrai o JSON embutido na própria página para pegar a lista oficial de categorias (ex: `SUSPENSÃO`, `IGNIÇÃO`).
* **Extração rápida via JS:** Injetando um `fetch` diretamente pelo Selenium (`execute_async_script`), a coleta aproveita os tokens de sessão já validados e roda de forma muito mais rápida.
* **Paginação inteligente:** O script lê qual é a última página (`last_page`) da API e faz o loop sozinho. Adicionei um *sleep* de 0.5s entre as requisições para evitar sobrecarregar o servidor e não tomar block por excesso de chamadas.

### 2. Tratamento - `pddados.py`
* **Padronização de texto:** Transformei todas as strings para MAIÚSCULO, evitando problemas de *case sensitive* mais pra frente e deixando o banco de dados visualmente limpo.
* **Ajuste seguro de tipos:** Colunas como preço, peso e dimensões foram convertidas para `float64` no Pandas. Usei o parâmetro `errors='coerce'` para garantir que qualquer dado corrompido vindo da API vire nulo (`NaN`) em vez de travar a execução do código.
* **Lidando com os JSONs aninhados:** A lista de carros compatíveis (`applications`) vinha como dicionários dentro do JSON. Para não perder essa informação e facilitar a exportação, transformei isso em uma lista de strings e salvei como formato texto, mantendo os dados acessíveis.

### 3. Carga - `main.py`
* **Banco local (SQLite):** Escolhi o SQLite pela praticidade. Não exige subir nenhum container ou serviço extra para quem quiser clonar e testar o projeto.
* **Sem peças duplicadas:** Coloquei um `UNIQUE` no `part_number` direto na criação da tabela. A regra de negócio e integridade ficam garantidas direto no banco.
* **Inserção à prova de falhas:** Usei o comando `INSERT OR IGNORE` fazendo um *Bulk Insert*. Se o pipeline rodar duas vezes seguidas, ele ignora o que já existe e adiciona apenas as peças novas, evitando duplicidade e poluição da base.

### 4. Análise Exploratória (EDA) - `analitec_eda.py`
* **Análise separada do ETL:** Criei um script isolado que conecta no SQLite já alimentado e usa SQL/Pandas para extrair valor prático dos dados.
* **O que foi respondido:**
  * Qual o ticket médio de cada categoria?
  * Quais são os 5 maiores fabricantes em volume de estoque?
  * Como está a distribuição dos prazos de garantia.

---

## Tecnologias e Ferramentas Utilizadas

* **Python 3.14:** Linguagem base do projeto com novos recursos de rastreamento de exceções.
* **uv:** Gerenciador de pacotes e ambientes virtualizados de alta performance da Astral (utilizando `pyproject.toml` e `uv.lock`).
* **Undetected ChromeDriver & Selenium:** Automação e bypass de mecanismos anti-bot.
* **Pandas:** Biblioteca de manipulação.
* **SQLite3:** Banco de dados relacional embarcado para armazenamento estruturado.

---

## Como Configurar e Executar o Projeto

### Pré-requisitos
Certifique-se de ter o Google Chrome instalado na sua máquina e o gerenciador `uv` instalado.

### 1. Clonar, inicializar o ambiente e executar o projeto
Abra o terminal no diretório do projeto e execute os comandos para criar o ambiente virtual, sincronizar as dependências através do `uv` e executar a aplicação:

```bash
# Inicializa o ambiente virtual (.venv) e instala as dependências do pyproject.toml
uv sync

# O uv executa o arquivo main.py dentro do ambiente Python. Ele fará o scraping, aplicará as transformações do Pandas e salvará tudo no SQLite:
uv run main.py

# Após a carga dos dados, para visualizar as métricas no terminal, rode:
uv run analitec_eda.py
