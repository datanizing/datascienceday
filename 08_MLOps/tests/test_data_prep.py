"""Test data_prep module
"""
import pandas as pd
from nuedigitalmlapi.data_prep import CustomFeatures

def test_transform():
    df = pd.DataFrame([{
        "sepal length (cm)": 0.5, "sepal width (cm)": 2.4,
        "petal length (cm)": 0.1, "petal width (cm)": 1.2,
        }])
    df_transformed = CustomFeatures().transform(df)
    expected = pd.DataFrame([{
        "sepal length (cm)": 0.5, "sepal width (cm)": 2.4,
        "petal length (cm)": 0.1, "petal width (cm)": 1.2,
        "sepal rectangle (cm2)": 1.2,
        }])
    pd.util.testing.assert_frame_equal(df_transformed, expected, check_like=True)