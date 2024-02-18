import numpy as np
import pandas as pd
from pytest import approx

def compute_analysis(dataframe) -> float:
    mean = dataframe["absolute_magnitude_h"].mean()
    return mean

def test_compute_analysis():
    inputs = pd.DataFrame.from_dict({'absolute_magnitude_h': [11,12,20]})
    exp_output = 14.33
    actual_output = compute_analysis(inputs)
    assert actual_output == approx(exp_output, rel=1e-3, abs=1e-3)
 