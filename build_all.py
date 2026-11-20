#!/usr/bin/env python3
"""
Script maestro para generar TODOS los targets de despliegue.
Ejecuta: python build_all.py

Genera:
1. docs_html/     - HTML estático (GitHub Pages) - lectura rápida
2. docs_lite/     - JupyterLite (WASM) - ejecución ligera en browser
3. docs_binder/   - Configuración para mybinder.org
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
NOTEBOOKS = ROOT / "notebooks"
VENV_PY = ROOT / ".venv" / "bin" / "python"
VENV_JUPYTER = ROOT / ".venv" / "bin" / "jupyter"


def _base_env():
    env = os.environ.copy()
    extra = [str(ROOT), str(ROOT / "src")]
    prev = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join([p for p in [*extra, prev] if p])
    # Matplotlib cache/config en lugar escribible
    env.setdefault("MPLCONFIGDIR", "/tmp/opencode/mplconfig")
    Path(env["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)
    return env


def run(cmd, cwd=None, check=True, env=None):
    """Ejecuta comando y muestra output en tiempo real."""
    print(f"\n🔧  {cmd}")
    merged_env = _base_env()
    if env:
        merged_env.update(env)
    result = subprocess.run(cmd, shell=True, cwd=cwd or ROOT, check=check, env=merged_env)
    return result


def jupyter_cmd():
    if VENV_JUPYTER.exists():
        return f"'{VENV_JUPYTER}'"
    return f"'{sys.executable}' -m jupyter"

def build_html():
    """HTML estático para GitHub Pages - lectura rápida, cero dependencias."""
    out = ROOT / "docs_html"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    print("\n" + "=" * 60)
    print("📄 Generando HTML estático (docs_html/)")
    print("=" * 60)

    jpy = jupyter_cmd()
    failures = []
    for nb in sorted(NOTEBOOKS.glob("*.ipynb")):
        print(f"  → {nb.name}")
        cmd_exec = (
            f"{jpy} nbconvert --to html '{nb}' --output-dir '{out}' "
            f"--execute --ExecutePreprocessor.timeout=900"
        )
        res = run(cmd_exec, check=False)
        if res.returncode != 0:
            print(f"  ⚠️  Falló con --execute: {nb.name}. Intentando sin ejecutar...")
            cmd_noexec = f"{jpy} nbconvert --to html '{nb}' --output-dir '{out}'"
            res2 = run(cmd_noexec, check=False)
            if res2.returncode != 0:
                failures.append(nb.name)
            else:
                failures.append(f"{nb.name} (sin ejecutar)")
    # Index.html que lista todos
    index = out / "index.html"
    lite_note = (
        '<a href="../docs_lite/index.html">→ JupyterLite (si está generado)</a>'
        if (ROOT / "docs_lite" / "index.html").exists()
        else 'JupyterLite: generar con <code>jupyter lite build</code> (si está disponible)'
    )
    index.write_text(
        f"""<!DOCTYPE html>
<html><head><meta charset=\"utf-8\"><title>Storytelling con Datos - MATCOM</title>
<style>body{{font-family:sans-serif;max-width:800px;margin:2rem auto;padding:0 1rem}}
h1{{color:#1f77b4}} a{{color:#1f77b4}} .card{{border:1px solid #ddd;border-radius:8px;padding:1rem;margin:1rem 0}}
.card h2{{margin-top:0}} .meta{{color:#444}}</style></head><body>
<h1>📊 Storytelling con Datos — 5 Historias, 5 Arquetipos</h1>
<p class=\"meta\"><strong>MATCOM — Universidad de La Habana</strong> | Entrega: 2026-11-20</p>
<p>Versión estática para lectura rápida. {lite_note}. Para ejecución completa en la nube, configura Binder en tu repositorio de GitHub.</p>
<hr>
<div class=\"card\"><h2>1. La curva que no miente</h2><p>Serie temporal + cambio estructural — CO₂ Mauna Loa (1958–2024)</p><a href=\"01_series_temporales_co2.html\">Leer →</a></div>
<div class=\"card\"><h2>2. Cuando el promedio miente</h2><p>Paradoja de Simpson — Gapminder (142 países × 12 años)</p><a href=\"02_comparacion_gapminder.html\">Leer →</a></div>
<div class=\"card\"><h2>3. La aguja en el pajar financiero</h2><p>Outliers + Detección de anomalías — Credit Card Fraud (dataset del repositorio)</p><a href=\"03_outliers_fraude.html\">Leer →</a></div>
<div class=\"card\"><h2>4. Pingüinos como termómetros</h2><p>Drill-down jerárquico — Palmer Penguins (3 especies × 3 islas)</p><a href=\"04_drilldown_penguins.html\">Leer →</a></div>
<div class=\"card\"><h2>5. ¿Ingreso causa precio o es la playa?</h2><p>Intersección multivariable y confounding espacial — California Housing</p><a href=\"05_interseccion_california.html\">Leer →</a></div>
<hr><p><small>Generado: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}</small></p>
</body></html>"""
    )
    if failures:
        print(f"⚠️  HTML generado con incidencias: {failures}")
    print(f"✅ HTML estático listo en {out}")
    return failures

def build_lite():
    """JupyterLite (WASM) - ejecución en browser sin servidor."""
    out = ROOT / "docs_lite"
    shutil.rmtree(out, ignore_errors=True)

    print("\n" + "=" * 60)
    print("🧠 Generando JupyterLite (docs_lite/)")
    print("=" * 60)

    jpy = jupyter_cmd()
    # Config para JupyterLite
    lite_config = ROOT / "jupyterlite_config.json"
    lite_config.write_text(
        """{
    "jupyterlite": {
        "contents": "notebooks",
        "outputDir": "docs_lite",
        "settings": {
            "theme": "JupyterLab Dark"
        }
    }
}"""
    )

    res = run(f"{jpy} lite build --config jupyterlite_config.json --force", check=False)
    if res.returncode != 0:
        print("⚠️  JupyterLite no se pudo generar (¿falta jupyterlite-core?). Se omite.")
        return False

    # Copiar index personalizado
    index = out / "index.html"
    if index.exists():
        html = index.read_text()
        html = html.replace(
            "<title>JupyterLite</title>",
            "<title>Storytelling con Datos — JupyterLite (WASM)</title>",
        )
        html = html.replace(
            "<body>",
            """<body>
<header style="background:#1f77b4;color:white;padding:1rem;text-align:center">
<h1>📊 Storytelling con Datos — JupyterLite (WASM)</h1>
<p>Ejecuta notebooks en el navegador. <strong>Sin instalar nada.</strong> 
<a href="../html/" style="color:#ffd700">→ Versión HTML estática</a> | 
<a href="https://mybinder.org/v2/gh/TU_USUARIO/storytelling-datos-matcom/HEAD?labpath=notebooks" style="color:#ffd700">→ Binder (TODO)</a></p>
</header>""",
        )
        index.write_text(html)

    print(f"✅ JupyterLite listo en {out}")
    return True

def build_binder():
    """Configuración para mybinder.org."""
    out = ROOT / ".github"
    out.mkdir(exist_ok=True)

    # postBuild para Binder
    postbuild = out / "postBuild"
    postbuild.write_text(
        """#!/bin/bash
set -e
# Instalar dependencias del sistema para prophet, libpysal, etc.
apt-get update && apt-get install -y -q g++ make cmake 2>/dev/null || true
pip install -q prophet==1.1 pmdarima==2.0 libpysal==5.0 spreg==1.2 econml==0.15 esda==3.0 splot==1.0
"""
    )
    postbuild.chmod(0o755)

    # apt.txt para Binder
    (out / "apt.txt").write_text("g++\nmake\ncmake\n")

    # runtime.txt para versión Python
    (ROOT / "runtime.txt").write_text("python-3.11\n")

    print(f"✅ Config Binder lista en {out}/")

def main():
    print("🚀 Storytelling con Datos — Build All Targets")
    print("=" * 60)

    # Verificar que estamos en el directorio correcto
    if not NOTEBOOKS.exists():
        print(f"❌ No se encuentra {NOTEBOOKS}")
        sys.exit(1)

    data_raw = ROOT / "data" / "raw"
    if not data_raw.exists() or not any(data_raw.glob("*.csv")):
        print("⚠️  No se encontraron datos en data/raw/. Ejecuta: python data/download_data.py")

    # Ejecutar builds (resilientes)
    html_failures = build_html() or []
    lite_ok = build_lite()
    build_binder()

    print("\n" + "=" * 60)
    print("🎉 PROCESO DE BUILD FINALIZADO")
    print("=" * 60)
    print(
        """
📁 docs_html/     → GitHub Pages (HTML estático, lectura rápida)
📁 docs_lite/     → GitHub Pages /docs_lite (JupyterLite WASM, si se generó)
📁 .github/       → Config para mybinder.org

📋 PRÓXIMOS PASOS:
1. git add docs_html docs_lite .github runtime.txt jupyterlite_config.json
2. git commit -m "Deploy: HTML + JupyterLite + Binder config"
3. git push

4. GitHub Settings → Pages:
   - Source: Deploy from branch
   - Branch: main / docs_html  (para HTML estático)

5. Binder: https://mybinder.org/v2/gh/TU_USUARIO/storytelling-datos-matcom/HEAD?labpath=notebooks
"""
    )
    if html_failures:
        print(f"⚠️  Incidencias en HTML: {html_failures}")
    if not lite_ok:
        print("⚠️  JupyterLite no fue generado en este entorno.")


if __name__ == "__main__":
    main()