import datetime as dt
import os

BASE_DIR = {
    (
        2022,
        2023,
        2024,
        2025,
        2026,
    ): "G:/path_1/{date:%Y}/{date:%m}. {month} {date:%Y}",
    (
        2016,
        2017,
    ): "G:/path_2/{date:%Y}/{date:%m} {month}/ML",
    (
        2018,
        2019,
        2020,
        2021,
    ): "G:/path_3/{date:%Y}/{date:%m} {month}/",
}


MONTHS = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]


def build_path(date: dt.datetime) -> str | None:
    month = MONTHS[date.month - 1]
    for years, path in BASE_DIR.items():
        if date.year in years:
            return os.path.join(path.format(date=date, month=month))
    return


# if __name__ == "__main__":
#     date = dt.datetime(2026, 3, 1)
#     print(date.strftime("%Y-%m-%d"))
#     print(build_path(date))
