"""
descargar_era5.py — Descarga datos de reanálisis ERA5 desde Copernicus CDS
========================================================================================
Plantilla genérica para descargar variables de ERA5 Single Levels para cualquier región
y período de tiempo. Edita la sección de CONFIGURACIÓN y ejecuta el script.

Requisitos:
    pip install cdsapi

    Cuenta en Copernicus CDS: https://cds.climate.copernicus.eu/
    Archivo de credenciales ~/.cdsapirc con el formato:
        url: https://cds.climate.copernicus.eu/api
        key: <tu-api-key>

Ejecución:
    python descargar_era5.py

Laboratorio de Oceanografía Física (LOFA)
Instituto de Ciencias Marinas y Limnológicas | Universidad Austral de Chile
https://github.com/Laboratorio-Oceanografia-Fisica-UACh
========================================================================================
"""

import os
import cdsapi

# ══════════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN — edita esta sección antes de ejecutar
# ══════════════════════════════════════════════════════════════════════════════════

# Región de interés: [lat_norte, lon_oeste, lat_sur, lon_este]
# Ejemplo: costa de Valdivia → [-39.5, -74.0, -40.5, -73.0]
# Ejemplo: costa centro-sur de Chile → [-30.0, -76.0, -45.0, -70.0]
AREA = [-39.5, -74.0, -40.5, -73.0]

# Rango de años a descargar (incluye ambos extremos)
AÑO_INICIO = 2000
AÑO_FIN    = 2024

# Meses a incluir (lista de strings con cero a la izquierda)
MESES = ['01', '02', '03', '04', '05', '06',
         '07', '08', '09', '10', '11', '12']

# Días del mes a incluir. Usa ['01'] para datos mensuales (día representativo),
# o lista todos los días para series diarias.
DIAS = ['01', '15']

# Hora UTC de los datos (formato 'HH:00')
HORA = '12:00'

# Variables a descargar.
# Referencia completa: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels
# Variables de flujos de calor superficial (más comunes en oceanografía):
VARIABLES = [
    'surface_net_solar_radiation',        # Radiación solar neta (acumulada)
    'surface_net_thermal_radiation',      # Radiación de onda larga neta (acumulada)
    'surface_latent_heat_flux',           # Flujo de calor latente (acumulado)
    'surface_sensible_heat_flux',         # Flujo de calor sensible (acumulado)
    'sea_surface_temperature',            # Temperatura superficial del mar (instantánea)
    # '10m_u_component_of_wind',          # Viento zonal a 10m
    # '10m_v_component_of_wind',          # Viento meridional a 10m
    # '2m_temperature',                   # Temperatura del aire a 2m
    # 'mean_sea_level_pressure',          # Presión a nivel del mar
]

# Nombre del archivo de salida (se guarda en la misma carpeta que el script)
NOMBRE_ARCHIVO = 'era5_datos.nc'

# ══════════════════════════════════════════════════════════════════════════════════

def descargar_era5():
    print("Iniciando conexión con Copernicus CDS...")
    c = cdsapi.Client()

    años = [str(a) for a in range(AÑO_INICIO, AÑO_FIN + 1)]

    parametros = {
        'product_type': 'reanalysis',
        'variable'    : VARIABLES,
        'year'        : años,
        'month'       : MESES,
        'day'         : DIAS,
        'time'        : HORA,
        'format'      : 'netcdf',
        'area'        : AREA,
    }

    ruta_salida = os.path.join(os.path.dirname(os.path.abspath(__file__)), NOMBRE_ARCHIVO)

    print(f"Región   : {AREA}  (N, O, S, E)")
    print(f"Período  : {AÑO_INICIO}–{AÑO_FIN}")
    print(f"Variables: {len(VARIABLES)}")
    print(f"Salida   : {ruta_salida}")
    print("\nDescargando... (puede tardar varios minutos según el tamaño de la solicitud)")

    c.retrieve('reanalysis-era5-single-levels', parametros, ruta_salida)

    print(f"\n¡Descarga completada! Archivo guardado en:\n{ruta_salida}")
    print("\nNota: si CDS devuelve un .zip en lugar de .nc, descomprímelo manualmente.")
    print("Los archivos acumulados e instantáneos pueden venir en ficheros separados.")


if __name__ == "__main__":
    descargar_era5()
