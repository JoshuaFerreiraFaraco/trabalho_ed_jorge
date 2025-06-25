"""
Módulo para geração de dados mockados baseados na estrutura real do banco de dados
do sistema de vendas de livros.

Estrutura das tabelas reais:
- cliente: id_cliente, nome, email, telefone
- autor: id_autor, nome, nacionalidade  
- editora: id_editora, nome, contato
- livro: id_livro, titulo, id_autor, id_editora, ano_publicacao
- endereco: id_endereco, id_cliente, rua, numero, cidade, estado, cep
- pedido: id_pedido, id_cliente, data, status
- item_pedido: id_item, id_pedido, id_livro, quantidade, preco_unitario
- pagamento: id_pagamento, id_pedido, forma_pagamento, valor_total, data
- estoque: id_estoque, id_livro, quantidade
- funcionario: id_funcionario, nome, cargo, email
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configurar seeds para reprodutibilidade
random.seed(42)
np.random.seed(42)

def get_vendas_temporais():
    """
    Gera dados temporais de vendas baseados nos pedidos
    """
    # Período de análise: últimos 12 meses
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    vendas_diarias = []
    
    for date in dates:
        # Simular sazonalidade
        base_pedidos = random.randint(15, 45)
        
        # Fins de semana têm mais vendas
        if date.weekday() >= 5:
            base_pedidos = int(base_pedidos * 1.3)
            
        # Calcular métricas
        itens_por_pedido = random.uniform(1.2, 3.0)
        preco_medio = random.uniform(50, 150)
        
        total_itens = int(base_pedidos * itens_por_pedido)
        receita_dia = base_pedidos * itens_por_pedido * preco_medio
        
        vendas_diarias.append({
            'data': date,
            'pedidos': base_pedidos,
            'itens_vendidos': total_itens,
            'receita': receita_dia,
            'mes': date.strftime('%Y-%m')
        })
    
    return pd.DataFrame(vendas_diarias)

def get_produtos_performance():
    """
    Gera dados de livros baseados na estrutura real
    """
    generos = ['Romance', 'Ficção', 'Biografia', 'Autoajuda', 'História', 'Técnico', 'Infantil']
    editoras = ['Companhia das Letras', 'Record', 'Globo', 'Intrínseca', 'Suma', 'Rocco']
    
    livros_data = []
    
    for i in range(100):
        genero = random.choice(generos)
        editora = random.choice(editoras)
        
        # Gerar dados do livro
        titulo = f"Livro {i+1}"
        autor = f"Autor {random.randint(1, 50)}"
        ano = random.randint(2015, 2024)
        preco = round(random.uniform(25, 200), 2)
        vendas = random.randint(50, 1000)
        
        livros_data.append({
            'id_livro': i + 1,
            'titulo': titulo,
            'autor': autor,
            'editora': editora,
            'genero': genero,
            'ano_publicacao': ano,
            'preco': preco,
            'vendas_total': vendas,
            'receita_total': vendas * preco,
            'avaliacoes': round(random.uniform(3.0, 5.0), 1)
        })
    
    return pd.DataFrame(livros_data)

def get_dados_operacionais():
    """
    Gera dados operacionais baseados na estrutura real
    """
    # Status de pedidos
    status_pedidos = ['Confirmado', 'Processando', 'Enviado', 'Entregue', 'Cancelado']
    pedidos_status = []
    
    for status in status_pedidos:
        if status == 'Entregue':
            quantidade = random.randint(800, 1200)
        elif status == 'Cancelado':
            quantidade = random.randint(50, 150)
        else:
            quantidade = random.randint(100, 400)
            
        pedidos_status.append({
            'status': status,
            'quantidade': quantidade
        })
    
    # Formas de pagamento
    formas_pagamento = ['Pix', 'Cartão', 'Boleto']
    pagamentos_data = []
    
    for forma in formas_pagamento:
        if forma == 'Pix':
            transacoes = random.randint(400, 600)
        elif forma == 'Cartão':
            transacoes = random.randint(300, 500)
        else:
            transacoes = random.randint(100, 200)
            
        pagamentos_data.append({
            'forma_pagamento': forma,
            'total_transacoes': transacoes,
            'receita_total': transacoes * random.uniform(80, 150)
        })
    
    # Controle de estoque
    status_estoque = ['Sem Estoque', 'Estoque Baixo', 'Estoque Normal', 'Estoque Alto']
    estoque_data = []
    
    for status in status_estoque:
        if status == 'Sem Estoque':
            quantidade = random.randint(5, 15)
        elif status == 'Estoque Baixo':
            quantidade = random.randint(10, 25)
        elif status == 'Estoque Normal':
            quantidade = random.randint(30, 50)
        else:
            quantidade = random.randint(15, 30)
            
        estoque_data.append({
            'status': status,
            'quantidade': quantidade
        })
    
    return {
        'pedidos_status': pd.DataFrame(pedidos_status),
        'pagamentos': pd.DataFrame(pagamentos_data),
        'estoque': pd.DataFrame(estoque_data)
    }

def get_kpis_principais():
    """
    Calcula KPIs principais baseados nos dados mockados
    """
    return {
        'total_clientes': random.randint(15000, 25000),
        'total_editoras': random.randint(15, 25),
        'total_autores': random.randint(200, 400),
        'total_livros': random.randint(800, 1500),
        'crescimento_vendas': round(random.uniform(5, 25), 1),
        'satisfacao_cliente': round(random.uniform(85, 95), 1)
    }

def get_all_data():
    """
    Retorna todos os datasets mockados
    """
    vendas = get_vendas_temporais()
    produtos = get_produtos_performance()
    operacionais = get_dados_operacionais()
    kpis = get_kpis_principais()
    
    return {
        'vendas_temporais': vendas,
        'produtos': produtos,
        'pedidos_status': operacionais['pedidos_status'],
        'pagamentos': operacionais['pagamentos'],
        'estoque': operacionais['estoque'],
        'kpis': kpis
    }
            base_pedidos = 45
        # Dia das Mães/Pais (maio/agosto)
        elif date.month in [5, 8]:
            base_pedidos = 40
        # Finais de semana
        if date.weekday() >= 5:  # Sábado/Domingo
            base_pedidos = int(base_pedidos * 1.3)
            
        # Adicionar variação aleatória
        num_pedidos = max(5, int(np.random.normal(base_pedidos, 8)))
        
        # Calcular métricas por dia
        itens_por_pedido = np.random.uniform(1.2, 3.5)  # Média de itens por pedido
        preco_medio_item = np.random.uniform(45, 120)   # Preço médio por item
        
        total_itens = int(num_pedidos * itens_por_pedido)
        receita_dia = num_pedidos * itens_por_pedido * preco_medio_item
        
        vendas_diarias.append({
            'data': date,
            'pedidos': num_pedidos,
            'itens_vendidos': total_itens,
            'receita': receita_dia,
            'ticket_medio': receita_dia / num_pedidos if num_pedidos > 0 else 0,
            'mes': date.strftime('%Y-%m'),
            'ano': date.year,
            'trimestre': f"{date.year}-Q{(date.month-1)//3 + 1}",
            'dia_semana': date.strftime('%A')
        })
    
    return pd.DataFrame(vendas_diarias)

def get_produtos_performance():
    """
    Gera dados de performance de produtos baseados na estrutura:
    livro + autor + editora + vendas
    """
    # Gêneros literários brasileiros mais vendidos
    generos = [
        'Romance', 'Ficção', 'Biografia', 'Autoajuda', 'História',
        'Policial', 'Fantasia', 'Técnico', 'Infantil', 'Poesia',
        'Ensaio', 'Crônica', 'Drama', 'Humor', 'Religioso'
    ]
    
    # Editoras brasileiras famosas
    editoras = [
        'Companhia das Letras', 'Record', 'Globo Livros', 'Intrínseca',
        'Arqueiro', 'Suma', 'Planeta', 'Rocco', 'Objetiva', 'Zahar',
        'Ática', 'Scipione', 'FTD', 'Moderna', 'Saraiva'
    ]
    
    livros_data = []
    
    for i in range(200):  # 200 livros para análise
        genero = random.choice(generos)
        editora = random.choice(editoras)
        
        # Gerar título baseado no gênero
        if genero == 'Autoajuda':
            titulo = f"Como {fake.word().title()} Sua {fake.word().title()}"
        elif genero == 'Romance':
            titulo = f"O {fake.word().title()} de {fake.first_name()}"
        elif genero == 'História':
            titulo = f"História {fake.word().title()} do Brasil"
        elif genero == 'Técnico':
            titulo = f"Manual de {fake.word().title()}"
        else:
            titulo = f"{fake.sentence(nb_words=3).replace('.', '')}"
        
        # Vendas baseadas na popularidade do gênero
        multiplicador_genero = {
            'Romance': 1.5, 'Autoajuda': 1.3, 'Ficção': 1.2,
            'Biografia': 1.0, 'História': 0.8, 'Infantil': 1.1,
            'Técnico': 0.6, 'Poesia': 0.4, 'Drama': 0.5
        }
        
        base_vendas = random.randint(200, 1500)
        vendas = int(base_vendas * multiplicador_genero.get(genero, 1.0))
        
        preco = round(random.uniform(25, 150), 2)
        if genero == 'Técnico':
            preco = round(random.uniform(80, 300), 2)
        elif genero == 'Infantil':
            preco = round(random.uniform(15, 60), 2)
            
        ano_publicacao = random.randint(2015, 2024)
        
        livros_data.append({
            'id_livro': i + 1,
            'titulo': titulo,
            'autor': fake.name(),
            'editora': editora,
            'genero': genero,
            'ano_publicacao': ano_publicacao,
            'preco': preco,
            'vendas_total': vendas,
            'receita_total': vendas * preco,
            'avaliacoes': round(random.uniform(3.0, 5.0), 1),
            'estoque_atual': random.randint(0, 500)
        })
    
    return pd.DataFrame(livros_data)

def get_clientes_regioes():
    """
    Gera dados de clientes por região baseados na estrutura:
    cliente + endereco
    """
    # Estados brasileiros com população proporcional
    estados_data = {
        'SP': {'nome': 'São Paulo', 'peso': 0.23},
        'RJ': {'nome': 'Rio de Janeiro', 'peso': 0.12},
        'MG': {'nome': 'Minas Gerais', 'peso': 0.10},
        'BA': {'nome': 'Bahia', 'peso': 0.08},
        'PR': {'nome': 'Paraná', 'peso': 0.06},
        'RS': {'nome': 'Rio Grande do Sul', 'peso': 0.06},
        'PE': {'nome': 'Pernambuco', 'peso': 0.05},
        'CE': {'nome': 'Ceará', 'peso': 0.05},
        'SC': {'nome': 'Santa Catarina', 'peso': 0.04},
        'GO': {'nome': 'Goiás', 'peso': 0.04},
        'MA': {'nome': 'Maranhão', 'peso': 0.03},
        'PB': {'nome': 'Paraíba', 'peso': 0.02},
        'ES': {'nome': 'Espírito Santo', 'peso': 0.02},
        'PI': {'nome': 'Piauí', 'peso': 0.02},
        'AL': {'nome': 'Alagoas', 'peso': 0.02},
        'DF': {'nome': 'Distrito Federal', 'peso': 0.02},
        'MT': {'nome': 'Mato Grosso', 'peso': 0.02},
        'MS': {'nome': 'Mato Grosso do Sul', 'peso': 0.01},
        'SE': {'nome': 'Sergipe', 'peso': 0.01},
        'RN': {'nome': 'Rio Grande do Norte', 'peso': 0.02}
    }
    
    base_clientes = 50000  # Total de clientes
    regioes_data = []
    
    for uf, info in estados_data.items():
        num_clientes = int(base_clientes * info['peso'])
        
        # Vendas por região (proporcional mas com variações)
        vendas_por_cliente = random.uniform(2.5, 5.5)
        total_vendas = int(num_clientes * vendas_por_cliente)
        
        # Ticket médio varia por região (SP/RJ maior poder aquisitivo)
        if uf in ['SP', 'RJ', 'DF']:
            ticket_medio = round(random.uniform(75, 120), 2)
        elif uf in ['SC', 'PR', 'RS', 'ES']:
            ticket_medio = round(random.uniform(60, 95), 2)
        else:
            ticket_medio = round(random.uniform(45, 80), 2)
            
        receita_total = total_vendas * ticket_medio
        
        regioes_data.append({
            'estado': uf,
            'estado_nome': info['nome'],
            'total_clientes': num_clientes,
            'clientes_ativos': int(num_clientes * random.uniform(0.6, 0.8)),
            'total_vendas': total_vendas,
            'receita_total': receita_total,
            'ticket_medio': ticket_medio,
            'nps': random.randint(65, 85),  # Net Promoter Score
            'taxa_conversao': round(random.uniform(0.15, 0.35), 3)
        })
    
    return pd.DataFrame(regioes_data)

def get_formas_pagamento():
    """
    Dados de formas de pagamento baseados na tabela pagamento
    """
    formas = ['Pix', 'Cartão', 'Boleto']
    
    # Distribuição baseada no mercado brasileiro atual
    dados_pagamento = []
    total_transacoes = 30000
    
    distribuicao = {
        'Pix': 0.45,      # 45% - crescimento do Pix
        'Cartão': 0.40,   # 40% - cartão ainda forte
        'Boleto': 0.15    # 15% - diminuindo
    }
    
    for forma, percentual in distribuicao.items():
        num_transacoes = int(total_transacoes * percentual)
        
        # Ticket médio varia por forma de pagamento
        if forma == 'Cartão':
            ticket_medio = round(random.uniform(80, 150), 2)
        elif forma == 'Pix':
            ticket_medio = round(random.uniform(45, 90), 2)
        else:  # Boleto
            ticket_medio = round(random.uniform(60, 120), 2)
            
        receita = num_transacoes * ticket_medio
        
        dados_pagamento.append({
            'forma_pagamento': forma,
            'total_transacoes': num_transacoes,
            'receita_total': receita,
            'ticket_medio': ticket_medio,
            'percentual': percentual * 100,
            'tempo_medio_aprovacao': random.randint(1, 5) if forma == 'Cartão' else 0
        })
    
    return pd.DataFrame(dados_pagamento)

def get_estoque_alertas():
    """
    Dados de controle de estoque baseados na tabela estoque
    """
    # Usar os mesmos gêneros dos produtos
    generos = [
        'Romance', 'Ficção', 'Biografia', 'Autoajuda', 'História',
        'Policial', 'Fantasia', 'Técnico', 'Infantil', 'Poesia'
    ]
    
    estoque_data = []
    
    for genero in generos:
        # Estoque atual baseado na popularidade
        if genero in ['Romance', 'Autoajuda', 'Ficção']:
            estoque_atual = random.randint(800, 2500)
            estoque_minimo = random.randint(200, 500)
        elif genero in ['História', 'Biografia', 'Infantil']:
            estoque_atual = random.randint(400, 1200)
            estoque_minimo = random.randint(100, 300)
        else:  # Gêneros menos populares
            estoque_atual = random.randint(50, 400)
            estoque_minimo = random.randint(50, 150)
            
        # Status baseado na proporção estoque_atual/estoque_minimo
        ratio = estoque_atual / estoque_minimo
        if ratio < 1.2:
            status = 'Crítico'
            prioridade = 'Alta'
        elif ratio < 2.0:
            status = 'Baixo'
            prioridade = 'Média'
        else:
            status = 'Normal'
            prioridade = 'Baixa'
            
        # Giro de estoque (quantas vezes o estoque vira por mês)
        giro_mensal = round(random.uniform(1.5, 4.0), 1)
        
        estoque_data.append({
            'genero': genero,
            'estoque_atual': estoque_atual,
            'estoque_minimo': estoque_minimo,
            'estoque_maximo': estoque_minimo * 4,
            'status': status,
            'prioridade_reposicao': prioridade,
            'giro_mensal': giro_mensal,
            'dias_estoque': int(30 / giro_mensal),
            'valor_estoque': estoque_atual * random.uniform(30, 80)
        })
    
    return pd.DataFrame(estoque_data)

def get_kpis_principais():  # sourcery skip: inline-immediately-returned-variable
    """
    Calcula KPIs principais do negócio
    """
    vendas_df = get_vendas_temporais()
    
    # Filtrar últimos 30 dias para comparação
    data_limite = datetime.now() - timedelta(days=30)
    vendas_recentes = vendas_df[vendas_df['data'] >= data_limite]
    vendas_mes_anterior = vendas_df[
        (vendas_df['data'] >= data_limite - timedelta(days=30)) & 
        (vendas_df['data'] < data_limite)
    ]
    
    # Calcular métricas
    kpis = {
        'total_pedidos': vendas_recentes['pedidos'].sum(),
        'total_itens': vendas_recentes['itens_vendidos'].sum(),
        'receita_total': vendas_recentes['receita'].sum(),
        'ticket_medio': vendas_recentes['receita'].sum() / vendas_recentes['pedidos'].sum(),
        
        # Comparações com mês anterior
        'crescimento_pedidos': (
            (vendas_recentes['pedidos'].sum() - vendas_mes_anterior['pedidos'].sum()) /
            vendas_mes_anterior['pedidos'].sum() * 100
        ) if vendas_mes_anterior['pedidos'].sum() > 0 else 0,
        
        'crescimento_receita': (
            (vendas_recentes['receita'].sum() - vendas_mes_anterior['receita'].sum()) /
            vendas_mes_anterior['receita'].sum() * 100
        ) if vendas_mes_anterior['receita'].sum() > 0 else 0,
        
        # Métricas operacionais
        'conversao_visita_venda': round(random.uniform(2.5, 4.8), 2),
        'taxa_abandono_carrinho': round(random.uniform(65, 75), 1),
        'tempo_medio_entrega': random.randint(3, 7),
        'nps_geral': random.randint(72, 85)
    }
    
    return kpis

# Função principal para obter todos os dados
def get_all_data():
    """
    Retorna todos os datasets mockados
    """
    return {
        'vendas_temporais': get_vendas_temporais(),
        'produtos': get_produtos_performance(),
        'regioes': get_clientes_regioes(),
        'pagamentos': get_formas_pagamento(),
        'estoque': get_estoque_alertas(),
        'kpis': get_kpis_principais()
    }
