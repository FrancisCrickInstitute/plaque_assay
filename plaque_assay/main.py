from .assay import Assay
from .plate import Plate

from . import data


def main(dataset=data.read_data_19()):
    assay = Assay(df=dataset)
    for name, value in assay.plates.items():
        if len(value.well_failures):
            print(name, value.well_failures)

    for name, value in assay.plates.items():
        if value.plate_failed:
            print(name, value.plate_failures)


if __name__ == "__main__":
    main()
