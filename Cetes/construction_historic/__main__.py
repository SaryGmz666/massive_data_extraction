import datetime as dt
import logging
import pandas as pd

from construction_historic.data_processing import Orchestrator

logging.basicConfig(
    level=logging.INFO,
    format="\n %(asctime)s | %(levelname)s | %(message)s",
)


def main(start_date: dt.datetime, finish_date: dt.datetime) -> pd.DataFrame:

    orchestrator = Orchestrator(start_date, finish_date)
    return orchestrator.run()


if __name__ == "__main__":
    import time

    start = time.time()
    start_date = dt.datetime(2016, 1, 1)
    finish_date = dt.datetime(2017, 12, 31)  # .today()

    data = main(start_date, finish_date)
    data.to_excel(
        f"output/data_cetes_{start_date.strftime('%Y%m%d')}_{finish_date.strftime('%Y%m%d')}.xlsx",
        index=False,
    )

    print(
        f"""El proceso tardó {time.time() - start: .2f} segundos, que equivale a """
        f"""{(time.time() - start)/(60*60*24): .6f} dias.\nPodrías ejecutar el código"""
        f""" {365*24*60*60/(time.time() - start): ,.2f} veces en un año.\n"""
    )
