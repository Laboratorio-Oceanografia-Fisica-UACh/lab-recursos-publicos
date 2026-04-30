"""
lofa_style.py — Configuración de estilo gráfico del LOFA
========================================================================================
Módulo importable que estandariza colores, tamaños y parámetros de visualización para
figuras producidas en el Laboratorio de Oceanografía Física (LOFA).

Uso básico:
    import lofa_style as ls

    ls.apply()                       # Activa rcParams del LOFA
    plt.plot(t, sst, color=ls.COLORES['sst'])
    ls.guardar_figura('serie_sst.png')

Laboratorio de Oceanografía Física (LOFA)
Instituto de Ciencias Marinas y Limnológicas | Universidad Austral de Chile
https://github.com/Laboratorio-Oceanografia-Fisica-UACh
========================================================================================
"""

import os
import matplotlib as mpl
import matplotlib.pyplot as plt

# ── Paleta de colores para variables oceanográficas ────────────────────────────
COLORES = {
    # Flujos de calor superficial
    'ssr'          : '#E07A30',  # Radiación solar neta (naranja)
    'str'          : '#D62728',  # Radiación onda larga neta (rojo)
    'slhf'         : '#1F77B4',  # Calor latente (azul)
    'sshf'         : '#9467BD',  # Calor sensible (morado)
    'qt'           : '#000000',  # Balance total Qt (negro)
    # Variables oceánicas y atmosféricas
    'sst'          : '#D62728',  # Temperatura superficial del mar (rojo)
    't2m'          : '#0072BD',  # Temperatura del aire a 2m (azul MATLAB)
    'wind'         : '#2C2C2C',  # Viento (gris oscuro)
    'ui'           : '#2CA02C',  # Índice de surgencia Ekman (verde)
    # Surgencia / no-surgencia
    'surgencia'    : '#CC4D4D',  # Evento de surgencia (rojo)
    'no_surgencia' : '#4D4DCC',  # Sin evento (azul)
    # Anomalías
    'positivo'     : '#D62728',  # Anomalía positiva (rojo)
    'negativo'     : '#1F77B4',  # Anomalía negativa (azul)
}

# ── Tamaños de figura estándar (ancho, alto en pulgadas) ──────────────────────
FIGSIZE = {
    'serie_tiempo' : (12, 5),
    'mapa'         : (7, 8),
    'climatologia' : (10, 5),
    'anomalias'    : (14, 4),
    'multi_panel'  : (10, 9),
    'correlacion'  : (8, 6),
    'heatmap'      : (8, 6),
}

# ── Configuración de mapas (cartopy) ──────────────────────────────────────────
MAPA = {
    'tierra'     : 'dimgray',   # Color de la tierra
    'costa'      : 'black',     # Color de la línea costera
    'grid_ls'    : '--',        # Estilo de la cuadrícula
    'grid_alpha' : 0.4,         # Transparencia de la cuadrícula
}


def apply():
    """
    Aplica los rcParams del LOFA al contexto actual de matplotlib.
    Llamar una vez al comienzo del script o notebook.
    """
    mpl.rcParams.update({
        'font.size'             : 11,
        'axes.titlesize'        : 12,
        'axes.titleweight'      : 'bold',
        'axes.labelsize'        : 11,
        'axes.labelweight'      : 'bold',
        'xtick.labelsize'       : 10,
        'ytick.labelsize'       : 10,
        'lines.linewidth'       : 1.5,
        'axes.grid'             : True,
        'grid.alpha'            : 0.3,
        'grid.linestyle'        : '--',
        'figure.dpi'            : 100,
        'savefig.dpi'           : 300,
        'savefig.bbox'          : 'tight',
    })


def guardar_figura(nombre_archivo, directorio='figuras'):
    """
    Guarda la figura activa con dpi=300 y cierra el contexto.

    Parámetros
    ----------
    nombre_archivo : str  Nombre del archivo (ej. 'serie_sst.png')
    directorio     : str  Carpeta de salida (se crea si no existe, default 'figuras')
    """
    os.makedirs(directorio, exist_ok=True)
    ruta = os.path.join(directorio, nombre_archivo)
    plt.savefig(ruta, bbox_inches='tight', dpi=300)
    plt.close('all')
    print(f"Figura guardada en: {ruta}")
