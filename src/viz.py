"""Estilo visual consistente para todos los notebooks"""
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

PALETA = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
          "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

def setup_plotting_style():
    plt.style.use("seaborn-v0_8-whitegrid")
    sns.set_palette(PALETA)
    plt.rcParams.update({
        "figure.figsize": (10, 5.5),
        "figure.dpi": 120,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "legend.fontsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
    })

def fig_ax(**kwargs):
    """Wrapper para fig, ax con estilo consistente"""
    setup_plotting_style()
    return plt.subplots(**kwargs)

def save_fig(name, subdir="figures"):
    """Guarda figura en reports/figures/ con nombre consistente"""
    path = Path(__file__).parents[1] / "reports" / subdir
    path.mkdir(parents=True, exist_ok=True)
    plt.savefig(path / f"{name}.png", dpi=200, bbox_inches="tight")
    plt.savefig(path / f"{name}.pdf", bbox_inches="tight")
    print(f"  Figura guardada: {path / name}.png")