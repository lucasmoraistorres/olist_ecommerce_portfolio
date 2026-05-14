from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
MODELS_DIR = PROJECT_ROOT / "models"

DEFAULT_RAW_DATA_DIR = DATA_DIR / "raw"
RAW_DATA_DIR = Path(os.getenv("OLIST_DATA_DIR", DEFAULT_RAW_DATA_DIR))

CSV_FILES = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

OPTIONAL_TABLES = {"geolocation"}
REQUIRED_TABLES = set(CSV_FILES) - OPTIONAL_TABLES


def ensure_project_dirs() -> None:
    """Garante que os diretorios de saida existem."""
    for path in [DATA_DIR, INTERIM_DATA_DIR, PROCESSED_DATA_DIR, REPORTS_DIR, FIGURES_DIR, MODELS_DIR]:
        path.mkdir(parents=True, exist_ok=True)
