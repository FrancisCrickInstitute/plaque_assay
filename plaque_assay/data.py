import logging
import os
import time

import pandas as pd

from . import utils
from . import consts
from . import db_models


def read_data_from_list(plate_list):
    plate_name_dict = {
        os.path.abspath(i): utils.get_dilution_from_barcode(i) for i in plate_list
    }
    dataframes = []
    for path, plate_num in plate_name_dict.items():
        df = pd.read_csv(
            # NOTE: might not always be Evaluation1
            os.path.join(path, "Evaluation1/PlateResults.txt"),
            skiprows=8,
            sep="\t",
        )
        plate_barcode = path.split(os.sep)[-1].split("__")[0]
        logging.info("plate barcode detected as %s", plate_barcode)
        df["Dilution"] = consts.plate_mapping[plate_num]
        # add well labels to dataframe
        well_labels = []
        for row, col in df[["Row", "Column"]].itertuples(index=False):
            well_labels.append(utils.row_col_to_well(row, col))
        df["Well"] = well_labels
        df["PlateNum"] = plate_num
        df["Plate_barcode"] = plate_barcode
        dataframes.append(df)
    df_concat = pd.concat(dataframes)
    logging.debug("input data shape: %s", df_concat.shape)
    return df_concat


def get_plate_list(data_dir):
    plate_list = [os.path.join(data_dir, i) for i in os.listdir(data_dir)]
    if len(plate_list) == 8:
        logging.debug("plate list detected: %s", plate_list)
    else:
        logging.error(
            "Did not detect 8 plates, detected %s :", len(plate_list), plate_list
        )
    return plate_list


def read_data_from_directory(data_dir):
    """
    read actual barcoded plate directory
    """
    plate_list = get_plate_list(data_dir)
    return read_data_from_list(plate_list)


def read_indexfiles_from_list(plate_list):
    plate_name_dict = {
        os.path.abspath(i): utils.get_dilution_from_barcode(i) for i in plate_list
    }
    dataframes = []
    for path, plate_num in plate_name_dict.items():
        df = pd.read_csv(os.path.join(path, "indexfile.txt"), sep="\t")
        plate_barcode = path.split(os.sep)[-1].split("__")[0]
        df["Plate_barcode"] = plate_barcode
        dataframes.append(df)
    df_concat = pd.concat(dataframes)
    # remove annoying empty "Unnamed: 16" column
    to_rm = [col for col in df_concat.columns if col.startswith("Unnamed:")]
    df_concat.drop(to_rm, axis=1, inplace=True)
    if len(to_rm) > 0:
        logging.info("removed columns: %s from concatenated indexfiles", to_rm)
    logging.debug("indexfile shape: %s", df_concat.shape)
    return df_concat


def read_indexfiles_from_directory(data_dir):
    plate_list = get_plate_list(data_dir)
    return read_indexfiles_from_list(plate_list)



def get_awaiting_raw(session, master_plate):
    awaiting_raw = (
        session.query(db_models.NE_workflow_tracking)
            .filter(db_models.NE_workflow_tracking.master_plate == master_plate)
            .filter(db_models.NE_workflow_tracking.status == "raw_results")
            .first()
    )
    return awaiting_raw


def upload_plate_results(session, awaiting_raw, plate_results_dataset):
    """docstring"""
    # check csv matches master plate selected
    workflow_id = awaiting_raw.workflow_id
    # TODO: filter and rename columns of raw_dataset
    plate_results_dataset["workflow_id"] = workflow_id
    # TODO: build insert into db_models.NE_raw_results
    awaiting_raw.status = "index_files"


def upload_indexfiles(session, awaiting_raw, indexfiles_dataset):
    """docstring"""
    # TODO: filter and rename columns
    indexfiles_dataset["workflow_id"] = awaiting_raw.workflow_id
    # TODO build insert into db_models.NE_raw_index
    awaiting_raw.status = "norm_results"


def upload_raw_results(session, master_plate, plate_results_dataset, indexfiles_dataset):
    """docstring"""
    awaiting_raw = get_awaiting_raw(master_plate)
    upload_plate_results(awaiting_raw, plate_results_dataset)
    upload_indexfiles(awaiting_raw, indexfiles_dataset)
    awaiting_raw.status = "norm_results"
    awaiting_raw.raw_results_upload = time.strftime("%Y-%m-%d %H:%M%:S")
    session.commit()


def upload_normalised_results(session, master_plate, norm_results):
    """docstring"""
    awaiting_norm = (
        session.query(db_models.NE_workflow_tracking)
            .filter(db_models.NE_workflow_tracking.master_plate == master_plate)
            .filter(db_models.NE_workflow_tracking.status == "norm_results")
            .first()
    )
    # TODO: filter and rename columns
    norm_results["workflow_id"] = awaiting_norm.workflow_id
    # TODO: bulk insert into db_models.NE_normalized results
    awaiting_norm.status = "final_results"
    awaiting_norm.normalized_results_upload = time.strftime("%Y-%m-%d %H:%M%:S")
    session.commit()


def upload_final_results(session):
    """docstring"""
    pass


def upload_percentage_infected(session):
    """docstring"""
    pass


def upload_model_parameters(session):
    """docstring"""
    pass

