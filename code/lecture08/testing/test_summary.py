import pandas as pd
import pytest

from calc_summary import calc_tips_summary


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "day": ["Fri", "Fri", "Sat", "Sat"],
            "total_bill": [10.0, 20.0, 30.0, 40.0],
            "tip": [1.0, 2.0, 3.0, 4.0],
        }
    )


def test_output_columns(sample_df):
    result = calc_tips_summary(sample_df)
    assert list(result.columns) == [
        "day",
        "count",
        "avg_bill",
        "avg_tip",
        "avg_tip_pct",
    ]


def test_groupby_day(sample_df):
    result = calc_tips_summary(sample_df)
    assert set(result["day"]) == {"Fri", "Sat"}
    assert len(result) == 2


def test_aggregation_values(sample_df):
    result = calc_tips_summary(sample_df)
    fri = result[result["day"] == "Fri"].iloc[0]
    assert fri["count"] == 2
    assert fri["avg_bill"] == 15.0
    assert fri["avg_tip"] == 1.5
    assert fri["avg_tip_pct"] == round((1 / 10 + 2 / 20) / 2, 2)


def test_rounding(sample_df):
    df = pd.DataFrame(
        {
            "day": ["Mon"],
            "total_bill": [3.0],
            "tip": [1.0],
        }
    )
    result = calc_tips_summary(df)
    assert result["avg_tip_pct"].iloc[0] == round(1 / 3, 2)
