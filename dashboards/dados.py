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
    autores = [f'Autor {i}' for i in range(1, 51)]
    
    livros_data = []
    
    for i in range(100):
        genero = random.choice(generos)
        editora = random.choice(editoras)
        autor = random.choice(autores)
        
        # Gerar dados do livro
        titulo = f"Livro {i+1} - {genero}"
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
