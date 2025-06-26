# Documentação da Camada Gold

## Camada Gold: Tabelas Finais para Análise de Vendas (Pedidos, Autores e Editoras)

As tabelas principais (criadas na camada Gold) são:

tb_relatorio_final: Um relatório de vendas detalhado que consolida informações dos pedidos com dados dos clientes e seus respectivos endereços.
tb_relatorio_autor: Um relatório agregado que calcula o total de vendas por autor.
tb_relatorio_editora: Um relatório agregado que calcula o total de vendas por editora.

Essas tabelas são salvas no formato Delta e são o resultado final do processo de ETL, prontas para consumo e análise.

## Processamento de Dados: Carregando Informações do Delta Lake (Silver) em DataFrames PySpark

Leitura de Dados do Delta Lake na Camada Silver para DataFrames PySpark

```
df_relatorio_vendas = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/vw_relatorio_vendas")
df_cliente_silver = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/cliente")
df_endereco_silver = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/endereco")

```
Neste bloco:

- spark.read.format('delta'): Especifica que os dados a serem lidos estão no formato Delta.
- .load(f"/mnt/{storageAccountName}/silver/..."): Aponta para o caminho exato no armazenamento (camada Silver) de onde os dados de cada tabela (vw_relatorio_vendas, cliente, endereco) devem ser carregados.
- df_... =: O resultado da leitura é atribuído a um novo dataframe no Spark para manipulação posterior.

## Escrita dos Dados

Salvando o Relatório Final de Vendas
Este código grava o DataFrame df_relatorio_final em um diretório no Data Lake e também o registra como uma tabela gerenciada chamada gold.tb_relatorio_final.,

    ```
    df_relatorio_final.write.format('delta').mode("overwrite").save(f"/mnt/{storageAccountName}/gold/tb_relatorio_final")
    df_relatorio_final.write.format("delta").mode("overwrite").saveAsTable("gold.tb_relatorio_final")
    ```

Salvando o Relatório de Vendas por Autor
Da mesma forma, o DataFrame df_relatorio_autor é salvo no formato Delta e como uma tabela gerenciada de nome gold.tb_relatorio_autor.,

    ```
    df_relatorio_autor.write.format('delta').mode("overwrite").save(f"/mnt/{storageAccountName}/gold/tb_relatorio_autor")
    df_relatorio_autor.write.format("delta").mode("overwrite").saveAsTable("gold.tb_relatorio_autor")
    ```

Salvando o Relatório de Vendas por Editora
Por fim, o DataFrame df_relatorio_editora é persistido como uma tabela Delta chamada gold.tb_relatorio_editora.,

    ```
    df_relatorio_editora.write.format('delta').mode("overwrite").save(f"/mnt/{storageAccountName}/gold/tb_relatorio_editora")
    df_relatorio_editora.write.format("delta").mode("overwrite").saveAsTable("gold.tb_relatorio_editora")
    ```

Em todos os casos, o método .mode("overwrite") garante que, se a tabela ou os dados já existirem, eles serão substituídos pela nova versão do DataFrame, mantendo os dados sempre atualizados.

## Criação da Tabela OBT (Operational Business Table)

A tabela tb_relatorio_final é uma OBT (Operational Business Table) ou "One Big Table".

O processo de criação dessa tabela:

Leitura dos Dados da Camada Silver: Inicialmente, são lidas três tabelas distintas da camada Silver: um relatório de vendas, a tabela de clientes e a de endereços.

    ```
    df_relatorio_vendas = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/vw_relatorio_vendas")
    df_cliente_silver = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/cliente")
    df_endereco_silver = spark.read.format('delta').load(f"/mnt/{storageAccountName}/silver/endereco")
    ```

Criação de Visões Temporárias: As tabelas lidas são registradas como visões temporárias para que possam ser utilizadas em consultas SQL.

    ```
    df_relatorio_vendas.createOrReplaceTempView("vw_relatorio_vendas")
    df_cliente_silver.createOrReplaceTempView("vw_cliente")
    df_endereco_silver.createOrReplaceTempView("vw_endereco")
    ```

Junção e Denormalização (Criação da OBT): Uma consulta SQL é executada para juntar (denormalizar) as três visões em uma única tabela. Essa consulta combina os dados de vendas com os detalhes dos clientes e seus respectivos endereços, selecionando as colunas mais relevantes para a análise de negócio.

    ```
    SELECT
        v.cod_pedido,
        v.data_pedido,
        c.nome,
        c.email,
        c.telefone,
        e.cidade,
        e.estado,
        e.pais,
        v.total_pedido
    FROM vw_relatorio_vendas v
    INNER JOIN vw_cliente c ON v.cod_cliente = c.cod_cliente
    INNER JOIN vw_endereco e on v.cod_endereco = e.cod_endereco
    ```
    
Armazenamento na Camada Gold: O DataFrame resultante dessa junção, chamado df_relatorio_final, é então salvo permanentemente na camada Gold como a tabela gold.tb_relatorio_final. Isso disponibiliza uma tabela larga e pré-agregada, pronta para ser consumida por ferramentas de BI e análise sem a necessidade de realizar joins complexos novamente.

## Inserção de Dados na Tabela OBT

A inserção de dados na OBT (Operational Business Table), que no caso é a tb_relatorio_final, é realizada após a conclusão das operações de junção que criam o DataFrame final.

O trecho de código do notebook Gold.ipynb que executa essa inserção é:

```
df_relatorio_final.write.format('delta').mode("overwrite").save(f"/mnt/{storageAccountName}/gold/tb_relatorio_final")
df_relatorio_final.write.format("delta").mode("overwrite").saveAsTable("gold.tb_relatorio_final")
```


Análise do Código:

```
df_relatorio_final.write: Inicia o processo de escrita (inserção) dos dados contidos no DataFrame df_relatorio_final.
.format('delta'): Define que os dados serão salvos no formato Delta Lake.
.mode("overwrite"): Especifica o modo de inserção. "Overwrite" significa que, se a tabela ou os dados no local de destino já existirem, eles serão completamente substituídos pelos novos dados. Isso garante que a tabela seja totalmente atualizada a cada execução do processo.
.save(...): Salva o conteúdo do DataFrame como arquivos no formato Delta no caminho especificado dentro do Azure Data Lake Storage.
.saveAsTable("gold.tb_relatorio_final"): Além de salvar os arquivos, este comando registra o DataFrame como uma tabela gerenciada no metastore do Spark, com o nome tb_relatorio_final dentro do banco de dados gold. Isso facilita o acesso à tabela através de consultas SQL em outras ferramentas e notebooks.
```

## Validação de Dados: Exibição das Tabelas Gold para Verificação dos Relatórios Finais

A exibição dos dados para verificação é realizada em várias etapas, mas principalmente ao final do processo, para confirmar que as tabelas na camada Gold foram criadas corretamente.

A exibição dos dados das tabelas finais é feita através de consultas SQL dentro do comando display().

Exibição das Tabelas Finais (Camada Gold)

- Relatório Final de Vendas: O conteúdo da tabela principal tb_relatorio_final, que funciona como uma OBT (Operational Business Table), é exibido com o seguinte comando:

```
display(spark.sql("select * from gold.tb_relatorio_final"))
```

- Relatório de Vendas por Autor: Para visualizar os dados agregados de vendas por autor, utiliza-se o comando:

```
display(spark.sql("select * from gold.tb_relatorio_autor"))
```

- Relatório de Vendas por Editora: A exibição do relatório de vendas por editora é feita executando a consulta:

```
display(spark.sql("select * from gold.tb_relatorio_editora"))
```