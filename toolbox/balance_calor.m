function [resultado] = balance_calor(ecuacion, varargin)
%BALANCE_CALOR - Calcula las ecuaciones principales del balance de calor oceánico
%=========================================================================================
% Este script agrupa todas las ecuaciones fundamentales para el cálculo del balance
% de calor oceánico.
% Permite calcular almacenamiento, calor latente, sensible, advectivo y radiación.
%
% Syntax: [resultado] = balance_calor(ecuacion, input1, input2, ...)
%
% Inputs:
% ecuacion = String con la fórmula a utilizar ('Qt', 'dH', 'Qsw', 'Qlat', 'Qsen', 'Qv')
% varargin = Variables requeridas según la ecuación seleccionada:
%            - 'Qt': Qsw, Qlw, Qlat, Qsen, Qv (en W/m2)
%            - 'dH': dT (°C), dz (m)
%            - 'Qsw': Qso (W/m2), k (coef. extinción), z (m)
%            - 'Qlat': E (evaporación en g)
%            - 'Qsen': R (Cociente de Bowen), Qlat (W/m2)
%            - 'Qv': v (m/s), dz (m), dT_dN (°C/m)
%
% Outputs:
% resultado = Valor numérico calculado (unidades dependen de la ecuación, ej: W/m2 o J/m2)
%=========================================================================================
% Example:
% % Calcular Calor Advectivo (Qv) con v = 0.5, dz = 50, dT_dN = 1.1e-7:
% Qv = balance_calor('Qv', 0.5, 50, 1.1e-7);
%
% $Other m-files required: none
% $Subfunctions: none
% $MAT-files required: none
% $Notes: Las constantes rho (1022.4 kg/m3), Cp (3940 J/kg°C) y L (2270 J/g) son internas.
% $Tested with: MATLAB Version 9.14 (R2023a)
%
% $Creation date: 2026-03-23; Last revision: 23-Mar-2026
%
% See also: 
%
% $Laboratorio de Oceanografía Física (LOFA) $
% $Instituto de Ciencias Marinas y Limnológicas | Universidad Austral de Chile $
% $GitHub: https://github.com/Laboratorio-Oceanografia-Fisica-UACh $
% $Basado en apuntes de: jgarces@docentes.uach.cl | jose.garces.vargas@gmail.com $
% $http://www.icml.uach.cl © $
%=========================================================================================

    % Constantes físicas del agua de mar
    rho = 1022.4; % Densidad del agua (kg/m3) [cite: 25]
    Cp = 3940;    % Calor específico (J/kg°C) [cite: 25]
    L = 2270;     % Calor latente de evaporación (J/g) [cite: 42]

    switch ecuacion
        case 'Qt'
            % Ecuación 1: Almacenamiento total [cite: 16]
            if length(varargin) < 5
                error('Faltan argumentos para Qt. Se requieren 5: Qsw, Qlw, Qlat, Qsen, Qv');
            end
            Qsw = varargin{1};
            Qlw = varargin{2};
            Qlat = varargin{3};
            Qsen = varargin{4};
            Qv = varargin{5};
            resultado = Qsw + Qlw + Qlat + Qsen + Qv; [cite: 16]

        case 'dH'
            % Ecuación 2: Cambio de calor [cite: 23]
            if length(varargin) < 2
                error('Faltan argumentos para dH. Se requieren 2: dT, dz');
            end
            dT = varargin{1};
            dz = varargin{2};
            resultado = rho * Cp * dT * dz; [cite: 23]

        case 'Qsw'
            % Ecuación 3: Radiación atenuada por profundidad [cite: 29]
            if length(varargin) < 3
                error('Faltan argumentos para Qsw. Se requieren 3: Qso, k, z');
            end
            Qso = varargin{1};
            k = varargin{2};
            z = varargin{3};
            resultado = Qso * exp(-k * z); [cite: 29]

        case 'Qlat'
            % Ecuación 4: Calor latente por evaporación [cite: 40]
            if isempty(varargin)
                error('Faltan argumentos para Qlat. Se requiere 1: E (en gramos)');
            end
            E = varargin{1};
            resultado = L * E; [cite: 40]

        case 'Qsen'
            % Ecuación 5: Calor sensible [cite: 44]
            if length(varargin) < 2
                error('Faltan argumentos para Qsen. Se requieren 2: R, Qlat');
            end
            R = varargin{1};
            Qlat = varargin{2};
            resultado = R * Qlat; [cite: 44]

        case 'Qv'
            % Ecuación 6: Calor advectivo [cite: 49]
            if length(varargin) < 3
                error('Faltan argumentos para Qv. Se requieren 3: v, dz, dT_dN');
            end
            v = varargin{1};
            dz = varargin{2};
            dT_dN = varargin{3};
            resultado = rho * Cp * v * dz * dT_dN; [cite: 49]

        otherwise
            error('Ecuación no reconocida. Usa: ''Qt'', ''dH'', ''Qsw'', ''Qlat'', ''Qsen'', ''Qv''');
    end
end