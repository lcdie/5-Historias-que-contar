"""Marcadores narrativos para estructurar las 3 cuartillas
Úsalos como celdas markdown: `display(Markdown(cuartilla_header(...)))`
"""
from IPython.display import Markdown, display

def cuartilla_header(num, titulo):
    return Markdown(f"---\n## Cuartilla {num}: {titulo}\n---")

def hallazgo(texto, evidencia=None, ic=None, pval=None):
    """Formatea un hallazgo cuantitativo con evidencia"""
    parts = [f"**Hallazgo:** {texto}"]
    if evidencia is not None:
        parts.append(f"- Evidencia: `{evidencia}`")
    if ic is not None:
        parts.append(f"- IC 95%: [{ic[0]:.3f}, {ic[1]:.3f}]")
    if pval is not None:
        parts.append(f"- p-valor: {pval:.4f}" if pval >= 0.001 else f"- p-valor: <0.001")
    return Markdown("\n".join(parts))

def limitacion(texto, severidad="media", mitigacion=None):
    """Registra una limitación explícita"""
    icon = {"alta": "🔴", "media": "🟡", "baja": "🟢"}[severidad]
    parts = [f"{icon} **Limitación ({severidad}):** {texto}"]
    if mitigacion:
        parts.append(f"  - Mitigación propuesta: {mitigacion}")
    return Markdown("\n".join(parts))

def conclusion_tecnica(respuesta, siguiente_paso, reproducibilidad=None):
    """Conclusión técnica estructurada"""
    parts = [
        f"**Respuesta a la pregunta de investigación:** {respuesta}",
        f"**Próximo paso replicable:** {siguiente_paso}",
    ]
    if reproducibilidad:
        parts.append(f"**Reproducibilidad:** {reproducibilidad}")
    return Markdown("\n".join(parts))