from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from .config import CSV_FILES, OPTIONAL_TABLES, RAW_DATA_DIR


DATE_COLUMNS = {
    "orders": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "order_items": ["shipping_limit_date"],
    "order_reviews": ["review_creation_date", "review_answer_timestamp"],
}


def _as_path(path: str | Path | None) -> Path:
    return Path(path) if path is not None else RAW_DATA_DIR


def validate_raw_files(raw_data_dir: str | Path | None = None) -> pd.DataFrame:
    """Retorna uma tabela com status dos arquivos esperados."""
    base_dir = _as_path(raw_data_dir)
    rows = []

    for table_name, file_name in CSV_FILES.items():
        path = base_dir / file_name
        exists = path.exists()
        rows.append(
            {
                "table": table_name,
                "file_name": file_name,
                "path": str(path),
                "required": table_name not in OPTIONAL_TABLES,
                "exists": exists,
                "size_mb": round(path.stat().st_size / 1024**2, 2) if exists else None,
            }
        )

    return pd.DataFrame(rows)


def load_table(
    table_name: str,
    raw_data_dir: str | Path | None = None,
    parse_dates: bool = True,
    **read_csv_kwargs: Any,
) -> pd.DataFrame:
    """Carrega uma tabela do dataset Olist pelo nome logico."""
    if table_name not in CSV_FILES:
        valid = ", ".join(sorted(CSV_FILES))
        raise KeyError(f"Tabela desconhecida: {table_name}. Opcoes validas: {valid}")

    path = _as_path(raw_data_dir) / CSV_FILES[table_name]
    date_cols = DATE_COLUMNS.get(table_name, []) if parse_dates else []
    return pd.read_csv(path, parse_dates=date_cols, **read_csv_kwargs)


def load_all(
    raw_data_dir: str | Path | None = None,
    include_geolocation: bool = False,
    nrows: int | None = None,
) -> dict[str, pd.DataFrame]:
    """Carrega as tabelas principais em um dicionario."""
    tables: dict[str, pd.DataFrame] = {}

    for table_name in CSV_FILES:
        if table_name == "geolocation" and not include_geolocation:
            continue
        kwargs = {"nrows": nrows} if nrows is not None else {}
        tables[table_name] = load_table(table_name, raw_data_dir=raw_data_dir, **kwargs)

    return tables


def first_mode(series: pd.Series) -> Any:
    """Retorna a moda mais frequente, com fallback para valor ausente."""
    values = series.dropna()
    if values.empty:
        return pd.NA
    mode = values.mode()
    return mode.iloc[0] if not mode.empty else values.iloc[0]


def build_order_items_agg(
    items: pd.DataFrame,
    products: pd.DataFrame,
    translations: pd.DataFrame,
) -> pd.DataFrame:
    """Agrega itens, produtos e categorias para o nivel de pedido."""
    item_product = items.merge(products, on="product_id", how="left")
    item_product = item_product.merge(translations, on="product_category_name", how="left")
    item_product["product_category_name_english"] = item_product[
        "product_category_name_english"
    ].fillna(item_product["product_category_name"])

    item_product["item_volume_cm3"] = (
        item_product["product_length_cm"]
        * item_product["product_height_cm"]
        * item_product["product_width_cm"]
    )

    return (
        item_product.groupby("order_id")
        .agg(
            order_items=("order_item_id", "max"),
            unique_products=("product_id", "nunique"),
            unique_sellers=("seller_id", "nunique"),
            products_value=("price", "sum"),
            freight_value=("freight_value", "sum"),
            avg_item_price=("price", "mean"),
            total_weight_g=("product_weight_g", "sum"),
            total_volume_cm3=("item_volume_cm3", "sum"),
            dominant_category=("product_category_name_english", first_mode),
        )
        .reset_index()
    )


def build_payments_agg(payments: pd.DataFrame) -> pd.DataFrame:
    """Agrega pagamentos para o nivel de pedido."""
    return (
        payments.groupby("order_id")
        .agg(
            payment_value=("payment_value", "sum"),
            payment_installments=("payment_installments", "max"),
            payment_methods=("payment_type", "nunique"),
            payment_count=("payment_sequential", "max"),
            dominant_payment_type=("payment_type", first_mode),
        )
        .reset_index()
    )


def build_reviews_agg(reviews: pd.DataFrame) -> pd.DataFrame:
    """Agrega reviews para o nivel de pedido."""
    tmp = reviews.copy()
    tmp["has_review_comment"] = tmp["review_comment_message"].notna()
    return (
        tmp.groupby("order_id")
        .agg(
            review_score=("review_score", "mean"),
            review_count=("review_id", "nunique"),
            has_review_comment=("has_review_comment", "max"),
            review_creation_date=("review_creation_date", "max"),
        )
        .reset_index()
    )


def build_order_level_dataset(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Integra as tabelas principais no nivel de pedido."""
    orders = tables["orders"].copy()

    item_agg = build_order_items_agg(
        tables["order_items"],
        tables["products"],
        tables["category_translation"],
    )
    payment_agg = build_payments_agg(tables["order_payments"])
    review_agg = build_reviews_agg(tables["order_reviews"])

    order_level = (
        orders.merge(tables["customers"], on="customer_id", how="left")
        .merge(item_agg, on="order_id", how="left")
        .merge(payment_agg, on="order_id", how="left")
        .merge(review_agg, on="order_id", how="left")
    )

    order_level["total_order_value"] = (
        order_level["products_value"].fillna(0) + order_level["freight_value"].fillna(0)
    )
    order_level["freight_ratio"] = order_level["freight_value"] / order_level["products_value"]
    order_level["freight_ratio"] = order_level["freight_ratio"].replace(
        [float("inf"), float("-inf")], pd.NA
    )

    return order_level
