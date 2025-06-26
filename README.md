# Pipeline de Dados para Sistema de Vendas de Livros em Nuvem

[![Lint & Tests](https://img.shields.io/github/actions/workflow/status/jlsilva01/projeto-ed-satc/ci.yml?branch=main)](https://github.com/jlsilva01/projeto-ed-satc/actions)  
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen.svg)](https://github.com/jlsilva01/projeto-ed-satc)  
[![Docker Pulls](https://img.shields.io/docker/pulls/jlsilva01/projeto-ed-satc)](https://hub.docker.com/r/jlsilva01/projeto-ed-satc)  
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://jlsilva01.github.io/projeto-ed-satc/)  
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Projeto desenvolvido para a disciplina de Engenharia de Dados, focado na criação de uma pipeline em nuvem para um sistema de vendas de livros. Utilizou-se Terraform para provisionamento, Azure Databricks e Data Lake para o tratamento dos dados, e Power BI para visualização dos resultados.

## Pré-requisitos e ferramentas utilizadas

- **Linguagem:** Python 3.11+  
- **Dashboard:** streamlit e plotly
- **Orquestração local:** Docker Compose  
- **Documentação:** MkDocs

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/JoshuaFerreiraFaraco/trabalho_ed_jorge.git

```

### 2. Instalar dependências & pre-commit

```bash
uv venv
source .venv/bin/activate
uv sync

# instalar hooks do pre-commit
uv run pre-commit install
```

### 3. Executar localmente

```bash
uv run uvicorn app.main:app --reload
```

Acesse a API em `http://localhost:8000` e a documentação automática em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc:       `http://localhost:8000/redoc`

## Documentação (MkDocs)

Toda a documentação está em `docs/`:

```bash
uv run mkdocs build
uv run mkdocs serve
```

Acesse o site em `http://127.0.0.1:8000`.

Para publicar o site estático:

```bash
uv run mkdocs gh-deploy
```

## Autores

* **Daniela Miranda Fernandez Cardoso** - *Geração do CSV - Banco de Dados* - [(https://github.com/linkParaPerfil)](https://github.com/DaniMFCardoso)
* **Emely Pickler Fernandes** - *Geração do CSV - Banco de Dados* - [https://github.com/linkParaPerfil](https://github.com/emelypickler)
* **João Victor Macan Fontanella** - *Azure - Bronze,Silver e Gold* - [https://github.com/linkParaPerfil](https://github.com/JoaoFontanella)
* **Joshua Ferreira Faraco** - *Azure - Bronze,Silver e Gold* - [https://github.com/linkParaPerfil](https://github.com/JoshuaFerreiraFaraco)
* **Miguel Rossi Fermo** - *Dashboard* - [https://github.com/linkParaPerfil](https://github.com/miguelfermo)
* **Weslaine Santana dos Santos** - *Mkdocs - Modelo ER* - [https://github.com/linkParaPerfil](https://github.com/weslainesantana)

## Referências

Documentação do Faker:
  **Faker**
  
      Fonte: https://faker.readthedocs.io/

Documentação Oficial de Python:

   **random**: 
   
      Fonte: https://docs.python.org/3/library/random.html
      
   **datetime**: 
   
      Fonte: https://docs.python.org/3/library/datetime.html
   
   **streamlit**:
   
      Fonte: https://docs.streamlit.io/
      Repositório no GitHub: https://github.com/streamlit/streamlit

   **Plotly (Plotly.py)**
   
      Fonte: https://plotly.com/python/
      Repositório no GitHub: https://github.com/plotly/plotly.py
   
   **Pandas**
   
      Fonte: https://pandas.pydata.org/docs/
      Repositório no GitHub: https://github.com/pandas-dev/pandas
      
   **NumPy**
   
      Fonte: https://numpy.org/doc/2.3/
      Repositório no GitHub: https://github.com/numpy/numpy

# Nossa documentação abaixo: 

## Modelagem relacional:

![Untitled](https://github.com/user-attachments/assets/7a0fe861-16c8-43f6-9389-72191e8fe879)



