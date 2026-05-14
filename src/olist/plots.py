from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns


def set_plot_style() -> None:
    """Configura estilo visual padrao dos graficos."""
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams["figure.figsize"] = (12, 6)
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.labelsize"] = 11


def save_current_figure(path: str | Path, dpi: int = 160) -> None:
    """Salva a figura atual garantindo a existencia do diretorio."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches="tight")

