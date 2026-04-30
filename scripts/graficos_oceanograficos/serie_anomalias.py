"""
serie_anomalias.py — Plantilla para series de tiempo de anomalías
========================================================================================
Calcula las anomalías de una variable respecto a su climatología mensual y las grafica
con relleno rojo (valores sobre la media) y azul (valores bajo la media).
Funciona con datos sintéticos por defecto; edita CONFIGURACIÓN para usar datos reales.

Requisitos:
    pip install matplotlib numpy pandas xarray netCDF4

Ejecución:
    python serie_anomalias.py

Laboratorio de Oceanografía Física (LOFA)
Instituto de Ciencias Marinas y Limnológicas | Universidad Austral de Chile
https://github.com/Laboratorio-Oceanografia-Fisica-UACh
========================================================================================
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Intentar importar lofa_style desde el toolbox
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from toolbox import lofa_style as ls
    ls.apply()
    COLOR_POS = ls.COLORES['positivo']
    COLOR_NEG = ls.COLORES['negativo']
    guardar   = ls.guardar_figura
except ImportError:
    COLOR_POS = '#D62728'
    COLOR_NEG = '#1F77B4'
    def guardar(nombre, directorio='figuras'):
        os.makedirs(directorio, exist_ok=True)
        plt.savefig(os.path.join(directorio, nombre), dpi=300, bbox_inches='tight')
        plt.close('all')

# ══════════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════════════════

# Para usar datos reales: ruta al archivo NetCDF o CSV
# - NetCDF: debe contener una variable escalar con dimensión temporal
# - CSV   : columnas 'fecha' (YYYY-MM-DD) y 'valor'
# Dejar vacío para usar datos sintéticos de demostración
ARCHIVO    = ""
VARIABLE   = "sst"              # Nombre de la variable en el NetCDF (si aplica)
ETIQUETA   = "Anomalía SST (°C)"
TITULO     = "Anomalías de SST — Costa de Valdivia"
NOMBRE_SALIDA = "serie_anomalias.png"

# ══════════════════════════════════════════════════════════════════════════════════


def generar_serie_sintetica():
    """Serie mensual de SST sintética con ciclo estacional y eventos anómalos."""
    np.random.seed(42)
    fechas = pd.date_range('2000-01-01', '2024-12-31', freq='MS')
    meses  = np.array([f.month for f in fechas])
    ciclo  = 2.5 * np.cos(2 * np.pi * (meses - 1) / 12)
    # Añadir un par de eventos anómalos tipo El Niño/La Niña
    anomalia_forzada = np.zeros(len(fechas))
    anomalia_forzada[48:60]  += 1.8   # calentamiento años 2004-2004
    anomalia_forzada[156:168] -= 1.5  # enfriamiento años 2013-2013
    anomalia_forzada[228:240] += 2.2  # calentamiento años 2019-2019
    ruido = np.random.normal(0, 0.5, len(fechas))
    sst   = 13.5 + ciclo + anomalia_forzada + ruido
    return pd.Series(sst, index=fechas, name='sst')


def cargar_serie(archivo, variable):
    """Carga una serie temporal desde CSV o NetCDF."""
    if archivo.endswith('.csv'):
        df = pd.read_csv(archivo, parse_dates=['fecha'], index_col='fecha')
        return df['valor']
    else:
        import xarray as xr
        ds  = xr.open_dataset(archivo)
        da  = ds[variable]
        dim_espacio = [d for d in da.dims if d not in ('time', 'valid_time')]
        if dim_espacio:
            da = da.mean(dim=dim_espacio)
        time_dim = 'valid_time' if 'valid_time' in da.dims else 'time'
        return pd.Series(da.values, index=pd.to_datetime(da[time_dim].values))


def calcular_anomalias(serie):
    """Sustrae la climatología mensual a la serie original."""
    climatologia = serie.groupby(serie.index.month).mean()
    anomalias = serie.copy()
    for mes in range(1, 13):
        mask = serie.index.month == mes
        anomalias[mask] = serie[mask] - climatologia[mes]
    return anomalias, climatologia


def main():
    # Cargar datos
    if ARCHIVO and os.path.exists(ARCHIVO):
        print(f"Cargando datos desde: {ARCHIVO}")
        serie = cargar_serie(ARCHIVO, VARIABLE)
    else:
        if ARCHIVO:
            print(f"Archivo no encontrado: {ARCHIVO}")
        print("Usando datos sintéticos de demostración...")
        serie = generar_serie_sintetica()

    print(f"Período: {serie.index[0].date()} → {serie.index[-1].date()}")

    # Calcular anomalías
    anomalias, climatologia = calcular_anomalias(serie)

    print(f"Anomalía máxima: +{anomalias.max():.2f}  |  mínima: {anomalias.min():.2f}")

    # ── Gráfico ──────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(14, 4))

    fechas = serie.index
    vals   = anomalias.values

    # Línea de anomalía
    ax.plot(fechas, vals, color='black', linewidth=0.9, alpha=0.8)

    # Relleno positivo / negativo
    ax.fill_between(fechas, 0, vals,
                    where=(vals > 0), color=COLOR_POS, alpha=0.45,
                    label='Anomalía positiva (calentamiento)')
    ax.fill_between(fechas, 0, vals,
                    where=(vals < 0), color=COLOR_NEG, alpha=0.45,
                    label='Anomalía negativa (enfriamiento)')

    # Línea de cero
    ax.axhline(0, color='black', linewidth=1.3, linestyle='--')

    # Umbral ±1 std (opcional, útil para identificar eventos extremos)
    std_total = anomalias.std()
    ax.axhline( std_total, color='gray', linewidth=0.8, linestyle=':', alpha=0.7)
    ax.axhline(-std_total, color='gray', linewidth=0.8, linestyle=':', alpha=0.7)
    ax.text(fechas[-1], std_total + 0.05, '+1σ', fontsize=8, color='gray', ha='right')
    ax.text(fechas[-1], -std_total - 0.15, '−1σ', fontsize=8, color='gray', ha='right')

    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=45)

    ax.set_ylabel(ETIQUETA, fontweight='bold')
    ax.set_xlabel('Fecha')
    ax.set_title(TITULO, fontweight='bold')
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    guardar(NOMBRE_SALIDA)
    print(f"Gráfico guardado: {NOMBRE_SALIDA}")


if __name__ == "__main__":
    main()
