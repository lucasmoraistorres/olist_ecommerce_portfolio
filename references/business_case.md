# Case de negocio

## Contexto

A Olist conecta vendedores a clientes finais em um marketplace. A experiencia do cliente depende de uma cadeia que combina produto, vendedor, pagamento, prazo prometido, entrega real e pos-venda. Pequenas friccoes nessa cadeia podem reduzir reviews, recompra e reputacao do marketplace.

## Problema de negocio

Identificar fatores associados a baixa satisfacao do cliente e atraso logistico, priorizando oportunidades que possam ser traduzidas em acoes praticas para operacoes, seller success, pricing de frete e experiencia do cliente.

## Perguntas principais

1. Quais estados, categorias e vendedores concentram maior volume e maior risco de baixa satisfacao?
2. Atrasos de entrega explicam uma parte relevante dos reviews baixos?
3. O peso do frete no valor do pedido esta associado a pior avaliacao?
4. Pedidos com mais itens, mais vendedores ou maior complexidade logistica apresentam maior risco?
5. E possivel construir um modelo simples para priorizar pedidos com maior probabilidade de review baixo?

## Hipoteses

- H1: pedidos entregues com atraso tem taxa de review baixo maior do que pedidos entregues no prazo.
- H2: quanto maior a proporcao de frete sobre o valor dos produtos, maior o risco de review baixo.
- H3: algumas categorias de produto concentram atrasos e reviews baixos de forma desproporcional.
- H4: estados mais distantes dos principais polos vendedores apresentam prazo e atraso maiores.
- H5: pedidos com maior complexidade, como varios itens ou varios vendedores, tem pior experiencia media.
- H6: um modelo com informacoes de pedido, cliente, pagamento, produto e entrega consegue ranquear pedidos por risco de review baixo melhor do que uma regra simples.

## Publico-alvo da apresentacao

Gestores de marketplace, operacoes logisticas, seller success, produto e analytics.

## Cuidado analitico

As analises sao observacionais. Correlacao nao deve ser apresentada como causalidade. Quando houver recomendacao operacional, ela deve ser acompanhada por proposta de validacao: teste A/B, piloto regional, monitoramento antes/depois ou experimento controlado.
