import pandas as pd
import numpy as np


def main():
    data = pd.read_excel("output/data_cetes_20220101_20260227.xlsx")
    data.set_index("DIAS X VENCER", inplace=True)

    def row_pct(row):
        valid = row.dropna()
        pct = valid.pct_change()
        out = pd.Series(np.nan, index=row.index)
        out.loc[pct.index] = pct
        return out

    pct_data = data.apply(row_pct, axis=1)
    pct_data.to_excel("output/data_cetes_20220101_20260227_variacion.xlsx")


if __name__ == "__main__":
    main()
