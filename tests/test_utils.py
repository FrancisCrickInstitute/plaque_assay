from plaque_assay import utils


def test_col_to_well():
    assert utils.row_col_to_well(1, 1) == "A01"
    assert utils.row_col_to_well(8, 12) == "H12"


def test_get_plate_num():
    tests = [
        ("0000017__2020-10-16T14_46_58-Measurement 1", 17),
        ("/complete/path/to/0000017__2020-10-16T14_46_58-Measurement 1", 17),
        ("../relative/path/0000017__2020-10-16T14_46_58-Measurement 1", 17),
        ("0000999__2020-10-16T14_46_58-Measurement 1", 999),
    ]
    for test_string, expected_answer in tests:
        assert utils.get_plate_num(test_string) == expected_answer


def test_get_dilution_from_barcode():
    barcode = "A110000001__2020_00_00T00_00_00-Measurement 1"
    assert utils.get_dilution_from_barcode(barcode) == 1
    barcode = "/some/other/paths/A110000001__2020_00_00T00_00_00-Measurement 1"
    assert utils.get_dilution_from_barcode(barcode) == 1
    barcode = "/some/other/paths/A410000001__2020_00_00T00_00_00-Measurement 1"
    assert utils.get_dilution_from_barcode(barcode) == 4


def test_well_384_to_96():
    assert utils.well_384_to_96("A01") == "A01"
    assert utils.well_384_to_96("P24") == "H12"
    assert utils.well_384_to_96("B02") == "A01"
    assert utils.well_384_to_96("P01") == "H01"


def test_get_dilution_from_384_well_label():
    assert utils.get_dilution_from_384_well_label("A01") == 1
    assert utils.get_dilution_from_384_well_label("A02") == 2
    assert utils.get_dilution_from_384_well_label("B01") == 3
    assert utils.get_dilution_from_384_well_label("B02") == 4
    assert utils.get_dilution_from_384_well_label("P24") == 4
    assert utils.get_dilution_from_384_well_label("A03") == 1


def test_mock_384_barcode():
    existing_barcodes = ["AA1000001", "AA2000001", "AA2000001"]
    wells = ["A01", "A02", "A03"]
    output = utils.mock_384_barcode(existing_barcodes, wells)
    assert output == ["A11000001", "A22000001", "A12000001"]
