from utils.countries import country_name_to_code


def test_easy_names():
    assert country_name_to_code("Vietnam") == "vn"
    assert country_name_to_code("viet Nam") == "vn"
    assert country_name_to_code("Singapore") == "sg"


def test_not_detected_in_pycountry():
    # Hardcoded mappings because pycountry's lookup function
    # doesn't recognize them.
    assert country_name_to_code("South Korea") == "kr"


def test_empty_names():
    assert country_name_to_code(None) is None
    assert country_name_to_code("") is None
