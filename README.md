<div>
  <img src="https://github.com/user-attachments/assets/9bc509a2-df1e-4fdd-9d58-8a9348790565" alt="Logo UACh" align="right" width="110">
  <img src="https://github.com/user-attachments/assets/ddc538b6-92e5-42b3-836f-b4d8da9812c2" alt="Logo_lab" align="left" width="150">
</div>
<br clear="all">
<br>

# 📂 Recursos Públicos y Herramientas Abiertas - LOFA

Bienvenidos al repositorio de ciencia abierta del **Laboratorio de Oceanografía Física (LOFA)** de la Universidad Austral de Chile.

En nuestro laboratorio hemos creado este espacio para compartir con la comunidad estudiantil e investigadora las herramientas, códigos y plantillas que desarrollamos y utilizamos.

---

## Contenido del repositorio

- **`scripts/`**: Códigos ejecutables listos para usar (edita la sección `CONFIGURACIÓN` al inicio de cada script).
  - `balance_calor/` — Calculadora interactiva del balance de calor oceánico (Python y MATLAB).
  - `descargar_era5/` — Plantilla para descargar datos ERA5 desde Copernicus CDS para cualquier región y período.
  - `extraer_modis_gee/` — Plantilla para extraer SST u otras variables de MODIS Aqua vía Google Earth Engine.
  - `indices_surgencia/` — Calcula el Índice de Upwelling de Ekman (IUE) desde datos de viento ERA5. Genera serie temporal y CSV.
- **`toolbox/`**: Funciones importables para usar en tus propios scripts y notebooks.
  - `balance_calor.m` / `balance_calor.py` — Funciones para calcular los componentes del balance de calor (Qt, dH, Qlat, Qsen, Qv…).
  - `lofa_style.py` — Configuración de estilo gráfico del LOFA: paleta de colores, rcParams y helper para guardar figuras.
  - `plantilla_funciones.m` — Plantilla estándar LOFA para documentar nuevas funciones MATLAB.
- **`notebooks/`**: Tutoriales interactivos de Jupyter Notebook.
  - `intro_xarray_netcdf.ipynb` — Introducción a xarray: cómo abrir, explorar, seleccionar, calcular y graficar archivos NetCDF.
  - `balance_calor_ejemplo.ipynb` — Ejemplo guiado del balance de calor usando el toolbox del LOFA.
- **`plantillas/`**: Formatos y recursos de diseño estandarizados para la comunicación científica del laboratorio.


---

## Cómo usar este repo?

Eres libre de descargar, modificar y utilizar estos recursos para tus propios estudios o investigaciones. 

1. **Para descargar todo el repositorio:** Puedes clonarlo usando la terminal:
   `git clone https://github.com/Laboratorio-Oceanografia-Fisica-UACh/lab-recursos-publicos.git`
2. **Requisitos:** Dentro de cada carpeta o script, se indica si se requiere alguna librería específica.
3. **Citar o Agradecer:** Si se utilizan los scripts de este repo para algún proyecto universitario o investigación, agregar agradecimientos nos ayuda a crecer como lab.

---

> Si tienes sugerencias, encuentras algún error en los códigos o te gustaría colaborar con el laboratorio, contactanos.

---

_Repositorio mantenido por el equipo del Laboratorio de Oceanografía Física - Universidad Austral de Chile._