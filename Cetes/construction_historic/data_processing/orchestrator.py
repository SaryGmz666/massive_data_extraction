import attr
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
from tqdm import tqdm

from construction_historic.config import build_path, ProgressBarManager
from construction_historic.data_processing.read_files import file_location, read_massive


@attr.s
class Orchestrator:
    date_inicial: dt.datetime = attr.ib()
    final_day: dt.datetime = attr.ib()

    def _dates_to_extract(self) -> list[dt.datetime]:
        periods = []
        current_date = self.date_inicial
        while current_date <= self.final_day:
            periods.append(current_date)
            current_date += relativedelta(months=1)

        self.periods = periods
        return periods

    def _data_extraction(self, manager) -> dict[str, pd.DataFrame]:
        result = {}

        tqdm.write("")
        tqdm.write("\033[1mINICIANDO ALGORITMO...\033[0m")

        with tqdm(
            self.periods,
            desc="Leyendo archivos...".ljust(manager.desc_length),
            ncols=manager.bar_width,
            colour=manager.colour,
            bar_format="{desc} |{bar}| {percentage:3.0f}%",
        ) as pbar:

            for date in pbar:
                pbar.set_postfix_str(date.strftime("%Y-%m"))

                dates = build_path(date)
                files_location = file_location(dates, "_Vector")

                params = {"usecols": ["EMISORA", "DIAS X VENCER", "RENDIMIENTO"]}

                data = read_massive(files_location, params)
                result.update(data)

        self.data = result
        return result

    def data_fusion(self, manager) -> pd.DataFrame:
        df_inicial = pd.DataFrame(
            range(1, 731), columns=["DIAS X VENCER"]
        )  # NOTE modificable

        with tqdm(
            self.data.items(),
            desc="Uniendo DataFrames...".ljust(manager.desc_length),
            ncols=manager.bar_width,
            colour=manager.colour,
            bar_format="{desc} |{bar}| {percentage:3.0f}%",
        ) as pbar:

            for date, df in pbar:
                pbar.set_postfix_str(date)

                df_copy = df.rename(columns={"RENDIMIENTO": date})
                df_inicial = pd.merge(
                    df_inicial, df_copy, on="DIAS X VENCER", how="outer"
                )

        return df_inicial

    def run(self):
        managers = ProgressBarManager.default_managers()
        self._dates_to_extract()
        self._data_extraction(managers["files"])
        return self.data_fusion(managers["fusion"])
