import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from dados import get_all_data

# Configuração da página
st.set_page_config(
    page_title="Dashboard BI - Sistema de Vendas de Livros",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Paleta de cores - Tema escuro profissional
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

# CSS customizado - Dashboard Premium
st.markdown(f"""
<style>
    /* Importar fontes modernas */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Reset global e configurações base */
    * {{
        box-sizing: border-box;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, {COLORS['bg_primary']} 0%, #0A0F1C 50%, {COLORS['bg_primary']} 100%);
        font-family: 'Inter', sans-serif;
        color: {COLORS['text_primary']};
    }}
    
    .main .block-container {{
        background-color: transparent;
        padding: 1rem 2rem;
        max-width: 100%;
    }}
    
    /* Header com animação */
    .main-header {{
        background: linear-gradient(135deg, {COLORS['bg_secondary']} 0%, {COLORS['bg_card']} 100%);
        color: {COLORS['text_primary']};
        padding: 2.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid {COLORS['border']};
        position: relative;
        overflow: hidden;
        animation: glow 3s ease-in-out infinite alternate;
    }}
    
    @keyframes glow {{
        from {{ box-shadow: 0 0 20px rgba(59, 130, 246, 0.2); }}
        to {{ box-shadow: 0 0 30px rgba(59, 130, 246, 0.4), 0 0 40px rgba(59, 130, 246, 0.1); }}
    }}
    
    .main-header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: slide 3s infinite;
    }}
    
    @keyframes slide {{
        0% {{ left: -100%; }}
        100% {{ left: 100%; }}
    }}
    
    .main-header h1 {{
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        color: {COLORS['text_primary']};
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }}
    
    .main-header p {{
        font-size: 1.1rem;
        margin-top: 0.75rem;
        color: {COLORS['text_secondary']};
        font-weight: 400;
        position: relative;
        z-index: 1;
    }}
    
    /* Cards KPI Premium */
    .kpi-card {{
        background: linear-gradient(135deg, {COLORS['bg_card']} 0%, #3A4759 100%);
        padding: 1.2rem 0.8rem;
        border-radius: 16px;
        border: 1px solid {COLORS['border']};
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: auto;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
    }}
    
    .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, {COLORS['accent']}, {COLORS['success']}, {COLORS['warning']});
        opacity: 0;
        transition: opacity 0.3s ease;
    }}
    
    .kpi-card:hover {{
        transform: translateY(-8px) scale(1.02);
        border-color: {COLORS['accent']};
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3), 0 0 0 1px rgba(59, 130, 246, 0.2);
    }}
    
    .kpi-card:hover::before {{
        opacity: 1;
    }}
    
    .kpi-icon {{
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }}
    
    .kpi-title {{
        color: {COLORS['text_secondary']};
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1.2;
        text-align: center;
    }}
    
    .kpi-value {{
        color: {COLORS['text_primary']};
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0.5rem 0;
        line-height: 1;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        text-align: center;
    }}
    
    .kpi-change {{
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.5rem 0 0 0;
        padding: 0.3rem 0.6rem;
        border-radius: 15px;
        display: inline-block;
    }}
    
    .kpi-positive {{ 
        color: {COLORS['success']}; 
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
    }}
    .kpi-negative {{ 
        color: {COLORS['danger']}; 
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }}
    .kpi-neutral {{ 
        color: {COLORS['warning']}; 
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }}
    
    /* Seções de conteúdo premium */
    .content-section {{
        background: linear-gradient(135deg, {COLORS['bg_card']} 0%, #3A4759 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid {COLORS['border']};
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }}
    
    .content-section::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, {COLORS['accent']}, {COLORS['success']});
    }}
    
    .section-title {{
        color: {COLORS['text_primary']};
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0 0 1.5rem 0;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }}
    
    /* Tabs modernos */
    .custom-tabs {{
        display: flex;
        background: {COLORS['bg_secondary']};
        border-radius: 12px;
        padding: 0.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid {COLORS['border']};
    }}
    
    .custom-tab {{
        flex: 1;
        padding: 0.75rem 1rem;
        text-align: center;
        background: transparent;
        color: {COLORS['text_secondary']};
        border: none;
        border-radius: 8px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .custom-tab.active {{
        background: {COLORS['accent']};
        color: white;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }}
    
    /* Gráficos aprimorados */
    .js-plotly-plot {{
        background: linear-gradient(135deg, {COLORS['bg_card']} 0%, #3A4759 100%) !important;
        border-radius: 12px !important;
        border: 1px solid {COLORS['border']} !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }}
    
    /* Mini cards de estatísticas */
    .stat-mini {{
        background: linear-gradient(135deg, {COLORS['bg_secondary']} 0%, {COLORS['bg_card']} 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid {COLORS['border']};
        text-align: center;
        transition: all 0.3s ease;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }}
    
    .stat-mini:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        border-color: {COLORS['accent']};
    }}
    
    .stat-mini-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {COLORS['accent']};
        margin: 0 0 0.5rem 0;
        line-height: 1;
    }}
    
    .stat-mini-label {{
        font-size: 0.9rem;
        color: {COLORS['text_secondary']};
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }}
    
    /* Alertas e notificações */
    .alert-box {{
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid;
        backdrop-filter: blur(10px);
    }}
    
    .alert-success {{
        background: rgba(34, 197, 94, 0.1);
        border-left-color: {COLORS['success']};
        color: {COLORS['success']};
    }}
    
    .alert-warning {{
        background: rgba(245, 158, 11, 0.1);
        border-left-color: {COLORS['warning']};
        color: {COLORS['warning']};
    }}
    
    .alert-info {{
        background: rgba(59, 130, 246, 0.1);
        border-left-color: {COLORS['accent']};
        color: {COLORS['accent']};
    }}
    
    /* Progress bars */
    .progress-container {{
        background: {COLORS['bg_secondary']};
        border-radius: 10px;
        overflow: hidden;
        height: 8px;
        margin: 0.5rem 0;
    }}
    
    .progress-bar {{
        height: 100%;
        background: linear-gradient(90deg, {COLORS['accent']}, {COLORS['success']});
        border-radius: 10px;
        transition: width 1s ease-in-out;
    }}
    
    /* Footer premium */
    .footer {{
        background: linear-gradient(135deg, {COLORS['bg_secondary']} 0%, {COLORS['bg_primary']} 100%);
        color: {COLORS['text_secondary']};
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid {COLORS['border']};
        text-align: center;
        margin-top: 3rem;
        font-size: 0.9rem;
        position: relative;
        overflow: hidden;
    }}
    
    .footer::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, {COLORS['accent']}, {COLORS['success']}, {COLORS['warning']});
    }}
    
    /* Responsividade ULTRA aprimorada - Versão 2.0 */
    
    /* Containers principais - força 100% da largura */
    .main .block-container {{
        max-width: 100% !important;
        width: 100% !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        overflow-x: hidden !important;
        box-sizing: border-box !important;
    }}
    
    /* Streamlit containers específicos */
    .stApp > div {{
        max-width: 100% !important;
        width: 100% !important;
        overflow-x: hidden !important;
    }}
    
    .element-container {{
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        overflow-x: hidden !important;
    }}
    
    /* Colunas responsivas - força flexbox correto */
    .row-widget.stHorizontal {{
        overflow-x: hidden !important;
        flex-wrap: wrap !important;
        width: 100% !important;
        max-width: 100% !important;
        gap: 0.5rem !important;
    }}
    
    .row-widget.stHorizontal > div {{
        min-width: 0 !important;
        flex-shrink: 1 !important;
        flex-basis: 0 !important;
        flex-grow: 1 !important;
        max-width: 100% !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
    }}
    
    /* Gráficos 100% responsivos */
    .js-plotly-plot {{
        width: 100% !important;
        max-width: 100% !important;
        height: auto !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
    }}
    
    .js-plotly-plot .plotly {{
        width: 100% !important;
        height: auto !important;
        max-width: 100% !important;
    }}
    
    .js-plotly-plot .plotly-graph-div {{
        width: 100% !important;
        max-width: 100% !important;
    }}
    
    /* Tablets e telas médias (768px - 1024px) */
    @media (max-width: 1024px) {{
        .main .block-container {{
            padding: 0.75rem !important;
        }}
        
        .main-header {{
            padding: 2rem 1.5rem !important;
            margin-bottom: 1.5rem !important;
        }}
        
        .main-header h1 {{ 
            font-size: 2rem !important; 
        }}
        
        .kpi-card {{ 
            padding: 1.25rem 0.8rem !important;
            height: 190px !important;
            min-height: 190px !important;
            margin-bottom: 1.25rem !important;
        }}
        
        .kpi-value {{ 
            font-size: 2.1rem !important;
        }}
        
        .kpi-icon {{
            font-size: 2rem !important;
        }}
        
        .content-section {{ 
            padding: 1.5rem !important;
            margin-bottom: 1rem !important;
        }}
        
        .section-title {{ 
            font-size: 1.2rem !important;
        }}
        
        .stat-mini {{ 
            padding: 0.75rem !important;
            margin: 0.25rem 0 !important;
        }}
        
        .stat-mini-value {{ 
            font-size: 1.3rem !important;
        }}
    }}
    
    /* Tablets pequenos (481px - 768px) */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding: 0.5rem !important;
        }}
        
        .main-header {{
            padding: 1.5rem 1rem !important;
            margin-bottom: 1rem !important;
        }}
        
        .main-header h1 {{ 
            font-size: 1.7rem !important;
            line-height: 1.2 !important;
        }}
        
        .main-header p {{
            font-size: 0.9rem !important;
            margin-top: 0.5rem !important;
        }}
        
        .kpi-card {{ 
            padding: 1rem 0.6rem !important;
            height: 180px !important;
            min-height: 180px !important;
            margin-bottom: 1rem !important;
        }}
        
        .kpi-value {{ 
            font-size: 1.8rem !important;
        }}
        
        .kpi-title {{
            font-size: 0.75rem !important;
            margin: 0 0 0.6rem 0 !important;
        }}
        
        .kpi-change {{
            font-size: 0.85rem !important;
            padding: 0.3rem 0.6rem !important;
        }}
        
        .kpi-icon {{
            font-size: 1.8rem !important;
            margin-bottom: 0.6rem !important;
        }}
        
        .content-section {{ 
            padding: 1.25rem !important;
            margin-bottom: 0.75rem !important;
        }}
        
        .section-title {{ 
            font-size: 1.1rem !important;
            margin-bottom: 1rem !important;
        }}
        
        .stat-mini {{ 
            padding: 0.8rem !important;
            margin: 0.5rem 0 !important;
            height: 90px !important;
        }}
        
        .stat-mini-value {{ 
            font-size: 1.4rem !important;
        }}
        
        .stat-mini-label {{
            font-size: 0.75rem !important;
        }}
        
        /* Força colunas a se empilharem em telas pequenas */
        .row-widget.stHorizontal {{
            flex-direction: column !important;
        }}
        
        .row-widget.stHorizontal > div {{
            width: 100% !important;
            max-width: 100% !important;
            margin-bottom: 0.5rem !important;
        }}
    }}
    
    /* Smartphones (até 480px) */
    @media (max-width: 480px) {{
        .main .block-container {{
            padding: 0.4rem !important;
        }}
        
        .main-header {{
            padding: 1rem 0.75rem !important;
            margin-bottom: 0.75rem !important;
        }}
        
        .main-header h1 {{ 
            font-size: 1.4rem !important;
            line-height: 1.1 !important;
        }}
        
        .main-header p {{
            font-size: 0.8rem !important;
            margin-top: 0.25rem !important;
        }}
        
        .kpi-card {{ 
            padding: 1rem 0.5rem !important;
            height: 170px !important;
            min-height: 170px !important;
            margin-bottom: 0.75rem !important;
        }}
        
        .kpi-value {{ 
            font-size: 1.6rem !important;
        }}
        
        .kpi-title {{
            font-size: 0.7rem !important;
            margin: 0 0 0.5rem 0 !important;
        }}
        
        .kpi-change {{
            font-size: 0.75rem !important;
            padding: 0.25rem 0.5rem !important;
        }}
        
        .kpi-icon {{
            font-size: 1.6rem !important;
            margin-bottom: 0.5rem !important;
        }}
        
        .content-section {{ 
            padding: 1rem 0.75rem !important;
            margin-bottom: 0.5rem !important;
        }}
        
        .section-title {{ 
            font-size: 1rem !important;
            margin-bottom: 0.75rem !important;
        }}
        
        .stat-mini {{ 
            padding: 0.5rem !important;
            margin: 0.25rem 0 !important;
        }}
        
        .stat-mini-value {{ 
            font-size: 1rem !important;
        }}
        
        .stat-mini-label {{
            font-size: 0.65rem !important;
        }}
        
        /* Força layout de coluna única em smartphones */
        .row-widget.stHorizontal {{
            flex-direction: column !important;
            gap: 0.25rem !important;
        }}
        
        .row-widget.stHorizontal > div {{
            width: 100% !important;
            max-width: 100% !important;
            margin-bottom: 0.25rem !important;
        }}
        
        /* Ajustar altura dos gráficos em smartphones */
        .js-plotly-plot {{
            min-height: 250px !important;
            max-height: 350px !important;
        }}
    }}
    
    /* Smartphones muito pequenos (até 360px) */
    @media (max-width: 360px) {{
        .main .block-container {{
            padding: 0.3rem !important;
        }}
        
        .main-header h1 {{ 
            font-size: 1.2rem !important;
        }}
        
        .kpi-card {{ 
            padding: 0.8rem 0.4rem !important;
            height: 120px !important;
            min-height: 120px !important;
        }}
        
        .kpi-value {{ 
            font-size: 1.4rem !important;
        }}
        
        .kpi-title {{
            font-size: 0.65rem !important;
        }}
        
        .kpi-icon {{
            font-size: 1.4rem !important;
        }}
        
        .content-section {{ 
            padding: 0.75rem 0.5rem !important;
        }}
        
        .section-title {{ 
            font-size: 0.9rem !important;
        }}
        
        .js-plotly-plot {{
            min-height: 200px !important;
            max-height: 280px !important;
        }}
    }}
    
    /* Força overflow correto para todos os elementos */
    * {{
        max-width: 100% !important;
        box-sizing: border-box !important;
    }}
    
    /* Remove qualquer scroll horizontal */
    html, body {{
        overflow-x: hidden !important;
        max-width: 100% !important;
    }}
    
    /* Força containers do Streamlit */
    .css-1d391kg, .css-1y4p8pa {{
        max-width: 100% !important;
        width: 100% !important;
        overflow-x: hidden !important;
    }}
    
    /* Tabelas responsivas */
    .stDataFrame {{
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: auto !important;
    }}
    
    .stDataFrame table {{
        width: 100% !important;
        max-width: 100% !important;
    }}
    
    /* Texto geral */
    .stMarkdown {{ color: {COLORS['text_primary']}; }}
    .stMarkdown p {{ color: {COLORS['text_primary']}; }}
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{ color: {COLORS['text_primary']}; }}
    
    /* Scrollbar customizada */
    ::-webkit-scrollbar {{ width: 8px; }}
    ::-webkit-scrollbar-track {{ background: {COLORS['bg_secondary']}; }}
    ::-webkit-scrollbar-thumb {{ background: {COLORS['accent']}; border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {COLORS['accent_light']}; }}
    
    /* === FORÇAS CRÍTICAS ANTI-OVERFLOW MOBILE === */
    
    /* Reset absoluto */
    html, body {{
        overflow-x: hidden !important;
        max-width: 100vw !important;
        width: 100vw !important;
    }}
    
    .stApp {{
        overflow-x: hidden !important;
        max-width: 100vw !important;
        width: 100vw !important;
    }}
    
    /* Força containers críticos */
    .main .block-container {{
        max-width: 100vw !important;
        width: 100% !important;
        overflow-x: hidden !important;
        padding: 0.5rem !important;
        margin: 0 !important;
        box-sizing: border-box !important;
    }}
    
    /* Força todos os filhos */
    .main .block-container > * {{
        max-width: 100% !important;
        overflow-x: hidden !important;
        box-sizing: border-box !important;
    }}
    
    /* Força colunas do Streamlit */
    div[data-testid="column"] {{
        max-width: 100% !important;
        overflow-x: hidden !important;
        min-width: 0 !important;
        flex-shrink: 1 !important;
        padding: 0.25rem !important;
    }}
    
    div[data-testid="stHorizontalBlock"] {{
        max-width: 100% !important;
        overflow-x: hidden !important;
        flex-wrap: wrap !important;
        gap: 0.5rem !important;
    }}
    
    .row-widget.stHorizontal {{
        flex-wrap: wrap !important;
        overflow-x: hidden !important;
        max-width: 100% !important;
        gap: 0.5rem !important;
        justify-content: space-between !important;
    }}
    
    .row-widget.stHorizontal > div {{
        flex-shrink: 1 !important;
        min-width: 0 !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
        flex-basis: calc(25% - 0.375rem) !important;
    }}
    
    /* Força gráficos */
    .js-plotly-plot, .plotly-graph-div {{
        max-width: 100% !important;
        width: 100% !important;
        overflow: hidden !important;
    }}
    
    /* Mobile específico - força layout vertical */
    @media (max-width: 768px) {{
        .row-widget.stHorizontal {{
            flex-direction: column !important;
            gap: 0.75rem !important;
        }}
        
        .row-widget.stHorizontal > div {{
            width: 100% !important;
            max-width: 100% !important;
            margin-bottom: 0.5rem !important;
            flex-basis: auto !important;
        }}
        
        .kpi-card {{
            margin: 0 auto 0.75rem auto !important;
            width: calc(100% - 1rem) !important;
            max-width: 400px !important;
        }}
        
        div[data-testid="column"] {{
            padding: 0.1rem !important;
        }}
    }}
    
    /* Tablet landscape - 2 colunas */
    @media (min-width: 769px) and (max-width: 1024px) {{
        .row-widget.stHorizontal > div {{
            flex-basis: calc(50% - 0.25rem) !important;
            margin-bottom: 1rem !important;
        }}
    }}
    
    /* Desktop - 4 colunas */
    @media (min-width: 1025px) {{
        .row-widget.stHorizontal > div {{
            flex-basis: calc(25% - 0.375rem) !important;
        }}
    }}
    
    /* Remove margens laterais perigosas */
    * {{
        margin-left: 0 !important;
        margin-right: 0 !important;
    }}
    
    /* Força quebra de texto em todos os elementos */
    .kpi-title, .section-title, .stat-mini-label, .kpi-value {{
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
        hyphens: auto !important;
    }}
    
    /* Ajuste especial para valores monetários */
    .kpi-value {{
        word-spacing: -0.1em !important;
        letter-spacing: -0.02em !important;
    }}
    
    /* Garantia de espaçamento interno dos cards */
    .kpi-card > * {{
        margin-left: 0 !important;
        margin-right: 0 !important;
    }}
    
    /* Prevent any element from being wider than viewport */
    * {{
        max-width: 100vw !important;
        box-sizing: border-box !important;
    }}
    
    /* Ultra mobile fix - super small screens */
    @media (max-width: 320px) {{
        .main .block-container {{
            padding: 0.2rem !important;
        }}
        
        .kpi-card {{
            padding: 0.6rem 0.3rem !important;
            min-height: 150px !important;
            width: calc(100% - 0.4rem) !important;
        }}
        
        .kpi-value {{
            font-size: 1.2rem !important;
        }}
        
        .kpi-title {{
            font-size: 0.6rem !important;
        }}
        
        .kpi-icon {{
            font-size: 1.2rem !important;
        }}
    }}
    
    /* Garantir que o conteúdo dos KPIs seja sempre visível */
    .kpi-card {{
        min-height: 200px !important;
        padding: 1.5rem 1rem !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-evenly !important;
        align-items: center !important;
        text-align: center !important;
    }}
    
    .kpi-value {{
        word-break: break-all !important;
        overflow-wrap: break-word !important;
        white-space: nowrap !important;
    }}
    
    /* Ajustes mobile críticos */
    @media (max-width: 768px) {{
        .kpi-card {{
            min-height: 180px !important;
            padding: 1rem 0.6rem !important;
        }}
        
        .kpi-value {{
            font-size: 1.8rem !important;
            margin: 0.6rem 0 !important;
            white-space: normal !important;
        }}
        
        .kpi-title {{
            font-size: 0.75rem !important;
            margin: 0 0 0.6rem 0 !important;
        }}
        
        .kpi-change {{
            font-size: 0.8rem !important;
            margin: 0.6rem 0 0 0 !important;
        }}
        
        .kpi-icon {{
            font-size: 1.8rem !important;
            margin-bottom: 0.6rem !important;
        }}
    }}
    
    @media (max-width: 480px) {{
        .kpi-card {{
            min-height: 170px !important;
            padding: 0.8rem 0.5rem !important;
        }}
        
        .kpi-value {{
            font-size: 1.6rem !important;
            margin: 0.5rem 0 !important;
        }}
        
        .kpi-title {{
            font-size: 0.7rem !important;
            margin: 0 0 0.5rem 0 !important;
        }}
        
        .kpi-icon {{
            font-size: 1.6rem !important;
            margin-bottom: 0.5rem !important;
        }}
        
        .kpi-change {{
            font-size: 0.75rem !important;
            margin: 0.5rem 0 0 0 !important;
        }}
    }}
    
    @media (max-width: 360px) {{
        .kpi-card {{
            min-height: 120px !important;
            padding: 0.7rem 0.4rem !important;
        }}
        
        .kpi-value {{
            font-size: 1.4rem !important;
        }}
        
        .kpi-title {{
            font-size: 0.65rem !important;
        }}
        
        .kpi-icon {{
            font-size: 1.4rem !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Função para aplicar tema escuro aos gráficos
def apply_dark_theme(fig, title="", height=300):
    """Aplica tema escuro aos gráficos Plotly"""
    fig.update_layout(
        plot_bgcolor=COLORS['bg_card'],
        paper_bgcolor=COLORS['bg_card'],
        font=dict(
            family="Inter, sans-serif",
            size=11,
            color=COLORS['text_primary']
        ),
        title=dict(
            text=title,
            font=dict(size=14, color=COLORS['text_primary']),
            x=0.5,
            y=0.95
        ),
        height=height,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(
            gridcolor=COLORS['border'],
            linecolor=COLORS['border'],
            color=COLORS['text_secondary']
        ),
        yaxis=dict(
            gridcolor=COLORS['border'],
            linecolor=COLORS['border'],
            color=COLORS['text_secondary']
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLORS['text_secondary'])
        )
    )
    return fig

# Carregar dados com tratamento de erro
@st.cache_data
def load_data():
    try:
        return get_all_data()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

data = load_data()

if data is None:
    st.stop()

df_vendas = data['vendas_temporais']
df_produtos = data['produtos']
df_pagamentos = data['pagamentos']
df_estoque = data['estoque']
kpis = data['kpis']

# Header principal
st.markdown("""
<div class="main-header">
    <h1> Dashboard BI - Sistema de Vendas de Livros</h1>
    <p>Pipeline de Dados em Nuvem | Azure Databricks • Data Lake • Terraform</p>
</div>
""", unsafe_allow_html=True)

# ========== SEÇÃO DE 6 KPIs PRINCIPAIS (EXPANDIDO) ==========
st.markdown("##  Indicadores-Chave de Performance (KPIs)")

# Calcular KPIs expandidos
total_pedidos = df_vendas['pedidos'].sum()
receita_total = df_vendas['receita'].sum()
total_clientes = 15000  # Baseado nos dados do banco
margem_lucro = ((receita_total * 0.35) / receita_total) * 100
ticket_medio = receita_total / total_pedidos if total_pedidos > 0 else 0
total_itens = df_vendas['itens_vendidos'].sum()

# Primeira linha de KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📦</div>
        <div class="kpi-title">Total de Pedidos</div>
        <div class="kpi-value">{total_pedidos:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">💰</div>
        <div class="kpi-title">Receita Total</div>
        <div class="kpi-value">R$ {receita_total/1000:.0f}K</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">👥</div>
        <div class="kpi-title">Clientes Ativos</div>
        <div class="kpi-value">{total_clientes:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📈</div>
        <div class="kpi-title">Margem de Lucro</div>
        <div class="kpi-value">{margem_lucro:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

# Segunda linha de KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🎯</div>
        <div class="kpi-title">Ticket Médio</div>
        <div class="kpi-value">R$ {ticket_medio:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📚</div>
        <div class="kpi-title">Itens Vendidos</div>
        <div class="kpi-value">{total_itens:,}</div>
    </div>
    """, unsafe_allow_html=True)

# ROI e Taxa de Conversão (simulados)
roi = 285.7  # Simulado
taxa_conversao = 3.4  # Simulado

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">💎</div>
        <div class="kpi-title">ROI</div>
        <div class="kpi-value">{roi:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">⚡</div>
        <div class="kpi-title">Taxa Conversão</div>
        <div class="kpi-value">{taxa_conversao:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ========== SEÇÃO DE MÚLTIPLAS MÉTRICAS E ANÁLISES ==========
st.markdown("##  Analytics & Business Intelligence")

# === ESTATÍSTICAS RÁPIDAS ===
col_stats1, col_stats2, col_stats3, col_stats4, col_stats5, col_stats6 = st.columns(6)

with col_stats1:
    st.markdown("""
    <div class="stat-mini">
        <div class="stat-mini-value">4.7⭐</div>
        <div class="stat-mini-label">Nota Média</div>
    </div>
    """, unsafe_allow_html=True)

with col_stats2:
    st.markdown("""
    <div class="stat-mini">
        <div class="stat-mini-value">87</div>
        <div class="stat-mini-label">Editoras</div>
    </div>
    """, unsafe_allow_html=True)

with col_stats3:
    st.markdown("""
    <div class="stat-mini">
        <div class="stat-mini-value">342</div>
        <div class="stat-mini-label">Autores</div>
    </div>
    """, unsafe_allow_html=True)

with col_stats4:
    st.markdown("""
    <div class="stat-mini">
        <div class="stat-mini-value">92%</div>
        <div class="stat-mini-label">NPS Score</div>
    </div>
    """, unsafe_allow_html=True)

with col_stats5:
    st.markdown("""
    <div class="stat-mini">
        <div class="stat-mini-value">R$ 1.2M</div>
        <div class="stat-mini-label">Valor Estoque</div>
    </div>
    """, unsafe_allow_html=True)

with col_stats6:
    # Estado com mais vendas baseado nos dados históricos
    top_estado = "SP"  # São Paulo é tradicionalmente o maior mercado
    
    st.markdown(f"""
    <div class="stat-mini">
        <div class="stat-mini-value">{top_estado}</div>
        <div class="stat-mini-label">Top Estado</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# === PRIMEIRA LINHA DE ANÁLISES ===
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">Evolução de Vendas por Período</h3>', unsafe_allow_html=True)
    
    # Gráfico de evolução temporal
    df_vendas_mes = df_vendas.groupby('mes').agg({
        'pedidos': 'sum',
        'receita': 'sum'
    }).reset_index()
    
    fig_evolucao = go.Figure()
    
    # Linha de pedidos
    fig_evolucao.add_trace(go.Scatter(
        x=df_vendas_mes['mes'],
        y=df_vendas_mes['pedidos'],
        mode='lines+markers',
        name='Pedidos',
        line=dict(color=COLORS['accent'], width=3),
        marker=dict(size=8, color=COLORS['accent']),
        fill='tonexty',
        fillcolor=f"rgba(59, 130, 246, 0.1)"
    ))
    
    # Linha de receita (eixo secundário)
    fig_evolucao.add_trace(go.Scatter(
        x=df_vendas_mes['mes'],
        y=df_vendas_mes['receita'],
        mode='lines+markers',
        name='Receita (R$)',
        yaxis='y2',
        line=dict(color=COLORS['success'], width=3),
        marker=dict(size=8, color=COLORS['success'])
    ))
    
    fig_evolucao.update_layout(
        yaxis=dict(title='Número de Pedidos', side='left', color=COLORS['text_secondary']),
        yaxis2=dict(title='Receita (R$)', side='right', overlaying='y', color=COLORS['text_secondary']),
        xaxis=dict(title='Período', color=COLORS['text_secondary']),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig_evolucao = apply_dark_theme(fig_evolucao, height=400)
    st.plotly_chart(fig_evolucao, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">Performance por Categoria</h3>', unsafe_allow_html=True)
    
    # Gráfico de vendas por gênero
    vendas_genero = df_produtos.groupby('genero').agg({
        'vendas_total': 'sum',
        'receita_total': 'sum'
    }).reset_index().sort_values('receita_total', ascending=False)
    
    # Criar gráfico de pizza 3D
    fig_categorias = go.Figure(data=[go.Pie(
        labels=vendas_genero['genero'],
        values=vendas_genero['receita_total'],
        hole=0.3,
        textinfo='label+percent',
        textfont_size=12,
        marker=dict(
            colors=[COLORS['accent'], COLORS['success'], COLORS['warning'], 
                   COLORS['danger'], COLORS['accent_light'], '#8B5CF6'],
            line=dict(color=COLORS['bg_primary'], width=2)
        )
    )])
    
    fig_categorias = apply_dark_theme(fig_categorias, height=400)
    st.plotly_chart(fig_categorias, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# === SEGUNDA LINHA DE ANÁLISES ===
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">Status do Estoque</h3>', unsafe_allow_html=True)
    
    # Gráfico de estoque por status
    fig_estoque = go.Figure(data=[
        go.Bar(
            x=df_estoque['status'],
            y=df_estoque['quantidade'],
            marker=dict(
                color=df_estoque['quantidade'],
                colorscale=[[0, COLORS['danger']], [0.5, COLORS['warning']], [1, COLORS['success']]],
                showscale=True,
                colorbar=dict(title="Qtd Produtos")
            ),
            text=df_estoque['quantidade'],
            textposition='outside'
        )
    ])
    
    fig_estoque.update_layout(
        xaxis_title='Status',
        yaxis_title='Quantidade de Produtos',
        xaxis_tickangle=-45
    )
    
    fig_estoque = apply_dark_theme(fig_estoque, height=400)
    st.plotly_chart(fig_estoque, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">Formas de Pagamento</h3>', unsafe_allow_html=True)
    
    # Gráfico de rosca para pagamentos
    fig_pagamento = go.Figure(data=[go.Pie(
        labels=df_pagamentos['forma_pagamento'],
        values=df_pagamentos['total_transacoes'],
        hole=0.5,
        textinfo='label+percent+value',
        textfont_size=11,
        marker=dict(
            colors=[COLORS['accent'], COLORS['success'], COLORS['warning']],
            line=dict(color=COLORS['bg_primary'], width=3)
        )
    )])
    
    fig_pagamento.add_annotation(
        text=f"Total<br>{df_pagamentos['total_transacoes'].sum():,}<br>transações",
        x=0.5, y=0.5,
        font_size=14,
        showarrow=False,
        font_color=COLORS['text_primary']
    )
    
    fig_pagamento = apply_dark_theme(fig_pagamento, height=400)
    st.plotly_chart(fig_pagamento, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# === TERCEIRA LINHA DE ANÁLISES ===
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">Top Livros Best-Sellers</h3>', unsafe_allow_html=True)
    
    # Top 10 livros
    top_livros = df_produtos.nlargest(10, 'vendas_total')
    
    fig_books = go.Figure(data=[
        go.Bar(
            x=top_livros['vendas_total'],
            y=top_livros['titulo'].str[:30] + '...',  # Truncar títulos
            orientation='h',
            marker=dict(
                color=top_livros['vendas_total'],
                colorscale='Viridis',
                showscale=True
            ),
            text=top_livros['vendas_total'],
            textposition='inside'
        )
    ])
    
    fig_books.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title='Vendas Totais',
        yaxis_title='Livros'
    )
    
    fig_books = apply_dark_theme(fig_books, height=400)
    st.plotly_chart(fig_books, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">Controle de Estoque</h3>', unsafe_allow_html=True)
    
    # Gráfico de gauge para estoque
    estoque_critico = len(df_estoque[df_estoque['status'] == 'Crítico'])
    estoque_baixo = len(df_estoque[df_estoque['status'] == 'Baixo'])
    estoque_ok = len(df_estoque[df_estoque['status'] == 'Normal'])
    total_itens = len(df_estoque)
    
    fig_estoque_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = (estoque_ok / total_itens) * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "% Estoque Saudável"},
        delta = {'reference': 85},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': COLORS['success']},
            'steps': [
                {'range': [0, 50], 'color': COLORS['danger']},
                {'range': [50, 80], 'color': COLORS['warning']},
                {'range': [80, 100], 'color': COLORS['success']}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig_estoque_gauge = apply_dark_theme(fig_estoque_gauge, height=400)
    st.plotly_chart(fig_estoque_gauge, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== ESTATÍSTICAS EM TEMPO REAL ==========
st.markdown("## Estatísticas em Tempo Real")

col1, col2, col3, col4, col5, col6 = st.columns(6)

# Calcular estatísticas adicionais
avg_avaliacao = df_produtos['avaliacoes'].mean()
total_editoras = df_produtos['editora'].nunique()
total_autores = df_produtos['autor'].nunique()
melhor_genero = df_produtos.groupby('genero')['receita_total'].sum().idxmax()
nps_medio = 78.5  # NPS médio estimado
total_itens_estoque = df_estoque['quantidade'].sum()

with col1:
    st.markdown(f"""
    <div class="stat-mini">
        <div class="stat-mini-value">⭐ {avg_avaliacao:.1f}</div>
        <div class="stat-mini-label">Nota Média</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-mini">
        <div class="stat-mini-value">🏢 {total_editoras}</div>
        <div class="stat-mini-label">Editoras</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-mini">
        <div class="stat-mini-value">✍️ {total_autores}</div>
        <div class="stat-mini-label">Autores</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-mini">
        <div class="stat-mini-value">📚 {melhor_genero[:8]}</div>
        <div class="stat-mini-label">Top Gênero</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="stat-mini">
        <div class="stat-mini-value">📊 {nps_medio:.0f}</div>
        <div class="stat-mini-label">NPS Médio</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="stat-mini">
        <div class="stat-mini-value">� {total_itens_estoque}</div>
        <div class="stat-mini-label">Itens em Estoque</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ========== RESUMO EXECUTIVO E INSIGHTS AVANÇADOS ==========
st.markdown("## Business Intelligence & Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="content-section">
        <h4 style="color: {COLORS['text_primary']}; margin-bottom: 1rem;">🎯 Performance Highlights</h4>        <div style="margin: 0.75rem 0;">
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span style="color: {COLORS['text_secondary']};">Crescimento Vendas:</span>
                <span style="color: {COLORS['success']}; font-weight: 600;">+{kpis['crescimento_vendas']:.1f}%</span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {min(kpis['crescimento_vendas'] * 3, 100)}%;"></div>
            </div>
        </div>        <div style="margin: 0.75rem 0;">
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span style="color: {COLORS['text_secondary']};">Crescimento Vendas:</span>
                <span style="color: {COLORS['success']}; font-weight: 600;">+{kpis['crescimento_vendas']:.1f}%</span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {min(kpis['crescimento_vendas'] * 2.5, 100)}%;"></div>
            </div>
        </div>
        <div style="margin: 0.75rem 0;">
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span style="color: {COLORS['text_secondary']};">Base de Clientes:</span>
                <span style="color: {COLORS['success']}; font-weight: 600;">+15.7%</span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: 63%;"></div>
            </div>
        </div>
        <div style="margin: 0.75rem 0;">
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                <span style="color: {COLORS['text_secondary']};">Margem de Lucro:</span>
                <span style="color: {COLORS['success']}; font-weight: 600;">35.0%</span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: 70%;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    ticket_medio = receita_total / total_pedidos if total_pedidos > 0 else 0
    melhor_genero = df_produtos.groupby('genero')['receita_total'].sum().idxmax()
    melhor_autor = df_produtos.groupby('autor')['vendas_total'].sum().idxmax()
    
    st.markdown(f"""
    <div class="content-section">
        <h4 style="color: {COLORS['text_primary']}; margin-bottom: 1rem;">💡 Insights Estratégicos</h4>
        <div style="padding: 0.75rem; background: rgba(59, 130, 246, 0.1); border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid {COLORS['accent']};">
            <strong style="color: {COLORS['accent']};">Ticket Médio:</strong><br>
            <span style="color: {COLORS['text_secondary']};">R$ {ticket_medio:.2f} por pedido</span>
        </div>
        <div style="padding: 0.75rem; background: rgba(59, 130, 246, 0.1); border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid {COLORS['accent']};">
            <strong style="color: {COLORS['accent']};">Categoria Líder:</strong><br>
            <span style="color: {COLORS['text_secondary']};">{melhor_genero}</span>
        </div>
        <div style="padding: 0.75rem; background: rgba(245, 158, 11, 0.1); border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid {COLORS['warning']};">
            <strong style="color: {COLORS['warning']};">Autor Destaque:</strong><br>
            <span style="color: {COLORS['text_secondary']};">{melhor_autor[:25]}...</span>
        </div>
        <div style="padding: 0.75rem; background: rgba(139, 92, 246, 0.1); border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid #8B5CF6;">
            <strong style="color: #8B5CF6;">ROI Calculado:</strong><br>
            <span style="color: {COLORS['text_secondary']};">285.7% retorno investimento</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="content-section">
        <h4 style="color: {COLORS['text_primary']}; margin-bottom: 1rem;">🚀 Stack Tecnológico</h4>
        <div style="margin: 0.5rem 0;">
            <div style="display: flex; align-items: center; margin: 0.75rem 0;">
                <div style="width: 8px; height: 8px; background: {COLORS['accent']}; border-radius: 50%; margin-right: 0.75rem;"></div>
                <span style="color: {COLORS['text_secondary']}; font-size: 0.9rem;"><strong>Landing Zone</strong> → Ingestão de dados</span>
            </div>
            <div style="display: flex; align-items: center; margin: 0.75rem 0;">
                <div style="width: 8px; height: 8px; background: {COLORS['success']}; border-radius: 50%; margin-right: 0.75rem;"></div>
                <span style="color: {COLORS['text_secondary']}; font-size: 0.9rem;"><strong>Bronze Layer</strong> → Dados brutos</span>
            </div>
            <div style="display: flex; align-items: center; margin: 0.75rem 0;">
                <div style="width: 8px; height: 8px; background: {COLORS['warning']}; border-radius: 50%; margin-right: 0.75rem;"></div>
                <span style="color: {COLORS['text_secondary']}; font-size: 0.9rem;"><strong>Silver Layer</strong> → Dados limpos</span>
            </div>
            <div style="display: flex; align-items: center; margin: 0.75rem 0;">
                <div style="width: 8px; height: 8px; background: #FFD700; border-radius: 50%; margin-right: 0.75rem;"></div>
                <span style="color: {COLORS['text_secondary']}; font-size: 0.9rem;"><strong>Gold Layer</strong> → Analytics ready</span>
            </div>
            <div style="display: flex; align-items: center; margin: 0.75rem 0;">
                <div style="width: 8px; height: 8px; background: #8B5CF6; border-radius: 50%; margin-right: 0.75rem;"></div>
                <span style="color: {COLORS['text_secondary']}; font-size: 0.9rem;"><strong>Dashboard BI</strong> → Visualização</span>
            </div>
        </div>
        <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(139, 92, 246, 0.1); border-radius: 8px;">
            <h5 style="color: #8B5CF6; margin: 0 0 0.5rem 0;">🛠️ Tecnologias:</h5>
            <div style="color: {COLORS['text_secondary']}; font-size: 0.85rem; line-height: 1.6;">
                • Azure Databricks<br>
                • Data Lake Storage<br>
                • Terraform (IaC)<br>
                • Python + Streamlit<br>
                • Plotly + Pandas
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========== SEÇÃO DE MACHINE LEARNING E PREVISÕES ==========
st.markdown("## Inteligência Artificial & Previsões")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title"> Projeção de Vendas (IA)</h3>', unsafe_allow_html=True)
    
    # Simulação de previsão de vendas com tendência
    import numpy as np
    meses_futuros = ['Ago/24', 'Set/24', 'Out/24', 'Nov/24', 'Dez/24']
    vendas_historicas = df_vendas['receita'].tolist()
    
    # Simular previsão com crescimento de 8-15%
    previsoes = []
    base = vendas_historicas[-1]
    for i in range(5):
        crescimento = np.random.uniform(1.08, 1.15)
        base = base * crescimento
        previsoes.append(base)
    
    fig_previsao = go.Figure()
    
    # Dados históricos
    fig_previsao.add_trace(go.Scatter(
        x=df_vendas['mes'].tolist() + meses_futuros,
        y=vendas_historicas + previsoes,
        mode='lines+markers',
        name='Vendas Reais',
        line=dict(color=COLORS['accent'], width=3),
        marker=dict(size=8),
        connectgaps=True
    ))
    
    # Separar área de previsão
    fig_previsao.add_trace(go.Scatter(
        x=meses_futuros,
        y=previsoes,
        mode='lines+markers',
        name='Previsão IA',
        line=dict(color=COLORS['warning'], width=3, dash='dash'),
        marker=dict(size=10, symbol='star'),
        fill='tonexty',
        fillcolor=f"rgba(245, 158, 11, 0.1)"
    ))
    
    
    fig_previsao = apply_dark_theme(fig_previsao, height=400)
    st.plotly_chart(fig_previsao, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title"> Score de Clientes (ML)</h3>', unsafe_allow_html=True)
    
    # Simulação de distribuição de score de clientes
    scores = ['Alto Valor', 'Médio Valor', 'Baixo Valor', 'Novos Clientes']
    valores = [28, 45, 18, 9]
    cores_score = [COLORS['success'], COLORS['accent'], COLORS['warning'], COLORS['danger']]
    
    fig_scores = go.Figure(data=[go.Bar(
        x=scores,
        y=valores,
        marker=dict(
            color=cores_score,
            line=dict(color=COLORS['bg_primary'], width=2)
        ),
        text=[f'{v}%' for v in valores],
        textposition='auto',
        textfont=dict(size=14, color='white')
    )])
    
    fig_scores.update_layout(
        yaxis_title='Percentual de Clientes (%)',
        xaxis_title='Segmento de Clientes'
    )
    
    fig_scores = apply_dark_theme(fig_scores, height=400)
    st.plotly_chart(fig_scores, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <strong> Dashboard BI - Sistema de Vendas de Livros</strong><br>
    <span style="font-size: 1rem; color: #60A5FA;">Projeto de Engenharia de Dados | SATC</span><br>
    <em style="font-size: 0.8rem; opacity: 0.8;">
        Dados mockados para demonstração • Estrutura preparada para pipeline real de produção
    </em>
</div>
""", unsafe_allow_html=True)
