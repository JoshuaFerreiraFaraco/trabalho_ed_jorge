import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from dados_clean import get_all_data

# Configuração da página
st.set_page_config(
    page_title="Dashboard BI - Sistema de Vendas de Livros",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Paleta de cores - Tema escuro profissional
COLORS = {
    'bg_primary': '#0F172A',
    'bg_secondary': '#1E293B',
    'bg_card': '#334155',
    'text_primary': '#F1F5F9',
    'text_secondary': '#94A3B8',
    'accent': '#3B82F6',
    'accent_light': '#60A5FA',
    'success': '#22C55E',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'border': '#475569'
}

# CSS customizado - Dashboard Premium limpo
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        box-sizing: border-box;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, {COLORS['bg_primary']} 0%, #0A0F1C 50%, {COLORS['bg_primary']} 100%);
        font-family: 'Inter', sans-serif;
        color: {COLORS['text_primary']};
    }}
    
    .main .block-container {{
        padding: 1rem 2rem;
        max-width: 100%;
        overflow-x: hidden;
    }}
    
    /* Header */
    .main-header {{
        background: linear-gradient(135deg, {COLORS['bg_secondary']} 0%, {COLORS['bg_card']} 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid {COLORS['border']};
    }}
    
    .main-header h1 {{
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        color: {COLORS['text_primary']};
    }}
    
    .main-header p {{
        font-size: 1rem;
        margin-top: 0.5rem;
        color: {COLORS['text_secondary']};
    }}
    
    /* Cards KPI */
    .kpi-card {{
        background: linear-gradient(135deg, {COLORS['bg_card']} 0%, #3A4759 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid {COLORS['border']};
        text-align: center;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }}
    
    .kpi-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
    }}
    
    .kpi-title {{
        color: {COLORS['text_secondary']};
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .kpi-value {{
        color: {COLORS['text_primary']};
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
    }}
    
    /* Seções de conteúdo */
    .content-section {{
        background: linear-gradient(135deg, {COLORS['bg_card']} 0%, #3A4759 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid {COLORS['border']};
        margin-bottom: 1.5rem;
    }}
    
    .section-title {{
        color: {COLORS['text_primary']};
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
        text-align: center;
    }}
    
    /* Gráficos */
    .js-plotly-plot {{
        background: transparent !important;
        border-radius: 8px !important;
    }}
    
    /* Responsividade */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding: 0.5rem 1rem;
        }}
        
        .main-header h1 {{
            font-size: 1.5rem;
        }}
        
        .kpi-card {{
            height: 110px;
            padding: 1rem;
        }}
        
        .kpi-value {{
            font-size: 1.6rem;
        }}
        
        .content-section {{
            padding: 1rem;
        }}
    }}
    
    @media (max-width: 480px) {{
        .main-header h1 {{
            font-size: 1.2rem;
        }}
        
        .kpi-card {{
            height: 100px;
            padding: 0.75rem;
        }}
        
        .kpi-value {{
            font-size: 1.4rem;
        }}
        
        .kpi-title {{
            font-size: 0.75rem;
        }}
    }}
    
    /* Texto geral */
    .stMarkdown {{ color: {COLORS['text_primary']}; }}
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{ color: {COLORS['text_primary']}; }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 8px; }}
    ::-webkit-scrollbar-track {{ background: {COLORS['bg_secondary']}; }}
    ::-webkit-scrollbar-thumb {{ background: {COLORS['accent']}; border-radius: 4px; }}
</style>
""", unsafe_allow_html=True)

# Função para aplicar tema escuro aos gráficos
def apply_dark_theme(fig, title="", height=300):
    fig.update_layout(
        plot_bgcolor=COLORS['bg_card'],
        paper_bgcolor=COLORS['bg_card'],
        font=dict(family="Inter, sans-serif", size=11, color=COLORS['text_primary']),
        title=dict(text=title, font=dict(size=14, color=COLORS['text_primary']), x=0.5),
        height=height,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(gridcolor=COLORS['border'], linecolor=COLORS['border'], color=COLORS['text_secondary']),
        yaxis=dict(gridcolor=COLORS['border'], linecolor=COLORS['border'], color=COLORS['text_secondary']),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS['text_secondary']))
    )
    return fig

# Carregar dados
@st.cache_data
def load_data():
    return get_all_data()

try:
    data = load_data()
    df_vendas = data['vendas_temporais']
    df_produtos = data['produtos']
    df_pedidos_status = data['pedidos_status']
    df_pagamentos = data['pagamentos']
    df_estoque = data['estoque']
    kpis = data['kpis']
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# Header principal
st.markdown("""
<div class="main-header">
    <h1>Dashboard BI - Sistema de Vendas de Livros</h1>
    <p>Análise de Dados | Pipeline Azure | Terraform Infrastructure</p>
</div>
""", unsafe_allow_html=True)

# Calcular KPIs principais
total_pedidos = df_vendas['pedidos'].sum()
receita_total = df_vendas['receita'].sum()
total_itens = df_vendas['itens_vendidos'].sum()
ticket_medio = receita_total / total_pedidos if total_pedidos > 0 else 0

# KPIs Principais
st.markdown("## Indicadores-Chave de Performance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total de Pedidos</div>
        <div class="kpi-value">{total_pedidos:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Receita Total</div>
        <div class="kpi-value">R$ {receita_total/1000:.0f}K</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Itens Vendidos</div>
        <div class="kpi-value">{total_itens:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Ticket Médio</div>
        <div class="kpi-value">R$ {ticket_medio:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# Segunda linha de KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total de Clientes</div>
        <div class="kpi-value">{kpis['total_clientes']:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Editoras Parceiras</div>
        <div class="kpi-value">{kpis['total_editoras']:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Autores Cadastrados</div>
        <div class="kpi-value">{kpis['total_autores']:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Livros Disponíveis</div>
        <div class="kpi-value">{kpis['total_livros']:,}</div>
    </div>
    """, unsafe_allow_html=True)

# Análises
st.markdown("## Análises de Negócio")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">Evolução de Vendas</h3>', unsafe_allow_html=True)
    
    # Gráfico de evolução temporal
    df_vendas_mes = df_vendas.groupby('mes').agg({
        'pedidos': 'sum',
        'receita': 'sum'
    }).reset_index()
    
    fig_evolucao = go.Figure()
    fig_evolucao.add_trace(go.Scatter(
        x=df_vendas_mes['mes'],
        y=df_vendas_mes['pedidos'],
        mode='lines+markers',
        name='Pedidos',
        line=dict(color=COLORS['accent'], width=3),
        marker=dict(size=8, color=COLORS['accent'])
    ))
    
    fig_evolucao.update_layout(
        xaxis_title='Período',
        yaxis_title='Número de Pedidos'
    )
    
    fig_evolucao = apply_dark_theme(fig_evolucao, height=350)
    st.plotly_chart(fig_evolucao, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">Status dos Pedidos</h3>', unsafe_allow_html=True)
    
    # Gráfico de status dos pedidos
    fig_status = go.Figure(data=[go.Pie(
        labels=df_pedidos_status['status'],
        values=df_pedidos_status['quantidade'],
        hole=0.3,
        textinfo='label+percent',
        marker=dict(
            colors=[COLORS['success'], COLORS['accent'], COLORS['warning'], COLORS['accent_light'], COLORS['danger']],
            line=dict(color=COLORS['bg_primary'], width=2)
        )
    )])
    
    fig_status = apply_dark_theme(fig_status, height=350)
    st.plotly_chart(fig_status, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Segunda linha de análises
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">Formas de Pagamento</h3>', unsafe_allow_html=True)
    
    # Gráfico de formas de pagamento
    fig_pagamento = go.Figure(data=[go.Bar(
        x=df_pagamentos['forma_pagamento'],
        y=df_pagamentos['total_transacoes'],
        marker=dict(
            color=[COLORS['accent'], COLORS['success'], COLORS['warning']],
            line=dict(color=COLORS['bg_primary'], width=1)
        )
    )])
    
    fig_pagamento.update_layout(
        xaxis_title='Forma de Pagamento',
        yaxis_title='Transações'
    )
    
    fig_pagamento = apply_dark_theme(fig_pagamento, height=350)
    st.plotly_chart(fig_pagamento, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">Controle de Estoque</h3>', unsafe_allow_html=True)
    
    # Gráfico de controle de estoque
    fig_estoque = go.Figure(data=[go.Pie(
        labels=df_estoque['status'],
        values=df_estoque['quantidade'],
        textinfo='label+percent',
        marker=dict(
            colors=[COLORS['danger'], COLORS['warning'], COLORS['success'], COLORS['accent']],
            line=dict(color=COLORS['bg_primary'], width=2)
        )
    )])
    
    fig_estoque = apply_dark_theme(fig_estoque, height=350)
    st.plotly_chart(fig_estoque, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Análise de produtos
st.markdown('<div class="content-section">', unsafe_allow_html=True)
st.markdown('<h3 class="section-title">Performance por Gênero</h3>', unsafe_allow_html=True)

# Gráfico de vendas por gênero
vendas_genero = df_produtos.groupby('genero').agg({
    'vendas_total': 'sum',
    'receita_total': 'sum'
}).reset_index().sort_values('receita_total', ascending=False)

fig_genero = go.Figure(data=[go.Bar(
    x=vendas_genero['genero'],
    y=vendas_genero['receita_total'],
    marker=dict(
        color=vendas_genero['receita_total'],
        colorscale='Blues',
        showscale=True
    )
)])

fig_genero.update_layout(
    xaxis_title='Gênero',
    yaxis_title='Receita Total (R$)'
)

fig_genero = apply_dark_theme(fig_genero, height=400)
st.plotly_chart(fig_genero, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, {COLORS['bg_secondary']} 0%, {COLORS['bg_primary']} 100%);
    color: {COLORS['text_secondary']};
    padding: 2rem;
    border-radius: 12px;
    border: 1px solid {COLORS['border']};
    text-align: center;
    margin-top: 2rem;
">
    <p style="margin: 0; font-size: 0.9rem;">
        Dashboard BI - Sistema de Vendas de Livros | 
        Dados em Tempo Real | 
        Análise Avançada de Negócios
    </p>
</div>
""", unsafe_allow_html=True)
