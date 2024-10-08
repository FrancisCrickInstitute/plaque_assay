from typing import List

import sqlalchemy

from plaque_assay import utils
from plaque_assay.main import create_engine

from . import db_uploader, ingest
from .titration_class import Titration


def run(plate_list: List[str]) -> None:
    """Run titration analysis pipeline

    Parameters
    -----------
    plate_list : list

    Returns
    -------
    None
        writes to database
    """
    engine = create_engine(test=False)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    lims_db_titration = db_uploader.TitrationDatabaseUploader(session)
    workflow_id = utils.get_workflow_id_from_plate_list(plate_list)
    variant = utils.get_variant_from_plate_list(plate_list, session, titration=True)
    if lims_db_titration.already_uploaded(workflow_id):
        print(f"workflow_id: {workflow_id} already have results in the database")
        # still exist successfully so task is marked complete
        return None
    dataset = ingest.read_data_from_list(plate_list)
    titration = Titration(dataset, variant=variant)
    normalised_results = titration.get_normalised_results()
    final_results = titration.get_final_results()
    model_parameters = titration.get_model_parameters()
    lims_db_titration.upload_normalised_results(normalised_results)
    lims_db_titration.upload_final_results(final_results)
    lims_db_titration.upload_model_parameters(model_parameters)
    lims_db_titration.update_workflow_tracking(workflow_id=workflow_id)
    lims_db_titration.commit()
