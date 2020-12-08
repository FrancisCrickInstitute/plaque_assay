"""
module docstring
"""

import pandas as pd

from .consts import VIRUS_ONLY_WELLS, NO_VIRUS_WELLS
from .plate import Plate


class Assay:
    """Assay class, holds plates"""

    def __init__(self, df):
        df = self.subtract_plaque_area_background(df)
        self.plates = {name: Plate(df) for name, df in df.groupby("PlateNum")}
        self.df = pd.concat([plate.df for plate in self.plates.values()])

    def subtract_plaque_area_background(self, df):
        """
        - Calculate the median of "Normalised Plaque area" fo no virus wells.
        - Subtract median from "Normalised Plaque area" for each well and save
          as "Background Subtracted Plaque Area"
        """
        feature = "Normalised Plaque area"
        new_colname = "Background Subtracted Plaque Area"
        no_virus_bool = df.Well.isin(NO_VIRUS_WELLS)
        background = df[no_virus_bool][feature].median()
        df[new_colname] = df[feature] - background
        return df
