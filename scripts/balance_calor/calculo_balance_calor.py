"""
Calculadora de Balance de Calor Oceánico
Basada en la guía de José Garcés Vargas
"""

import math

# ── Constantes por defecto ──────────────────────────────────────────────────
RHO = 1022.4   # Densidad del agua de mar (kg/m³)
CP  = 3940.0   # Calor específico (J/kg·°C)
L   = 2270.0   # Calor latente de evaporación (J/g)

# ── Utilidades ──────────────────────────────────────────────────────────────

def pedir_float(prompt, default=None):
    if default is not None:
        texto = f"  {prompt} [{default}]: "
    else:
        texto = f"  {prompt}: "
    while True:
        entrada = input(texto).strip()
        if entrada == "" and default is not None:
            return float(default)
        try:
            return float(entrada)
        except ValueError:
            print("  ⚠ Ingresa un número válido.")

def separador():
    print("\n" + "─" * 58)

def titulo(texto):
    separador()
    print(f"  {texto}")
    separador()

# ── Funciones de cálculo ────────────────────────────────────────────────────

def calc_delta_T():
    """
    Variación de temperatura en una capa durante un período.

    Combina dos pasos:
      1) Qt = Qsw + Qlw + Qlat·(1+R) + Qv   → flujo neto (W/m²)
      2) ΔT = Qt · Δt / (ρ · Cp · ΔZ)        → cambio de temperatura (°C)

    Típico de los ejercicios 1a y 1b de la guía.
    """
    titulo("ΔT — Variación de temperatura en una capa")
    print("  Paso 1: Qt = Qsw + Qlw + Qlat·(1+R) + Qv")
    print("  Paso 2: ΔT = Qt · Δt / (ρ · Cp · ΔZ)\n")

    Qsw  = pedir_float("Radiación solar              Qsw   (W/m²)")
    Qlw  = pedir_float("Radiación onda larga         Qlw   (W/m², negativo)")
    Qlat = pedir_float("Calor latente                Qlat  (W/m², negativo)")
    R    = pedir_float("Cociente de Bowen            R     (adim.)", 0.3)
    Qv   = pedir_float("Calor advectivo              Qv    (W/m², 0 si se ignora)", 0.0)

    Qt = Qsw + Qlw + Qlat * (1 + R) + Qv

    print(f"\n  Qt = {Qsw} + ({Qlw}) + ({Qlat})·(1+{R}) + ({Qv})")
    print(f"  Qt = {Qt:.4f} W/m²")

    print()
    dt_dias = pedir_float("Período de tiempo            Δt    (días)")
    dZ      = pedir_float("Grosor de la capa            ΔZ    (m)")
    rho     = pedir_float("Densidad                     ρ     (kg/m³)", RHO)
    cp      = pedir_float("Calor específico             Cp    (J/kg·°C)", CP)

    dt_s = dt_dias * 86400
    dT   = Qt * dt_s / (rho * cp * dZ)

    print(f"\n  Δt = {dt_dias} días = {dt_s:,.0f} s")
    print(f"  ΔT = {Qt:.4f} × {dt_s:,.0f} / ({rho} × {cp} × {dZ})")
    print(f"  ΔT = {dT:.4f} °C")

    if abs(dT) > 5 and dZ <= 2:
        print("\n  ⚠ Resultado muy alto para una capa tan delgada.")
        print("    En la práctica la radiación penetra mucho más de 1 m.")
        print("    Prueba distribuir el calor en 50 m para obtener un valor realista.")
    return dT


def calc_delta_H():
    """Ec. 2: ΔH = ρ · Cp · ΔT · ΔZ"""
    titulo("ΔH — Cambio de calor en el volumen  (Ec. 2)")
    print("  Fórmula: ΔH = ρ · Cp · ΔT · ΔZ\n")
    rho = pedir_float("Densidad ρ  (kg/m³)", RHO)
    cp  = pedir_float("Calor específico Cp  (J/kg·°C)", CP)
    dT  = pedir_float("Cambio de temperatura ΔT  (°C)")
    dZ  = pedir_float("Grosor del volumen ΔZ  (m)")

    dH = rho * cp * dT * dZ
    print(f"\n  ΔH = {rho} × {cp} × {dT} × {dZ}")
    print(f"  ΔH = {dH:,.2f} J/m²")
    return dH


def calc_Qt_tasa():
    """Qt = ΔH / Δt"""
    titulo("Qt — Tasa de almacenamiento  (Ec. 1, primer término)")
    print("  Fórmula: Qt = ΔH / Δt\n")
    dH      = pedir_float("Cambio de calor ΔH  (J/m²)")
    dt_dias = pedir_float("Período de tiempo Δt  (días)")

    dt_s = dt_dias * 86400
    Qt   = dH / dt_s
    print(f"\n  Δt = {dt_dias} días = {dt_s:,.0f} s")
    print(f"  Qt = {dH:,.2f} / {dt_s:,.0f}")
    print(f"  Qt = {Qt:.4f} W/m²")
    return Qt


def calc_Qt_balance():
    """Ec. 1: Qt = Qsw + Qlw + Qlat·(1+R) + Qv"""
    titulo("Qt — Balance total de calor  (Ec. 1)")
    print("  Fórmula: Qt = Qsw + Qlw + Qlat·(1+R) + Qv")
    print("  (positivo = ganancia, negativo = pérdida)\n")
    Qsw  = pedir_float("Radiación solar       Qsw  (W/m²)")
    Qlw  = pedir_float("Radiación onda larga  Qlw  (W/m², negativo)")
    Qlat = pedir_float("Calor latente         Qlat (W/m², negativo)")
    R    = pedir_float("Cociente de Bowen     R    (adim.)", 0.3)
    Qv   = pedir_float("Calor advectivo       Qv   (W/m², 0 si se ignora)", 0.0)

    Qt = Qsw + Qlw + Qlat * (1 + R) + Qv
    print(f"\n  Qt = {Qsw} + ({Qlw}) + ({Qlat})·(1+{R}) + ({Qv})")
    print(f"  Qt = {Qt:.4f} W/m²")
    estado = "ganancia" if Qt > 0 else "pérdida" if Qt < 0 else "equilibrio térmico"
    print(f"  → El volumen experimenta {estado} de calor.")
    return Qt


def calc_Qsw_z():
    """Ec. 3: Qsw(z) = Qso · e^(-k·z)"""
    titulo("Qsw(z) — Radiación solar a profundidad z  (Ec. 3)")
    print("  Fórmula: Qsw(z) = Qso · e^(−k·z)\n")
    Qso = pedir_float("Insolación en superficie Qso  (W/m²)")
    k   = pedir_float("Coeficiente de extinción k   (m⁻¹)", 0.04)
    z   = pedir_float("Profundidad z  (m)")

    Qz   = Qso * math.exp(-k * z)
    frac = (Qz / Qso) * 100
    print(f"\n  Qsw({z} m) = {Qso} · e^(−{k}·{z})")
    print(f"  Qsw({z} m) = {Qz:.4f} W/m²")
    print(f"  Corresponde al {frac:.1f}% de la insolación superficial.")

    resp = input("\n  ¿Calcular el calor neto entre dos profundidades? (s/n): ").strip().lower()
    if resp == "s":
        z1 = pedir_float("  Profundidad superior Z1  (m)")
        z2 = pedir_float("  Profundidad inferior Z2  (m, > Z1)")
        Q1 = Qso * math.exp(-k * z1)
        Q2 = Qso * math.exp(-k * z2)
        Qneto = Q1 - Q2
        print(f"\n  Qsw(Z1={z1} m) = {Q1:.4f} W/m²")
        print(f"  Qsw(Z2={z2} m) = {Q2:.4f} W/m²")
        print(f"  Calor neto absorbido = {Qneto:.4f} W/m²")
    return Qz


def calc_Qlat():
    """Ec. 4: Qlat = L · E"""
    titulo("Qlat — Calor latente por evaporación  (Ec. 4)")
    print("  Fórmula: Qlat = L · E")
    print("  (E en cm/día → conversión automática a g·s⁻¹·m⁻²)\n")
    L_val = pedir_float("Calor latente de evaporación L  (J/g)", L)
    E_cm  = pedir_float("Evaporación E  (cm/día)")

    E_gs  = E_cm * 10000 / 86400
    Qlat  = L_val * E_gs
    print(f"\n  E = {E_cm} cm/día = {E_gs:.6f} g/(s·m²)")
    print(f"  Qlat = {L_val} × {E_gs:.6f}")
    print(f"  Qlat = {Qlat:.4f} W/m²  (pérdida → negativo: {-Qlat:.4f} W/m²)")
    return -Qlat


def calc_Qsen():
    """Ec. 5: Qsen = R · Qlat"""
    titulo("Qsen — Calor sensible por conducción  (Ec. 5)")
    print("  Fórmula: Qsen = R · Qlat\n")
    R    = pedir_float("Cociente de Bowen R  (adim.)", 0.3)
    Qlat = pedir_float("Calor latente Qlat  (W/m², negativo si el océano pierde)")

    Qsen = R * Qlat
    print(f"\n  Qsen = {R} × {Qlat}")
    print(f"  Qsen = {Qsen:.4f} W/m²")
    return Qsen


def calc_Qv():
    """Ec. 6: Qv = ρ · Cp · V · ΔZ · (ΔT/ΔN)"""
    titulo("Qv — Calor advectivo por corrientes  (Ec. 6)")
    print("  Fórmula: Qv = ρ · Cp · V · ΔZ · (ΔT/ΔN)\n")
    rho   = pedir_float("Densidad ρ  (kg/m³)", RHO)
    cp    = pedir_float("Calor específico Cp  (J/kg·°C)", CP)
    V     = pedir_float("Velocidad de corriente V  (m/s)")
    dZ    = pedir_float("Grosor de la capa ΔZ  (m)")
    gradT = pedir_float("Gradiente de temperatura ΔT/ΔN  (°C/m)")

    Qv = rho * cp * V * dZ * gradT
    print(f"\n  Qv = {rho} × {cp} × {V} × {dZ} × {gradT}")
    print(f"  Qv = {Qv:.4f} W/m²")
    estado = "ganancia" if Qv > 0 else "pérdida"
    print(f"  → {estado} de calor al volumen de control.")
    return Qv


def calc_gradT():
    """Ec. 6 despejada: ΔT/ΔN = Qv / (ρ · Cp · ΔZ · V)"""
    titulo("ΔT/ΔN — Gradiente de temperatura  (Ec. 6 despejada)")
    print("  Fórmula: ΔT/ΔN = Qv / (ρ · Cp · ΔZ · V)\n")
    Qv  = pedir_float("Calor advectivo Qv  (W/m²)")
    rho = pedir_float("Densidad ρ  (kg/m³)", RHO)
    cp  = pedir_float("Calor específico Cp  (J/kg·°C)", CP)
    dZ  = pedir_float("Grosor de la capa ΔZ  (m)")
    V   = pedir_float("Velocidad de corriente V  (m/s)")

    gradT        = Qv / (rho * cp * dZ * V)
    gradT_1000km = gradT * 1e6

    print(f"\n  ΔT/ΔN = {Qv} / ({rho} × {cp} × {dZ} × {V})")
    print(f"  ΔT/ΔN = {gradT:.4e} °C/m")
    print(f"  ΔT/ΔN = {gradT_1000km:.4f} °C/1000 km")

    if gradT > 0:
        print("  → La temperatura aumenta en la dirección de la corriente.")
    else:
        print("  → La temperatura disminuye en la dirección de la corriente.")
    return gradT


def calc_evaporacion_desde_flujos():
    """Despeja evaporación E dado Qnet, Qsw, Qlw y R"""
    titulo("E — Evaporación desde flujos conocidos")
    print("  Despeja E de: Qnet = Qsw + Qlw + L·E·(10000/86400)·(1+R)\n")
    Qnet  = pedir_float("Flujo neto requerido Qnet  (W/m²)")
    Qsw   = pedir_float("Radiación solar Qsw  (W/m²)")
    Qlw   = pedir_float("Radiación onda larga Qlw  (W/m², negativo)")
    R     = pedir_float("Cociente de Bowen R", 0.3)
    L_val = pedir_float("Calor latente L  (J/g)", L)

    Qlat  = (Qnet - Qsw - Qlw) / (1 + R)
    E_gs  = Qlat / (L_val * 10000 / 86400)
    E_cm  = E_gs * 86400 / 10000

    print(f"\n  Qlat = ({Qnet} - {Qsw} - ({Qlw})) / (1+{R}) = {Qlat:.4f} W/m²")
    print(f"  E = {E_gs:.6f} g/(s·m²)")
    print(f"  E = {E_cm:.4f} cm/día")
    return E_cm


# ── Menú principal ──────────────────────────────────────────────────────────

OPCIONES = {
    "1":  ("ΔT      — Variación de temperatura en una capa  ← Ej. 1a y 1b", calc_delta_T),
    "2":  ("ΔH      — Cambio de calor en el volumen         (Ec. 2)",        calc_delta_H),
    "3":  ("Qt      — Tasa de almacenamiento (ΔH/Δt)        (Ec. 1)",        calc_Qt_tasa),
    "4":  ("Qt      — Balance total de calor                (Ec. 1)",        calc_Qt_balance),
    "5":  ("Qsw(z)  — Radiación solar a profundidad z       (Ec. 3)",        calc_Qsw_z),
    "6":  ("Qlat    — Calor latente por evaporación         (Ec. 4)",        calc_Qlat),
    "7":  ("Qsen    — Calor sensible (cociente de Bowen)    (Ec. 5)",        calc_Qsen),
    "8":  ("Qv      — Calor advectivo por corrientes        (Ec. 6)",        calc_Qv),
    "9":  ("ΔT/ΔN  — Gradiente de temperatura perpendicular (Ec. 6)",        calc_gradT),
    "10": ("E       — Evaporación desde flujos conocidos",                    calc_evaporacion_desde_flujos),
    "0":  ("Salir", None),
}

def menu():
    print("\n" + "═" * 58)
    print("   CALCULADORA DE BALANCE DE CALOR OCEÁNICO")
    print("═" * 58)
    print("  Selecciona la variable que quieres calcular:\n")
    for clave, (desc, _) in OPCIONES.items():
        print(f"  [{clave:>2}] {desc}")
    print()

def main():
    while True:
        menu()
        opcion = input("  Opción: ").strip()
        if opcion not in OPCIONES:
            print("  ⚠ Opción no válida, intenta de nuevo.")
            continue
        desc, funcion = OPCIONES[opcion]
        if funcion is None:
            print("\n  ¡Hasta luego!\n")
            break
        try:
            funcion()
        except KeyboardInterrupt:
            print("\n  (cálculo cancelado)")
        input("\n  Presiona Enter para continuar...")

if __name__ == "__main__":
    main()