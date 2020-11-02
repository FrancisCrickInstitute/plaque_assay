import json

from plaque_assay import data
from plaque_assay import qc
from plaque_assay import stats
from plaque_assay import plotting


def main(plot=False):
    df = data.read_data_21()
    failures = qc.detect_low_cells_image_region_area(df, 0.7)
    df = stats.subtract_background(df)
    df = stats.calc_percentage_infected(df)
    df = df.reset_index(drop=True)
    failures_high_background = qc.detect_high_background(df)
    # remove high-background points from data before fitting the model
    high_background_rows = [i["index"] for i in failures_high_background]
    df = df.drop(high_background_rows, axis=0)
    results = stats.calc_results_model(df)
    all_results = {
        "failures": {
            "high_background": failures_high_background,
            "low_cells_image_region_area": {
                "failed_entire_plates": failures.failed_plates,
                "failed_wells": failures.failed_wells,
            },
        },
        "results": results,
    }
    with open("results.json", "w") as f:
        json.dump(all_results, f, indent=4)
    if plot:
        plotting.test_plot(df)
    return all_results


if __name__ == "__main__":
    main(plot=True)
