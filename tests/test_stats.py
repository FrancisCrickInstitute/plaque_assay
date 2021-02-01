from plaque_assay import stats
from plaque_assay import utils


import pandas as pd

THRESHOLD = 50
WEAK_THRESHOLD = 60


dilutions = [
    0.000391,
    0.000391,
    0.001563,
    0.001563,
    0.006250,
    0.006250,
    0.025000,
    0.025000,
]

perc_inf_weak = [
    116.263735,
    93.992355,
    113.685992,
    97.030688,
    122.177319,
    103.793316,
    52.342949,
    61.026772,
]

df_weak_inhibition = pd.DataFrame(
    {"Dilution": dilutions, "Percentage Infected": perc_inf_weak}
)

perc_inf_no = [
    98.729667,
    100.000000,
    100.000000,
    97.147718,
    94.675382,
    100.000000,
    94.496768,
    100.000000,
]

df_no_inhibition = pd.DataFrame(
    {"Dilution": dilutions, "Percentage Infected": perc_inf_no}
)


# percentage infected for something that should be able to fit a model
perc_good = [
    100.556437,
    102.200186,
    104.246412,
    96.365569,
    110.787072,
    118.955933,
    44.517334,
    54.988952,
]


df_good_inhibition = pd.DataFrame(
    {"Dilution": dilutions, "Percentage Infected": perc_good}
)


def test_calc_heuristics_dilutions():
    weak_inhibition_out = stats.calc_heuristics_dilutions(
        df_weak_inhibition, THRESHOLD, WEAK_THRESHOLD
    )
    assert utils.INT_TO_RESULT[weak_inhibition_out] == "weak inhibition"
    no_inhibition_out = stats.calc_heuristics_dilutions(
        df_no_inhibition, THRESHOLD, WEAK_THRESHOLD
    )
    assert utils.INT_TO_RESULT[no_inhibition_out] == "no inhibition"
    good_inhib_out = stats.calc_heuristics_dilutions(
        df_good_inhibition, THRESHOLD, WEAK_THRESHOLD
    )
    assert good_inhib_out is None
