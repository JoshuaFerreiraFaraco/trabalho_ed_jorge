import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from dados import get_all_data

# Configuração da página
st.set_page_config(
    page_title="Dashboard BI - Sistema de Vendas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de cores - Tema escuro limpo
COLORS = {
    'bg_primary': '#0F172A',     # Fundo principal muito escuro
    'bg_secondary': '#1E293B',   # Fundo secundário
    'bg_card': '#334155',        # Fundo dos cards
    'text_primary': '#F1F5F9',   # Texto principal (branco suave)
    'text_secondary': '#94A3B8', # Texto secundário
    'accent': '#3B82F6',         # Azul para destaques
    'accent_light': '#60A5FA',   # Azul claro
    'success': '#22C55E',        # Verde sucesso
    'warning': '#F59E0B',        # Amarelo aviso
    'danger': '#EF4444',         # Vermelho perigo
    'border': '#475569'          # Bordas
}

# CSS customizado - Tema escuro consistente
st.markdown(f"""
<style>
    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset global e fundo */
    .stApp {{
        background-color: {COLORS['bg_primary']};
        font-family: 'Inter', sans-serif;
    }}
    
    .main .block-container {{
        background-color: {COLORS['bg_primary']};
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}
    
    /* Sidebar escura */
    .css-1d391kg {{
        background-color: {COLORS['bg_secondary']};
    }}
    
    .css-1d391kg .stMarkdown {{
        color: {COLORS['text_primary']};
    }}
    
    /* Header principal */
    .main-header {{
        background: linear-gradient(135deg, {COLORS['bg_secondary']} 0%, {COLORS['bg_card']} 100%);
        color: {COLORS['text_primary']};
        padding: 2.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid {COLORS['border']};
    }}
    
    .main-header h1 {{
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.025em;
        color: {COLORS['text_primary']};
    }}
    
    .main-header p {{
        font-size: 1.125rem;
        margin-top: 0.75rem;
        color: {COLORS['text_secondary']};
        font-weight: 400;
    }}
    
    /* Títulos de seção */
    .section-header {{
        color: {COLORS['text_primary']};
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid {COLORS['accent']};
    }}
    
    /* Cards de métricas uniformes */
    .metric-container {{
        background: {COLORS['bg_card']};
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid {COLORS['border']};
        transition: all 0.3s ease;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    
    .metric-container:hover {{
        transform: translateY(-2px);
        border-color: {COLORS['accent']};
    }}
    
    .metric-container h3 {{
        color: {COLORS['text_secondary']};
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .metric-container h2 {{
        color: {COLORS['text_primary']};
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0.5rem 0;
        line-height: 1;
    }}
    
    .metric-container p {{
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0;
    }}
    
    .metric-positive {{ color: {COLORS['success']}; }}
    .metric-negative {{ color: {COLORS['danger']}; }}
    .metric-neutral {{ color: {COLORS['warning']}; }}
    
    /* Elementos interativos */
    .stSelectbox > div > div {{
        background-color: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        color: {COLORS['text_primary']};
    }}
    
    .stMultiSelect > div > div {{
        background-color: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        color: {COLORS['text_primary']};
    }}
    
    .stSelectbox label, .stMultiSelect label {{
        color: {COLORS['text_primary']} !important;
        font-weight: 500;
    }}
    
    /* Gráficos uniformes */
    .js-plotly-plot {{
        background-color: {COLORS['bg_card']} !important;
        border-radius: 12px;
        border: 1px solid {COLORS['border']};
    }}
    
    /* Tabelas escuras */
    .stDataFrame {{
        background-color: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        overflow: hidden;
    }}
    
    .stDataFrame table {{
        background-color: {COLORS['bg_card']} !important;
        color: {COLORS['text_primary']} !important;
    }}
    
    .stDataFrame thead tr th {{
        background-color: {COLORS['bg_secondary']} !important;
        color: {COLORS['text_primary']} !important;
        border-bottom: 1px solid {COLORS['border']} !important;
        font-weight: 600;
    }}
    
    .stDataFrame tbody tr td {{
        background-color: {COLORS['bg_card']} !important;
        color: {COLORS['text_primary']} !important;
        border-bottom: 1px solid {COLORS['border']} !important;
    }}
    
    /* Tabs escuras */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {COLORS['bg_secondary']};
        border-radius: 8px;
        padding: 0.25rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        color: {COLORS['text_secondary']};
        font-weight: 500;
        border-radius: 6px;
        padding: 0.5rem 1rem;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {COLORS['accent']} !important;
        color: white !important;
    }}
    
    /* Alertas escuros */
    .alert-success {{
        background-color: rgba(34, 197, 94, 0.1);
        border: 1px solid {COLORS['success']};
        border-radius: 8px;
        padding: 1rem;
        color: {COLORS['success']};
        margin: 1rem 0;
    }}
    
    .alert-warning {{
        background-color: rgba(245, 158, 11, 0.1);
        border: 1px solid {COLORS['warning']};
        border-radius: 8px;
        padding: 1rem;
        color: {COLORS['warning']};
        margin: 1rem 0;
    }}
    
    .alert-danger {{
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid {COLORS['danger']};
        border-radius: 8px;
        padding: 1rem;
        color: {COLORS['danger']};
        margin: 1rem 0;
    }}
    
    /* Texto geral */
    .stMarkdown {{
        color: {COLORS['text_primary']};
    }}
    
    .stMarkdown p {{
        color: {COLORS['text_primary']};
    }}
    
    /* Footer escuro */
    .footer-dark {{
        background-color: {COLORS['bg_secondary']};
        color: {COLORS['text_secondary']};
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid {COLORS['border']};
        text-align: center;
        margin-top: 2rem;
    }}
    
    .footer-dark h4 {{
        color: {COLORS['text_primary']};
        margin-bottom: 1rem;
    }}
</style>
""", unsafe_allow_html=True)

# Função para padronizar tema dos gráficos
def apply_dark_theme(fig, title=""):
    """Aplica tema escuro consistente aos gráficos Plotly"""
    fig.update_layout(
        plot_bgcolor=COLORS['bg_card'],
        paper_bgcolor=COLORS['bg_card'],
        font=dict(
            family="Inter, sans-serif",
            size=12,
            color=COLORS['text_primary']
        ),
        title=dict(
            text=title,
            font=dict(size=16, weight="bold", color=COLORS['text_primary']),
            x=0.02,
            y=0.95
        ),
        xaxis=dict(
            gridcolor=COLORS['border'],
            linecolor=COLORS['border'],
            tickcolor=COLORS['text_secondary'],
            color=COLORS['text_secondary']
        ),
        yaxis=dict(
            gridcolor=COLORS['border'],
            linecolor=COLORS['border'],
            tickcolor=COLORS['text_secondary'],
            color=COLORS['text_secondary']
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor=COLORS['border'],
            font=dict(color=COLORS['text_secondary'])
        ),
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

# Paleta de cores para gráficos
CHART_COLORS = [
    COLORS['accent'],
    COLORS['accent_light'], 
    COLORS['success'],
    COLORS['warning'],
    COLORS['danger'],
    '#8B5CF6',  # Roxo
    '#06B6D4',  # Ciano
    '#F97316',  # Laranja
    '#EC4899',  # Rosa
    '#84CC16'   # Lima
]

# Carregar dados mockados
@st.cache_data
def load_dashboard_data():
    """Carrega todos os dados necessários para o dashboard"""
    return get_all_data()

# Carregar dados
data = load_dashboard_data()
df_vendas = data['vendas_temporais']
df_produtos = data['produtos']
df_regioes = data['regioes']
df_pagamentos = data['pagamentos']
df_estoque = data['estoque']
kpis = data['kpis']

# Header principal
st.markdown("""
<div class="main-header">
    <h1>Dashboard Business Intelligence</h1>
    <p>Sistema de Vendas de Livros - Pipeline de Dados em Nuvem</p>
</div>
""", unsafe_allow_html=True)

# Sidebar com filtros
st.sidebar.markdown("## Filtros de Análise")

# Filtro de período
periodo = st.sidebar.selectbox(
    "Período:",
    ["Últimos 30 dias", "Últimos 90 dias", "2024", "2023", "2022", "Todos os dados"]
)

# Aplicar filtro de período
hoje = datetime.now()
if periodo == "Últimos 30 dias":
    data_inicio = hoje - timedelta(days=30)
    df_vendas_filtrado = df_vendas[df_vendas['data'] >= data_inicio]
elif periodo == "Últimos 90 dias":
    data_inicio = hoje - timedelta(days=90)
    df_vendas_filtrado = df_vendas[df_vendas['data'] >= data_inicio]
elif periodo == "2024":
    df_vendas_filtrado = df_vendas[df_vendas['ano'] == 2024]
elif periodo == "2023":
    df_vendas_filtrado = df_vendas[df_vendas['ano'] == 2023]
elif periodo == "2022":
    df_vendas_filtrado = df_vendas[df_vendas['ano'] == 2022]
else:
    df_vendas_filtrado = df_vendas

# Filtro de gênero
generos_disponiveis = df_produtos['genero'].unique()
genero_selecionado = st.sidebar.multiselect(
    "Gêneros:",
    generos_disponiveis,
    default=generos_disponiveis
)

df_produtos_filtrado = df_produtos[df_produtos['genero'].isin(genero_selecionado)]

# Filtro de região
regioes_disponiveis = df_regioes['estado'].unique()
regioes_selecionadas = st.sidebar.multiselect(
    "Estados:",
    regioes_disponiveis,
    default=regioes_disponiveis
)

df_regioes_filtrado = df_regioes[df_regioes['estado'].isin(regioes_selecionadas)]

# KPIs principais
st.markdown('<h2 class="section-header">Indicadores Principais</h2>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

# Calcular métricas do período filtrado
total_pedidos = df_vendas_filtrado['pedidos'].sum()
total_itens = df_vendas_filtrado['itens_vendidos'].sum()
receita_total = df_vendas_filtrado['receita'].sum()
ticket_medio = receita_total / total_pedidos if total_pedidos > 0 else 0
total_clientes = df_regioes_filtrado['total_clientes'].sum()

with col1:
    st.markdown("""
    <div class="metric-container">
        <h3>Pedidos</h3>
        <h2>{:,}</h2>
        <p class="metric-positive">+{:.1f}%</p>
    </div>
    """.format(total_pedidos, kpis['crescimento_pedidos']), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-container">
        <h3>Itens Vendidos</h3>
        <h2>{:,}</h2>
        <p class="metric-positive">+{:.1f}%</p>
    </div>
    """.format(total_itens, kpis['crescimento_receita'] * 0.8), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-container">
        <h3>Receita Total</h3>
        <h2>R$ {:,.0f}</h2>
        <p class="metric-positive">+{:.1f}%</p>
    </div>
    """.format(receita_total, kpis['crescimento_receita']), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-container">
        <h3>Ticket Médio</h3>
        <h2>R$ {:.2f}</h2>
        <p class="metric-negative">-2.1%</p>
    </div>
    """.format(ticket_medio), unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="metric-container">
        <h3>Clientes Ativos</h3>
        <h2>{:,}</h2>
        <p class="metric-positive">+{:.1f}%</p>
    </div>
    """.format(total_clientes, 15.7), unsafe_allow_html=True)

# Análise temporal
st.markdown('<h2 class="section-header">Evolução Temporal</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Vendas ao longo do tempo (agrupado por mês)
    df_vendas_mes = df_vendas_filtrado.groupby('mes').agg({
        'pedidos': 'sum',
        'receita': 'sum',
        'itens_vendidos': 'sum'
    }).reset_index()
    
    fig_vendas_tempo = px.line(
        df_vendas_mes, 
        x='mes', 
        y='pedidos',
        labels={'pedidos': 'Número de Pedidos', 'mes': 'Período'},
        color_discrete_sequence=[COLORS['accent']]
    )
    fig_vendas_tempo = apply_dark_theme(fig_vendas_tempo, 'Evolução dos Pedidos')
    fig_vendas_tempo.update_traces(line=dict(width=3))
    st.plotly_chart(fig_vendas_tempo, use_container_width=True)

with col2:
    # Receita ao longo do tempo
    fig_receita_tempo = px.area(
        df_vendas_mes, 
        x='mes', 
        y='receita',
        labels={'receita': 'Receita (R$)', 'mes': 'Período'},
        color_discrete_sequence=[COLORS['success']]
    )
    fig_receita_tempo = apply_dark_theme(fig_receita_tempo, 'Evolução da Receita')
    fig_receita_tempo.update_traces(fill='tonexty', fillcolor=f"rgba(34, 197, 94, 0.3)")
    st.plotly_chart(fig_receita_tempo, use_container_width=True)

# Análise de produtos
st.markdown('<h2 class="section-header">Performance de Produtos</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Top 15 livros mais vendidos
    top_livros = df_produtos_filtrado.nlargest(15, 'vendas_total')
    
    fig_top_livros = px.bar(
        top_livros,
        x='vendas_total',
        y='titulo',
        orientation='h',
        labels={'vendas_total': 'Vendas Totais', 'titulo': 'Título'},
        color_discrete_sequence=[COLORS['accent']]
    )
    fig_top_livros = apply_dark_theme(fig_top_livros, 'Top 15 Livros Mais Vendidos')
    fig_top_livros.update_layout(
        height=600, 
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig_top_livros, use_container_width=True)

with col2:
    # Distribuição por gênero
    vendas_genero = df_produtos_filtrado.groupby('genero').agg({
        'vendas_total': 'sum',
        'receita_total': 'sum'
    }).reset_index()
    
    fig_genero = px.pie(
        vendas_genero,
        values='vendas_total',
        names='genero',
        color_discrete_sequence=CHART_COLORS
    )
    fig_genero = apply_dark_theme(fig_genero, 'Distribuição de Vendas por Gênero')
    fig_genero.update_layout(height=600)
    fig_genero.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        textfont_size=11
    )
    st.plotly_chart(fig_genero, use_container_width=True)

# Análise de receita por gênero
col1, col2 = st.columns(2)

with col1:
    # Receita por gênero
    fig_receita_genero = px.bar(
        vendas_genero.sort_values('receita_total', ascending=True),
        x='receita_total',
        y='genero',
        orientation='h',
        labels={'receita_total': 'Receita (R$)', 'genero': 'Gênero'},
        color_discrete_sequence=[COLORS['success']]
    )
    fig_receita_genero = apply_dark_theme(fig_receita_genero, 'Receita por Gênero')
    fig_receita_genero.update_layout(height=400)
    st.plotly_chart(fig_receita_genero, use_container_width=True)

with col2:
    # Preço médio por gênero
    preco_genero = df_produtos_filtrado.groupby('genero')['preco'].mean().reset_index()
    
    fig_preco_genero = px.bar(
        preco_genero.sort_values('preco', ascending=True),
        x='preco',
        y='genero',
        orientation='h',
        labels={'preco': 'Preço Médio (R$)', 'genero': 'Gênero'},
        color_discrete_sequence=[COLORS['warning']]
    )
    fig_preco_genero = apply_dark_theme(fig_preco_genero, 'Preço Médio por Gênero')
    fig_preco_genero.update_layout(height=400)
    st.plotly_chart(fig_preco_genero, use_container_width=True)

# Análise regional
st.markdown('<h2 class="section-header">Análise Regional</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Receita por estado
    fig_estados = px.bar(
        df_regioes_filtrado.sort_values('receita_total', ascending=True),
        x='receita_total',
        y='estado',
        orientation='h',
        labels={'receita_total': 'Receita Total (R$)', 'estado': 'Estado'},
        color_discrete_sequence=[COLORS['accent']]
    )
    fig_estados = apply_dark_theme(fig_estados, 'Receita por Estado')
    fig_estados.update_layout(height=400)
    st.plotly_chart(fig_estados, use_container_width=True)

with col2:
    # Clientes vs Ticket médio
    fig_clientes_ticket = px.scatter(
        df_regioes_filtrado,
        x='total_clientes',
        y='ticket_medio',
        size='total_vendas',
        color='nps',
        hover_name='estado_nome',
        labels={
            'total_clientes': 'Total de Clientes', 
            'ticket_medio': 'Ticket Médio (R$)',
            'nps': 'NPS'
        },
        color_continuous_scale=['#EF4444', '#F59E0B', '#22C55E']
    )
    fig_clientes_ticket = apply_dark_theme(fig_clientes_ticket, 'Clientes vs Ticket Médio por Estado')
    fig_clientes_ticket.update_layout(height=400)
    st.plotly_chart(fig_clientes_ticket, use_container_width=True)

# Análise de pagamentos
st.markdown('<h2 class="section-header">Formas de Pagamento</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Distribuição das formas de pagamento
    fig_pagamentos = px.pie(
        df_pagamentos,
        values='total_transacoes',
        names='forma_pagamento',
        color_discrete_sequence=CHART_COLORS[:3]
    )
    fig_pagamentos = apply_dark_theme(fig_pagamentos, 'Distribuição das Transações por Forma de Pagamento')
    fig_pagamentos.update_layout(height=400)
    fig_pagamentos.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        textfont_size=11
    )
    st.plotly_chart(fig_pagamentos, use_container_width=True)

with col2:
    # Receita por forma de pagamento
    fig_receita_pagamento = px.bar(
        df_pagamentos,
        x='forma_pagamento',
        y='receita_total',
        labels={'receita_total': 'Receita (R$)', 'forma_pagamento': 'Forma de Pagamento'},
        color_discrete_sequence=[COLORS['success']]
    )
    fig_receita_pagamento = apply_dark_theme(fig_receita_pagamento, 'Receita por Forma de Pagamento')
    fig_receita_pagamento.update_layout(height=400)
    st.plotly_chart(fig_receita_pagamento, use_container_width=True)

# Controle de estoque
st.markdown('<h2 class="section-header">Controle de Estoque</h2>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # Gráfico de estoque
    fig_estoque = go.Figure()
    
    # Estoque atual
    fig_estoque.add_trace(go.Bar(
        name='Estoque Atual',
        x=df_estoque['genero'],
        y=df_estoque['estoque_atual'],
        marker_color=COLORS['accent'],
        opacity=0.8
    ))
    
    # Estoque mínimo
    fig_estoque.add_trace(go.Scatter(
        name='Estoque Mínimo',
        x=df_estoque['genero'],
        y=df_estoque['estoque_minimo'],
        mode='lines+markers',
        line=dict(color=COLORS['danger'], width=3, dash='dash'),
        marker=dict(size=8, color=COLORS['danger'])
    ))
    
    fig_estoque = apply_dark_theme(fig_estoque, 'Níveis de Estoque por Gênero')
    fig_estoque.update_layout(
        height=400,
        xaxis_title='Gênero',
        yaxis_title='Quantidade'
    )
    
    st.plotly_chart(fig_estoque, use_container_width=True)

with col2:
    # Alertas de estoque
    st.markdown("### Alertas de Estoque")
    
    estoque_critico = df_estoque[df_estoque['status'] == 'Crítico']
    estoque_baixo = df_estoque[df_estoque['status'] == 'Baixo']
    
    if not estoque_critico.empty:
        st.markdown('<div class="alert-danger">', unsafe_allow_html=True)
        st.markdown("**Estoque Crítico:**")
        for _, row in estoque_critico.iterrows():
            st.write(f"• **{row['genero']}**: {row['estoque_atual']} unidades")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if not estoque_baixo.empty:
        st.markdown('<div class="alert-warning">', unsafe_allow_html=True)
        st.markdown("**Estoque Baixo:**")
        for _, row in estoque_baixo.iterrows():
            st.write(f"• **{row['genero']}**: {row['estoque_atual']} unidades")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if estoque_critico.empty and estoque_baixo.empty:
        st.markdown('<div class="alert-success">', unsafe_allow_html=True)
        st.markdown("**Todos os estoques estão em níveis adequados**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Métricas de estoque
    st.markdown("### Resumo")
    total_valor_estoque = df_estoque['valor_estoque'].sum()
    giro_medio = df_estoque['giro_mensal'].mean()
    
    st.write(f"**Valor total em estoque:** R$ {total_valor_estoque:,.0f}")
    st.write(f"**Giro médio mensal:** {giro_medio:.1f}x")
    st.write(f"**Itens em alerta:** {len(estoque_critico) + len(estoque_baixo)}")

# Dados detalhados
st.markdown('<h2 class="section-header">Dados Detalhados</h2>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Produtos", "Regiões", "Pagamentos", "Estoque"])

with tab1:
    # Configurar colunas a exibir
    colunas_produtos = ['titulo', 'autor', 'genero', 'editora', 'vendas_total', 'preco', 'receita_total', 'avaliacoes']
    df_produtos_display = df_produtos_filtrado[colunas_produtos].sort_values('vendas_total', ascending=False)
    
    st.dataframe(
        df_produtos_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "vendas_total": st.column_config.NumberColumn("Vendas", format="%d"),
            "preco": st.column_config.NumberColumn("Preço", format="R$ %.2f"),
            "receita_total": st.column_config.NumberColumn("Receita", format="R$ %.0f"),
            "avaliacoes": st.column_config.NumberColumn("Avaliação", format="⭐ %.1f")
        }
    )

with tab2:
    df_regioes_display = df_regioes_filtrado.sort_values('receita_total', ascending=False)
    
    st.dataframe(
        df_regioes_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "total_clientes": st.column_config.NumberColumn("Clientes", format="%d"),
            "receita_total": st.column_config.NumberColumn("Receita", format="R$ %.0f"),
            "ticket_medio": st.column_config.NumberColumn("Ticket Médio", format="R$ %.2f"),
            "nps": st.column_config.NumberColumn("NPS", format="%d"),
            "taxa_conversao": st.column_config.NumberColumn("Conversão", format="%.1%")
        }
    )

with tab3:
    st.dataframe(
        df_pagamentos,
        use_container_width=True,
        hide_index=True,
        column_config={
            "total_transacoes": st.column_config.NumberColumn("Transações", format="%d"),
            "receita_total": st.column_config.NumberColumn("Receita", format="R$ %.0f"),
            "ticket_medio": st.column_config.NumberColumn("Ticket Médio", format="R$ %.2f"),
            "percentual": st.column_config.NumberColumn("Participação", format="%.1f%%")
        }
    )

with tab4:
    st.dataframe(
        df_estoque.sort_values('estoque_atual', ascending=True),
        use_container_width=True,
        hide_index=True,
        column_config={
            "estoque_atual": st.column_config.NumberColumn("Estoque Atual", format="%d"),
            "estoque_minimo": st.column_config.NumberColumn("Mínimo", format="%d"),
            "giro_mensal": st.column_config.NumberColumn("Giro Mensal", format="%.1fx"),
            "valor_estoque": st.column_config.NumberColumn("Valor", format="R$ %.0f")
        }
    )

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: {COLORS['text_secondary']}; padding: 2rem; background-color: {COLORS['bg_secondary']}; border-radius: 8px; margin-top: 2rem; border: 1px solid {COLORS['border']};'>
    <h4 style='color: {COLORS['text_primary']}; margin-bottom: 1rem;'>Dashboard BI - Sistema de Vendas de Livros</h4>
    <p style='margin: 0.5rem 0; color: {COLORS['text_secondary']};'><strong>Pipeline:</strong> Landing Zone → Bronze → Silver → Gold → Dashboard</p>
    <p style='margin: 0.5rem 0; color: {COLORS['text_secondary']};'><strong>Tecnologias:</strong> Azure Databricks • Data Lake • Terraform • Streamlit • Python</p>
    <p style='margin: 0.5rem 0; color: {COLORS['text_secondary']};'><strong>Projeto:</strong> Engenharia de Dados - SATC</p>
    <p style='margin-top: 1rem; font-size: 0.9rem; opacity: 0.8; color: {COLORS['text_secondary']};'>
        Dados mockados para demonstração • Estrutura preparada para integração com pipeline real
    </p>
</div>
""", unsafe_allow_html=True)
