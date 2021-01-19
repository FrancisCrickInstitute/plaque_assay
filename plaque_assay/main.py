import os

import sqlalchemy

from plaque_assay.experiment import Experiment
from plaque_assay.consts import UNWANTED_METADATA
from plaque_assay import data


def create_engine(test=True):
    user = os.environ.get("NE_USER")
    if test:
        host = os.environ.get("NE_HOST_TEST")
    else:
        host = os.environ.get("NE_HOST_PROD")
    password = os.environ.get("NE_PASSWORD")
    if None in (user, host, password):
        raise RuntimeError(
            "db credentials not found in environent.",
            "Need to set NE_USER, NE_HOST_{TEST,PROD}, NE_PASSWORD"
    )
    engine = sqlalchemy.create_engine(
        f"mysql://{user}:{password}@{host}/serology"
    )
    return engine


def run(plate_list):
    Session = sqlalchemy.orm.sessionmaker(bind=create_engine())
    session = Session()
    print(data.get_awaiting_raw(session, "TEST000001"))
    dataset = data.read_data_from_list(plate_list)
    experiment = Experiment(dataset)
