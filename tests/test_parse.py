import adsctl
from adsctl import queries


def test_parse_1(customer_id):
    google_ads = adsctl.GoogleAds()

    tables = google_ads.query(queries.GET_CAMPAIGNS_LIST)

    for table_name, table in tables.items():
        print(table_name)
        print(table, "\n")


def test_parse_2(customer_id):
    google_ads = adsctl.GoogleAds()

    tables = google_ads.query(queries.GET_CAMPAIGNS_UI)

    # for table_name, table in tables.items():
    #     print(table_name)
    #     print(table, "\n")

    assert isinstance(tables, dict)
    assert len(tables) > 0
    assert "campaign" in tables
    assert "metrics" in tables
    assert "campaignBudget" in tables