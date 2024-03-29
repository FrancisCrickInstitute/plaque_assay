"""
Class to encapsulate all plates and samples.
"Experiment" covers a given workflow and variant.
"""

import logging
import os
from collections import defaultdict
from typing import Dict, List, Any

import pandas as pd

from plaque_assay import utils
from plaque_assay.plate import Plate
from plaque_assay.sample import Sample


class Experiment:
    """Experiment class, holds plates and samples.

    Parameters
    ----------
    df : pandas.DataFrame

    Attributes
    -----------
    df : pandas.DataFrame
    experiment_name : str
    plate_store : dict
    sample_store : dict
    samples : key-value pairs
    plates: key-value pairs

    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.experiment_name = df["Plate_barcode"].values[0][3:]
        self.variant = df["variant"].values[0]
        self.plate_store = {name: Plate(df) for name, df in df.groupby("Plate_barcode")}
        self.df = pd.concat([plate.df for plate in self.plate_store.values()])
        self.sample_store = self.make_samples()

    @property
    def samples(self):
        """Key-value store of all samples in the experiment"""
        return self.sample_store.items()

    @property
    def plates(self):
        """Key-value store of all plates in the experiment"""
        return self.plate_store.items()

    def make_samples(self) -> Dict:
        """Return samples in the form of a dictionary.

        Returns
        -------
        dict
            `{sample_name: Sample}`
        """
        sample_dict = dict()
        for name, group in self.df.groupby("Well"):
            sample_df = group[["Dilution", "Percentage Infected"]]
            sample_dict[name] = Sample(name, sample_df, self.variant)
        return sample_dict

    def get_failures_as_dataframe(self) -> pd.DataFrame:
        """Return failures a dataframe

        Returns
        --------
        pandas.DataFrame
        """
        failures_list = []
        for _, plate_object in self.plates:
            if plate_object.plate_failed:
                failures_list.extend(plate_object.plate_failures)
            failures_list.extend(plate_object.well_failures)
        for _, sample_object in self.samples:
            failures_list.extend(sample_object.failures)
        df = pd.DataFrame(failures_list)
        df["experiment"] = self.experiment_name
        df["variant"] = self.variant
        return df

    def save_failures_as_dataframe(self, output_dir: str) -> None:
        """Save failures as a csv file.

        Parameters
        -----------
        output_dir : str
            directory in which the failure csv is saved

        Returns
        -------
        None
        """
        failures_df = self.get_failures_as_dataframe()
        failure_output_path = os.path.join(
            output_dir, f"failures_{self.experiment_name}.csv"
        )
        failures_df.to_csv(failure_output_path, index=False)
        logging.info("failures dataframe saved to %s", failure_output_path)

    def get_results_as_json(self) -> Dict:
        """Return final results as a dictionary.

        Returns
        -------
        dict
        """
        results = {}
        results["result_mapping"] = utils.INT_TO_RESULT
        results["results"] = {}
        for sample_name, sample in self.samples:
            results["results"][sample_name] = sample.ic50
        return results

    def get_results_as_dataframe(self) -> pd.DataFrame:
        """Return final results as a dataframe.

        Returns
        -------
        pandas.DataFrame
        """
        results_dict = self.get_results_as_json()
        result_mapping = results_dict["result_mapping"]
        wells = []
        ic50s: List[Any] = []
        statuses = []
        for well, value in results_dict["results"].items():
            wells.append(well)
            if value < 0:
                # is an error code
                ic50s.append(None)
                status_string = result_mapping[value]
                statuses.append(status_string)
            else:
                # is an ic50 value
                ic50s.append(value)
                statuses.append(None)
        df = pd.DataFrame({"well": wells, "ic50": ic50s, "status": statuses})
        df["experiment"] = self.experiment_name
        df["variant"] = self.variant
        return df

    def save_results_as_dataframe(self, output_dir: str) -> None:
        results_df = self.get_results_as_dataframe()
        result_output_path = os.path.join(
            output_dir, f"results_{self.experiment_name}.csv"
        )
        results_df.to_csv(result_output_path, index=False)
        logging.info("results dataframe saved to %s", result_output_path)

    def get_normalised_data(self) -> pd.DataFrame:
        """Get normalised data

        Returns
        --------
        pandas.DataFrame
        """
        dataframes = []
        for _, plate_object in self.plates:
            df = plate_object.get_normalised_data()
            dataframes.append(df)
        df_concat = pd.concat(dataframes)
        df_concat["variant"] = self.variant
        return df_concat

    def save_normalised_data(self, output_dir: str, concatenate: bool = True) -> None:
        """Save normalised data as a csv file

        Parameters
        ------------
        output_dir : str
            directory in which to save the csv file
        concatenate : bool
            if `True` then all plates will be joined into a single
            dataframe, otherwise `False` will return a dataframe
            per plate.

        Returns
        --------
        None
            Saves file to disk.
        """
        if concatenate:
            df_concat = self.get_normalised_data()
            save_path = os.path.join(
                output_dir, f"normalised_{self.experiment_name}.csv"
            )
            df_concat.to_csv(save_path, index=False)
            logging.info("concatenated normalised data saved to %s", save_path)
        else:
            # save as individual dataframe per plate
            for _, plate_object in self.plates:
                plate_object.save_normalised_data(output_dir)

    def get_model_parameters(self) -> pd.DataFrame:
        """Return curve-fitting parameters as a dataframe.

        The dataframe contains a row for every well. For wells
        where no model was fitted then these will be `NaN`.

        Returns
        --------
        pandas.DataFrame
            columns of

              - `well`
              - `experiment`
              - `variant`
              - `param_top`
              - `param_bottom`
              - `param_ec50`
              - `param_hillslope`
              - `mean_squared_error`
        """
        param_dict = defaultdict(list)
        for well, sample_obj in self.sample_store.items():
            model_params = sample_obj.model_params
            mean_squared_error = sample_obj.mean_squared_error
            if model_params is not None:
                top, bottom, ec50, hillslope = model_params
            else:
                top, bottom, ec50, hillslope = None, None, None, None
            param_dict["well"].append(well)
            param_dict["param_top"].append(top)
            param_dict["param_bottom"].append(bottom)
            param_dict["param_ec50"].append(ec50)
            param_dict["param_hillslope"].append(hillslope)
            param_dict["mean_squared_error"].append(mean_squared_error)
        df = pd.DataFrame(param_dict)
        df["experiment"] = self.experiment_name
        df["variant"] = self.variant
        return df

    def get_percentage_infected_dataframe(self) -> pd.DataFrame:
        """Return dataframe value of dilutions and percentage infected

        Returns
        --------
        pandas.DataFrame
        """
        dataframe_list = []
        for well, sample_obj in self.sample_store.items():
            sample_df = sample_obj.data.copy()
            sample_df["well"] = well
            dataframe_list.append(sample_df)
        df = pd.concat(dataframe_list)
        df["experiment"] = self.experiment_name
        df["variant"] = self.variant
        # remove capitalization and whitespace from column names
        df.columns = [i.replace(" ", "_").lower() for i in df.columns]
        return df
