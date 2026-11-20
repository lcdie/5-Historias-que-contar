"""Herramientas estadísticas reutilizables para storytelling con datos"""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import bootstrap
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import acf, pacf, kpss
from statsmodels.stats.diagnostic import acorr_ljungbox, het_breuschpagan
from statsmodels.stats.weightstats import ttest_ind
try:
    import ruptures as rpt
    RUPTURES_AVAILABLE = True
except ImportError:
    RUPTURES_AVAILABLE = False
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False


# ============================================================
# INFERENCIA BÁSICA
# ============================================================
def ic_media_bootstrap(data, n_resamples=10000, confidence=0.95, statistic=np.mean):
    """IC bootstrap para cualquier estadístico (default: media)"""
    data = np.asarray(data)
    data = data[~np.isnan(data)]
    if len(data) < 10:
        return (np.nan, np.nan)
    res = bootstrap((data,), statistic, n_resamples=n_resamples,
                    confidence_level=confidence, method="percentile", random_state=42)
    return res.confidence_interval


def efecto_tamano_cohen_d(x, y):
    """Cohen's d para dos grupos independientes con IC bootstrap"""
    x, y = np.asarray(x), np.asarray(y)
    x, y = x[~np.isnan(x)], y[~np.isnan(y)]
    nx, ny = len(x), len(y)
    if nx < 2 or ny < 2:
        return np.nan
    pooled_std = np.sqrt(((nx-1)*np.var(x, ddof=1) + (ny-1)*np.var(y, ddof=1)) / (nx + ny - 2))
    d = (np.mean(x) - np.mean(y)) / pooled_std
    return d


def t_test_welch(x, y):
    """t-test de Welch (varianzas desiguales) + IC para diferencia de medias"""
    x, y = np.asarray(x), np.asarray(y)
    x, y = x[~np.isnan(x)], y[~np.isnan(y)]
    t_stat, p_val, df = ttest_ind(x, y, alternative='two-sided', usevar='unequal')
    diff = np.mean(x) - np.mean(y)
    se = np.sqrt(np.var(x, ddof=1)/len(x) + np.var(y, ddof=1)/len(y))
    ci = (diff - stats.t.ppf(0.975, df)*se, diff + stats.t.ppf(0.975, df)*se)
    return {"t": t_stat, "p": p_val, "df": df, "diff": diff, "ci": ci, "se": se}


# ============================================================
# SERIES TEMPORALES (Historia 1: CO2)
# ============================================================
def stl_decomposition(series, period=12, seasonal=13, trend=None, robust=True):
    """Descomposición STL robusta. Retorna trend, seasonal, resid"""
    series = pd.Series(series).interpolate(limit_direction='both')
    stl = STL(series, period=period, seasonal=seasonal, trend=trend, robust=robust)
    result = stl.fit()
    return pd.DataFrame({
        'observed': series,
        'trend': result.trend,
        'seasonal': result.seasonal,
        'resid': result.resid
    }, index=series.index)


def growth_rate_annual(series, periods=12):
    """Tasa de crecimiento interanual (diff 12 meses)"""
    return series.diff(periods)


def changepoint_pelt(series, penalty=10, model="rbf", min_size=24):
    """Detección de changepoints con PELT (ruptures). Retorna índices."""
    if not RUPTURES_AVAILABLE:
        raise ImportError("Requiere ruptures: pip install ruptures")
    series = np.asarray(series)
    series = series[~np.isnan(series)]
    if len(series) < min_size * 2:
        return []
    algo = rpt.Pelt(model=model).fit(series.reshape(-1, 1))
    return algo.predict(pen=penalty)


def changepoint_bai_perron(series, max_breaks=3, h=0.15):
    """Test de Bai-Perron para cambios estructurales múltiples (statsmodels)"""
    from statsmodels.tsa.breakpoints import breakpoints
    series = pd.Series(series).dropna()
    bp = breakpoints(series, h=int(h*len(series)), breaks=max_breaks)
    return bp


def piecewise_linear_regression(x, y, breakpoints):
    """
    Regresión lineal por tramos (piecewise) con breakpoints dados.
    x, y: arrays 1D. breakpoints: lista de índices donde cambia la pendiente.
    Retorna: modelo ajustado, predicciones, tabla de coeficientes.
    """
    x, y = np.asarray(x), np.asarray(y)
    mask = ~np.isnan(x) & ~np.isnan(y)
    x, y = x[mask], y[mask]
    
    # Crear variables dummy para cada segmento
    X = pd.DataFrame({'x': x})
    segments = np.zeros_like(x, dtype=int)
    prev = 0
    for i, bp in enumerate(sorted(breakpoints)):
        segments[(x >= x[bp])] = i + 1
    X['segment'] = segments
    
    # Interacciones x * segment
    for s in X['segment'].unique():
        X[f'x_s{s}'] = X['x'] * (X['segment'] == s)
    
    # Modelo: y ~ x_s0 + x_s1 + ... (sin intercepto global, cada segmento tiene su pendiente)
    cols = [c for c in X.columns if c.startswith('x_s')]
    X_model = sm.add_constant(X[cols], has_constant='add')
    model = sm.OLS(y, X_model).fit()
    return model


def rolling_origin_forecast(series, model_func, window=60, horizon=12, step=6):
    """
    Validación rolling origin (expanding window).
    model_func: función que toma (train_series) y retorna forecast array de len=horizon.
    Retorna: DataFrame con forecasts, actuals, métricas.
    """
    series = pd.Series(series).dropna()
    forecasts, actuals, origins = [], [], []
    
    for i in range(window, len(series) - horizon + 1, step):
        train = series.iloc[:i]
        test = series.iloc[i:i+horizon]
        try:
            pred = model_func(train)
            forecasts.extend(pred)
            actuals.extend(test.values)
            origins.extend([i] * horizon)
        except Exception:
            continue
    
    if len(forecasts) == 0:
        return pd.DataFrame()
    
    df = pd.DataFrame({'origin': origins, 'forecast': forecasts, 'actual': actuals})
    df['error'] = df['actual'] - df['forecast']
    df['abs_error'] = np.abs(df['error'])
    df['pct_error'] = df['error'] / df['actual'] * 100
    return df


def mase_score(actual, forecast, seasonal_period=12):
    """Mean Absolute Scaled Error (Hyndman & Koehler 2006)"""
    actual, forecast = np.asarray(actual), np.asarray(forecast)
    mask = ~np.isnan(actual) & ~np.isnan(forecast)
    actual, forecast = actual[mask], forecast[mask]
    if len(actual) < seasonal_period + 1:
        return np.nan
    mae = np.mean(np.abs(actual - forecast))
    scale = np.mean(np.abs(actual[seasonal_period:] - actual[:-seasonal_period]))
    return mae / scale if scale > 0 else np.nan


def ts_diagnostics(residuals, lags=24):
    """Diagnósticos completos de residuos de serie temporal"""
    residuals = np.asarray(residuals)
    residuals = residuals[~np.isnan(residuals)]
    
    lb = acorr_ljungbox(residuals, lags=[lags], return_df=True)
    bp = het_breuschpagan(residuals, np.column_stack([np.ones(len(residuals)), np.arange(len(residuals))]))
    kpss_stat, kpss_p, _, _ = kpss(residuals, regression='c')
    
    return {
        'ljung_box_p': lb['lb_pvalue'].iloc[0],
        'breusch_pagan_p': bp[1],
        'kpss_stat': kpss_stat,
        'kpss_p': kpss_p,
        'skew': stats.skew(residuals),
        'kurtosis': stats.kurtosis(residuals),
        'jarque_bera_p': stats.jarque_bera(residuals)[1]
    }


# ============================================================
# MODELOS JERÁRQUICOS / PANEL (Historias 2, 4)
# ============================================================
def mixed_model_variance_partition(data, formula, groups, re_formula=None):
    """
    Mixed model con partición de varianza.
    formula: 'y ~ x1 + x2'
    groups: variable de agrupamiento (ej. 'country')
    re_formula: fórmula para efectos aleatorios (default: '1' = random intercept)
    """
    if re_formula is None:
        re_formula = '1'
    model = smf.mixedlm(formula, data, groups=data[groups], re_formula=re_formula)
    result = model.fit(reml=True)
    
    # Variance components
    vc = result.cov_re
    if hasattr(vc, 'shape') and vc.shape[0] > 1:
        var_components = np.diag(vc)
    else:
        var_components = np.array([vc])
    
    total_var = np.sum(var_components) + result.scale
    icc = var_components / total_var if total_var > 0 else np.zeros_like(var_components)
    
    return {
        'model': result,
        'var_components': var_components,
        'total_var': total_var,
        'icc': icc,
        'fixed_effects': result.fe_params,
        'random_effects': result.random_effects
    }


def hausman_test(fe_model, re_model):
    """Test de Hausman: FE vs RE. H0: RE consistente (efectos aleatorios no correlacionados con X)"""
    b_fe = fe_model.fe_params
    b_re = re_model.fe_params
    v_fe = fe_model.cov_params()
    v_re = re_model.cov_params()
    
    # Diferencia en coeficientes comunes
    common = b_fe.index.intersection(b_re.index)
    if len(common) == 0:
        return {'stat': np.nan, 'p': np.nan, 'df': 0}
    
    diff = b_fe[common] - b_re[common]
    var_diff = v_fe.loc[common, common] - v_re.loc[common, common]
    
    try:
        stat = diff.T @ np.linalg.inv(var_diff) @ diff
        p_val = 1 - stats.chi2.cdf(stat, df=len(common))
    except np.linalg.LinAlgError:
        stat, p_val = np.nan, np.nan
    
    return {'stat': stat, 'p': p_val, 'df': len(common)}


def within_between_decomposition(data, y_var, x_var, group_var):
    """
    Descomposición Within-Between (Mundlak 1978).
    Retorna coeficientes within, between, y pooled.
    """
    df = data[[y_var, x_var, group_var]].dropna().copy()
    df['x_mean'] = df.groupby(group_var)[x_var].transform('mean')
    df['x_dev'] = df[x_var] - df['x_mean']
    
    # Within (FE): y ~ x_dev + C(group)
    fe_formula = f'{y_var} ~ x_dev + C({group_var})'
    fe_model = smf.ols(fe_formula, df).fit()
    
    # Between: group_means
    gb = df.groupby(group_var)[[y_var, x_var]].mean().reset_index()
    be_model = smf.ols(f'{y_var} ~ {x_var}', gb).fit()
    
    # Pooled
    pooled_model = smf.ols(f'{y_var} ~ {x_var}', df).fit()
    
    return {
        'within': fe_model.params.get('x_dev', np.nan),
        'within_ci': fe_model.conf_int().loc['x_dev'].values if 'x_dev' in fe_model.params else [np.nan, np.nan],
        'between': be_model.params.get(x_var, np.nan),
        'between_ci': be_model.conf_int().loc[x_var].values if x_var in be_model.params else [np.nan, np.nan],
        'pooled': pooled_model.params.get(x_var, np.nan),
        'pooled_ci': pooled_model.conf_int().loc[x_var].values if x_var in pooled_model.params else [np.nan, np.nan],
        'fe_model': fe_model,
        'be_model': be_model,
        'pooled_model': pooled_model
    }


def icc_naked(data, value_col, group_col):
    """ICC 'naked' (sin covariables): var(group_means) / var(total)"""
    df = data[[value_col, group_col]].dropna()
    group_means = df.groupby(group_col)[value_col].mean()
    total_var = df[value_col].var(ddof=1)
    between_var = group_means.var(ddof=1)
    return between_var / total_var if total_var > 0 else 0


# ============================================================
# DETECCIÓN DE ANOMALÍAS (Historia 3)
# ============================================================
def isolation_forest_scores(X, contamination=0.01, n_estimators=200, random_state=42):
    """Isolation Forest con scores de anomalía (más negativo = más anómalo)"""
    from sklearn.ensemble import IsolationForest
    clf = IsolationForest(contamination=contamination, n_estimators=n_estimators,
                          random_state=random_state, n_jobs=-1)
    clf.fit(X)
    scores = clf.decision_function(X)  # negativo = outlier
    preds = clf.predict(X)  # -1 = outlier, 1 = inlier
    return scores, preds, clf


def pr_auc_score(y_true, y_score):
    """PR-AUC (Average Precision)"""
    from sklearn.metrics import average_precision_score
    return average_precision_score(y_true, y_score)


def optimal_threshold_cost(y_true, y_score, cost_fn=100, cost_fp=1):
    """Umbral que minimiza costo esperado: C_FN * FN + C_FP * FP.

    Convención: `y_score` más alto => mayor probabilidad/anomalía (clase positiva).
    """
    y_true = np.asarray(y_true)
    y_score = np.asarray(y_score)
    thresholds = np.unique(y_score[~np.isnan(y_score)])
    if len(thresholds) == 0:
        return np.nan, np.nan
    # Evaluar candidatos y extremos
    thresholds = np.r_[thresholds.min() - 1e-9, thresholds, thresholds.max() + 1e-9]

    costs = []
    for t in thresholds:
        y_pred = (y_score >= t).astype(int)
        fn = np.sum((y_true == 1) & (y_pred == 0))
        fp = np.sum((y_true == 0) & (y_pred == 1))
        costs.append(cost_fn * fn + cost_fp * fp)

    best_idx = int(np.argmin(costs))
    return thresholds[best_idx], float(costs[best_idx])


def fbeta_score_at_threshold(y_true, y_score, threshold, beta=2):
    """F-beta score en un umbral dado (score alto => positivo)."""
    from sklearn.metrics import fbeta_score
    y_score = np.asarray(y_score)
    y_pred = (y_score >= threshold).astype(int)
    return fbeta_score(y_true, y_pred, beta=beta, zero_division=0)


# ============================================================
# CAUSALIDAD OBSERVACIONAL / SPATIAL (Historia 5)
# ============================================================
def morans_i(residuals, coords, k=5):
    """Moran's I para autocorrelación espacial en residuos"""
    try:
        from libpysal.weights import KNN
        from esda.moran import Moran
        w = KNN.from_array(coords, k=k)
        w.transform = 'r'
        mi = Moran(residuals, w)
        return {'I': mi.I, 'p_sim': mi.p_sim, 'p_norm': mi.p_norm, 'z_sim': mi.z_sim}
    except ImportError:
        return {'I': np.nan, 'p_sim': np.nan, 'error': 'libpysal/esda no instalados'}


def spatial_lag_model(y, X, coords, k=5):
    """Modelo Spatial Lag (SAR): y = rho*Wy + X*beta + eps"""
    try:
        from spreg import ML_Lag
        from libpysal.weights import KNN
        w = KNN.from_array(coords, k=k)
        w.transform = 'r'
        model = ML_Lag(y, X, w=w, name_y='y', name_x=X.columns.tolist() if hasattr(X, 'columns') else None)
        return model
    except ImportError:
        return None


def oster_sensitivity(beta_controlled, beta_uncontrolled, r2_controlled, r2_uncontrolled, r2_max=1.3):
    """
    Sensibilidad de Oster (2019) para confounding no observado.
    delta = (beta_controlled - beta_uncontrolled) / (beta_uncontrolled * (r2_max - r2_controlled) / (r2_controlled - r2_uncontrolled))
    """
    if r2_controlled <= r2_uncontrolled:
        return np.nan
    delta = (beta_controlled - beta_uncontrolled) / (beta_uncontrolled * (r2_max - r2_controlled) / (r2_controlled - r2_uncontrolled))
    return delta


def partial_dependence(model, X, feature, percentiles=(0.05, 0.95), grid_resolution=20):
    """Partial Dependence Plot (compatibilidad sklearn antigua/nueva)."""
    from sklearn.inspection import partial_dependence as skl_partial_dependence
    result = skl_partial_dependence(model, X, [feature], percentiles=percentiles, grid_resolution=grid_resolution)
    grid = result.get('grid_values', result.get('values'))
    values = np.asarray(grid[0] if isinstance(grid, (list, tuple)) else grid).ravel()
    avg = np.asarray(result['average'])
    avg = avg[0] if avg.ndim > 1 else avg
    return values, avg.ravel()


# ============================================================
# SHAP / INTERPRETABILIDAD (Historias 3, 5)
# ============================================================
def shap_summary(model, X, feature_names=None, max_display=10, plot_type='beeswarm'):
    """Wrapper SHAP consistente"""
    if not SHAP_AVAILABLE:
        raise ImportError("Requiere shap: pip install shap")
    
    # Detectar tipo de modelo
    if hasattr(model, 'estimators_') or hasattr(model, 'feature_importances_'):
        explainer = shap.TreeExplainer(model)
    else:
        explainer = shap.Explainer(model, X)
    
    shap_values = explainer(X)
    
    if plot_type == 'beeswarm':
        shap.plots.beeswarm(shap_values, max_display=max_display, show=False)
    elif plot_type == 'bar':
        shap.plots.bar(shap_values, max_display=max_display, show=False)
    elif plot_type == 'waterfall':
        shap.plots.waterfall(shap_values[0], max_display=max_display, show=False)
    
    return shap_values, explainer


# ============================================================
# VALIDACIÓN CRUZADA ESPACIAL (Historia 5)
# ============================================================
def spatial_block_cv(coords, n_splits=5, buffer=0):
    """
    Genera índices para Spatial Block CV.
    coords: (n, 2) array de [lat, lon] o [x, y]
    Retorna: lista de (train_idx, test_idx)
    """
    from sklearn.model_selection import KFold

    coords = np.asarray(coords)
    n = len(coords)
    n_splits = max(2, min(int(n_splits), n))

    # Intentar partición basada en vecindad espacial si libpysal está disponible
    try:
        from libpysal.weights import KNN
        from scipy.sparse.csgraph import connected_components

        w = KNN.from_array(coords, k=max(5, min(20, n - 1)))
        n_components, labels = connected_components(w.sparse, directed=False)
        if n_components >= n_splits:
            unique_labels = np.unique(labels)
            rng = np.random.default_rng(42)
            rng.shuffle(unique_labels)
            fold_assign = {label: i % n_splits for i, label in enumerate(unique_labels)}
            folds = np.array([fold_assign[l] for l in labels])
            splits = []
            for i in range(n_splits):
                test_idx = np.where(folds == i)[0]
                train_idx = np.where(folds != i)[0]
                if len(test_idx) and len(train_idx):
                    splits.append((train_idx, test_idx))
            if len(splits) == n_splits:
                return splits
    except Exception:
        pass

    # Fallback: bloques por cuantiles en la primera coordenada (proxy espacial)
    try:
        order = np.argsort(coords[:, 0])
        block_ids = np.zeros(n, dtype=int)
        bins = np.array_split(order, n_splits)
        for i, idxs in enumerate(bins):
            block_ids[idxs] = i
        splits = []
        for i in range(n_splits):
            test_idx = np.where(block_ids == i)[0]
            train_idx = np.where(block_ids != i)[0]
            if len(test_idx) and len(train_idx):
                splits.append((train_idx, test_idx))
        if splits:
            return splits
    except Exception:
        pass

    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    return list(kf.split(np.arange(n)))


# ============================================================
# UTILIDADES DE VISUALIZACIÓN ESTADÍSTICA
# ============================================================
def coef_plot(model, ax=None, exclude_intercept=True, color='#1f77b4'):
    """Gráfico de coeficientes con IC 95%"""
    import matplotlib.pyplot as plt
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, max(4, len(model.params)*0.3)))
    
    params = model.params.copy()
    conf = model.conf_int()
    
    if exclude_intercept and 'Intercept' in params.index:
        params = params.drop('Intercept')
        conf = conf.drop('Intercept')
    
    params = params[::-1]  # invertir para que el primero quede arriba
    conf = conf.loc[params.index]
    
    y_pos = np.arange(len(params))
    ax.hlines(y_pos, conf[0], conf[1], color=color, linewidth=2)
    ax.plot(params, y_pos, 'o', color=color, markersize=6)
    ax.axvline(0, color='gray', linestyle='--', linewidth=0.8)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(params.index)
    ax.set_xlabel('Coeficiente (IC 95%)')
    return ax


def residuals_vs_fitted(model, ax=None):
    """Gráfico residuos vs ajustados"""
    import matplotlib.pyplot as plt
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))
    
    fitted = model.fittedvalues
    resid = model.resid
    ax.scatter(fitted, resid, alpha=0.5, s=20)
    ax.axhline(0, color='red', linestyle='--', linewidth=1)
    ax.set_xlabel('Valores ajustados')
    ax.set_ylabel('Residuos')
    ax.set_title('Residuos vs Ajustados')
    return ax


def qq_plot(residuals, ax=None):
    """Q-Q plot de residuos"""
    import matplotlib.pyplot as plt
    from scipy import stats
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))
    
    stats.probplot(residuals, dist="norm", plot=ax)
    ax.set_title('Q-Q Plot')
    return ax