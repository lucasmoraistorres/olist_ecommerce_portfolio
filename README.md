# Brazilian E-Commerce Olist: Análise de Negócio e Ciência de Dados

Projeto de ciência de dados usando o dataset público **Brazilian E-Commerce Public Dataset by Olist**.

O objetivo é construir um case completo, com narrativa executiva, notebooks reproduzíveis e um dashboard em Streamlit para responder:

> Quais fatores explicam desempenho comercial, atraso logístico e baixa satisfação dos clientes no marketplace da Olist, e como transformar esses sinais em ações de negócio?

## Entregáveis

- Análise exploratória e diagnóstico de qualidade dos dados.
- Modelo analítico no nível de pedido, integrando clientes, pedidos, itens, pagamentos, reviews, produtos e vendedores.
- Teste de hipóteses de negócio sobre atraso, frete, categorias, estados e satisfação.
- Dataset de modelagem para risco de review baixo.
- Modelo preditivo interpretável para priorização operacional.


## Fonte de dados

Os CSVs usados pelo app ficam versionados em:

```text
data/raw

## Estrutura

olist_ecommerce/
  data/
    raw/          # CSVs usados pelos notebooks
    interim/      # bases intermediárias geradas pelos notebooks
    processed/    # dataset final de modelagem
  models/         # modelos treinados localmente
  notebooks/      # roteiro executável do projeto
  references/     # problema de negócio, hipóteses e dicionários
  reports/
    figures/      # gráficos exportados localmente
  src/olist/      # funções reutilizáveis
  streamlit_app.py # entrada do dashboard no Streamlit Cloud

## Ordem recomendada dos notebooks
00_contexto.ipynb
01_eda_qualidade_e_integracao.ipynb
02_analise_negocio_e_hipoteses.ipynb
03_feature_engineering_e_dataset_modelagem.ipynb
04_modelo_review_baixo.ipynb
05_insights_e_recomendacoes.ipynb


## Para trabalhar também com os notebooks:

pip install -r requirements-dev.txt
jupyter notebook

## Deploy no Streamlit Cloud
Publique este diretório em um repositório do GitHub.
No Streamlit Cloud, crie um novo app apontando para esse repositório.
Use streamlit_app.py como arquivo principal.
Mantenha requirements.txt na raiz do projeto.

## Observação metodológica
O modelo preditivo deste projeto está sendo apresentado como ferramenta de priorização e diagnóstico, não como prova causal. As hipóteses de negócio são avaliadas com evidências observacionais; qualquer decisão de produto, logística ou política comercial deveria ser confirmada com experimento ou acompanhamento operacional.