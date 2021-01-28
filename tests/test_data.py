from plaque_assay import data


def test_create_barcode_change_384_df():
    workflow_id = "000001"
    df = data.create_barcode_change_384_df(workflow_id)
    print(df)
    assert df["assay_plate_384"].values.tolist() == [
        f"AA1{workflow_id}",
        f"AA2{workflow_id}",
    ]
    assert df["workflow_id"].values.tolist() == [workflow_id, workflow_id]
    assert df["ap_10"].values.tolist() == [f"A11{workflow_id}", f"A12{workflow_id}"]
    assert df["ap_40"].values.tolist() == [f"A21{workflow_id}", f"A22{workflow_id}"]
    assert df["ap_160"].values.tolist() == [f"A31{workflow_id}", f"A32{workflow_id}"]
    assert df["ap_640"].values.tolist() == [f"A41{workflow_id}", f"A42{workflow_id}"]
