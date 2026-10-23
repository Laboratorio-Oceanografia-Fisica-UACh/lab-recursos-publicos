%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  tesisbima.cls
%  Clase LaTeX para Tesis de Grado
%  Escuela de Biología Marina — Universidad Austral de Chile
%
%  Implementa las "Pautas para la presentación del documento de la Tesis"
%  de la Escuela de Biología Marina y la portada del Anexo 3 del
%  Reglamento de Tesis.
%
%  Mantenido por el Laboratorio de Oceanografía Física (LOFA) — UACh
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{tesisbima}[2026/10/23 v1.0 Tesis Escuela de Biologia Marina UACh]

%------------------------------------------------------------------------------
% OPCIONES DE CLASE
%------------------------------------------------------------------------------
%   [times]     Times New Roman (por defecto)
%   [arial]     Arial / Helvetica — la pauta acepta ambas, tamaño 12
%   [borrador]  numera las líneas del texto (cómodo para la revisión)
%------------------------------------------------------------------------------
\newif\if@bima@arial    \@bima@arialfalse
\newif\if@bima@borrador \@bima@borradorfalse

\DeclareOption{arial}{\@bima@arialtrue}
\DeclareOption{times}{\@bima@arialfalse}
\DeclareOption{borrador}{\@bima@borradortrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions\relax

% Pauta: papel tamaño carta, letra tamaño 12.
\LoadClass[12pt,letterpaper,oneside]{report}

%------------------------------------------------------------------------------
% CODIFICACIÓN Y TIPOGRAFÍA
%------------------------------------------------------------------------------
\RequirePackage{iftex}
\ifPDFTeX
  \RequirePackage[T1]{fontenc}
  \RequirePackage[utf8]{inputenc}
  \if@bima@arial
    \RequirePackage{helvet}
    \renewcommand{\familydefault}{\sfdefault}
  \else
    \RequirePackage{mathptmx}   % Times para texto y matemáticas
  \fi
\else
  % XeLaTeX / LuaLaTeX: usa las fuentes reales instaladas en el sistema
  \RequirePackage{fontspec}
  \if@bima@arial
    \setmainfont{Arial}
  \else
    \setmainfont{Times New Roman}
  \fi
\fi

%------------------------------------------------------------------------------
% IDIOMA
%------------------------------------------------------------------------------
% El inglés queda disponible para el capítulo Summary
% (entorno \begin{otherlanguage}{english}); el idioma principal es el español.
\RequirePackage[english,spanish,es-tabla,es-noquoting,es-lcroman]{babel}

%------------------------------------------------------------------------------
% GEOMETRÍA DE PÁGINA
%   Pauta: papel carta, márgenes superior e izquierdo de 3,0 cm,
%          inferior de 2,5 cm y derecho de 2,0 cm.
%------------------------------------------------------------------------------
\RequirePackage[letterpaper,
                top=3.0cm, left=3.0cm, bottom=2.5cm, right=2.0cm,
                headheight=15pt, headsep=1.0cm,
                heightrounded=true]{geometry}

%------------------------------------------------------------------------------
% INTERLINEADO
%   Pauta: "escrita a doble espacio".
%------------------------------------------------------------------------------
\RequirePackage{setspace}
\doublespacing
\setlength{\parindent}{1.25cm}
\setlength{\parskip}{0pt}
\emergencystretch=2em

%------------------------------------------------------------------------------
% PAQUETES DE APOYO
%------------------------------------------------------------------------------
\RequirePackage{graphicx}
\RequirePackage{float}
\RequirePackage{booktabs}
\RequirePackage{longtable}
\RequirePackage{multirow}
\RequirePackage{array}
\RequirePackage{amsmath,amssymb}
\RequirePackage{siunitx}
\RequirePackage{enumitem}
\RequirePackage{chngcntr}
\RequirePackage{fancyhdr}
\RequirePackage{titlesec}
\RequirePackage{csquotes}
\RequirePackage{xcolor}
\RequirePackage[font={small,singlespacing},
                labelfont=bf, labelsep=period,
                justification=justified,
                singlelinecheck=false]{caption}
\RequirePackage{subcaption}

\if@bima@borrador
  \RequirePackage{lineno}
  \AtBeginDocument{\linenumbers}
\fi

%------------------------------------------------------------------------------
% ENCABEZADO
%   Pauta: "En el ángulo superior derecho deberá consignarse el número
%           de la página."
%------------------------------------------------------------------------------
\pagestyle{fancy}
\fancyhf{}
\fancyhead[R]{\thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
% Las páginas de inicio de capítulo también llevan el número arriba a la derecha
\fancypagestyle{plain}{%
  \fancyhf{}%
  \fancyhead[R]{\thepage}%
  \renewcommand{\headrulewidth}{0pt}%
  \renewcommand{\footrulewidth}{0pt}%
}

%------------------------------------------------------------------------------
% NOMBRES DE LOS ÍNDICES Y RÓTULOS, SEGÚN LA PAUTA
%------------------------------------------------------------------------------
\addto\captionsspanish{%
  \renewcommand{\contentsname}{Índice General}%
  \renewcommand{\listfigurename}{Índice de Figuras}%
  \renewcommand{\listtablename}{Índice de Tablas}%
  \renewcommand{\bibname}{Literatura Citada}%
  \renewcommand{\figurename}{Figura}%
  \renewcommand{\tablename}{Tabla}%
  \renewcommand{\appendixname}{Anexo}%
}

%------------------------------------------------------------------------------
% TÍTULOS DE CAPÍTULO Y SECCIÓN
%   Los capítulos van numerados 1..7, sin la palabra "Capítulo",
%   en mayúscula y negrita, centrados.
%------------------------------------------------------------------------------
\titleformat{\chapter}[hang]
  {\centering\normalfont\bfseries\large\singlespacing}
  {\thechapter.}{0.6em}{\MakeUppercase}
\titleformat{name=\chapter,numberless}[hang]
  {\centering\normalfont\bfseries\large\singlespacing}
  {}{0pt}{\MakeUppercase}
\titlespacing*{\chapter}{0pt}{0pt}{2.5em}
\titlespacing*{name=\chapter,numberless}{0pt}{0pt}{2.5em}

\titleformat{\section}
  {\normalfont\bfseries\normalsize\singlespacing}{\thesection}{0.8em}{}
\titleformat{\subsection}
  {\normalfont\bfseries\itshape\normalsize\singlespacing}{\thesubsection}{0.8em}{}
\titleformat{\subsubsection}
  {\normalfont\itshape\normalsize\singlespacing}{\thesubsubsection}{0.8em}{}
\titlespacing*{\section}{0pt}{1.6ex}{0.8ex}
\titlespacing*{\subsection}{0pt}{1.4ex}{0.6ex}
\titlespacing*{\subsubsection}{0pt}{1.2ex}{0.4ex}

\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{2}

%------------------------------------------------------------------------------
% NUMERACIÓN DE FIGURAS Y TABLAS
%   Pauta: "Las figuras se numeran con números arábigos […] Las Tablas se
%   numeran con números romanos en mayúsculas". Numeración corrida en toda
%   la tesis (no se reinicia en cada capítulo).
%------------------------------------------------------------------------------
\counterwithout{figure}{chapter}
\counterwithout{table}{chapter}
\renewcommand{\thefigure}{\arabic{figure}}
\renewcommand{\thetable}{\Roman{table}}

%------------------------------------------------------------------------------
% BIBLIOGRAFÍA
%   Pauta: ordenada alfabéticamente. En el texto: Becker (1968) o
%   (Becker, 1968); dos autores (Becker y Ortiz, 1968); más de dos
%   (Becker et al., 1968). El estilo APA de biblatex reproduce ese formato.
%------------------------------------------------------------------------------
\RequirePackage[style=apa,backend=biber,sortcites=true,uniquename=false]{biblatex}
\DeclareLanguageMapping{spanish}{spanish-apa}
% La pauta une el último autor con «y», no con «&»
\DeclareDelimFormat[bib,biblist]{finalnamedelim}{\addcomma\addspace y\addspace}
\setlength\bibitemsep{0.8\baselineskip}
\AtBeginBibliography{\singlespacing}

%------------------------------------------------------------------------------
% HIPERVÍNCULOS (sin color: el PDF se imprime igual que en pantalla)
%------------------------------------------------------------------------------
\RequirePackage[hidelinks,bookmarksnumbered]{hyperref}

%------------------------------------------------------------------------------
% DATOS DE LA TESIS  (se definen en config.tex)
%------------------------------------------------------------------------------
\newcommand{\bima@titulo}{Título de la tesis}
\newcommand{\titulotesis}[1]{\renewcommand{\bima@titulo}{#1}}

\newcommand{\bima@autor}{Nombre completo del autor}
\newcommand{\autor}[1]{\renewcommand{\bima@autor}{#1}}

\newcommand{\bima@patrocinante}{Dr. XXX}
\newcommand{\patrocinante}[1]{\renewcommand{\bima@patrocinante}{#1}}

\newcommand{\bima@institutopat}{Instituto de XXX}
\newcommand{\institutopatrocinante}[1]{\renewcommand{\bima@institutopat}{#1}}

\newcommand{\bima@facultadpat}{Facultad de Ciencias -- Universidad Austral de Chile}
\newcommand{\facultadpatrocinante}[1]{\renewcommand{\bima@facultadpat}{#1}}

% Co-patrocinante: dejar \copatrocinante{} vacío si no corresponde
\newcommand{\bima@copatrocinante}{}
\newcommand{\copatrocinante}[1]{\renewcommand{\bima@copatrocinante}{#1}}
\newcommand{\bima@institutocopat}{}
\newcommand{\institutocopatrocinante}[1]{\renewcommand{\bima@institutocopat}{#1}}
\newcommand{\bima@facultadcopat}{}
\newcommand{\facultadcopatrocinante}[1]{\renewcommand{\bima@facultadcopat}{#1}}

\newcommand{\bima@grado}{Tesis de Grado presentada como parte
  de los requisitos para optar al grado de \textbf{Licenciado en
  Biología Marina} y \textbf{Título Profesional de Biólogo Marino.}}
\newcommand{\textogrado}[1]{\renewcommand{\bima@grado}{#1}}

\newcommand{\bima@ciudad}{Valdivia -- Chile}
\newcommand{\ciudad}[1]{\renewcommand{\bima@ciudad}{#1}}

\newcommand{\bima@anio}{\the\year}
\newcommand{\anio}[1]{\renewcommand{\bima@anio}{#1}}

% Profesores informantes u otros miembros de la comisión. Bloque libre, para
% que quepan tantos como haga falta; va debajo del patrocinante. El Anexo 3
% solo menciona al co-patrocinante, pero las tesis aprobadas suelen listar
% también a los informantes.
\newcommand{\bima@informantes}{}
\newcommand{\informantes}[1]{\renewcommand{\bima@informantes}{#1}}

% Logos de la portada. Déjalo vacío —\logosportada{}— para obtener la portada
% exactamente como el Anexo 3 del Reglamento, que no lleva logos.
\newcommand{\bima@logos}{}
\newcommand{\logosportada}[1]{\renewcommand{\bima@logos}{#1}}

% Ancho de los bloques alineados a la derecha (profesores y mención del grado)
\newcommand{\bima@anchobloque}{0.55\textwidth}

%------------------------------------------------------------------------------
% PORTADA  (Anexo 3 del Reglamento de Tesis)
%------------------------------------------------------------------------------
\newcommand{\portada}{%
  % La portada, la dedicatoria y los agradecimientos van sin numerar; se
  % desactivan sus anclas de hyperref para que no choquen con las páginas
  % arábigas del cuerpo, que vuelven a empezar en 1.
  \hypersetup{pageanchor=false}%
  \begin{titlepage}
  \thispagestyle{empty}
  \singlespacing
  % Los espacios elásticos de abajo (\vfill) reparten el sobrante vertical;
  % los fijos se mantienen chicos para que la portada quepa en UNA página
  % aunque la comisión sea numerosa (patrocinante + co-patrocinante +
  % varios informantes).
  \ifx\bima@logos\empty\else
    \begin{center}\bima@logos\end{center}
    \vspace{0.5cm}
  \fi
  % --- Bloque de profesores, en la mitad derecha de la página ---
  \begin{flushright}
  \begin{minipage}{\bima@anchobloque}
    \raggedright
    Profesor Patrocinante:\\
    \bima@patrocinante\\
    \bima@institutopat\\
    \bima@facultadpat
    \ifx\bima@copatrocinante\empty\else
      \\[1em]
      Profesor Co-patrocinante:\\
      \bima@copatrocinante
      \ifx\bima@institutocopat\empty\else\\ \bima@institutocopat\fi
      \ifx\bima@facultadcopat\empty\else\\ \bima@facultadcopat\fi
    \fi
    \ifx\bima@informantes\empty\else
      \\[1em]
      \bima@informantes
    \fi
  \end{minipage}
  \end{flushright}
  \vfill
  % --- Título: mayúscula, negrita, 15-16 pt, centrado ---
  \begin{center}
    {\fontsize{15}{20}\selectfont\bfseries\MakeUppercase{\bima@titulo}}
  \end{center}
  \vfill
  % --- Mención del grado: bloque alineado a la derecha ---
  \begin{flushright}
    \begin{minipage}{\bima@anchobloque}
      \bima@grado
    \end{minipage}
  \end{flushright}
  \vfill
  % --- Autor: mayúscula, negrita, 15-16 pt, centrado ---
  \begin{center}
    {\fontsize{15}{20}\selectfont\bfseries\MakeUppercase{\bima@autor}}\\[0.9cm]
    {\bfseries\MakeUppercase{\bima@ciudad}}\\[0.6em]
    {\bfseries\bima@anio}
  \end{center}
  \end{titlepage}
  % La portada, la dedicatoria y los agradecimientos no llevan número de
  % página: la numeración parte recién en el Índice General (pauta).
  \pagenumbering{gobble}%
  \pagestyle{fancy}%
}

%------------------------------------------------------------------------------
% SECCIONES PRELIMINARES
%   Pauta: "A partir del Índice General con números romanos en minúsculas
%   (página 1) y a partir del capítulo 1 RESUMEN, con números arábigos
%   (página 1)". La Dedicatoria y los Agradecimientos van antes del Índice.
%------------------------------------------------------------------------------

% Capítulo sin número que sí aparece en el Índice General
\newcommand{\capitulosinnumero}[1]{%
  \chapter*{#1}%
  \addcontentsline{toc}{chapter}{#1}%
}

% Dedicatoria (opcional): bloque en cursiva, abajo a la derecha
\newenvironment{dedicatoria}
  {\clearpage\thispagestyle{empty}\vspace*{\fill}%
   \begin{flushright}\begin{minipage}{0.6\textwidth}\itshape\raggedleft}
  {\end{minipage}\end{flushright}\vspace*{\fill}\clearpage}

% Agradecimientos: van antes del Índice General y por lo tanto sin número de
% página, así que tampoco se listan en el Índice. Si tu comisión prefiere que
% aparezcan en el Índice, cambia esta línea por \capitulosinnumero{Agradecimientos}
% y añade \pagenumbering{roman} antes de \agradecimientos en main.tex.
\newcommand{\agradecimientos}{\chapter*{Agradecimientos}}

% Arranca la numeración romana (justo antes del Índice General)
\newcommand{\iniciarpreliminares}{%
  \clearpage
  \hypersetup{pageanchor=true}%
  \pagenumbering{roman}%
  \setcounter{page}{1}%
  \pagestyle{fancy}%
}

% Los tres índices, a espacio simple
\newcommand{\indices}{%
  \begingroup
  \singlespacing
  \tableofcontents
  \clearpage
  \phantomsection
  \addcontentsline{toc}{chapter}{\listfigurename}%
  \listoffigures
  \clearpage
  \phantomsection
  \addcontentsline{toc}{chapter}{\listtablename}%
  \listoftables
  \clearpage
  \endgroup
}

% Lista de Abreviaturas
%   \begin{listaabreviaturas}
%     \abrev{TSM}{Temperatura superficial del mar}
%   \end{listaabreviaturas}
\newcommand{\abrev}[2]{\item[#1] #2}
\newenvironment{listaabreviaturas}[1][3.5cm]
  {\capitulosinnumero{Lista de Abreviaturas}%
   \begingroup\singlespacing
   \begin{list}{}{%
     \setlength{\labelwidth}{#1}%
     \setlength{\leftmargin}{\dimexpr#1+1em\relax}%
     \setlength{\labelsep}{1em}%
     \setlength{\itemsep}{0.4\baselineskip}%
     \setlength{\parsep}{0pt}%
     \renewcommand{\makelabel}[1]{\textbf{##1}\hfill}}}
  {\end{list}\endgroup}

% Arranca el cuerpo: números arábigos desde el capítulo 1 RESUMEN
\newcommand{\iniciarcuerpo}{%
  \clearpage
  \pagenumbering{arabic}%
  \setcounter{page}{1}%
  \pagestyle{fancy}%
}

%------------------------------------------------------------------------------
% LITERATURA CITADA (capítulo numerado, incluido en el Índice General)
%------------------------------------------------------------------------------
\newcommand{\literaturacitada}{%
  \printbibliography[heading=bibnumbered,title={Literatura Citada}]%
}

%------------------------------------------------------------------------------
% AYUDAS DE REDACCIÓN
%------------------------------------------------------------------------------
% Pauta: los nombres científicos, las expresiones greco-latinas y las palabras
% en idioma extranjero sin equivalente en español van en cursiva.
\newcommand{\especie}[1]{\textit{#1}}
\newcommand{\extranjero}[1]{\textit{#1}}

% Figura con la leyenda BAJO el cuerpo de la figura.
%   \figura[ancho]{archivo}{Título. Leyenda…}{etiqueta}
\newcommand{\figura}[4][0.85\linewidth]{%
  \begin{figure}[htbp]
    \centering
    \includegraphics[width=#1]{#2}
    \caption{#3}
    \label{fig:#4}
  \end{figure}%
}

% Tabla con la leyenda SOBRE el cuerpo de la tabla.
%   \begin{tablabima}{Título de la tabla}{etiqueta}
%     \begin{tabular}{…} … \end{tabular}
%   \end{tablabima}
\newenvironment{tablabima}[2]
  {\begin{table}[htbp]\centering\singlespacing
   \caption{#1}\label{tab:#2}\par\vspace{0.4em}}
  {\end{table}}

% Referencias cruzadas con el rótulo que pide la pauta
\newcommand{\reffig}[1]{Figura~\ref{fig:#1}}
\newcommand{\reftab}[1]{Tabla~\ref{tab:#1}}

\endinput
