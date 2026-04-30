"""
mapa_sst.py — Plantilla para mapas de Temperatura Superficial del Mar (SST)
========================================================================================
Genera un mapa de la costa chilena con datos de SST usando cartopy.
Funciona con datos sintéticos por defecto; edita CONFIGURACIÓN para usar datos reales.

Requisitos:
    pip install matplotlib numpy netCDF4 xarray
    conda install cartopy          ← instalar con conda es más confiable que pip

Ejecución:
    python mapa_sst.py

Laboratorio de Oceanografía Física (LOFA)
Instituto de Ciencias Marinas y Limnológicas | Universidad Austral de Chile
https://github.com/Laboratorio-Oceanografia-Fisica-UACh
========================================================================================
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Intentar importar lofa_style desde el toolbox
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from toolbox import lofa_style as ls
    ls.apply()
    COLOR_TIERRA = ls.MAPA['tierra']
    COLOR_COSTA  = ls.MAPA['costa']
    guardar      = ls.guardar_figura
except ImportError:
    COLOR_TIERRA = 'dimgray'
    COLOR_COSTA  = 'black'
    def guardar(nombre, directorio='figuras'):
        os.makedirs(directorio, exist_ok=True)
        plt.savefig(os.path.join(directorio, nombre), dpi=300, bbox_inches='tight')
        plt.close('all')

# ══════════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN — edita esta sección para usar datos reales
# ══════════════════════════════════════════════════════════════════════════════════

# Ruta al archivo NetCDF con SST (dejar vacío para usar datos sintéticos)
ARCHIVO_SST = ""

# Extensión del mapa: [lon_min, lon_max, lat_min, lat_max]
EXTENSION = [-76.0, -68.0, -45.0, -28.0]

# Rectángulo de zona de estudio (opcional, dejar None para omitir)
# Formato: [lon_min, lon_max, lat_min, lat_max]
ZONA_ESTUDIO = [-74.0, -72.0, -41.0, -39.0]

# Título del mapa
TITULO = 'Temperatura Superficial del Mar — Costa de Chile'

# Nombre del archivo de salida
NOMBRE_SALIDA = 'mapa_sst.png'

# ══════════════════════════════════════════════════════════════════════════════════


def generar_sst_sintetica(extension):
    """Genera una grilla de SST sintética para demostración."""
    lon = np.linspace(extension[0], extension[1], 120)
    lat = np.linspace(extension[2], extension[3], 160)
    LON, LAT = np.meshgrid(lon, lat)

    # SST base: más fría hacia el sur y cerca de la costa
    sst = (
        18.0
        + (LAT - extension[2]) * 0.25          # gradiente latitudinal
        + (LON - extension[1]) * (-0.8)         # más fría cerca de la costa
        + np.random.normal(0, 0.4, LON.shape)   # ruido
    )
    # Enfriar zona de surgencia costera (cerca de -71° lon)
    sst += np.exp(-((LON - (-72.0))**2 / 1.5)) * (-3.0)
    return lon, lat, sst


def cargar_sst_netcdf(archivo):
    """Carga SST promedio desde un archivo NetCDF con xarray."""
    import xarray as xr
    ds = xr.open_dataset(archivo)

    # Detectar variable SST (nombres comunes en ERA5 y MODIS)
    candidatos = ['sst', 'analysed_sst', 'sea_surface_temperature', 'SST']
    var = next((v for v in candidatos if v in ds.data_vars), None)
    if var is None:
        raise ValueError(f"No se encontró variable SST. Variables disponibles: {list(ds.data_vars)}")

    # Detectar coordenadas lat/lon
    lat_dim = next((d for d in ['lat', 'latitude'] if d in ds.coords), None)
    lon_dim = next((d for d in ['lon', 'longitude'] if d in ds.coords), None)

    sst_media = ds[var].mean(dim='time') if 'time' in ds[var].dims else ds[var]
    return ds[lon_dim].values, ds[lat_dim].values, sst_media.values


def main():
    try:
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
    except ImportError:
        print("ERROR: cartopy no está instalado.")
        print("Instalar con: conda install cartopy")
        return

    # Cargar o generar datos SST
    if ARCHIVO_SST and os.path.exists(ARCHIVO_SST):
        print(f"Cargando SST desde: {ARCHIVO_SST}")
        lon, lat, sst = cargar_sst_netcdf(ARCHIVO_SST)
    else:
        if ARCHIVO_SST:
            print(f"Archivo no encontrado: {ARCHIVO_SST}")
        print("Usando datos sintéticos de demostración...")
        lon, lat, sst = generar_sst_sintetica(EXTENSION)

    # ── Crear mapa ──────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(8, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())
    ax.set_extent(EXTENSION, crs=ccrs.PlateCarree())

    # Fondo del mapa
    ax.add_feature(cfeature.LAND,       facecolor=COLOR_TIERRA, zorder=2)
    ax.add_feature(cfeature.COASTLINE,  edgecolor=COLOR_COSTA, linewidth=0.8, zorder=3)
    ax.add_feature(cfeature.BORDERS,    edgecolor='gray',       linewidth=0.5, zorder=3)
    ax.add_feature(cfeature.RIVERS,     edgecolor='steelblue',  linewidth=0.3, zorder=3)

    # Cuadrícula con etiquetas
    gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5, zorder=4)
    gl.top_labels   = False
    gl.right_labels = False

    # Campo de SST
    LON, LAT = np.meshgrid(lon, lat) if lon.ndim == 1 else (lon, lat)
    cf = ax.contourf(
        LON, LAT, sst,
        levels=20, cmap='RdYlBu_r',
        transform=ccrs.PlateCarree(), zorder=1
    )
    cbar = plt.colorbar(cf, ax=ax, orientation='vertical', pad=0.06, shrink=0.75)
    cbar.set_label('SST (°C)', fontweight='bold')

    # Zona de estudio (si está definida)
    if ZONA_ESTUDIO is not None:
        lon_min, lon_max, lat_min, lat_max = ZONA_ESTUDIO
        rect_lon = [lon_min, lon_max, lon_max, lon_min, lon_min]
        rect_lat = [lat_min, lat_min, lat_max, lat_max, lat_min]
        ax.plot(rect_lon, rect_lat, color='white', linewidth=2.0,
                linestyle='--', transform=ccrs.PlateCarree(), zorder=5)

    ax.set_title(TITULO, fontweight='bold', pad=10)

    guardar(NOMBRE_SALIDA)
    print(f"Mapa guardado: {NOMBRE_SALIDA}")


if __name__ == "__main__":
    main()
