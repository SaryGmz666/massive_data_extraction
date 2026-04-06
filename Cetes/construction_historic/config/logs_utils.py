from tqdm import tqdm
import attr
import time
import datetime as dt


@attr.s(slots=True)
class ProgressBarManager:
    desc_length = attr.ib(default=34, type=int)
    bar_width = attr.ib(default=100, type=int)
    colour = attr.ib(default="#FFFFFF", type=str)
    delay = attr.ib(default=0.0, type=float)

    def _format_item_name(self, item) -> str:
        """Formatea el nombre dependiendo del tipo de item."""
        if isinstance(item, dt.datetime):
            return item.strftime("%Y-%m")
        return str(item)

    def show_progress_bar(self, items, desc, is_dict=False):
        with tqdm(
            items,
            desc=desc.ljust(self.desc_length),
            ncols=self.bar_width,
            colour=self.colour,
            dynamic_ncols=False,
            bar_format="{desc} |{bar}| {percentage:3.0f}%",
        ) as pbar:
            for item in pbar:
                name = item[0] if is_dict else self._format_item_name(item)
                pbar.set_postfix_str(name)
                if self.delay:
                    time.sleep(self.delay)

    def process_files(self, periods):
        tqdm.write("")
        tqdm.write("\033[1mINICIANDO ALGORITMO...\033[0m")
        self.show_progress_bar(periods, "Procesando meses...")

    def process_data_fusion(self, data: dict):
        self.show_progress_bar(data.items(), "Uniendo DataFrames...", is_dict=True)

    @classmethod
    def default_managers(cls):
        colores = {
            "files": "#F0873C",
            "fusion": "#C95E2E",
        }
        return {name: cls(colour=color) for name, color in colores.items()}
