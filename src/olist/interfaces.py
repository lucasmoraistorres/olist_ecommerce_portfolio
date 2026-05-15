import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
FIGURES_DIR = BASE_DIR / "reports" / "figures"

def componentes():
    st.markdown("""
    <style>

    .section-title {
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
                
    .section-header {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }
                
    .orange-line {
        width: 80px;
        height: 4px;
        background-color: #F58518;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
                
    .blue-line {
        width: 80px;
        height: 4px;
        background-color: #3B82F6;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
                
    .highlight-box {
        background-color: #EAF4FF;
        border-left: 6px solid #3B82F6;
        padding: 1.5rem;
        border-radius: 10px;
        font-size: 1.1rem;
        line-height: 1.7;
        margin-bottom: 1.5rem;
    }

    .hypothesis-card {
        padding: 1rem 0.5rem;
        margin-bottom: 1rem;
    }

    .h-code {
        color: #F97316;
        font-size: 1.7rem;
        font-weight: 800;
        margin-bottom: 0.6rem;
    }

    .h-text {
        font-size: 1rem;
        line-height: 1.2;
    }


    .section-text {
        font-size: 1.1rem;
        line-height: 1.8;
        margin-bottom: 3rem;
    }

    .icon-box {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        border: 4px solid #F97316;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: auto;
        margin-bottom: 1rem;
        font-size: 2rem;
    }

    .card-title {
        text-align: center;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }

    .card-text {
        text-align: center;
        font-size: 1rem;
        line-height: 1.6;
        color: #333;
    }

    .footer-box {
        margin-top: 3rem;
        background: linear-gradient(90deg, #1f77b4, #4C78A8);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 600;
    }

    .insight-box-blue {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 14px;
        border-left: 6px solid #1f77b4;
    }
                
    .insight-box-orange {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 14px;
    border-right: 6px solid #F58518;
    } 
                
    .insight-box-recomendacoes {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 14px;
    border-left: 6px solid #F58518;
    border-right: 6px solid #1f77b4;
    }
                
    </style>
    """, unsafe_allow_html=True)

def slide_contexto():
    st.markdown("""
    <div class="highlight-box">
    <div class="section-title">Contexto do Negócio</div>

    Em plataformas de e-commerce como a **Olist**, a satisfação do cliente não depende apenas da qualidade do produto.
    A experiência é resultado de uma cadeia que combina produto, vendedor, pagamento, prazo prometido, entrega real e atendimento pós-venda.
    Pequenas fricções nessa cadeia podem reduzir significativamente reviews, recompra e reputação do marketplace.
                
    Este projeto investigou quais fatores possuem maior associação com reviews ruins
    e se seria possível antecipar clientes com maior risco de insatisfação.
    </div>

    """, unsafe_allow_html=True)

def slide_hipoteses():

    # =====================================================
    # TÍTULO
    # =====================================================
    st.markdown("""
    <div class="section-title">
    Cinco Perguntas Guiaram a Investigação
    </div>

    <div class="orange-line"></div>
    """, unsafe_allow_html=True)



    # =====================================================
    # GRID DAS HIPÓTESES
    # =====================================================
    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="hypothesis-card">
            <div class="h-code">H1</div>
            <div class="h-text">
            Pedidos entregues com atraso têm maior chance de review baixo
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hypothesis-card">
            <div class="h-code">H3</div>
            <div class="h-text">
            Categorias e estados específicos concentram atrasos e insatisfação
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hypothesis-card">
            <div class="h-code">H5</div>
            <div class="h-text">
            Um modelo simples consegue ranquear pedidos por risco de review baixo melhor que uma regra manual
            </div>
        </div>
        """, unsafe_allow_html=True)


    with col2:

        st.markdown("""
        <div class="hypothesis-card">
            <div class="h-code">H2</div>
            <div class="h-text">
            Frete alto em relação ao valor dos produtos prejudica a avaliação
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hypothesis-card">
            <div class="h-code">H4</div>
            <div class="h-text">
            Pedidos com maior complexidade operacional têm pior experiência
            </div>
        </div>
        """, unsafe_allow_html=True)

def slide_consolida_bases():

    # =========================================================
    # TÍTULO
    # =========================================================

    st.markdown("""
    <div class="section-title">
    Consolidação de Múltiplas Fontes em Base Analítica Única
    </div>

    <div class="blue-line"></div>
    """, unsafe_allow_html=True)


    # =========================================================
    # TEXTO
    # =========================================================

    st.markdown("""
    <div class="section-text">

    O dataset da **Olist** possui múltiplas tabelas relacionadas a clientes,
    pedidos, pagamentos, produtos, vendedores e reviews.

    A preparação envolveu:

    </div>
    """, unsafe_allow_html=True)


    # =========================================================
    # CARDS
    # =========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="icon-box">🗂️</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card-title">
        Consolidação
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card-text">
        Integração de informações de múltiplas tabelas relacionais
        </div>
        """, unsafe_allow_html=True)


    with col2:

        st.markdown("""
        <div class="icon-box">🧹</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card-title">
        Tratamento
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card-text">
        Limpeza de dados ausentes e conversão de formatos de datas
        </div>
        """, unsafe_allow_html=True)


    with col3:

        st.markdown("""
        <div class="icon-box">📈</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card-title">
        Métricas Derivadas
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card-text">
        Criação de variáveis:
        atraso, complexidade e proporção frete/valor
        </div>
        """, unsafe_allow_html=True)


    # =========================================================
    # FOOTER
    # =========================================================

    st.markdown("""
    <div class="footer-box">
    Base analítica única pronta para investigação de hipóteses
    </div>
    """, unsafe_allow_html=True)

def slide_atraso_experiencia_cliente():

    # =========================================================
    # TÍTULO
    # =========================================================
    st.header('Atraso e Experiência do Cliente')

    col1, col2, col3 = st.columns([1.3, 1, 1])
    with col1:
        st.markdown("""
        <div class='insight-box-blue'>
                    
        A maior parte das avaliações estão concentradas em notas altas, principalmente 4 e 5 estrelas:
        Já a distribuição dos atrasos mostra que maioria dos pedidos são entregues no prazo ou antes (< 0).\n
        Mas ainda existe um volume relevante de baixas avaliações, e de pedidos entregues fora do prazo (> 0) que foram tratadas no projeto como indicativo de experiência negativa.\n
        O cenário é relativamente saudável no geral, mas com oportunidades claras de melhoria operacional.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.image(
            str(FIGURES_DIR / "01_reviews.png"),
            width=600,

        )

    with col3:
        st.image(
            str(FIGURES_DIR / "01_atrasos.png"),
            width=500

        )


def slide_h1():
        
    # =========================================================
    # TÍTULO
    # =========================================================
    st.header("H1- Impacto operacional do atraso")


    col1, col2 = st.columns([1, 1])


    with col1:
        st.image(
            str(FIGURES_DIR / "02_h1_atraso_review_baixo.png"),
            use_container_width=True
        )

    with col2:

        st.markdown("""
        <div class='insight-box-orange'>

        ##### Conclusão
                    
        Pedidos entregues com atraso apresentaram taxa significativamente maior de reviews negativas, indicando que a experiência de entrega possui forte impacto na percepção do cliente.

        ##### Implicação Operacional
        Melhorar previsibilidade logística e cumprimento de SLA pode reduzir significativamente avaliações negativas.

        ##### Observação
        Embora a análise não permita afirmar causalidade direta, a magnitude e consistência do efeito tornam o atraso um forte indicador de risco operacional.
                    
        </div>

        """, unsafe_allow_html=True)


def slide_h2():
    st.header("H2 - Frete relativo vs satisfação")

    col1, col2 = st.columns([1, 1])   

    with col2:
        st.image(
            str(FIGURES_DIR / "02_h2_frete_relativo.png"),
            use_container_width=True
        )

    with col1:
        st.markdown("""
    <div class='insight-box-blue'>

    ##### Conclusão

    A proporção de reviews negativas variou pouco entre as diferentes faixas de frete relativo, sugerindo associação limitada entre custo do frete e satisfação.

    ##### Implicação Operacional
    Os resultados indicam que previsibilidade e cumprimento da entrega parecem influenciar mais a experiência do cliente do que pequenas diferenças proporcionais no frete.

    ##### Observação
    O efeito observado foi significativamente menor do que o impacto associado aos atrasos logísticos.

    </div>
    """, unsafe_allow_html=True)

def slide_h3_categoria():

    st.header("H3 - Categorias com maior criticidade")

    col1, col2 = st.columns([1, 0.8])

    with col1:
        st.image(
            str(FIGURES_DIR / "02_h3_criticidade_por_categorias.png"),
            use_container_width=True
        )

    with col2:
        st.markdown("""
    <div class='insight-box-orange'>

    ##### Conclusão
    O impacto dos atrasos variou significativamente entre categorias, com algumas apresentando sensibilidade muito maior a problemas de entrega.
                    
    ##### Implicação Operacional
    Estratégias segmentadas por categoria podem gerar ganhos mais eficientes de satisfação e redução de reviews negativas.
                    
    ##### Observação
    Categorias relacionadas à urgência ou expectativa de entrega apresentaram maior sensibilidade operacional.
    </div>
    """, unsafe_allow_html=True)

def slide_h3_estado():
    st.header("H3 - Estados com maior criticidade")

    col1, col2 = st.columns([0.8, 1])

    with col2:
        st.image(
            str(FIGURES_DIR / "02_h3_criticidade_por_estados.png"),
            use_container_width=True
        )

    with col1:
        st.markdown("""
    <div class='insight-box-blue'>

    ##### Conclusão
    A análise regional mostrou diferenças relevantes entre os estados, com algumas regiões concentrando simultaneamente maiores taxas de atraso e maior proporção de reviews negativas.
                    
    ##### Implicação Operacional
    Os resultados sugerem que fatores logísticos regionais possuem impacto importante na experiência do cliente, indicando oportunidades para estratégias segmentadas por região.
        
    ##### Observação
    Estados com infraestrutura logística mais desafiadora apresentaram maior concentração de problemas operacionais e insatisfação.
    </div>
    """, unsafe_allow_html=True)

def slide_h4():
    st.header("H4 - Complexidade operacional")

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.image(
            str(FIGURES_DIR / "02_h4_complexidade.png"),
            use_container_width=True
        )

    with col2:
        st.markdown("""
    <div class='insight-box-orange'>

    ##### Conclusão
    Pedidos mais complexos apresentaram aumento moderado na taxa de avaliações negativas, especialmente em cenários com maior fragmentação operacional.
                    
    ##### Implicação Operacional
    Operações mais complexas tendem a aumentar pontos de fricção durante a jornada do cliente.
        
    ##### Observação
    O efeito foi moderado quando comparado ao impacto observado nos atrasos.

    </div>
    """, unsafe_allow_html=True)

def slide_h5():
    
    st.header("H5 - Modelo preditivo")

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            str(FIGURES_DIR / "01_h5_threshold_analysis.png"),
            width=500
        )

    with col2:
        st.image(
            str(FIGURES_DIR / "02_h5_confusion_matrix.png"),
            width=300

        )

    st.markdown("""
    <div class='insight-box-blue'>

    ##### Conclusão
    O modelo conseguiu identificar razoavelmente bem pedidos com maior risco de avaliações negativas, demonstrando presença de sinal relevante nos dados.
                
    ##### Implicação Operacional
    Modelos preditivos podem apoiar monitoramento preventivo e priorização operacional.
        
    ##### Observação
    O modelo não foi construí­do para substituir completamente a análise operacional, mas para priorizar pedidos com maior probabilidade de insatisfação, reduzindo o volume de monitoramento necessário e aumentando a eficiência da detecão de casos crí­ticos.
    </div>
    """, unsafe_allow_html=True)

def slide_recomendacoes():

    st.header("Recomendações estratégicas")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
    <div class='insight-box-recomendacoes'>

    ##### Foco em Previsibilidade Logística

    - Aumentar monitoramento automatico de atrasos;
    - Implementar sistemas de alerta para pedidos de risco;
    - Priorizar melhoria de SLA em regiões e segmentos críticos.

    </div>
    """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
    <div class='insight-box-recomendacoes'>

    ##### Estratégias Segmentadas

    - Diferenciar abordagens por categoria de produto;
    - Investir em lógistica regional, especialmente em estados com maior criticidade;
    - Customizar prazos de entrega conforme sensibilidade da categoria.

    </div>
    """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
    <div class='insight-box-recomendacoes'>

    ##### Utilização de Modelos Preditivos

    - Implementar sistemas personalizados de scoring de risco;
    - Direcionar ações preventivas antes que a experiência negativa aconteça;
    - Monitorar continuamente performance do modelo.

    </div>
    """, unsafe_allow_html=True)

def slide_sobre_projeto():
    st.markdown("---")

    st.markdown("""
    ### Sobre o projeto

    Projeto de Ciência de Dados utilizando o dataset público da Olist.

    Tecnologias utilizadas:
    - Python
    - Pandas
    - Scikit-learn
    - Seaborn
    - Matplotlib
    - Streamlit

    Autor: **Lucas Morais Torres**\n
    Código Fonte e + análises do negócio: https://github.com/lucasmoraistorres/olist_ecommerce_portfolio
    """)