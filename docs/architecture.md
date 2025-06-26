# Arquitetura de Solução

## Origem

## Processo de Ingestão de Dados no Azure Databricks

A ingestão dos dados é realizada dentro do Azure Databricks, utilizando um Jupyter Notebook que faz a extração, transformação e carga (ETL) dos dados brutos. Após o processamento, os dados são convertidos para o formato Parquet e armazenados no container landing-zone, garantindo eficiência e compatibilidade com o ambiente de big data.

Para detalhes técnicos sobre a implementação do script de ingestão, consulte o link disponível aqui (insira o link correspondente).

## Orquestração e Processamento em Delta Lake com Azure Databricks

No Azure Databricks, o processamento e a orquestração das tarefas são gerenciados de forma sequencial, garantindo que cada etapa só seja executada após o sucesso da anterior. Os dados são inicialmente armazenados no container landing-zone e, em seguida, processados e salvos nos demais containers no formato Delta Lake. Essa abordagem transforma o ADLS em um Delta Lake, assegurando as propriedades ACID (atomicidade, consistência, isolamento e durabilidade) em todas as operações realizadas.


## Armazenamento e Processamento de Dados em Camadas no Azure 

Os dados são armazenados em um Blob Storage, que serve como repositório central para informações em diferentes estágios: desde a coleta inicial até os dados processados e prontos para análise. A estrutura segue o modelo de arquitetura em camadas "medalhão", organizada em quatro níveis principais:

- Landing-Zone – Camada de ingestão, onde os dados brutos são armazenados no formato Parquet, mantendo sua forma original após a extração de fontes relacionais.

- Camada Bronze – Recebe os dados da landing-zone e os converte em Delta Tables, preservando o histórico de extrações e metadados para rastreabilidade.

- Camada Silver – Realiza transformações mais avançadas, como desnormalizações e consolidação de informações, mantendo a estrutura em Delta com auditoria de origem e versões.

- Camada Gold – Consolida os dados tratados em uma estrutura otimizada para análise, seguindo o modelo OBT (One Big Table) no formato Delta, com métricas e KPIs prontos para consumo em ferramentas de BI e relatórios.

## Dashboard Analítico com Streamlit: Métricas e KPIs para Tomada de Decisão

A análise dos dados foi realizada por meio de um dashboard interativo, desenvolvido com o Streamlit, que consolida as principais métricas e KPIs extraídos da camada Gold (OBT - One Big Table).