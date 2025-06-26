---
hide:
  - navigation
---

# Sobre o Projeto

## 👨‍💻 Integrantes

<div class="grid cards" markdown>

- :fontawesome-solid-user: **Aluno 1** – Weslaine Santana
- :fontawesome-solid-user: **Aluno 2** – Joshua Ferreira Faraco
- :fontawesome-solid-user: **Aluno 3** –  João Victor Macan Fontanella
- :fontawesome-solid-user: **Aluno 4** –  Miguel Rossi Fermo
- :fontawesome-solid-user: **Aluno 5** – Emely Pickler Fernandes
- :fontawesome-solid-user: **Aluno 6** – Daniela Miranda Fernandez Cardoso

</div>

## 📈 Premissas Técnicas

!!! info "Componentes obrigatórios do projeto"

- Dados com no mínimo **10 tabelas** e **20.000 registros por tabela principal**.
- Distribuição temporal para os **últimos 3 anos**.
- **Geração de dados** pode ser feita com `faker` ou bibliotecas similares.
- Armazenamento em **object storage** com arquitetura em camadas:  
  `Landing → Bronze → Silver → Gold`.
- Transformações realizadas com **Apache Spark** (preferencialmente PySpark).
- Dados na camada Gold em modelo **dimensional ou OBT**.
- Construção de um **dashboard (One Page View)** com:
  - 4 KPIs
  - 2 Métricas
- Ferramenta de orquestração como **Apache Airflow**, **Prefect** etc.
- Documentação completa em **MkDocs** com **repositório GitHub versionado** via Pull Requests.

## 🛠️ Ferramentas recomendadas

- **Apache Spark**
- **Delta Lake / Apache Iceberg**
- **Python + PySpark**
- **Docker (local)** ou **Cloud (Azure, GCP, AWS)**
- **Ferramentas de visualização:** Power BI, Metabase, Superset, etc.
- **Diagramação:** [Excalidraw](https://excalidraw.com), [Miro](https://miro.com/pt/), [Draw.io](https://app.diagrams.net/)

## 💡 Observações

!!! note ""
    A entrega final deverá conter:
    
    - Link para repositório GitHub com branch protegida.
    - Documentação completa no MkDocs publicada via GitHub Pages.
    - Dashboard funcional conectado à camada Gold do pipeline.
    - Apresentação oral (20 minutos) com jornada de dados demonstrada na prática.
