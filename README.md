### 1. Extração (Extract) - `scrandados.py`
* **Ignorando Barreiras de Segurança (WAF):** Utilização do `undetected-chromedriver` com parametrização específica (`version_main`) para emular o comportamento humano legítimo e contornar os desafios de segurança e detecção automatizada (como Cloudflare Turnstile).
* **Mapeamento Dinâmico:** Em vez de mapear seletores visuais frágeis (XPaths posicionais), o script lê a tag `<script type="application/json">` na raiz do site para descobrir de forma dinâmica e 100% estável todas as categorias disponíveis no servidor (ex: `SUSPENSÃO`, `IGNIÇÃO`, etc.).
* **Injeção de JavaScript Assíncrono:** Execução de chamadas assíncronas nativas (`fetch`) com tokens da sessão injetadas diretamente no motor de renderização do navegador via `execute_async_script`, otimizando a velocidade de coleta.
* **Paginação Resiliente com Throttle:** Orquestração de loops dinâmicos baseados no metadado `last_page` da API. Aplicação de atraso tático (*throttle* de 0.5s) para mitigar riscos de *rate-limiting* ou bloqueios de IP.

### 2. Tratamento (Transform) - `pddados.py`
* **Padronização Estrita:** Transformação de todos os campos de texto do conjunto de dados para caixa alta (`UPPERCASE`), garantindo consistência relacional e eliminando divergências de caracteres.
* **Tipagem Técnica e Financeira Vetorizada:** Conversão rigorosa de preços e especificações de dimensões (`price`, `gross_weight`, `length`, `width`) para o tipo ponto flutuante (`float64`) nativo do Pandas utilizando coerção de erros (`errors='coerce'`) para proteção contra anomalias.
* **Achatamento de Estruturas Complexas (Nested JSON):** O campo de dicionários aninhados `applications` (compatibilidade de veículos) é mapeado, concatenado e transformado em um array literal plano serializado em string JSON para manter a integridade da informação ao ser exportado ou persistido.

### 3. Carga (Load) - `main.py`
* **Modelo Físico Relacional:** Modelagem e criação automática da tabela `dim_produtos` utilizando *SQLite3* pela portabilidade do ambiente local.
* **Garantia Física de Não Duplicidade:** Aplicação de uma constraint `UNIQUE` no campo chave do produto (`part_number`) direto no DDL da tabela.
* **Idempotência do Pipeline:** Ingestão massiva em lote (*Bulk Insert*) otimizada via dicionários com a instrução `INSERT OR IGNORE`. Caso o pipeline seja executado repetidas vezes, registros preexistentes são ignorados no nível do motor do banco, impedindo a poluição e duplicação da base.

### 4. Análise Exploratória (EDA) - `analitec_eda.py`
* **Camada de Inteligência:** Script desacoplado que consome a base purificada (`hubbi_etl.db`) usando Pandas e SQL.
* **Métricas Estratégicas Extradas:**
  * Ticket médio financeiro por categoria para precificação e classificação de produtos.
  * Identificação de gargalos de inventário (Top 5 fabricantes por volume físico em estoque).
  * Distribuição dos termos de garantia para controle de qualidade e auditoria de nulos (`NaN`).

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

### 1. Clonar e Inicializar o Ambiente
Abra o terminal no diretório do projeto e execute os comandos para criar o ambiente virtual e sincronizar as dependências através do `uv`:

```bash
# Inicializa o ambiente virtual (.venv) e instala as dependências do pyproject.toml
uv sync