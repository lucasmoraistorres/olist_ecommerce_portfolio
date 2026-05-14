# Brazilian E-Commerce Olist: Analise de Negocio e Ciencia de Dados

Projeto de portfolio de ciencia de dados usando o dataset publico **Brazilian E-Commerce Public Dataset by Olist**.

O objetivo e construir um case completo, com narrativa executiva, notebooks reproduziveis e um dashboard em Streamlit para responder:

> Quais fatores explicam desempenho comercial, atraso logistico e baixa satisfacao dos clientes no marketplace da Olist, e como transformar esses sinais em acoes de negocio?

## Entregaveis

- Analise exploratoria e diagnostico de qualidade dos dados.
- Modelo analitico no nivel de pedido, integrando clientes, pedidos, itens, pagamentos, reviews, produtos e vendedores.
- Teste de hipoteses de negocio sobre atraso, frete, categorias, estados e satisfacao.
- Dataset de modelagem para risco de review baixo.
- Modelo preditivo interpretavel para priorizacao operacional.
- Dashboard Streamlit pronto para deploy no Streamlit Cloud.

## Fonte de dados

Os CSVs usados pelo app ficam versionados em:

```text
data/raw
```

Durante desenvolvimento local, voce ainda pode usar outro diretorio definindo a variavel de ambiente `OLIST_DATA_DIR`. No Streamlit Cloud, o projeto usa `data/raw` por padrao. A tabela de geolocalizacao e opcional nesta versao do dashboard.

## Estrutura

```text
olist_ecommerce_portfolio/
  data/
    raw/          # CSVs usados pelo Streamlit Cloud
    interim/      # bases intermediarias geradas pelos notebooks
    processed/    # dataset final de modelagem
  models/         # modelos treinados localmente
  notebooks/      # roteiro executavel do projeto
  references/     # problema de negocio, hipoteses e dicionarios
  reports/
    figures/      # graficos exportados localmente
  src/olist/       # funcoes reutilizaveis
  streamlit_app.py # entrada do dashboard no Streamlit Cloud
```

## Ordem recomendada dos notebooks

1. `00_contexto.ipynb`
2. `01_eda_qualidade_e_integracao.ipynb`
3. `02_analise_negocio_e_hipoteses.ipynb`
4. `03_feature_engineering_e_dataset_modelagem.ipynb`
5. `04_modelo_review_baixo.ipynb`
6. `05_insights_e_recomendacoes.ipynb`

## Como executar localmente

```powershell
cd olist_ecommerce_portfolio
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Para trabalhar tambem com os notebooks:

```powershell
pip install -r requirements-dev.txt
jupyter notebook
```

## Deploy no Streamlit Cloud

1. Publique este diretorio em um repositorio do GitHub.
2. No Streamlit Cloud, crie um novo app apontando para esse repositorio.
3. Use `streamlit_app.py` como arquivo principal.
4. Mantenha `requirements.txt` na raiz do projeto.

## Observacao metodologica

O modelo preditivo deste projeto deve ser apresentado como ferramenta de priorizacao e diagnostico, nao como prova causal. As hipoteses de negocio sao avaliadas com evidencias observacionais; qualquer decisao de produto, logistica ou politica comercial deveria ser confirmada com experimento ou acompanhamento operacional.
