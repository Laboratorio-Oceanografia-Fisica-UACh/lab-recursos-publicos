"""
extraer_modis_gee.py — Extracción de datos MODIS desde Google Earth Engine
========================================================================================
Plantilla genérica para descargar imágenes de la colección MODIS Aqua (L3SMI) usando
la API de Google Earth Engine. Edita la sección de CONFIGURACIÓN y ejecuta el script.

Requisitos:
    pip install earthengine-api requests

    Cuenta de Google Cloud con acceso a Earth Engine.
    Autenticación inicial (solo una vez):
        earthengine authenticate

Ejecución:
    python extraer_modis_gee.py

Productos MODIS disponibles en GEE (NASA/OCEANDATA/MODIS-Aqua/L3SMI):
    'sst'    — Temperatura Superficial del Mar (°C)
    'chlor_a'— Concentración de clorofila-a (mg/m³)
    'Rrs_*'  — Reflectancia de teledetección por banda

Laboratorio de Oceanografía Física (LOFA)
Instituto de Ciencias Marinas y Limnológicas | Universidad Austral de Chile
https://github.com/Laboratorio-Oceanografia-Fisica-UACh
========================================================================================
"""

import os
import requests
import ee

# ══════════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN — edita esta sección antes de ejecutar
# ══════════════════════════════════════════════════════════════════════════════════

# ID de tu proyecto de Google Cloud con Earth Engine habilitado
GEE_PROJECT = 'tu-proyecto-gee'

# Región de interés: [lon_min, lat_min, lon_max, lat_max]
# Ejemplo: costa de Valdivia → [-74.0, -40.5, -73.0, -39.5]
# Ejemplo: costa centro-sur de Chile → [-76.0, -45.0, -70.0, -30.0]
REGION = [-74.0, -40.5, -73.0, -39.5]

# Rango de fechas para calcular el promedio temporal ('YYYY-MM-DD')
FECHA_INICIO = '2000-01-01'
FECHA_FIN    = '2024-12-31'

# Variable de la colección a extraer (ver opciones en el docstring del módulo)
VARIABLE = 'sst'

# Resolución espacial en metros (MODIS L3SMI tiene ~4 km de resolución nativa)
ESCALA_METROS = 4000

# Nombre del archivo de salida GeoTIFF (se guarda en la misma carpeta que el script)
NOMBRE_ARCHIVO = 'modis_promedio.tif'

# ══════════════════════════════════════════════════════════════════════════════════

def extraer_modis():
    print("Inicializando Google Earth Engine...")
    ee.Initialize(project=GEE_PROJECT)

    roi = ee.Geometry.Rectangle(REGION)

    print(f"Colección : NASA/OCEANDATA/MODIS-Aqua/L3SMI  →  banda '{VARIABLE}'")
    print(f"Período   : {FECHA_INICIO} — {FECHA_FIN}")
    print(f"Región    : {REGION}  (lon_min, lat_min, lon_max, lat_max)")
    print(f"Resolución: {ESCALA_METROS} m")

    dataset = (
        ee.ImageCollection('NASA/OCEANDATA/MODIS-Aqua/L3SMI')
        .filterDate(FECHA_INICIO, FECHA_FIN)
        .select(VARIABLE)
    )

    imagen_promedio = dataset.mean().clip(roi)

    print("\nGenerando enlace de descarga...")
    url = imagen_promedio.getDownloadURL({
        'scale' : ESCALA_METROS,
        'crs'   : 'EPSG:4326',
        'region': roi,
        'format': 'GEO_TIFF',
    })

    ruta_salida = os.path.join(os.path.dirname(os.path.abspath(__file__)), NOMBRE_ARCHIVO)

    print("Descargando imagen... (puede tardar unos momentos)")
    respuesta = requests.get(url, timeout=120)
    respuesta.raise_for_status()

    with open(ruta_salida, 'wb') as f:
        f.write(respuesta.content)

    print(f"\n¡Descarga completada! Archivo guardado en:\n{ruta_salida}")
    print("\nPuedes abrirlo con QGIS, xarray+rioxarray, o rasterio.")


if __name__ == "__main__":
    extraer_modis()
