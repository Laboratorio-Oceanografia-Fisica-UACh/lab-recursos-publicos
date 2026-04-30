"""
balance_calor - Funciones para el cálculo del balance de calor oceánico
========================================================================================
Módulo importable con las ecuaciones fundamentales del balance de calor superficial.
Equivalente Python de la función MATLAB balance_calor.m del mismo toolbox.

Uso básico:
    import balance_calor as bc

    qt = bc.Qt(Qsw=200, Qlw=-50, Qlat=-80, R=0.3)
    dh = bc.dH(dT=0.5, dz=50)
    dt = bc.delta_T(Qt_val=qt, dt_dias=30, dz=50)

Constantes físicas internas (sobreescribibles por parámetro):
    RHO = 1022.4  kg/m³  — densidad del agua de mar
    CP  = 3940.0  J/kg·°C — calor específico
    L   = 2270.0  J/g    — calor latente de evaporación

Para uso interactivo (menú de cálculo paso a paso) ver:
    scripts/balance_calor/calculo_balance_calor.py

Basado en apuntes de: jgarces@docentes.uach.cl | jose.garces.vargas@gmail.com
Laboratorio de Oceanografía Física (LOFA)
Instituto de Ciencias Marinas y Limnológicas | Universidad Austral de Chile
https://github.com/Laboratorio-Oceanografia-Fisica-UACh
========================================================================================
"""

import math

# ── Constantes físicas del agua de mar ─────────────────────────────────────────
RHO = 1022.4  # Densidad del agua de mar (kg/m³)
CP  = 3940.0  # Calor específico (J/kg·°C)
L   = 2270.0  # Calor latente de evaporación (J/g)


def Qt(Qsw, Qlw, Qlat, R=0.3, Qv=0.0):
    """
    Balance total de calor (Ec. 1).

    Qt = Qsw + Qlw + Qlat·(1 + R) + Qv

    Parámetros
    ----------
    Qsw  : float  Radiación solar neta de onda corta (W/m²)
    Qlw  : float  Radiación neta de onda larga (W/m², usualmente negativo)
    Qlat : float  Flujo de calor latente (W/m², usualmente negativo)
    R    : float  Cociente de Bowen, adimensional (default 0.3)
    Qv   : float  Calor advectivo (W/m², default 0.0)

    Retorna
    -------
    float  Almacenamiento total de calor (W/m²). Positivo = ganancia.
    """
    return Qsw + Qlw + Qlat * (1 + R) + Qv


def dH(dT, dz, rho=RHO, cp=CP):
    """
    Cambio de calor en el volumen (Ec. 2).

    ΔH = ρ · Cp · ΔT · ΔZ

    Parámetros
    ----------
    dT  : float  Cambio de temperatura (°C)
    dz  : float  Grosor de la capa (m)
    rho : float  Densidad del agua (kg/m³, default 1022.4)
    cp  : float  Calor específico (J/kg·°C, default 3940.0)

    Retorna
    -------
    float  Cambio de calor (J/m²)
    """
    return rho * cp * dT * dz


def delta_T(Qt_val, dt_dias, dz, rho=RHO, cp=CP):
    """
    Variación de temperatura en una capa durante un período.

    ΔT = Qt · Δt / (ρ · Cp · ΔZ)

    Parámetros
    ----------
    Qt_val  : float  Flujo neto de calor (W/m²)
    dt_dias : float  Duración del período (días)
    dz      : float  Grosor de la capa (m)
    rho     : float  Densidad del agua (kg/m³, default 1022.4)
    cp      : float  Calor específico (J/kg·°C, default 3940.0)

    Retorna
    -------
    float  Cambio de temperatura (°C)
    """
    dt_s = dt_dias * 86400
    return Qt_val * dt_s / (rho * cp * dz)


def Qsw_z(Qso, k, z):
    """
    Radiación solar a profundidad z (Ec. 3).

    Qsw(z) = Qso · e^(−k·z)

    Parámetros
    ----------
    Qso : float  Insolación en superficie (W/m²)
    k   : float  Coeficiente de extinción (m⁻¹)
    z   : float  Profundidad (m, positivo hacia abajo)

    Retorna
    -------
    float  Radiación solar a profundidad z (W/m²)
    """
    return Qso * math.exp(-k * z)


def Qlat(E_cm_dia, L_val=L):
    """
    Flujo de calor latente por evaporación (Ec. 4).

    Qlat = −L · E

    Parámetros
    ----------
    E_cm_dia : float  Evaporación (cm/día)
    L_val    : float  Calor latente de evaporación (J/g, default 2270.0)

    Retorna
    -------
    float  Flujo de calor latente (W/m², negativo = pérdida del océano)
    """
    E_gs = E_cm_dia * 10000 / 86400  # cm/día → g/(s·m²)
    return -L_val * E_gs


def Qsen(R, Qlat_val):
    """
    Flujo de calor sensible por conducción (Ec. 5).

    Qsen = R · Qlat

    Parámetros
    ----------
    R        : float  Cociente de Bowen (adimensional)
    Qlat_val : float  Flujo de calor latente (W/m²)

    Retorna
    -------
    float  Flujo de calor sensible (W/m²)
    """
    return R * Qlat_val


def Qv(V, dz, gradT, rho=RHO, cp=CP):
    """
    Calor advectivo por corrientes (Ec. 6).

    Qv = ρ · Cp · V · ΔZ · (ΔT/ΔN)

    Parámetros
    ----------
    V     : float  Velocidad de la corriente (m/s)
    dz    : float  Grosor de la capa (m)
    gradT : float  Gradiente de temperatura perpendicular a la corriente (°C/m)
    rho   : float  Densidad del agua (kg/m³, default 1022.4)
    cp    : float  Calor específico (J/kg·°C, default 3940.0)

    Retorna
    -------
    float  Calor advectivo (W/m²)
    """
    return rho * cp * V * dz * gradT
