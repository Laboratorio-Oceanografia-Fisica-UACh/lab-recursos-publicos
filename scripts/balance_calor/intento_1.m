clc; clear;

disp('=== BALANCE DE CALOR AUTOMATICO ===');

% Constantes
rho = 1022.4;
Cp  = 3940;
L   = 2.27e6;

% ===== FUNCION PARA PARSEAR UNIDADES =====
parse_input = @(str, default_unit) deal(str2double(regexp(str,'[\d.]+','match','once')), str);

% ===== INGRESO =====
disp('Ingrese variables sin unidad de medida. De tener otra unidad escribir el valor en conjunto con la unidad (ej: 200, o 0.3 g/dia cm2). Enter para omitir');

Qsw_str = input('Qsw (W/m2): ','s');
Qlw_str = input('Qlw (W/m2): ','s');
E_str   = input('Qsen (Evaporacion) (kg/m²/s): ','s');
R_str   = input('R (adimensional): ','s');
V_str   = input('Velocidad (m/s): ','s');
dZ_str   = input('Delta Z (m): ','s');

% ===== INICIALIZAR =====
Qsw=[]; Qlw=[]; Qlat=[]; Qsen=[]; Qv=[]; R=[]; V=[]; dZ=[];

% ===== PARSEO BASICO =====
if ~isempty(Qsw_str), Qsw = str2double(Qsw_str); end
if ~isempty(Qlw_str), Qlw = str2double(Qlw_str); end
if ~isempty(R_str),   R   = str2double(R_str); end
if ~isempty(V_str),   V   = str2double(V_str); end
if ~isempty(dZ_str),  dZ  = str2double(dZ_str); end

% ===== EVAPORACION (CONVERSION AUTOMATICA) =====
if contains(E_str,'g')
    val = str2double(regexp(E_str,'[\d.]+','match','once'));
    % g/dia cm2 → kg/m2/s
    E = val * 0.001 * 10000 / 86400;
else
    E = str2double(E_str);
end

% ===== CALCULOS =====
disp('--- CALCULOS POSIBLES ---');

% Qlat
if exist('E','var')
    Qlat = -L * E;
    fprintf('Qlat = %.2f W/m2\n', Qlat);
end

% Qsen
if ~isempty(Qlat) && ~isempty(R)
    Qsen = R * Qlat;
    fprintf('Qsen = %.2f W/m2\n', Qsen);
end

% Qt = 0 (modo automático si no se da)
if ~isempty(Qsw) && ~isempty(Qlw) && ~isempty(Qlat) && ~isempty(Qsen)
    Qt = Qsw + Qlw + Qlat + Qsen;
    fprintf('Qt (sin Qv) = %.2f W/m2\n', Qt);

    Qv = -Qt;
    fprintf('Qv = %.2f W/m2\n', Qv);
end

% Gradiente
if ~isempty(Qv) && ~isempty(V) && ~isempty(dZ)
    grad = Qv / (rho * Cp * V * dZ);
    fprintf('dT/dN = %.3e °C/m\n', grad);
    fprintf('≈ %.3f °C/1000 km\n', grad*1e6);
end

disp('--- FIN ---');