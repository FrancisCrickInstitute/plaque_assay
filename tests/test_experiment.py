import os

import pandas as pd

from plaque_assay.experiment import Experiment


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "test_data", "experiment_df"))
EXAMPLE_EXPERIMENT_PATH = os.path.join(TEST_DATA_DIR, "experiment_df_example.csv")
EXAMPLE_EXPERIMENT_PATH_2 = os.path.join(TEST_DATA_DIR, "experiment_df_example_2.csv")
EXPERIMENT_DF = pd.read_csv(EXAMPLE_EXPERIMENT_PATH)
EXPERIMENT_DF_2 = pd.read_csv(EXAMPLE_EXPERIMENT_PATH)

experiment_list = [
    Experiment(EXPERIMENT_DF),
    Experiment(EXPERIMENT_DF_2),
]


def test_experiment_failures_as_dataframe():
    for experiment in experiment_list:
        failures_df = experiment.get_failures_as_dataframe()
        assert isinstance(failures_df, pd.DataFrame)


def test_experiment_results_as_json():
    for experiment in experiment_list:
        results_dict = experiment.get_results_as_json()
        assert isinstance(results_dict, dict)


def test_experiment_results_as_dataframe():
    for experiment in experiment_list:
        results_df = experiment.get_results_as_dataframe()
        assert isinstance(results_df, pd.DataFrame)
        assert results_df.shape[0] > 0


def test_experiment_get_normalised_data():
    for experiment in experiment_list:
        norm_df = experiment.get_normalised_data()
        assert isinstance(norm_df, pd.DataFrame)
        assert norm_df.shape[0] > 0


def test_experiment_get_model_parameters():
    for experiment in experiment_list:
        model_param_df = experiment.get_model_parameters()
        assert isinstance(model_param_df, pd.DataFrame)
        assert model_param_df.shape[0] > 0


def test_experiment_get_percentage_infected_dataframe():
    for experiment in experiment_list:
        perc_infected_df = experiment.get_percentage_infected_dataframe()
        assert isinstance(perc_infected_df, pd.DataFrame)
        assert perc_infected_df.shape[0] > 0
