import sqlite3
from pddados import df

def realizar_ingestao(df_tratado):

    print("Iniciando conexão com SQLite...")

    # Conectando ao banco SQLite.
    conn = sqlite3.connect('hubbi_etl.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dim_produtos (
        id INTEGER PRIMARY KEY,
        name TEXT,
        part_number TEXT UNIQUE, 
        category TEXT,
        manufacturer_name TEXT,
        price REAL,
        gross_weight REAL,
        length REAL,
        width REAL,
        warranty TEXT,
        material TEXT,
        photo_url TEXT,
        stock_quantity INTEGER,
        applications TEXT
    )
    ''')

    # Colunas alvo para inserir no bd.
    colunas_alvo = [
        'id', 'name', 'part_number', 'category', 'manufacturer_name',
        'price', 'gross_weight', 'length', 'width', 'warranty',
        'material', 'photo_url', 'stock_quantity', 'applications'
    ]

    df_load = df_tratado[[col for col in colunas_alvo if col in df_tratado.columns]]

    registros = df_load.to_dict(orient='records')
    
    colunas_sql = ', '.join(df_load.columns)
    placeholders = ', '.join([':' + col for col in df_load.columns])

    # Placeholders para a query de inserção, usando o formato de dicionário do SQLite.
    query = f'''
        INSERT OR IGNORE INTO dim_produtos ({colunas_sql})
        VALUES ({placeholders})
    '''
    
    cursor.executemany(query, registros)
    conn.commit()
    print(f"Ingestão concluída. Linhas processadas: {len(registros)} | Novas linhas inseridas: {cursor.rowcount}")
    conn.rollback()
    conn.close()

# Trás os dados tratados do Pandas e realiza a ingestão no banco SQLite.
realizar_ingestao(df)