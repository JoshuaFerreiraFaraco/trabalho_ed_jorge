# Pipeline de Dados para Sistema de Vendas de Livros em Nuvem

[![Lint & Tests](https://img.shields.io/github/actions/workflow/status/jlsilva01/projeto-ed-satc/ci.yml?branch=main)](https://github.com/jlsilva01/projeto-ed-satc/actions)  
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen.svg)](https://github.com/jlsilva01/projeto-ed-satc)  
[![Docker Pulls](https://img.shields.io/docker/pulls/jlsilva01/projeto-ed-satc)](https://hub.docker.com/r/jlsilva01/projeto-ed-satc)  
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://jlsilva01.github.io/projeto-ed-satc/)  
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Projeto desenvolvido para a disciplina de Engenharia de Dados, focado na criação de uma pipeline em nuvem para um sistema de vendas de livros. Utilizou-se Terraform para provisionamento, Azure Databricks e Data Lake para o tratamento dos dados, e Power BI para visualização dos resultados.

## Desenho de Arquitetura

Coloque uma imagem do seu projeto, como no exemplo abaixo:

![image](https://github.com/jlsilva01/projeto-ed-satc/assets/484662/541de6ab-03fa-49b3-a29f-dec8857360c1)

## Pré-requisitos e ferramentas utilizadas

- **Linguagem:** Python 3.11+  
- **Framework web:** FastAPI  
- **Servidor ASGI:** Uvicorn  
- **Qualidade de código:** pre-commit (ruff, black, isort, flake8, mypy)  
- **Container:** Docker  
- **Orquestração local:** Docker Compose  
- **Documentação:** MkDocs + mkdocstrings + mkdocs-material

```
Dar exemplos
```

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

## Colaboração

1. Abra uma **issue** para discutir sua feature ou bug.  
2. Crie um **branch**:  

   ```bash
   git checkout -b feature/nome-da-sua-feature
   ```
3. Faça suas alterações e **commit** seguindo o [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).  
4. Envie um **pull request** para `main`.  
5. Aguarde revisão e merge.

## Versão

Fale sobre a versão e o controle de versões para o projeto. 

## Autores

Mencione todos aqueles que ajudaram a levantar o projeto desde o seu início

* **Aluno 1** - *Trabalho Inicial* - [(https://github.com/linkParaPerfil)](https://github.com/linkParaPerfil)
* **Aluno 2** - *Documentação* - [https://github.com/linkParaPerfil](https://github.com/linkParaPerfil)

## Referências

Cite aqui todas as referências utilizadas neste projeto, pode ser outros repositórios, livros, artigos de internet etc.


# Nossa documentação abaixo: 

## Modelagem relacional:

![Untitled](https://github.com/user-attachments/assets/7a0fe861-16c8-43f6-9389-72191e8fe879)





