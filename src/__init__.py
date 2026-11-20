"""storytelling-matcom: utilidades de visualización, estadística y narrativa.

Se importan submódulos bajo demanda en notebooks (`from src.viz ...`, etc.).
Este `__init__` expone utilidades comunes de forma tolerante para evitar
fallos si alguna dependencia opcional no está instalada.
"""
from .viz import fig_ax, save_fig, setup_plotting_style
from .narrative import conclusion_tecnica, cuartilla_header, hallazgo, limitacion

__all__ = [
    "setup_plotting_style",
    "save_fig",
    "fig_ax",
    "cuartilla_header",
    "hallazgo",
    "limitacion",
    "conclusion_tecnica",
]

# Exponer helpers estadísticos disponibles sin romper si faltan dependencias
try:
    from . import stats_helpers as stats_helpers  # noqa: F401

    for _name in [
        "ic_media_bootstrap",
        "efecto_tamano_cohen_d",
        "changepoint_pelt",
        "shap_summary_plot",
    ]:
        if hasattr(stats_helpers, _name):
            globals()[_name] = getattr(stats_helpers, _name)
            __all__.append(_name)
except Exception:
    stats_helpers = None  # type: ignore
