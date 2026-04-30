"""
indices_surgencia.py — Índice de Upwelling de Ekman desde ERA5
========================================================================================
Calcula el Índice de Upwelling de Ekman (IUE) a partir de datos de viento ERA5,
lo grafica como serie de tiempo y lo exporta a CSV.

El IUE mide el transporte de Ekman perpendicular a la costa (componente offshore).
Valores positivos indican condiciones favorables para la surgencia costera.

Requisitos:
    pip install xarray numpy pandas matplotlib netCDF4

    El archivo ERA5 debe contener las variables de viento a 10m. Puedes descargarlo
    usando el script scripts/descargar_era5/descargar_era5.py con estas variables:
        '10m_u_component_of_wind'
        '10m_v_component_of_wind'

Ejecución:
    python indices_surgencia.py

Referencia:
    Bakun (1973). Coastal upwelling indices, west coast of North America.
    NOAA Technical Report NMFS SSRF-671.

Laboratorio de Oceanografía Física (LOFA)
Instituto de Ciencias Marinas y Limnológicas | Universidad Austral de Chile
https://github.com/Laboratorio-Oceanografia-Fisica-UACh
========================================================================================
"""

import os
import sys
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ══════════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN — edita esta sección antes de ejecutar
# ══════════════════════════════════════════════════════════════════════════════════

# Ruta al archivo ERA5 con variables u10 y v10
FILE_ERA5 = ""  # Ej: "era5_vientos_valdivia.nc"

# Latitud de referencia para el parámetro de Coriolis (punto costero de interés)
# Valdivia: -39.8 | Puerto Montt: -41.5 | Coquimbo: -30.0
LAT_REFERENCIA = -39.8

# Orientación de la costa: ángulo en grados desde el norte, sentido horario.
# Para la costa central y sur de Chile se usa ~30.7°
# (la costa inclina levemente al oeste respecto al eje N-S)
ANGULO_COSTA_DEG = 30.7

# Nombre del archivo CSV de salida
NOMBRE_CSV = 'iue_ekman.csv'

# ── Constantes físicas ─────────────────────────────────────────────────────────
RHO_AIRE  = 1.225    # Densidad del aire (kg/m³)
CD        = 1.3e-3   # Coeficiente de arrastre bulk (adim.)
RHO_AGUA  = 1025.0   # Densidad del agua de mar (kg/m³)
OMEGA     = 7.2921e-5  # Velocidad angular de la Tierra (rad/s)

# ══════════════════════════════════════════════════════════════════════════════════


def _detectar_variables_viento(ds):
    """Detecta los nombres de las variables de viento en el dataset."""
    candidatos = {
        'u': ['u10', '10u', 'u_component_of_wind_10m', 'eastward_wind'],
        'v': ['v10', '10v', 'v_component_of_wind_10m', 'northward_wind'],
    }
    u_var, v_var = None, None
    for nombre in candidatos['u']:
        if nombre in ds.data_vars or nombre in ds.coords:
            u_var = nombre; break
    for nombre in candidatos['v']:
        if nombre in ds.data_vars or nombre in ds.coords:
            v_var = nombre; break
    if u_var is None or v_var is None:
        raise ValueError(
            f"No se encontraron variables de viento en el archivo. "
            f"Variables disponibles: {list(ds.data_vars)}"
        )
    return u_var, v_var


def calcular_iue(u10_da, v10_da, lat_ref, angulo_costa_deg):
    """
    Calcula el Índice de Upwelling de Ekman (IUE) como serie temporal.

    Pasos:
      1. Esfuerzo del viento con bulk formula: τ = ρ_aire · Cd · |V| · V
      2. Transporte de Ekman: UE = τ_y / (ρ_agua · f),  VE = -τ_x / (ρ_agua · f)
      3. Proyección sobre la normal a la costa (dirección offshore)
      4. IUE [m³/s por km de costa] = (UE·nx + VE·ny) · 1000

    Convención de signo: IUE > 0 → transporte offshore → condición de surgencia.

    Parámetros
    ----------
    u10_da         : xr.DataArray  Viento zonal a 10m (m/s)
    v10_da         : xr.DataArray  Viento meridional a 10m (m/s)
    lat_ref        : float         Latitud de referencia para Coriolis (°)
    angulo_costa_deg: float        Ángulo de la costa desde el norte, horario (°)

    Retorna
    -------
    xr.DataArray  IUE en m³/s por km, con coordenada temporal
    """
    # 1. Esfuerzo del viento
    vel = np.sqrt(u10_da**2 + v10_da**2)
    tau_x = RHO_AIRE * CD * vel * u10_da
    tau_y = RHO_AIRE * CD * vel * v10_da

    # 2. Parámetro de Coriolis en la latitud de referencia
    f = 2 * OMEGA * np.sin(np.deg2rad(lat_ref))
    if abs(f) < 1e-10:
        raise ValueError("Latitud de referencia demasiado cercana al ecuador (f ≈ 0).")

    # 3. Transporte de Ekman (m²/s)
    UE = tau_y / (RHO_AGUA * f)
    VE = -tau_x / (RHO_AGUA * f)

    # 4. Normal a la costa (dirección offshore)
    theta = np.deg2rad(angulo_costa_deg)
    nx = -np.cos(theta)  # componente zonal del vector offshore
    ny =  np.sin(theta)  # componente meridional del vector offshore

    # 5. IUE (m³/s por km de costa)
    iue = (UE * nx + VE * ny) * 1000.0
    return iue


def main():
    if not FILE_ERA5:
        print("ERROR: Define FILE_ERA5 en la sección de CONFIGURACIÓN antes de ejecutar.")
        sys.exit(1)

    if not os.path.exists(FILE_ERA5):
        print(f"ERROR: No se encontró el archivo: {FILE_ERA5}")
        sys.exit(1)

    print(f"Cargando datos de viento desde: {FILE_ERA5}")
    ds = xr.open_dataset(FILE_ERA5)

    u_var, v_var = _detectar_variables_viento(ds)
    print(f"Variables de viento detectadas: u='{u_var}', v='{v_var}'")

    # Promedio espacial si el dataset tiene dimensiones lat/lon
    dim_space = [d for d in ds[u_var].dims if d not in ('time', 'valid_time')]
    u10 = ds[u_var].mean(dim=dim_space) if dim_space else ds[u_var]
    v10 = ds[v_var].mean(dim=dim_space) if dim_space else ds[v_var]

    # Normalizar nombre de la dimensión temporal
    if 'valid_time' in u10.dims:
        u10 = u10.rename({'valid_time': 'time'})
        v10 = v10.rename({'valid_time': 'time'})

    print(f"Período: {str(u10.time.values[0])[:10]} → {str(u10.time.values[-1])[:10]}")
    print(f"Latitud referencia: {LAT_REFERENCIA}° | Ángulo costa: {ANGULO_COSTA_DEG}°")

    # Calcular IUE
    iue = calcular_iue(u10, v10, LAT_REFERENCIA, ANGULO_COSTA_DEG)

    # Suavizado de 30 días para eliminar variabilidad de alta frecuencia
    iue_suavizado = iue.rolling(time=30, center=True, min_periods=1).mean()

    # ── Exportar a CSV ──────────────────────────────────────────────────────────
    df = pd.DataFrame({
        'fecha'    : iue.time.values,
        'iue'      : iue.values,
        'iue_30d'  : iue_suavizado.values,
    })
    ruta_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), NOMBRE_CSV)
    df.to_csv(ruta_csv, index=False)
    print(f"CSV guardado en: {ruta_csv}")

    # ── Graficar ────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(14, 4))

    ax.plot(iue.time.values, iue.values,
            color='lightsteelblue', linewidth=0.8, alpha=0.6, label='IUE (sin suavizar)')
    ax.plot(iue_suavizado.time.values, iue_suavizado.values,
            color='steelblue', linewidth=2.0, label='IUE (media 30 días)')

    ax.fill_between(iue.time.values, 0, iue.values,
                    where=(iue.values > 0), color='steelblue', alpha=0.25,
                    label='Surgencia favorable')
    ax.fill_between(iue.time.values, 0, iue.values,
                    where=(iue.values < 0), color='tomato', alpha=0.25,
                    label='Hundimiento favorable')

    ax.axhline(0, color='black', linewidth=1.2, linestyle='--')

    ax.set_title(f'Índice de Upwelling de Ekman — lat {LAT_REFERENCIA}°',
                 fontweight='bold')
    ax.set_ylabel('IUE (m³/s por km de costa)')
    ax.set_xlabel('Fecha')
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
