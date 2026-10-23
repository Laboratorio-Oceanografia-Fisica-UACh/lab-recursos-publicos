# Plantilla LaTeX — Tesis de Grado, Escuela de Biología Marina (UACh)

Plantilla para escribir la Tesis de Grado de **Biología Marina** de la
Universidad Austral de Chile. Reproduce en LaTeX las *Pautas para la
presentación del documento de la Tesis* de la Escuela

```
plantilla-tesis-bima/
├── README.md                   ← este archivo
├── tesis-bima-overleaf.zip     ← súbelo tal cual a Overleaf
└── tesis-bima/                 ← la plantilla (cópiala si trabajas en tu PC)
```

> **¿Nunca has usado LaTeX?** Anda directo a [Opción A: Overleaf](#opción-a--overleaf-recomendado-si-recién-partes).
> No tienes que instalar nada y se edita desde el navegador.

---

## Opción A — Overleaf (recomendado si recién partes)

Overleaf es un editor de LaTeX que corre en el navegador: escribes a la
izquierda y ves el PDF a la derecha. Es gratis para un proyecto como este y te
evita instalar nada.

### 1. Consigue el ZIP

Necesitas el archivo **`tesis-bima-overleaf.zip`** de esta carpeta.

- **Si estás viendo esto en GitHub:** entra a `tesis-bima-overleaf.zip`
  y aprieta el botón **Download** (o **Raw**). El navegador lo baja solo.
- **Si clonaste el repositorio:** ya lo tienes en esta misma carpeta.

> El ZIP contiene exactamente lo mismo que la carpeta `tesis-bima/`, pero
> empaquetado como Overleaf lo necesita (con `main.tex` en la raíz).

### 2. Crea el proyecto

1. Entra a [overleaf.com](https://www.overleaf.com) y crea una cuenta (sirve tu
   correo UACh).
2. Botón verde **New Project** → **Upload Project**.
3. Arrastra `tesis-bima-overleaf.zip` a la ventana que se abre.
4. Espera unos segundos: Overleaf descomprime todo y te deja dentro del
   proyecto.

### 3. Configura el compilador

Esto es importante y se hace **una sola vez**. Arriba a la izquierda, en
**Menu**:

| Opción | Valor |
|---|---|
| **Compiler** | `pdfLaTeX` |
| **TeX Live version** | 2021 o posterior (deja la más nueva) |
| **Main document** | `main.tex` |

Cierra el menú y aprieta **Recompile**. Deberías ver la portada en el PDF de la
derecha. Si sale un error, mira [Problemas frecuentes](#problemas-frecuentes).

### 4. Escribe

En el panel de archivos de la izquierda:

- **`config.tex`** → tus datos: título, nombre, profesor patrocinante, año.
  Es el único archivo que necesitas tocar para personalizar la portada.
- **`capitulos/`** → un archivo por capítulo. Haz doble clic y escribe.
- **`figuras/`** → arrastra aquí tus imágenes (`.png`, `.pdf`, `.jpg`).
- **`referencias.bib`** → pega aquí tus referencias en formato BibTeX. Puedes hacer la conexion directa con Zotero o ddescragar todas tus referencias en un archivo .bib

Overleaf guarda solo, no existe el botón "guardar". Cada vez que quieras ver
cómo va quedando, aprieta **Recompile**.

### 5. Compártelo con tu profesor

Botón **Share** arriba a la derecha → **Turn on link sharing** → copia el link
de *Can edit* o *Can view* y mándaselo. Tu patrocinante puede comentar y
corregir en el mismo documento.

> **Truco para la revisión:** en `main.tex`, cambia la primera línea a
> `\documentclass[times,borrador]{tesisbima}`. Eso numera cada línea del texto
> y tu profesor puede decirte "en la línea 143 cambia tal cosa". Sácalo antes
> de entregar la versión definitiva.

---

## Opción B — En tu computador (VS Code u otro editor)

Si prefieres trabajar local, con Git y sin depender de internet.

### 1. Instala LaTeX

| Sistema | Qué instalar |
|---|---|
| **Windows** | [MiKTeX](https://miktex.org/download) — instala los paquetes que falten solo, la primera compilación demora |
| **macOS** | [MacTeX](https://tug.org/mactex/) |
| **Linux** | `sudo apt install texlive-full latexmk biber` |

### 2. Copia la plantilla

```bash
git clone https://github.com/Laboratorio-Oceanografia-Fisica-UACh/lab-recursos-publicos.git
cp -r lab-recursos-publicos/plantilla-tesis-bima/tesis-bima ~/mi-tesis
cd ~/mi-tesis
```

### 3. Compila

```bash
latexmk -pdf main.tex
```

`latexmk` se encarga solo de las pasadas de `pdflatex` y de `biber`. Si
prefieres hacerlo a mano:

```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

Para borrar los archivos auxiliares: `latexmk -c` (o `latexmk -C` si también
quieres borrar el PDF).

### 4. VS Code

Instala la extensión **LaTeX Workshop** (James Yu). Con eso tienes compilación
automática al guardar, vista previa del PDF al lado, y `Ctrl+click` para saltar
del texto al PDF y viceversa. No necesitas configurar nada más: la extensión
detecta `latexmk`.

---

## Estructura de la plantilla

```
tesis-bima/
├── main.tex              ← documento principal: el orden.
├── config.tex            ← Los Datos: Nombres, etc.
├── tesisbima.cls         ← la clase; no hace falta tocarla
├── referencias.bib       ← bibliografía
├── capitulos/
│   ├── 00_dedicatoria.tex
│   ├── 01_agradecimientos.tex
│   ├── 02_abreviaturas.tex
│   ├── 03_resumen.tex           → 1. Resumen
│   ├── 04_summary.tex           →    Summary
│   ├── 05_introduccion.tex      → 2. Introducción
│   ├── 06_materiales.tex        → 3. Materiales y Métodos
│   ├── 07_resultados.tex        → 4. Resultados
│   ├── 08_discusion.tex         → 5. Discusión;conclusiones
│   └── 09_anexos.tex            → 7. Anexos
├── figuras/              ← tus figuras
└── logos/                ← escudo UACh y de tu laboratorio
```

La **Literatura citada** (capítulo 6) se genera sola desde `referencias.bib`.

---

## Cómo se escriben las cosas

### Citar en el texto

```latex
Como parte de la frase:   \textcite{Dayton1984}   →  Dayton et al. (1984)
Entre paréntesis:         \parencite{Dayton1984}  →  (Dayton et al., 1984)
Varias a la vez:          \parencite{Conover1980, Dayton1984}
```

En overleaf puedes usar la conexion con zotero o hacerlo a mano, donde buscas el trabajo en Google Scholar o en el
sitio de la revista, usa **Exportar / Cite → BibTeX** y pega el resultado en
`referencias.bib`. Ahí ya están los cuatro ejemplos de la pauta (revista,
libro, tesis y capítulo de libro) para que los uses de molde.

### Figuras

Número arábigo, título y leyenda **bajo** el cuerpo de la figura:

```latex
\figura[0.8\linewidth]{area_estudio.png}
  {Área de estudio. Batimetría de la plataforma continental frente a Valdivia
   y ubicación de las estaciones de muestreo. Fuente: elaboración propia.}
  {area-estudio}
```

Se cita con `\reffig{area-estudio}` → «Figura 1».

### Tablas

Número romano en mayúscula, numeración y título **sobre** el cuerpo:

```latex
\begin{tablabima}{Conjuntos de datos utilizados.}{datos}
  \begin{tabular}{llll}
    \toprule
    \textbf{Producto} & \textbf{Variable} & \textbf{Resolución} & \textbf{Período} \\
    \midrule
    ERA5 & Viento a 10 m & 0,25\textdegree{} / 1 h & 1990--2024 \\
    \bottomrule
  \end{tabular}
\end{tablabima}
```

Se cita con `\reftab{datos}` → «Tabla I».

### Nombres científicos, palabras extranjeras y unidades

```latex
\especie{Macrocystis pyrifera}    →  Macrocystis pyrifera (cursiva)
\extranjero{upwelling}            →  upwelling (cursiva)
\qty{12.4}{\degreeCelsius}        →  12,4 °C
\qty{0.25}{\meter\per\second}     →  0,25 m/s
```

---

## Opciones de la clase

En la primera línea de `main.tex`:

```latex
\documentclass[times]{tesisbima}            % Times New Roman (por defecto)
\documentclass[arial]{tesisbima}            % Arial / Helvetica
\documentclass[times,borrador]{tesisbima}   % numera las líneas, para la revisión
```

La pauta acepta Times New Roman o Arial, ambas tamaño 12.

---

## Portada

La portada sigue el **Anexo 3 del Reglamento**, con el logo institucional de la
UACh arriba al centro y la Escuela debajo, que es como vienen las tesis de
Biología Marina aprobadas. Todo se controla desde `config.tex`:

- **Cambiar o sacar el logo:** en el bloque `\logosportada{...}` hay cuatro
  variantes listas — logo UACh solo (la que viene activa), sin logo para el
  Anexo 3 literal, UACh + ICML lado a lado, y escudo UACh + logo del
  laboratorio. En `logos/` están todos los archivos, listados en `config.tex`
  con una línea que explica cuál es cuál.
- **Profesor co-patrocinante:** los tres comandos `\copatrocinante{}`,
  `\institutocopatrocinante{}` y `\facultadcopatrocinante{}`. Si los dejas
  vacíos, el bloque entero desaparece de la portada.
- **Profesores informantes:** el comando `\informantes{}` recibe un bloque
  libre, así que caben tantos como tenga tu comisión. El Anexo 3 solo menciona
  al co-patrocinante, pero las tesis aprobadas suelen listar también a los
  informantes, con su instituto y facultad.

El bloque de profesores va en la mitad derecha de la página, alineado con el
de la mención del grado, igual que en el Anexo 3 y en las tesis aprobadas.

La portada cabe en una sola página incluso con patrocinante, co-patrocinante y
dos informantes. Si tu comisión es más numerosa y se parte en dos, baja el
ancho del logo en `config.tex` (de `6.5cm` a `5cm`, por ejemplo).

> El título y el nombre del autor se imprimen en MAYÚSCULA automáticamente,
> como pide la pauta — escríbelos normales en `config.tex`, con sus tildes.
> (Algunas tesis aprobadas los dejan en minúscula; si tu comisión lo prefiere
> así, quita los `\MakeUppercase` del comando `\portada` en `tesisbima.cls`.)

---

## Agradecer al laboratorio

Si la plantilla te sirvió, dejar una línea en tus Agradecimientos nos ayuda a
que el laboratorio la siga manteniendo. **Ya viene incluida** al final de
`capitulos/01_agradecimientos.tex`:

```latex
Este documento fue formateado con la plantilla \LaTeX{} para tesis de Biología
Marina desarrollada por el \textbf{Laboratorio de Oceanografía Física (LOFA)}
de la Universidad Austral de Chile.
```

Es completamente voluntaria: si no la quieres, borra esas líneas y listo.

---

## Decisiones que conviene conocer

Tres puntos donde la pauta de la Escuela no es definitiva y pueddes decidir sobre la plantilla:

1. **El Summary va sin número.** La pauta rotula tanto el Resumen como el
   Summary con un «1.», y después numera la Introducción como «2.». Se tomó el
   «1.» del Summary como errata: acá el Summary es un capítulo sin número que
   sí aparece en el Índice General, y la Introducción conserva el número 2. Si
   tu comisión prefiere que lleve número, en `capitulos/04_summary.tex` cambia
   `\capitulosinnumero{Summary}` por `\chapter{Summary}` (la Introducción
   pasará a ser el capítulo 3).

2. **La Dedicatoria y los Agradecimientos no llevan número de página** ni
   aparecen en el Índice, porque la pauta hace partir la numeración recién en
   el Índice General. En `tesisbima.cls` hay un comentario sobre cómo
   incluirlos si lo prefieres.

3. **Las conclusiones y proyecciones son secciones de la Discusión**, no un
   capítulo aparte, porque la pauta dice que «la parte final de la discusión
   corresponderá a las conclusiones y proyecciones del trabajo».

Una diferencia menor de formato: el estilo APA abrevia la edición como
«2.ª ed.» mientras la pauta escribe «2ª. Ed.». Si tu comisión es estricta en
esto, revísalo en el PDF final.

---

## Qué exige la pauta y cómo lo resuelve la plantilla

| Requisito de la Escuela | Cómo está implementado |
|---|---|
| Papel tamaño carta | `geometry` con `letterpaper` |
| Márgenes superior e izquierdo 3,0 cm; inferior 2,5 cm; derecho 2,0 cm | `geometry` |
| Letra Times New Roman o Arial, tamaño 12 | opción de clase `[times]` o `[arial]` |
| Doble espacio | `setspace` con `\doublespacing` |
| Número de página en el ángulo superior derecho | `fancyhdr`, también en las páginas de inicio de capítulo |
| Numeración romana minúscula desde el Índice General | `\iniciarpreliminares` |
| Numeración arábiga desde el capítulo 1 Resumen | `\iniciarcuerpo` |
| Figuras en números arábigos, título y leyenda **bajo** la figura | `\figura{...}` |
| Tablas en números romanos mayúsculos, título **sobre** la tabla | entorno `tablabima` |
| Numeración corrida de figuras y tablas en toda la tesis | `chngcntr` |
| Citas Becker (1968) / (Becker, 1968) / (Becker y Ortiz, 1968) / (Becker et al., 1968) | `biblatex` estilo APA mapeado al español |
| Bibliografía alfabética, solo la literatura citada | `biblatex` + `biber` |
| Nombres científicos y palabras extranjeras en cursiva | `\especie{}` y `\extranjero{}` |

---

## Problemas frecuentes

**«Undefined control sequence» en `\printbibliography` o citas que salen como
`[Dayton1984]`.**
Falta correr `biber`. En Overleaf basta apretar **Recompile** una segunda vez.
En local, usa `latexmk -pdf main.tex` en vez de solo `pdflatex`.

**En Overleaf sale un error raro apenas subo el proyecto.**
Revisa que en *Menu* el **Compiler** sea `pdfLaTeX` (no XeLaTeX ni LuaLaTeX) y
que **Main document** sea `main.tex`.

«File `tesisbima.cls' not found».
El `.cls` tiene que estar en la misma carpeta que `main.tex`. Si subiste los
archivos sueltos a Overleaf en vez del ZIP, probablemente quedó dentro de una
subcarpeta: arrástralo a la raíz del proyecto.

**En MiKTeX la primera compilación demora muchísimo o abre ventanas.**
Está descargando los paquetes que faltan. Déjalo terminar y acepta las
instalaciones; la segunda vez es rápida.

**Una figura no aparece.**
Revisa que el archivo esté en `figuras/` y que lo llames por su nombre sin la
ruta: `\figura{area_estudio.png}{...}{...}`, no `figuras/area_estudio.png`.

**Quiero usar XeLaTeX o LuaLaTeX.**
Funciona: la clase detecta el motor y usa las fuentes Times New Roman o Arial
reales del sistema. Solo cámbialo en *Menu → Compiler*.

---

## Antes de entregar

- [ ] Sacaste la opción `borrador` de `\documentclass`.
- [ ] El Resumen y el Summary no exceden una hoja tamaño carta cada uno.
- [ ] Todas las figuras y tablas están citadas en el texto y aparecen en la
      página siguiente a su primera cita.
- [ ] Las figuras y tablas están en castellano e indican la fuente si no son
      originales.
- [ ] La bibliografía contiene solo la literatura citada.
- [ ] Agradeciste en forma detallada a la institución que financió la
      investigación (FONDECYT, proyecto, fundación, etc.).
- [ ] El ejemplar definitivo se entrega **en PDF a la Escuela**.


---

_Plantilla mantenida por el Laboratorio de Oceanografía Física (LOFA) —
Universidad Austral de Chile._
