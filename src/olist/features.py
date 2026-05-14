from __future__ import annotations

import numpy as np
import pandas as pd


def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Cria variaveis de calendario a partir da data de compra."""
    out = df.copy()
    purchase_date = pd.to_datetime(out["order_purchase_timestamp"], errors="coerce")

    out["purchase_date"] = purchase_date.dt.date
    out["purchase_month"] = purchase_date.dt.to_period("M").astype("string")
    out["purchase_year"] = purchase_date.dt.year
    out["purchase_dayofweek"] = purchase_date.dt.dayofweek
    out["purchase_hour"] = purchase_date.dt.hour
    out["is_weekend_purchase"] = out["purchase_dayofweek"].isin([5, 6]).astype("int8")

    return out


def add_delivery_features(df: pd.DataFrame) -> pd.DataFrame:
    """Cria variaveis de prazo, atraso e velocidade de entrega."""
    out = df.copy()
    date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for col in date_cols:
        out[col] = pd.to_datetime(out[col], errors="coerce")

    out["approval_time_hours"] = (
        out["order_approved_at"] - out["order_purchase_timestamp"]
    ).dt.total_seconds() / 3600
    out["carrier_time_days"] = (
        out["order_delivered_carrier_date"] - out["order_approved_at"]
    ).dt.total_seconds() / 86400
    out["delivery_time_days"] = (
        out["order_delivered_customer_date"] - out["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    out["estimated_delivery_time_days"] = (
        out["order_estimated_delivery_date"] - out["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    out["delay_days"] = (
        out["order_delivered_customer_date"] - out["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400
    out["is_late"] = (out["delay_days"] > 0).astype("int8")
    out.loc[out["delay_days"].isna(), "is_late"] = np.nan

    return out


def add_review_target(df: pd.DataFrame, low_review_threshold: int = 2) -> pd.DataFrame:
    """Cria alvo binario para baixa satisfacao."""
    out = df.copy()
    out["is_low_review"] = (out["review_score"] <= low_review_threshold).astype("int8")
    out.loc[out["review_score"].isna(), "is_low_review"] = np.nan
    return out


def prepare_modeling_dataset(order_level: pd.DataFrame) -> pd.DataFrame:
    """Seleciona variaveis para modelagem no nivel de pedido."""
    df = add_review_target(add_delivery_features(add_temporal_features(order_level)))

    df = df[df["order_status"].eq("delivered")].copy()
    df = df[df["review_score"].notna()].copy()

    numeric_defaults = {
        "order_items": 0,
        "unique_products": 0,
        "unique_sellers": 0,
        "products_value": 0,
        "freight_value": 0,
        "total_order_value": 0,
        "payment_value": 0,
        "payment_installments": 0,
        "payment_methods": 0,
        "payment_count": 0,
        "total_weight_g": 0,
        "total_volume_cm3": 0,
    }

    for col, value in numeric_defaults.items():
        if col in df.columns:
            df[col] = df[col].fillna(value)

    df["freight_ratio"] = df["freight_ratio"].replace([np.inf, -np.inf], np.nan)
    df["freight_ratio"] = df["freight_ratio"].clip(lower=0, upper=df["freight_ratio"].quantile(0.99))
    df["dominant_category"] = df["dominant_category"].fillna("unknown")
    df["dominant_payment_type"] = df["dominant_payment_type"].fillna("unknown")

    return df

