from pathlib import Path
import sys

import streamlit as st


# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Olist Executive Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).resolve().parent
FIGURES_DIR = BASE_DIR / "reports" / "figures"
INTERFACES = BASE_DIR / "src"
if str(INTERFACES) not in sys.path:
    sys.path.append(str(INTERFACES))

from olist.interfaces import *
componentes()
st.markdown(
    """
    <div class="section-header">E-commerce Analytics</div>
    """, unsafe_allow_html=True)


# =========================================================
# ABAS E TITULO
# =========================================================


tab1, tab2, tab3 = st.tabs(["Problema de négocio", "Análise de Hipóteses", "Apresentação em vídeo"])

with tab1:

    slide_contexto()
    st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

    slide_hipoteses()
    st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

    slide_consolida_bases()
    st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

    
with tab2:

    # =========================================================
    # REVIEWS E ATRASO
    # =========================================================
    slide_atraso_experiencia_cliente()
    st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

    # =========================================================
    # H1
    # =========================================================
    slide_h1()
    st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

    # =========================================================
    # FRETE
    # =========================================================
    slide_h2()
    st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

    # =========================================================
    # CATEGORIAS
    # =========================================================
    slide_h3_categoria()
    st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

    # =========================================================
    # ESTADOS
    # =========================================================
    slide_h3_estado()
    st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

    # =========================================================
    # COMPLEXIDADE
    # =========================================================
    slide_h4()
    st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

    # =========================================================
    # MODELO
    # =========================================================
    slide_h5()
    st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

    # =========================================================
    # RECOMENDAÇÕES
    # =========================================================
    slide_recomendacoes()
    st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

    # =========================================================
    # FOOTER
    # =========================================================
    slide_sobre_projeto()
    st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

