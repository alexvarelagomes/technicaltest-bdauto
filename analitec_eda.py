# analise_dados.py
import sqlite3
import pandas as pd

def executar_analise():
    conn = sqlite3.connect('hubbi_etl.db')

    # Queries de insight
    queries = {
        "TICKET MÉDIO POR CATEGORIA": 
            "SELECT category, ROUND(AVG(price), 2) as preco_medio FROM dim_produtos GROUP BY category",
        
        "TOP 5 FABRICANTES (ESTOQUE)": 
            "SELECT manufacturer_name, SUM(stock_quantity) as total_estoque FROM dim_produtos GROUP BY manufacturer_name ORDER BY total_estoque DESC LIMIT 5",
        
        "DISTRIBUIÇÃO DE GARANTIA": 
            "SELECT warranty, COUNT(*) as qtd FROM dim_produtos GROUP BY warranty ORDER BY qtd DESC"
    }

    for titulo, sql in queries.items():
        print(f"\n{titulo}")
        print(pd.read_sql(sql, conn))

    conn.close()

if __name__ == "__main__":
    executar_analise()