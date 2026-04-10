clc; clear;

disp('=== BALANCE DE CALOR OCEANICO ===');

% Constantes
rho = 1022.4;      % kg/m3
Cp  = 3940;        % J/kg°C
L   = 2.27e6;      % J/kg 

% Selección de variable
disp('Variable a calcular:');
disp('1 = Qt');
disp('2 = Qlat');
disp('3 = Qsen');
disp('4 = Qv');
disp('5 = DeltaT (desde almacenamiento)');
op = input('Seleccione opción: ');

switch op

    case 1 % Qt
        Qsw = input('Qsw (W/m2): ');
        Qlw = input('Qlw (W/m2): ');
        Qlat = input('Qlat (W/m2): ');
        R = input('R (Bowen): ');
        Qv = input('Qv (W/m2): ');

        Qsen = R * Qlat;

        Qt = Qsw + Qlw + Qlat + Qsen + Qv;

        fprintf('Qt = %.2f W/m2\n', Qt);

    case 2 % Qlat
        E = input('Evaporacion (kg/m2/s): ');
        Qlat = L * E;

        fprintf('Qlat = %.2f W/m2\n', Qlat);

    case 3 % Qsen
        Qlat = input('Qlat (W/m2): ');
        R = input('R (Bowen): ');

        Qsen = R * Qlat;

        fprintf('Qsen = %.2f W/m2\n', Qsen);

    case 4 % Qv
        V = input('Velocidad (m/s): ');
        dZ = input('Delta Z (m): ');
        dT_dN = input('Gradiente dT/dN (°C/m): ');

        Qv = rho * Cp * V * dZ * dT_dN;

        fprintf('Qv = %.2f W/m2\n', Qv);

    case 5 % Delta T
        Qt = input('Qt (W/m2): ');
        dt = input('Tiempo (s): ');
        dZ = input('Delta Z (m): ');

        dT = (Qt * dt) / (rho * Cp * dZ);

        fprintf('Delta T = %.4f °C\n', dT);

    otherwise
        disp('Opcion invalida');
end