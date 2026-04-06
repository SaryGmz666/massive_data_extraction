"""Contiene la validación de días hábiles para México."""

import pandas as pd
from datetime import date, timedelta

FIXED_HOLIDAYS = {
    (1, 1),  # Año Nuevo
    (5, 1),  # Día del Trabajo
    (9, 16),  # Independencia
    (11, 2),  # Día de muertos
    (12, 12),  # Empleado bancario
    (12, 25),  # Navidad
}


def get_constitution_day(year: int) -> date:
    """Retorna el primer lunes de febrero, correspondiente al Día de la
    Constitución Mexicana."""
    d = date(year, 2, 1)
    while d.weekday() != 0:
        d += timedelta(days=1)
    return d


def get_benito_juarez_holiday(year: int) -> date:
    """Retorna el tercer lunes de marzo, correspondiente al natalicio de
    Benito Juárez."""
    d = date(year, 3, 1)
    mondays = 0
    while True:
        if d.weekday() == 0:
            mondays += 1
            if mondays == 3:
                return d
        d += timedelta(days=1)


def get_easter_sunday(year: int) -> date:
    """Calcula la fecha del Domingo de Pascua (Easter Sunday) para el año
    dado usando el algoritmo de computus."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def get_holy_thursday(year: int) -> date:
    """Retorna la fecha del Jueves Santo para el año dado."""
    return get_easter_sunday(year) - timedelta(days=3)


def get_good_friday(year: int) -> date:
    """Retorna la fecha del Viernes Santo para el año dado."""
    return get_easter_sunday(year) - timedelta(days=2)


def get_revolution_day(year: int) -> date:
    """Retorna el tercer lunes de noviembre, correspondiente al Día de la
    Revolución Mexicana."""
    d = date(year, 11, 1)
    mondays = 0
    while True:
        if d.weekday() == 0:
            mondays += 1
            if mondays == 3:
                return d
        d += timedelta(days=1)


def get_transition_day(year: int) -> date | None:
    """Retorna el cambio de posición de mandato el cual es cada 6 años."""
    # Excepción del sexenio de Claudia Sheinbaum
    if year == 2024:
        return date(2024, 10, 1)

    if (year - 2024) % 6 == 0:
        return date(year, 12, 1)
    return None


def get_mobile_holidays_for_year(year: int) -> set[tuple[int, int, int]]:
    """Retorna un conjunto de tuplas (año, mes, día) correspondientes a los
    días feriados móviles para el año dado en México, incluyendo días oficiales
    y de transición de mandato si aplica."""
    holidays = {
        get_constitution_day(year),
        get_benito_juarez_holiday(year),
        get_holy_thursday(year),
        get_good_friday(year),
        get_revolution_day(year),
    }
    transition = get_transition_day(year)
    if transition:
        holidays.add(transition)
    return {(d.year, d.month, d.day) for d in holidays}


def get_last_360_dates(end_date: date, days: int = 361) -> pd.DataFrame:
    """Genera un DataFrame con los últimos 'days' días hábiles (por defecto 361)
    previos a la fecha 'end_date', excluyendo fines de semana y feriados (fijos y
    móviles) en México.

    Args:
        end_date (date): Fecha final para calcular los días hábiles.
        days (int): Número de días hábiles a retornar (por defecto 361).

    Returns:
        pd.DataFrame: DataFrame con una columna 'fecha' de días hábiles.
    """
    if isinstance(days, date):
        raise TypeError(f"'days' debe ser un número entero, no una fecha: {days}")
    days = int(days)

    dates = []
    actual = end_date

    years = range(end_date.year - 3, end_date.year + 3)
    mobile_holidays = set()
    for y in years:
        mobile_holidays.update(get_mobile_holidays_for_year(y))

    while len(dates) < days:
        date_tuple = (actual.year, actual.month, actual.day)
        fixed_tuple = (actual.month, actual.day)

        if (
            actual.weekday() < 5
            and fixed_tuple not in FIXED_HOLIDAYS
            and date_tuple not in mobile_holidays
        ):
            dates.append(actual)

        actual -= timedelta(days=1)

    dates.reverse()
    df = pd.DataFrame(dates, columns=["fecha"])
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df


def get_fixed_holidays(year):
    """Obtiene los feriados fijos"""
    return [date(year, month, day) for month, day in FIXED_HOLIDAYS]


def is_holiday(date_to_validate):
    """Valida si una fecha es día feríado"""
    anio = date_to_validate.year
    return date_to_validate in [
        get_constitution_day(anio),
        get_benito_juarez_holiday(anio),
        get_good_friday(anio),
        get_holy_thursday(anio),
        get_revolution_day(anio),
        get_transition_day(anio),
        *get_fixed_holidays(anio),
    ]
