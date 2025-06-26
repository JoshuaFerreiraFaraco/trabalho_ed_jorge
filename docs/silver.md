# Documentação da Camada Silver

## Transformações na Camada Silver: Preparando Dados Estruturados para Análise

A camada Silver processa os dados brutos provenientes da Bronze, aplicando regras de qualidade, transformações e modelagem para estruturá-los de forma consistente. Essas otimizações garantem que os dados estejam prontos para consumo analítico na camada Gold, com esquemas definidos e relações estabelecidas.

## Preparação dos Dados de Cliente para Armazenamento em Silver

O código aplicado está transformando os dados brutos da camada Bronze e preparando-os para a camada Silver com as seguintes ações:

withColumn("data_hora_silver", current_timestamp())

- O que faz: adiciona uma nova coluna chamada data_hora_silver.

- Valor adicionado: o timestamp atual (data e hora exatos do processamento).

- Objetivo: registrar o momento em que a transformação foi feita. Isso ajuda no controle de versões e auditoria dos dados no pipeline.

withColumn("nome_arquivo", lit("cliente"))

- O que faz: adiciona uma coluna fixa chamada nome_arquivo.

- Valor: Ex: "cliente" (valor fixo usando lit, ou literal).

- Objetivo: identificar de qual conjunto de dados o registro veio, útil para rastreabilidade ou auditoria em pipelines com várias fontes e tabelas.

## Codigo: Fluxo de Dados Bronze → Silver

🔄 Leitura dos dados da camada Bronze:

```
df_autor   = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/autor")
df_cliente   = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/cliente")
df_editora   = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/editora")
df_endereco   = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/endereco")
df_estoque   = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/estoque")
df_item_pedido   = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/item_pedido")
df_livro  = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/livro")
df_pagamento  = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/pagamento")
df_pedido  = spark.read.format('delta').load(f"/mnt/{storageAccountName}/bronze/pedido")

```

🛠 Transformações aplicadas para a camada Silver:

```
from pyspark.sql.functions import current_timestamp, lit

df_autor   = df_autor.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("autor"))
df_cliente     = df_cliente.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("cliente"))
df_editora   = df_editora.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("editora"))
df_endereco  = df_endereco.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("endereco"))
df_estoque  = df_estoque.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("estoque"))
df_item_pedido  = df_item_pedido.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("item_pedido"))
df_livro  = df_livro.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("livro"))
df_pagamento  = df_pagamento.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("pagamento"))
df_pedido  = df_pedido.withColumn("data_hora_silver", current_timestamp()).withColumn("nome_arquivo", lit("pedido"))

```

## Tabela de conversão silver
