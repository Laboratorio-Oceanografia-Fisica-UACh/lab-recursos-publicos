"""
ciclo_estacional.py — Plantilla para el ciclo estacional (climatología mensual)
========================================================================================
Calcula y grafica la climatología mensual de una variable oceanográfica
(media ± desviación estándar) a partir de una serie temporal.
Funciona con datos sintéticos por defecto; edita CONFIGURACIÓN para usar datos reales.

Requisitos:
    pip install matplotlib numpy pandas xarray netCDF4

Ejecución:
    python ciclo_estacional.py

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

# Intentar importar lofa_style desde el toolbox
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from toolbox import lofa_style as ls
    ls.apply()
    guardar = ls.guardar_figura
except ImportError:
    def guardar(nombre, directorio='figuras'):
        os.makedirs(directorio, exist_ok=True)
        plt.savefig(os.path.join(directorio, nombre), dpi=300, bbox_inches='tight')
        plt.close('all')

# ══════════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════════════════

# Para usar datos reales: ruta al archivo NetCDF o CSV
# - NetCDF: debe contener una variable escalar con dimensión temporal
# - CSV   : debe tener columnas 'fecha' y 'valor'
# Dejar vacío para usar datos sintéticos de demostración
ARCHIVO    = ""
VARIABLE   = "sst"        # Nombre de la variable en el NetCDF (si aplica)
ETIQUETA   = "SST (°C)"   # Etiqueta del eje Y
TITULO     = "Ciclo Estacional de SST — Costa de Valdivia"
NOMBRE_SALIDA = "ciclo_estacional.png"

# ══════════════════════════════════════════════════════════════════════════════════

MESES_ES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']


def generar_serie_sintetica():
    """Serie mensual de SST sintética con ciclo estacional (2015–2024)."""
    fechas = pd.date_range('2015-01-01', '2024-12-31', freq='MS')
    meses  = np.array([f.month for f in fechas])
    ciclo  = 2.5 * np.cos(2 * np.pi * (meses - 1) / 12)   # máx verano austral
    ruido  = np.random.normal(0, 0.6, len(fechas))
    sst    = 13.5 + ciclo + ruido
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

    print(f"Período: {serie.index[0].date()} → {serie.index[-1].date()}  ({len(serie)} datos)")

    # Climatología mensual
    df = pd.DataFrame({'valor': serie, 'mes': serie.index.month})
    clim = df.groupby('mes')['valor'].agg(['mean', 'std'])

    print("\nClimatología mensual (media ± std):")
    for i, row in clim.iterrows():
        print(f"  {MESES_ES[i-1]:>3}: {row['mean']:+.2f} ± {row['std']:.2f}")

    # ── Gráfico ──────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(11, 5))

    x     = np.arange(1, 13)
    media = clim['mean'].values
    std   = clim['std'].values

    # Barras de fondo (media)
    bars = ax.bar(x, media, color='#4C72B0', alpha=0.5, width=0.6, label='Media mensual')

    # Línea con sombreado ±1 std
    ax.plot(x, media, color='#1F4E8C', linewidth=2.5, marker='o',
            markersize=6, zorder=3, label='Climatología')
    ax.fill_between(x, media - std, media + std,
                    color='#4C72B0', alpha=0.2, label='±1 desv. estándar')

    # Línea de la media anual
    media_anual = media.mean()
    ax.axhline(media_anual, color='black', linestyle='--', linewidth=1.2,
               label=f'Media anual ({media_anual:.1f})')

    ax.set_xticks(x)
    ax.set_xticklabels(MESES_ES)
    ax.set_xlabel('Mes', fontweight='bold')
    ax.set_ylabel(ETIQUETA, fontweight='bold')
    ax.set_title(TITULO, fontweight='bold')
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    guardar(NOMBRE_SALIDA)
    print(f"\nGráfico guardado: {NOMBRE_SALIDA}")


if __name__ == "__main__":
    main()
