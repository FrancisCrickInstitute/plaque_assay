import os

import pandas as pd

from . import utils


# --- TEMP STUFF ---#
# this will change as the barcodes are standardised
# but for now we are hard-coding this in the code

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR_14 = os.path.abspath(os.path.join(THIS_DIR, "../data/RuthExpt20201014"))
DATA_DIR_19 = os.path.abspath(os.path.join(THIS_DIR, "../data/RuthExpt20201019"))
DATA_DIR_21 = os.path.abspath(os.path.join(THIS_DIR, "../data/RuthExpt20201021"))
DATA_DIR_20201106 = os.path.abspath(os.path.join(THIS_DIR, "../data/RuthExpt20201106"))
DATA_DIR_20201202 = os.path.abspath(os.path.join(THIS_DIR, "../data/RuthExpt20201202"))

# NOTE: this is temporary until the barcodes are standardised
plate_mapping = {17: 1 / 40, 19: 1 / 160, 21: 1 / 640, 23: 1 / 2560}

real_plate_mapping = {1: 1 / 40, 2: 1 / 160, 3: 1 / 640, 4: 1 / 2560}

VIRUS_ONLY_WELLS = ("A12", "B12", "C12")
NO_VIRUS_WELLS = ("F12", "G12", "H12")


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
        df["Dilution"] = real_plate_mapping[plate_num]
        # add well labels to dataframe
        well_labels = []
        for row, col in df[["Row", "Column"]].itertuples(index=False):
            well_labels.append(utils.row_col_to_well(row, col))
        df["Well"] = well_labels
        df["PlateNum"] = plate_num
        df["Plate_barcode"] = plate_barcode
        dataframes.append(df)
    return pd.concat(dataframes)


def read_data_14(data_dir=DATA_DIR_14):
    """docstring"""
    # don't yet know how plates will be barcoded to identify the dilution series
    # for now just hard-code this information
    experiments = [os.path.join(data_dir, i) for i in os.listdir(data_dir)]
    plate_name_dict = {os.path.abspath(i): utils.get_plate_num(i) for i in experiments}
    dataframes = []
    for path, plate_num in plate_name_dict.items():
        df = pd.read_csv(
            # NOTE: might not always be Evaluation2
            os.path.join(path, "Evaluation2/PlateResults.txt"),
            skiprows=8,
            sep="\t",
        )
        df["Dilution"] = plate_mapping[plate_num]
        # add well labels to dataframe
        well_labels = []
        for row, col in df[["Row", "Column"]].itertuples(index=False):
            well_labels.append(utils.row_col_to_well(row, col))
        df["Well"] = well_labels
        df["PlateNum"] = plate_num
        dataframes.append(df)
    return pd.concat(dataframes)


def read_data_19(data_dir=DATA_DIR_19):
    """
    read in data from the 19 experiment, not yet using standardised barcodes
    so this is call hard-coded and custom for each experimental run
    """
    all_experiments = [os.path.join(data_dir, i) for i in os.listdir(data_dir)]
    # plate mapping, pairs of adjacent plates are duplicates of one another
    # with increasing dilutions
    plate_mapping = {
        25: 1 / 40,
        26: 1 / 40,
        27: 1 / 160,
        28: 1 / 160,
        29: 1 / 640,
        30: 1 / 640,
        31: 1 / 2560,
        32: 1 / 2560,
    }
    plate_name_dict = {
        os.path.abspath(i): utils.get_plate_num(i) for i in all_experiments
    }
    dataframes = []
    for path, plate_num in plate_name_dict.items():
        df = pd.read_csv(
            os.path.join(path, "Evaluation1/PlateResults.txt"), skiprows=8, sep="\t"
        )
        df["Dilution"] = plate_mapping[plate_num]
        well_labels = []
        for row, col in df[["Row", "Column"]].itertuples(index=False):
            well_labels.append(utils.row_col_to_well(row, col))
        df["Well"] = well_labels
        df["PlateNum"] = plate_num
        dataframes.append(df)
    return pd.concat(dataframes)


def read_data_21(data_dir=DATA_DIR_21):
    """
    read in data from the 21 experiment, not yet using standardised barcodes
    so this is call hard-coded and custom for each experimental run
    """
    all_experiments = [os.path.join(data_dir, i) for i in os.listdir(data_dir)]
    # plate mapping, pairs of adjacent plates are duplicates of one another
    # with increasing dilutions
    plate_mapping = {
        33: 1 / 40,
        34: 1 / 40,
        35: 1 / 160,
        36: 1 / 160,
        37: 1 / 640,
        38: 1 / 640,
        39: 1 / 2560,
        40: 1 / 2560,
    }
    plate_name_dict = {
        os.path.abspath(i): utils.get_plate_num(i) for i in all_experiments
    }
    dataframes = []
    for path, plate_num in plate_name_dict.items():
        df = pd.read_csv(
            os.path.join(path, "Evaluation1/PlateResults.txt"), skiprows=8, sep="\t"
        )
        df["Dilution"] = plate_mapping[plate_num]
        well_labels = []
        for row, col in df[["Row", "Column"]].itertuples(index=False):
            well_labels.append(utils.row_col_to_well(row, col))
        df["Well"] = well_labels
        df["PlateNum"] = plate_num
        dataframes.append(df)
    return pd.concat(dataframes)


def read_data_20201106(data_dir=DATA_DIR_20201106):
    """
    read in data from the 20201106 experiment, not yet using standardised barcodes
    so this is call hard-coded and custom for each experimental run
    """
    all_experiments = [os.path.join(data_dir, i) for i in os.listdir(data_dir)]
    # plate mapping, pairs of adjacent plates are duplicates of one another
    # with increasing dilutions
    plate_mapping = {
        222022: 1 / 40,
        222023: 1 / 40,
        222024: 1 / 160,
        222025: 1 / 160,
        222026: 1 / 640,
        222027: 1 / 640,
        222028: 1 / 2560,
        222029: 1 / 2560,
    }
    plate_name_dict = {
        os.path.abspath(i): utils.get_plate_num(i) for i in all_experiments
    }
    dataframes = []
    for path, plate_num in plate_name_dict.items():
        df = pd.read_csv(
            os.path.join(path, "Evaluation1/PlateResults.txt"), skiprows=8, sep="\t"
        )
        df["Dilution"] = plate_mapping[plate_num]
        well_labels = []
        for row, col in df[["Row", "Column"]].itertuples(index=False):
            well_labels.append(utils.row_col_to_well(row, col))
        df["Well"] = well_labels
        df["PlateNum"] = plate_num
        dataframes.append(df)
    return pd.concat(dataframes)


def read_data_20201202(data_dir=DATA_DIR_20201202):
    """
    read in data from the 20201202 experiment, not yet using standardised barcodes
    so this is call hard-coded and custom for each experimental run
    """
    all_experiments = [os.path.join(data_dir, i) for i in os.listdir(data_dir)]
    # plate mapping, pairs of adjacent plates are duplicates of one another
    # with increasing dilutions
    plate_mapping = {
        222069: 1 / 40,
        222070: 1 / 40,
        222071: 1 / 160,
        222072: 1 / 160,
        222073: 1 / 640,
        222074: 1 / 640,
        222075: 1 / 2560,
        222076: 1 / 2560,
    }
    plate_name_dict = {
        os.path.abspath(i): utils.get_plate_num(i) for i in all_experiments
    }
    dataframes = []
    for path, plate_num in plate_name_dict.items():
        df = pd.read_csv(
            os.path.join(path, "Evaluation1/PlateResults.txt"), skiprows=8, sep="\t"
        )
        df["Dilution"] = plate_mapping[plate_num]
        well_labels = []
        for row, col in df[["Row", "Column"]].itertuples(index=False):
            well_labels.append(utils.row_col_to_well(row, col))
        df["Well"] = well_labels
        df["PlateNum"] = plate_num
        dataframes.append(df)
    return pd.concat(dataframes)


# --- END TEMP STUFF ---#

if __name__ == "__main__":
    out = read_data_20201202()
    out.to_csv("/home/warchas/plaque_assay_df.csv", index=False)
