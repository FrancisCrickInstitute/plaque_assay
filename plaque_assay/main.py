from plaque_assay.experiment import Experiment
from plaque_assay.plate import Plate
from plaque_assay import data


def main():
    dataset = data.read_data("../data/RawDataExample")
    experiment = Experiment(df=dataset)
    for plate_name, plate in experiment.plates.items():
        print(plate.plate_failures)
        print(plate.well_failures)



if __name__ == "__main__":
    main()
