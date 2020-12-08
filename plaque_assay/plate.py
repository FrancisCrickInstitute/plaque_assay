"""
module docstring
"""

import pandas as pd

from . import failure
from .consts import VIRUS_ONLY_WELLS


class Plate:
    """Plate class"""

    def __init__(self, df):
        self.df = df
        assert df["PlateNum"].nunique() == 1
        self.barcode = df["PlateNum"].values[0]
        assert df["Dilution"].nunique() == 1
        self.dilution = df["Dilution"].values[0]
        self.plate_failed = False
        self.well_failures = []
        self.plate_failures = []
        self.calc_percentage_infected()
        self.outside_image_area()
        self.high_background_wells()

    def __len__(self):
        return self.df.shape[0]

    def __str__(self):
        return f"Plate {self.barcode}"

    def outside_image_area(self):
        feature = "Cells - Image Region Area [µm²] - Mean per Well"
        experiment_median = self.df[feature].median()
        ratio = self.df[feature] / experiment_median
        self.df["ratio"] = ratio
        low = self.df[self.df["ratio"] < 0.7]
        high = self.df[self.df["ratio"] > 1.25]
        outliers = pd.concat([low, high])
        control_outliers = outliers[outliers["Well"].str.endswith("12")]
        if control_outliers.shape[0] > 0:
            # plate failure due to control well failure
            self.plate_failed = True
            self.plate_failures.append(
                failure.CellAreaPlateFailure(
                    plate=self.barcode,
                    wells=control_outliers["Well"].values.to_list(),
                    reason="cell region area outside expected range for control wells",
                )
            )
        if outliers.shape[0]:
            for _, row in outliers.iterrows():
                self.well_failures.append(
                    failure.WellFailure(
                        well=row["Well"],
                        plate=self.barcode,
                        reason="cell region area outside expected range",
                    )
                )

    def calc_percentage_infected(self):
        """docstring"""
        feature = "Background Subtracted Plaque Area"
        virus_only_bool = self.df.Well.isin(VIRUS_ONLY_WELLS)
        infection = self.df[virus_only_bool][feature].median()
        if infection < 0.3 or infection > 0.7:
            self.plate_failed = True
            self.plate_failures.append(
                failure.InfectionPlateFailure(
                    plate=self.barcode,
                    wells=VIRUS_ONLY_WELLS,
                    reason="plate fail due to infection outside optimal range",
                )
            )
        self.df["Percentage Infected"] = self.df[feature] / infection * 100

    def high_background_wells(self):
        """
        Identify wells with high fluorescent background.
        This is detected by wells with over 110% of the plate median
        in the DAPI channel.
        """
        colname = "Cells - Intensity Image Region DAPI (global) Mean - Mean per Well"
        experiment_median = self.df[colname].median()
        threshold = experiment_median * 1.1
        columns = ["Well", "PlateNum", colname]
        for idx, well, plate, val in self.df[columns].itertuples():
            if val > threshold:
                failed_well = failure.WellFailure(
                    well=well,
                    plate=plate,
                    reason="high fluorescent background in DAPI channel",
                )
                self.well_failures.append(failed_well)
