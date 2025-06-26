import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import ResourceExistsError
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

def elt_sql_sqlserver_to_adls():
    print("🔄 Iniciando processo ELT...")

    # Carregar variáveis de ambiente do arquivo .env
    load_dotenv()
    print("✅ Variáveis de ambiente carregadas.")

    # Configurações do Azure Data Lake Storage
    account_name = os.getenv("ADLS_ACCOUNT_NAME")
    file_system_name = os.getenv("ADLS_FILE_SYSTEM_NAME")
    directory_name = os.getenv("ADLS_DIRECTORY_NAME")
    sas_token = os.getenv("ADLS_SAS_TOKEN")

    print(f"📦 ADLS Config -> account: {account_name}, filesystem: {file_system_name}, directory: {directory_name}")

    # Configurações do SQL Server
    server = os.getenv("SQL_SERVER")
    database = os.getenv("SQL_DATABASE")
    schema = os.getenv("SQL_SCHEMA")
    username = os.getenv("SQL_USERNAME")
    password = os.getenv("SQL_PASSWORD")

    print(f"🗄️ SQL Server Config -> server: {server}, database: {database}, schema: {schema}, user: {username}")

    # Proteger senha na URL
    password = quote_plus(password)

    # Conectar ao SQL Server
    conn_str = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    print("🔌 String de conexão criada com sucesso.")

    try:
        # Criar a engine do SQLAlchemy
        engine = create_engine(conn_str)
        print("✅ Conexão com SQL Server estabelecida.")
    except Exception as e:
        print("❌ Erro ao conectar no SQL Server:", e)
        return

    # Consulta SQL para obter todas as tabelas do esquema
    query = f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = '{schema}'"
    print("📄 Executando consulta de tabelas:", query)

    try:
        tables_df = pd.read_sql(query, engine)
        print("📥 Tabelas encontradas:\n", tables_df)
    except Exception as e:
        print("❌ Erro ao buscar as tabelas:", e)
        return

    # Criar cliente do Azure Data Lake Storage
    try:
        file_system_client = DataLakeServiceClient(
            account_url=f"https://{account_name}.dfs.core.windows.net",
            credential=sas_token,
            api_version="2020-02-10"
        )
        print("✅ Conexão com Azure Data Lake estabelecida.")
    except Exception as e:
        print("❌ Erro ao conectar no ADLS:", e)
        return

    # Criar diretório, se necessário
    try:
        directory_client = file_system_client.get_file_system_client(file_system_name).get_directory_client(directory_name)
        directory_client.create_directory()
        print(f"📁 Diretório '{directory_name}' criado com sucesso.")
    except ResourceExistsError:
        print(f"ℹ️ Diretório '{directory_name}' já existe.")
    except Exception as e:
        print("❌ Erro ao criar diretório no ADLS:", e)
        return

    # Loop nas tabelas
    for index, row in tables_df.iterrows():
        table_name = row["table_name"]
        full_table_name = f"{schema}.{table_name}"
        print(f"\n🔍 Processando tabela: {full_table_name}")

        try:
            query = f"SELECT * FROM {full_table_name}"
            print(f"📄 Executando query: {query}")
            df = pd.read_sql(query, conn_str)
            print(f"📊 Linhas extraídas da tabela '{table_name}': {len(df)}")
        except Exception as e:
            print(f"❌ Erro ao extrair dados da tabela '{full_table_name}':", e)
            continue

        # Salvar no ADLS
        try:
            file_client = directory_client.get_file_client(f"{table_name}.csv")
            data = df.to_csv(index=False).encode()
            file_client.upload_data(data, overwrite=True)
            print(f"✅ Dados da tabela '{table_name}' enviados ao ADLS com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao enviar '{table_name}.csv' para o ADLS:", e)

# Executar a função
if __name__ == "__main__":
    elt_sql_sqlserver_to_adls()