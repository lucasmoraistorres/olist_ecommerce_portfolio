from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.append(str(SRC_PATH))

from olist.config import RAW_DATA_DIR  # noqa: E402
from olist.data import build_order_level_dataset, load_all, load_table, validate_raw_files  # noqa: E402
from olist.features import add_delivery_features, add_review_target, add_temporal_features  # noqa: E402


st.set_page_config(
    page_title="Olist Ecommerce Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner="Carregando e integrando os dados da Olist...")
def load_order_level() -> pd.DataFrame:
    tables = load_all(include_geolocation=False)
    order_level = build_order_level_dataset(tables)
    order_level = add_temporal_features(order_level)
    order_level = add_delivery_features(order_level)
    order_level = add_review_target(order_level)
    order_level["order_purchase_timestamp"] = pd.to_datetime(
        order_level["order_purchase_timestamp"], errors="coerce"
    )
    return order_level


@st.cache_data(show_spinner="Calculando indicadores por vendedor...")
def load_seller_risk(delivered_orders: pd.DataFrame) -> pd.DataFrame:
    items = load_table("order_items")
    seller_orders = items[["order_id", "seller_id"]].drop_duplicates()

    return (
        seller_orders.merge(
            delivered_orders[["order_id", "review_score", "is_low_review", "is_late"]],
            on="order_id",
            how="inner",
        )
        .groupby("seller_id")
        .agg(
            orders=("order_id", "nunique"),
            avg_review=("review_score", "mean"),
            late_rate=("is_late", "mean"),
            low_review_rate=("is_low_review", "mean"),
        )
        .reset_index()
    )


def percent(value: float | int | None) -> str:
    if pd.isna(value):
        return "-"
    return f"{value:.1%}"


def money(value: float | int | None) -> str:
    if pd.isna(value):
        return "-"
    return f"R$ {value:,.0f}".replace(",", ".")


def metric_row(df: pd.DataFrame) -> None:
    orders = df["order_id"].nunique()
    revenue = df["products_value"].sum()
    avg_review = df["review_score"].mean()
    low_review_rate = df["is_low_review"].mean()
    late_rate = df["is_late"].mean()
    avg_delivery = df["delivery_time_days"].mean()

    cols = st.columns(6)
    cols[0].metric("Pedidos", f"{orders:,.0f}".replace(",", "."))
    cols[1].metric("Valor produtos", money(revenue))
    cols[2].metric("Review medio", f"{avg_review:.2f}" if pd.notna(avg_review) else "-")
    cols[3].metric("Review baixo", percent(low_review_rate))
    cols[4].metric("Atraso", percent(late_rate))
    cols[5].metric("Entrega media", f"{avg_delivery:.1f} dias" if pd.notna(avg_delivery) else "-")


def bar_chart(data: pd.DataFrame, x: str, y: str, title: str, xlabel: str = "", ylabel: str = ""):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=data, x=x, y=y, ax=ax, color="#2563EB")
    ax.set_title(title, loc="left", fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis="x", alpha=0.25)
    return fig


def line_chart(data: pd.DataFrame, x: str, y: str, title: str, ylabel: str = ""):
    fig, ax = plt.subplots(figsize=(11, 5))
    sns.lineplot(data=data, x=x, y=y, marker="o", ax=ax, color="#2563EB")
    ax.set_title(title, loc="left", fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=45)
    ax.grid(alpha=0.25)
    return fig


def build_segment_table(df: pd.DataFrame, group_col: str, min_orders: int) -> pd.DataFrame:
    summary = (
        df.groupby(group_col)
        .agg(
            orders=("order_id", "nunique"),
            products_value=("products_value", "sum"),
            avg_review=("review_score", "mean"),
            late_rate=("is_late", "mean"),
            low_review_rate=("is_low_review", "mean"),
            avg_delivery_days=("delivery_time_days", "mean"),
        )
        .query("orders >= @min_orders")
        .sort_values(["low_review_rate", "orders"], ascending=[False, False])
        .reset_index()
    )
    return summary


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filtros")

    min_date = df["order_purchase_timestamp"].min().date()
    max_date = df["order_purchase_timestamp"].max().date()
    selected_dates = st.sidebar.date_input(
        "Periodo da compra",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date, end_date = min_date, max_date

    states = sorted(df["customer_state"].dropna().unique().tolist())
    selected_states = st.sidebar.multiselect("Estados", states, default=states)

    categories = sorted(df["dominant_category"].dropna().unique().tolist())
    default_categories = categories[:]
    selected_categories = st.sidebar.multiselect(
        "Categorias",
        categories,
        default=default_categories,
    )

    filtered = df[
        df["order_purchase_timestamp"].dt.date.between(start_date, end_date)
        & df["customer_state"].isin(selected_states)
        & df["dominant_category"].isin(selected_categories)
    ].copy()

    return filtered


st.title("Olist Ecommerce Analytics")
st.caption("Dashboard de portfolio para diagnostico comercial, logistico e satisfacao do cliente.")

file_status = validate_raw_files()
missing_required = file_status[file_status["required"] & ~file_status["exists"]]

with st.expander("Status dos arquivos de dados", expanded=False):
    st.dataframe(file_status, use_container_width=True)

if not missing_required.empty:
    st.error(
        "Arquivos obrigatorios ausentes em data/raw. Confira o repositorio antes de fazer o deploy."
    )
    st.stop()

try:
    order_level = load_order_level()
except Exception as exc:
    st.exception(exc)
    st.stop()

delivered = order_level[
    order_level["order_status"].eq("delivered") & order_level["review_score"].notna()
].copy()

filtered = apply_filters(delivered)

st.sidebar.markdown("---")
st.sidebar.write(f"Fonte de dados: `{RAW_DATA_DIR}`")
st.sidebar.write(f"Pedidos filtrados: {filtered['order_id'].nunique():,.0f}".replace(",", "."))

if filtered.empty:
    st.warning("Nenhum pedido encontrado para os filtros selecionados.")
    st.stop()

metric_row(filtered)

tab_overview, tab_satisfaction, tab_logistics, tab_segments, tab_actions = st.tabs(
    ["Visao geral", "Satisfacao", "Logistica", "Segmentos", "Prioridades"]
)

with tab_overview:
    monthly = (
        filtered.groupby("purchase_month")
        .agg(
            orders=("order_id", "nunique"),
            products_value=("products_value", "sum"),
            avg_review=("review_score", "mean"),
        )
        .reset_index()
    )
    monthly["purchase_month"] = monthly["purchase_month"].astype(str)

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(line_chart(monthly, "purchase_month", "orders", "Pedidos por mes", "Pedidos"))
    with col2:
        st.pyplot(
            line_chart(
                monthly,
                "purchase_month",
                "products_value",
                "Valor de produtos por mes",
                "Valor de produtos",
            )
        )

    st.subheader("Amostra da base integrada")
    st.dataframe(
        filtered[
            [
                "order_id",
                "customer_state",
                "dominant_category",
                "products_value",
                "freight_value",
                "review_score",
                "delay_days",
            ]
        ].head(1000),
        use_container_width=True,
    )

with tab_satisfaction:
    review_dist = (
        filtered["review_score"].value_counts().sort_index().rename_axis("review_score").reset_index(name="orders")
    )
    review_dist["review_score"] = review_dist["review_score"].astype(str)
    late_summary = (
        filtered.dropna(subset=["is_late"])
        .groupby("is_late")
        .agg(
            orders=("order_id", "nunique"),
            avg_review=("review_score", "mean"),
            low_review_rate=("is_low_review", "mean"),
        )
        .reset_index()
    )
    late_summary["status"] = late_summary["is_late"].map({0: "No prazo", 1: "Atrasado"})

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(bar_chart(review_dist, "orders", "review_score", "Distribuicao das notas", "Pedidos", "Nota"))
    with col2:
        st.pyplot(
            bar_chart(
                late_summary,
                "low_review_rate",
                "status",
                "Taxa de review baixo por atraso",
                "Review baixo",
                "",
            )
        )

    st.dataframe(late_summary, use_container_width=True)

with tab_logistics:
    delay_bins = filtered.copy()
    delay_bins["delay_range"] = pd.cut(
        delay_bins["delay_days"],
        bins=[-999, -10, -3, 0, 3, 10, 999],
        labels=[">10 dias antes", "3-10 dias antes", "No prazo", "1-3 dias atraso", "4-10 dias atraso", ">10 dias atraso"],
    )
    delay_summary = (
        delay_bins.groupby("delay_range", observed=True)
        .agg(orders=("order_id", "nunique"), avg_review=("review_score", "mean"), low_review_rate=("is_low_review", "mean"))
        .reset_index()
    )
    delay_summary["delay_range"] = delay_summary["delay_range"].astype(str)

    st.pyplot(
        bar_chart(
            delay_summary,
            "low_review_rate",
            "delay_range",
            "Review baixo por faixa de atraso",
            "Review baixo",
            "",
        )
    )
    st.dataframe(delay_summary, use_container_width=True)

with tab_segments:
    min_orders = st.slider("Volume minimo por segmento", min_value=20, max_value=1000, value=200, step=20)

    category_risk = build_segment_table(filtered, "dominant_category", min_orders)
    state_risk = build_segment_table(filtered, "customer_state", min_orders)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Categorias com maior risco")
        st.dataframe(category_risk.head(20), use_container_width=True)
    with col2:
        st.subheader("Estados com maior risco")
        st.dataframe(state_risk.head(20), use_container_width=True)

with tab_actions:
    st.subheader("Fila de investigacao operacional")
    st.write(
        "Esta tabela prioriza segmentos com volume relevante, alta taxa de review baixo e atraso. "
        "Ela deve ser usada como ponto de partida para analise humana, nao como decisao automatica."
    )

    priority_categories = build_segment_table(filtered, "dominant_category", min_orders=100)
    priority_categories["priority_score"] = (
        priority_categories["low_review_rate"].rank(pct=True)
        + priority_categories["late_rate"].rank(pct=True)
        + priority_categories["orders"].rank(pct=True)
    ) / 3
    priority_categories = priority_categories.sort_values("priority_score", ascending=False)

    st.dataframe(priority_categories.head(15), use_container_width=True)

    seller_risk = load_seller_risk(filtered)
    seller_risk = seller_risk.query("orders >= 50").sort_values(
        ["low_review_rate", "orders"], ascending=[False, False]
    )
    st.subheader("Vendedores para investigacao")
    st.dataframe(seller_risk.head(20), use_container_width=True)

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Baixar base filtrada",
        data=csv,
        file_name="olist_filtered_orders.csv",
        mime="text/csv",
    )
