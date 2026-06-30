import pandas as pd
import json
from scrandados import extrair_dados


dados = extrair_dados()
df = pd.DataFrame(dados['data'])

# Extrai os dados úteis do dicionário os aninhando e converte para uma string de array JSON.
def formatar_aplicacoes(aplicacoes):
    if not isinstance(aplicacoes, list) or len(aplicacoes) == 0:
        return "[]"
    
    # Extrai marca, modelo e anos, já convertendo para maiúsculo
    lista_formatada = [f"{app.get('make', '')} {app.get('model', '')} {app.get('years', '')}".strip().upper() for app in aplicacoes]
    return json.dumps(lista_formatada, ensure_ascii=False)

df['applications'] = df['applications'].apply(formatar_aplicacoes)

# Padronização de texto para maiúsculas em todas as colunas de texto, exceto 'applications' que já foi tratada.
colunas_texto = df.select_dtypes(include=['object']).columns

for col in colunas_texto:
    if col != 'applications': # Ignora a coluna 'applications'.
        df[col] = df[col].apply(lambda x: str(x).upper() if pd.notnull(x) else x)

# Tipagem de colunas numéricas para float.
colunas_float = ['price', 'gross_weight', 'length', 'width']

for col in colunas_float:
    df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)

print("\nAMOSTRA DOS DADOS TRATADOS:")
print(df[['name', 'price', 'applications']].head(2))