import os

import pandas as pd

from . import utils
from . import consts


def read_data(data_dir):
    """
    read actual barcoded plate directory
    """
    experiments = [os.path.join(data_dir, i) for i in os.listdir(data_dir)]
    plate_name_dict = {
        os.path.abspath(i): utils.get_dilution_from_barcode(i) for i in experiments
    }
    dataframes = []
    for path, plate_num in plate_name_dict.items():
        df = pd.read_csv(
            # NOTE: might not always be Evaluation2
            os.path.join(path, "Evaluation1/PlateResults.txt"),
            skiprows=8,
            sep="\t",
        )
        plate_barcode = path.split(os.sep)[-1].split("__")[0]
        df["Dilution"] = consts.plate_mapping[plate_num]
        # add well labels to dataframe
        well_labels = []
        for row, col in df[["Row", "Column"]].itertuples(index=False):
            well_labels.append(utils.row_col_to_well(row, col))
        df["Well"] = well_labels
        df["PlateNum"] = plate_num
        df["Plate_barcode"] = plate_barcode
        dataframes.append(df)
    return pd.concat(dataframes)
