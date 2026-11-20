#!/usr/bin/env python3
"""
Descarga los 5 datasets para las 5 historias.
Uso: python data/download_data.py
Guarda todo en data/raw/
"""
import io
import os
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

RAW_DIR = Path(__file__).parent / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def _urlopen(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=timeout)

def download_co2():
    """CO2 Mauna Loa - formato NOAA requiere parsing especial"""
    url = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt"
    path = RAW_DIR / "co2_mm_mlo.csv"
    if path.exists() and path.stat().st_size > 0:
        print(f"  ✓ {path.name} ya existe")
        return
    print("Descargando CO2 Mauna Loa...")
    try:
        with _urlopen(url) as response:
            lines = response.read().decode("utf-8", errors="replace").splitlines()
        # Saltar header NOAA (líneas que empiezan con #)
        data_lines = [l.strip() for l in lines if l.strip() and not l.lstrip().startswith("#")]
        rows = []
        for line in data_lines:
            parts = line.split()
            if len(parts) < 5:
                continue
            try:
                nums = [float(x) for x in parts]
            except Exception:
                continue
            # Formato clásico: year month decimal average deseasonalized ndays sdev unc
            if len(nums) >= 7 and 1900 <= nums[0] <= 2100 and 1 <= nums[1] <= 12 and 1900 <= nums[2] <= 2100:
                year = int(nums[0]); month = int(nums[1]); decimal = nums[2]
                average = nums[3]; deseasonalized = nums[4] if len(nums) > 4 else np.nan
                ndays = nums[5] if len(nums) > 5 else np.nan
                # Mapear a esquema esperado por notebooks
                co2 = np.nan if average in (-99.99, -9.99) else average
                interpolated = deseasonalized if deseasonalized not in (-99.99, -9.99) else average
                trend = deseasonalized if deseasonalized not in (-99.99, -9.99) else np.nan
                days = np.nan if ndays in (-1, -9.99, -99.99) else ndays
                rows.append({
                    "year": year, "month": month, "decimal_date": decimal,
                    "co2": co2, "interpolated": interpolated, "trend": trend, "days": days,
                })
            # Algunos mirrors/formatos: year month decimal average interpolated trend ndays ...
            elif len(nums) >= 7 and 1900 <= nums[0] <= 2100 and 1 <= nums[1] <= 12:
                year = int(nums[0]); month = int(nums[1]); decimal = nums[2]
                co2 = nums[3]
                interpolated = nums[4]
                trend = nums[5]
                days = nums[6]
                for k, v in [("co2", co2), ("interpolated", interpolated), ("trend", trend), ("days", days)]:
                    pass
                co2 = np.nan if co2 in (-99.99, -9.99) else co2
                interpolated = np.nan if interpolated in (-99.99, -9.99) else interpolated
                trend = np.nan if trend in (-99.99, -9.99) else trend
                days = np.nan if days in (-1, -9.99, -99.99) else days
                rows.append({
                    "year": year, "month": month, "decimal_date": decimal,
                    "co2": co2, "interpolated": interpolated, "trend": trend, "days": days,
                })
            else:
                continue
        if not rows:
            raise ValueError("No se pudieron parsear filas CO2 válidas")
        df = pd.DataFrame(rows)
        # Asegurar tipos razonables
        df["year"] = df["year"].astype(int)
        df["month"] = df["month"].astype(int)
        df.to_csv(path, index=False)
        print(f"  -> {path} ({len(df)} filas)")
    except Exception as e:
        print(f"  ✗ No se pudo descargar CO2: {e}")

def download_gapminder():
    urls = [
        "https://raw.githubusercontent.com/jennybc/gapminder/master/inst/extdata/gapminder.tsv",
        "https://raw.githubusercontent.com/jennybc/gapminder/master/inst/extdata/gapminder.csv",
        "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv",
        "https://raw.githubusercontent.com/resbaz/r-novice-gapminder-files/master/data/gapminder-FiveYearData.csv",
    ]
    path = RAW_DIR / "gapminder.csv"
    if path.exists() and path.stat().st_size > 0:
        print(f"  ✓ {path.name} ya existe")
        return
    print("Descargando Gapminder...")
    last_err = None
    for url in urls:
        try:
            with _urlopen(url) as response:
                data = response.read()
            sep = "\t" if url.endswith(".tsv") else ","
            df = pd.read_csv(io.BytesIO(data), sep=sep)
            # Normalizar columnas esperadas
            rename = {}
            for c in df.columns:
                lc = c.lower()
                if lc in ("country",):
                    rename[c] = "country"
                elif lc in ("continent",):
                    rename[c] = "continent"
                elif lc in ("year",):
                    rename[c] = "year"
                elif lc in ("lifeexp", "life_exp"):
                    rename[c] = "lifeExp"
                elif lc in ("pop", "population"):
                    rename[c] = "pop"
                elif lc in ("gdppercap", "gdppercap", "gdp_percap", "gdppercapita"):
                    rename[c] = "gdpPercap"
            if rename:
                df = df.rename(columns=rename)
            needed = {"country", "continent", "year", "lifeExp", "pop", "gdpPercap"}
            if not needed.issubset(df.columns):
                raise ValueError(f"columnas inesperadas: {list(df.columns)}")
            df = df[["country", "continent", "year", "lifeExp", "pop", "gdpPercap"]]
            df.to_csv(path, index=False)
            print(f"  -> {path} ({len(df)} filas, fuente: {url})")
            return
        except Exception as e:
            last_err = e
            continue
    print(f"  ✗ No se pudo descargar Gapminder: {last_err}")


def download_penguins():
    urls = [
        "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv",
        "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/master/inst/extdata/penguins.csv",
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv",
    ]
    path = RAW_DIR / "penguins.csv"
    if path.exists() and path.stat().st_size > 0:
        print(f"  ✓ {path.name} ya existe")
        return
    print("Descargando Penguins...")
    last_err = None
    for url in urls:
        try:
            with _urlopen(url) as response:
                data = response.read()
            df = pd.read_csv(io.BytesIO(data))
            # Normalizar nombres de columnas comunes
            cols = {c.lower().strip(): c for c in df.columns}
            # seaborn-data ya usa species,island,bill_length_mm,... que es compatible
            df.to_csv(path, index=False)
            print(f"  -> {path} ({len(df)} filas, fuente: {url})")
            return
        except Exception as e:
            last_err = e
            continue
    print(f"  ✗ No se pudo descargar Penguins: {last_err}")


def download_california():
    path = RAW_DIR / "california_housing.csv"
    if path.exists() and path.stat().st_size > 0:
        print(f"  ✓ {path.name} ya existe")
        return
    print("Descargando/Generando California Housing...")
    try:
        from sklearn.datasets import fetch_california_housing

        data = fetch_california_housing(as_frame=True)
        data.frame.to_csv(path, index=False)
        print(f"  -> {path} ({len(data.frame)} filas)")
        return
    except Exception as e:
        print(f"  ! fetch_california_housing no disponible/falló: {e}")

    # Fallback: intentar descargar CSV público con esquema compatible (MedInc,...,MedHouseVal)
    urls = [
        "https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv",
        "https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.csv",
    ]
    for url in urls:
        try:
            with _urlopen(url) as response:
                raw = response.read()
            df = pd.read_csv(io.BytesIO(raw))
            if {"median_income", "median_house_value", "latitude", "longitude"}.issubset(df.columns):
                mapped = pd.DataFrame(
                    {
                        "MedInc": df["median_income"].astype(float),
                        "HouseAge": df.get("housing_median_age", np.nan).astype(float),
                        "AveRooms": (df["total_rooms"] / df["households"]).replace([np.inf, -np.inf], np.nan).astype(float),
                        "AveBedrms": (df["total_bedrooms"] / df["households"]).replace([np.inf, -np.inf], np.nan).astype(float),
                        "Population": df.get("population", np.nan).astype(float),
                        "AveOccup": (df["population"] / df["households"]).replace([np.inf, -np.inf], np.nan).astype(float),
                        "Latitude": df["latitude"].astype(float),
                        "Longitude": df["longitude"].astype(float),
                        "MedHouseVal": (df["median_house_value"] / 100000.0).astype(float),
                    }
                )
                mapped = mapped.dropna().reset_index(drop=True)
                mapped.to_csv(path, index=False)
                print(f"  -> {path} (fallback mapeado, {len(mapped)} filas)")
                return
        except Exception:
            continue
    print("  ✗ No se pudo obtener California Housing")

def download_creditcard():
    """
    NOTA: El dataset de Credit Card Fraud de Kaggle requiere autenticación.
    Opciones:
    1. Descarga manual desde https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
       y coloca creditcard.csv en data/raw/
    2. Usa dataset alternativo: IEEE-CIS Fraud Detection (también Kaggle)
    3. Dataset sintético con mismas características para desarrollo
    """
    path = RAW_DIR / "creditcard.csv"
    if path.exists() and path.stat().st_size > 0:
        print(f"  ✓ {path.name} ya existe")
        return
    print("⚠️  Credit Card Fraud: no disponible localmente; generando sintético")
    print("   (para usar el real de Kaggle, coloca creditcard.csv en data/raw/)")
    # Crear dataset sintético para que el notebook corra
    create_synthetic_fraud(path)

def create_synthetic_fraud(path, n=50000, fraud_rate=0.0017):
    """Genera datos sintéticos con estructura PCA-like correlacionada para desarrollo"""
    np.random.seed(42)
    n_fraud = int(n * fraud_rate)
    n_normal = n - n_fraud
    
    # Matriz de covarianza realista para 28 componentes PCA-like
    # Los componentes PCA reales son ortogonales, pero en la práctica 
    # la muestra finita tiene correlaciones pequeñas
    np.random.seed(123)
    A = np.random.randn(28, 28) * 0.3
    cov_normal = A @ A.T + np.eye(28) * 0.5  # semi-definida positiva
    
    # Fraude: misma estructura pero mayor varianza y media desplazada en algunos componentes
    cov_fraud = cov_normal * 2.5
    mean_fraud = np.zeros(28)
    mean_fraud[::3] = np.random.normal(0, 1.5, 10)  # algunos componentes desplazados
    
    # Generar datos
    data = {}
    data["Time"] = np.cumsum(np.random.exponential(60, n))
    data["Amount"] = np.concatenate([
        np.random.lognormal(3, 1.5, n_normal),
        np.random.lognormal(5, 2, n_fraud)
    ])
    
    # V1-V28 con estructura correlacionada
    v_normal = np.random.multivariate_normal(np.zeros(28), cov_normal, n_normal)
    v_fraud = np.random.multivariate_normal(mean_fraud, cov_fraud, n_fraud)
    v_all = np.vstack([v_normal, v_fraud])
    
    for i in range(28):
        data[f"V{i+1}"] = v_all[:, i]
    
    data["Class"] = np.concatenate([np.zeros(n_normal), np.ones(n_fraud)])
    
    # Shuffle
    idx = np.random.permutation(n)
    df = pd.DataFrame(data).iloc[idx].reset_index(drop=True)
    df.to_csv(path, index=False)
    print(f"  -> {path} (sintético, {len(df)} filas, {fraud_rate*100:.2f}% fraude, PCA-like)")

if __name__ == "__main__":
    tasks = [
        ("CO2", download_co2),
        ("Gapminder", download_gapminder),
        ("Penguins", download_penguins),
        ("California", download_california),
        ("CreditCard", download_creditcard),
    ]
    ok = 0
    for name, fn in tasks:
        try:
            fn()
            path = RAW_DIR / {
                "CO2": "co2_mm_mlo.csv",
                "Gapminder": "gapminder.csv",
                "Penguins": "penguins.csv",
                "California": "california_housing.csv",
                "CreditCard": "creditcard.csv",
            }[name]
            if path.exists() and path.stat().st_size > 0:
                ok += 1
        except Exception as e:
            print(f"  ✗ {name}: {e}")

    print(f"\n✅ Datasets disponibles: {ok}/{len(tasks)} en {RAW_DIR}")
    if ok < len(tasks):
        print("⚠️  Algunos datasets faltan; la ejecución completa de notebooks puede fallar.")