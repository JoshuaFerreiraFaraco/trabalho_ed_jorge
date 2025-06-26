# 📚 Dashboard - Sistema de Vendas de Livros

Este dashboard representa a camada final do pipeline de dados do sistema de vendas de livros. Ele simula o Business Intelligence (BI) que seria alimentado pelos dados processados nas camadas Bronze, Silver e Gold do Azure Databricks.

## 🎯 Objetivo

Criar uma visualização completa e interativa dos dados de vendas de livros, simulando o resultado final do pipeline de engenharia de dados.

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework para criação do dashboard web
- **Plotly**: Biblioteca para gráficos interativos
- **Pandas**: Manipulação e análise de dados
- **Faker**: Geração de dados mockados realistas
- **NumPy**: Computação numérica

## 📊 Funcionalidades

### KPIs Principais
- Total de vendas
- Receita total
- Ticket médio
- Total de clientes

### Análises Disponíveis
- **Vendas Temporais**: Evolução das vendas e receita ao longo do tempo
- **Análise de Produtos**: Top livros mais vendidos e distribuição por gênero
- **Análise Regional**: Performance por estado e ticket médio regional
- **Controle de Estoque**: Monitoramento de estoque com alertas automáticos

### Filtros Interativos
- Período de análise (30 dias, 90 dias, anual)
- Seleção de gêneros literários
- Dados em tempo real

## 🚀 Como Executar

1. Certifique-se que o ambiente Poetry está ativo:
```bash
poetry shell
```

2. Execute o dashboard:
```bash
poetry run streamlit run dashboards/app.py
```

3. Acesse no navegador: `http://localhost:8501`

## 📈 Dados Simulados

O dashboard utiliza dados mockados que simulam:

- **25.000+ clientes** distribuídos por 10 estados
- **30.000+ livros** em 8 gêneros diferentes
- **2 anos de histórico** de vendas (2023-2024)
- **Sazonalidade realista** (picos em dezembro e julho)
- **Controle de estoque** com alertas automáticos

## 🏗️ Arquitetura do Pipeline

```
Landing Zone → Bronze → Silver → Gold → Dashboard (Streamlit)
     ↓           ↓        ↓       ↓           ↓
   CSV Raw    Delta    Cleaned  Aggregated  Visualized
   Files      Lake     Data     Data        Data
```

## 📋 Métricas Monitoradas

### Vendas
- Volume de vendas por período
- Receita total e ticket médio
- Tendências sazonais
- Performance por região

### Produtos
- Livros mais vendidos
- Distribuição por gênero
- Análise de receita por categoria

### Operações
- Níveis de estoque
- Alertas de reposição
- Status operacional

## 🎨 Interface

O dashboard possui:
- **Layout responsivo** adaptável a diferentes telas
- **Tema moderno** com cores corporativas
- **Interatividade completa** com filtros dinâmicos
- **Visualizações profissionais** usando Plotly
- **KPIs destacados** com métricas de comparação

## 📝 Estrutura dos Dados

### Vendas Diárias
- Data, quantidade, valor total
- Segmentação mensal e anual
- Métricas calculadas

### Catálogo de Livros
- Título, gênero, preço
- Vendas acumuladas
- Receita por produto

### Dados Regionais
- Estados, clientes por região
- Ticket médio regional
- Performance por localização

### Controle de Estoque
- Estoque atual vs mínimo
- Status de criticidade
- Alertas automáticos

## 🔄 Integração com Pipeline

Este dashboard representa o destino final dos dados processados pelo pipeline de engenharia de dados:

1. **Landing Zone**: Dados brutos em CSV
2. **Bronze**: Dados ingeridos no Delta Lake
3. **Silver**: Dados limpos e transformados
4. **Gold**: Dados agregados e prontos para BI
5. **Dashboard**: Visualização final dos insights

## 📊 Próximos Passos

Quando os dados reais estiverem disponíveis:

1. Substituir `generate_mock_data()` por conexões reais
2. Conectar com Azure Databricks Gold tables
3. Implementar refresh automático
4. Adicionar mais métricas específicas do negócio
5. Configurar alertas em tempo real
