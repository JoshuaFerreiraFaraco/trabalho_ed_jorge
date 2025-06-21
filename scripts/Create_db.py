import pandas as pd
import pyodbc

# Conexão com o banco de dados no Docker
try:
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=127.0.0.1;"
        "DATABASE=projeto_ed;"
        "UID=sa;"
        "PWD=satc@2025"
    )
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()
    print("Conexão com o banco de dados estabelecida com sucesso.")
except Exception as e:
    print("Erro ao conectar no banco de dados:", e)
    exit(1)

# Dicionário com nomes dos arquivos e DDLs atualizadas
csv_tables = {
    "autor": """
        CREATE TABLE autor (
            id_autor INT PRIMARY KEY,
            nome VARCHAR(100),
            nacionalidade VARCHAR(100)
        )
    """,
    "cliente": """
        CREATE TABLE cliente (
            id_cliente INT PRIMARY KEY,
            nome VARCHAR(100),
            email VARCHAR(100),
            telefone VARCHAR(20)
        )
    """,
    "editora": """
        CREATE TABLE editora (
            id_editora INT PRIMARY KEY,
            nome VARCHAR(100),
            contato VARCHAR(100)
        )
    """,
    "endereco": """
        CREATE TABLE endereco (
            id_endereco INT PRIMARY KEY,
            id_cliente INT,
            rua VARCHAR(100),
            numero VARCHAR(10),
            cidade VARCHAR(100),
            estado VARCHAR(50),
            cep VARCHAR(20)
        )
    """,
    "estoque": """
        CREATE TABLE estoque (
            id_estoque INT PRIMARY KEY,
            id_livro INT,
            quantidade INT
        )
    """,
    "funcionario": """
        CREATE TABLE funcionario (
            id_funcionario INT PRIMARY KEY,
            nome VARCHAR(100),
            cargo VARCHAR(50),
            email VARCHAR(100)
        )
    """,
    "item_pedido": """
        CREATE TABLE item_pedido (
            id_item INT PRIMARY KEY,
            id_pedido INT,
            id_livro INT,
            quantidade INT,
            preco_unitario DECIMAL(10,2)
        )
    """,
    "livro": """
        CREATE TABLE livro (
            id_livro INT PRIMARY KEY,
            titulo VARCHAR(150),
            id_autor INT,
            id_editora INT,
            ano_publicacao INT
        )
    """,
    "pagamento": """
        CREATE TABLE pagamento (
            id_pagamento INT PRIMARY KEY,
            id_pedido INT,
            forma_pagamento VARCHAR(50),
            valor_total DECIMAL(10,2),
            data DATE
        )
    """,
    "pedido": """
        CREATE TABLE pedido (
            id_pedido INT PRIMARY KEY,
            id_cliente INT,
            data DATE,
            status VARCHAR(50)
        )
    """
}

# Criar tabelas
for nome_tabela, ddl in csv_tables.items():
    try:
        print(f"\nCriando tabela {nome_tabela}...")
        cursor.execute(f"IF OBJECT_ID('{nome_tabela}', 'U') IS NOT NULL DROP TABLE {nome_tabela}")
        cursor.execute(ddl)
        print(f"Tabela {nome_tabela} criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar tabela {nome_tabela}:", e)

# Inserir dados dos CSVs
for nome_tabela in csv_tables:
    try:
        print(f"\nLendo arquivo {nome_tabela}.csv...")
        df = pd.read_csv(f"./banco_eng_dados/{nome_tabela}.csv")
        print(f"Inserindo dados em {nome_tabela}...")

        cols = ", ".join(df.columns)
        placeholders = ", ".join(["?"] * len(df.columns))

        # Converte tipos numpy para tipos Python nativos
        data = [tuple(map(lambda x: x.item() if hasattr(x, 'item') else x, row)) for row in df.to_numpy()]

        cursor.fast_executemany = True
        cursor.executemany(f"INSERT INTO {nome_tabela} ({cols}) VALUES ({placeholders})", data)

        print(f"Dados inseridos com sucesso em {nome_tabela}.")
    except FileNotFoundError:
        print(f"Arquivo {nome_tabela}.csv não encontrado.")
    except Exception as e:
        print(f"Erro geral ao inserir dados em {nome_tabela}:", e)

# Adicionar foreign keys
fks = [
    "ALTER TABLE endereco ADD CONSTRAINT fk_endereco_cliente FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)",
    "ALTER TABLE livro ADD CONSTRAINT fk_livro_autor FOREIGN KEY (id_autor) REFERENCES autor(id_autor)",
    "ALTER TABLE livro ADD CONSTRAINT fk_livro_editora FOREIGN KEY (id_editora) REFERENCES editora(id_editora)",
    "ALTER TABLE pedido ADD CONSTRAINT fk_pedido_cliente FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)",
    "ALTER TABLE item_pedido ADD CONSTRAINT fk_item_pedido_pedido FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)",
    "ALTER TABLE item_pedido ADD CONSTRAINT fk_item_pedido_livro FOREIGN KEY (id_livro) REFERENCES livro(id_livro)",
    "ALTER TABLE estoque ADD CONSTRAINT fk_estoque_livro FOREIGN KEY (id_livro) REFERENCES livro(id_livro)",
    "ALTER TABLE pagamento ADD CONSTRAINT fk_pagamento_pedido FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)"
]

print("\nAdicionando FKs...")
for fk in fks:
    try:
        cursor.execute(fk)
        print(f"Executado: {fk}")
    except Exception as e:
        print(f"Erro ao adicionar FK: {fk} -> {e}")

print("\nFinalizado com sucesso.")
conn.close()