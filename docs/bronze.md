# Documentação da Camada Bronze

## Camada Bronze: A Base Crucial para Rastreabilidade de Dados

A camada Bronze representa o primeiro estágio estruturado em nosso pipeline de dados, atuando como um repositório confiável para informações em seu estado original. Nesta fase, preservamos os dados brutos exatamente como foram recebidos da landing-zone, porém agora organizados em tabelas Delta.

## Conta de Armazenamento

- Conta: 

## Integração de Dados na Camada Bronze: Base para Processamento e Análise

A camada Bronze recebe e estrutura os dados em seu formato bruto, provenientes diretamente da landing-zone, garantindo sua preservação integral antes de qualquer transformação. Nesta etapa, são consolidados os seguintes conjuntos de dados essenciais:

Principais tabelas incorporadas:

- Cadastros básicos: cliente, autor, editora, funcionário

- Dados transacionais: pedido, item_pedido, pagamento

- Informações operacionais: estoque, livro

- Dados complementares: endereço

## Processo de Ingestão na Camada Bronze

O fluxo de ingestão segue três etapas principais:

- Leitura: Dados são extraídos da landing-zone em formato Parquet

- Enriquecimento: Adição de metadados essenciais:

    - dt_insert_bronze: timestamp da ingestão

    - filename: origem dos dados

- Armazenamento: Gravação na Bronze em formato Delta, garantindo rastreabilidade e versionamento.

## Código de Exemplo Pipeline Dados

O código em PySpark a seguir foi utilizado para ler os arquivos no formato CSV da "landing-zone" e carregá-los em dataframes.

```
df_autor   = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/Csvs/autor.csv")
df_cliente = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/Csvs/cliente.csv")
df_editora   = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/Csvs/editora.csv")
df_endereco = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/Csvs/endereco.csv")
df_estoque = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/Csvs/estoque.csv")
df_item_pedido = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/Csvs/item_pedido.csv")
df_livro = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/Csvs/livro.csv")
df_pagamento = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/Csvs/pagamento.csv")
df_pedido = spark.read.option("infeschema", "true").option("header", "true").csv(f"/mnt/{storageAccountName}/landing-zone/Csvs/pedido.csv")

```

### **Detalhes do Código:**

  * **`spark.read`**: Inicia a leitura de dados usando o Spark.
  * **`.option("infeschema", "true")`**: Essa opção instrui o Spark a inferir o esquema (tipos de dados) das colunas a partir dos próprios dados, o que é útil para evitar a definição manual de cada tipo de coluna.
  * **`.option("header", "true")`**: Indica que a primeira linha do arquivo CSV contém o cabeçalho, que será usado como nome das colunas no dataframe.
  * **`.csv(f"/mnt/{storageAccountName}/landing-zone/Csvs/...")`**: Especifica o formato do arquivo como CSV e o caminho para o arquivo de origem. O caminho utiliza o ponto de montagem configurado anteriormente para acessar os dados no Azure Data Lake Storage.