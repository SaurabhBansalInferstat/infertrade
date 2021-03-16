"""
Functions used to compute allocations - % of your portfolio to invest in a market or asset.

Copyright 2021 InferStat Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Created by: Joshua Mason
Created date: 11/03/2021
"""


import pandas as pd
from sklearn.preprocessing import FunctionTransformer


def fifty_fifty(dataframe) -> pd.DataFrame:
    """Allocates 50% of strategy budget to asset, 50% to cash."""
    dataframe["position"] = 0.5
    return dataframe


def constant_allocation_size(dataframe: pd.DataFrame, fixed_allocation_size: float = 1.0) -> pd.DataFrame:
    """
    Returns a constant allocation, controlled by the constant_position_size parameter.

    parameters:
    constant_allocation_size: determines allocation size.
    """
    dataframe["position"] = fixed_allocation_size
    return dataframe


def high_low_difference(dataframe: pd.DataFrame, scale: float = 1.0, constant: float = 0.0) -> pd.DataFrame:
    """
    Returns an allocation based on the difference in high and low values. This has been added as an
    example with multiple series and parameters

    parameters:
    scale: determines amplitude factor.
    """
    dataframe["position"] = ((dataframe["high"] - dataframe["low"]) * scale + constant)
    return dataframe


export_positions = {
    "fifty_fifty": {
        "function": fifty_fifty,
        "parameters": {},
        "series": []
    },
    "constant_allocation_size": {
        "function": constant_allocation_size,
        "parameters": {"constant_allocation_size": 1.0},
        "series": []
    },
    "high_low_difference": {
        "function": high_low_difference,
        "parameters":  {"scale": 1.0, "constant": 0.},
        "series": ["high", "low"]
    },
}


def scikit_position_factory(position_function: callable) -> FunctionTransformer:
    """This creates a SciKit Learn compatible Transformer embedding the position calculation."""
    return FunctionTransformer(position_function)
