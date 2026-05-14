# Deploy no Streamlit Cloud

Este projeto esta preparado para deploy no Streamlit Cloud usando GitHub.

## Arquivos importantes

- `streamlit_app.py`: arquivo principal do app.
- `requirements.txt`: dependencias instaladas pelo Streamlit Cloud.
- `runtime.txt`: versao de Python sugerida para o Cloud.
- `.streamlit/config.toml`: tema visual do app.
- `data/raw`: CSVs versionados usados pelo app.

## Publicar no GitHub

Com Git instalado:

```powershell
cd olist_ecommerce_portfolio
git init
git add .
git commit -m "Prepare Streamlit Cloud deployment"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/olist_ecommerce_portfolio.git
git push -u origin main
```

Antes do push, confira se os arquivos grandes estao dentro do limite do GitHub. Nesta versao, os CSVs em `data/raw` ficam abaixo do limite individual de 100 MB.

## Criar app no Streamlit Cloud

1. Acesse Streamlit Cloud.
2. Escolha o repositorio publicado no GitHub.
3. Defina o arquivo principal como `streamlit_app.py`.
4. Salve e aguarde o build.

## Observacoes

- O app nao depende de caminhos locais como `F:\dados_olist`.
- A tabela `olist_geolocation_dataset.csv` e opcional nesta versao.
- Os notebooks foram limpos sem outputs para evitar paths locais e reduzir ruido no GitHub.
- Arquivos gerados por notebooks em `data/interim`, `data/processed`, `models` e `reports/figures` ficam ignorados pelo Git.
