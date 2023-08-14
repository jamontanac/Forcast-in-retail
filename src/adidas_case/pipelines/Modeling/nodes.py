"""
This is a boilerplate pipeline 'Modeling'
generated using Kedro 0.18.12
"""

import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler, QuantileTransformer, PowerTransformer
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
from typing import Tuple, Dict

class CustomBucketizer(BaseEstimator, TransformerMixin):
    def __init__(self, categories):
        self.categories = categories
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        bucketized = X.applymap(_bucketize).iloc[:,0]
        encoder = OneHotEncoder(categories=[self.categories])
        one_hot_encoded = encoder.fit_transform(bucketized.values.reshape(-1, 1))
        return one_hot_encoded.toarray()

def _bucketize(sizes):
    all_sizes = set(['xxs', 'xs', 's', 'm', 'l', 'xl', 'xxl'])
    sizes_set = set(sizes.split(','))
    if sizes_set == all_sizes:
        return "has it all"
    elif sizes_set & set(['xxs', 'xs', 's']):
        return "has small"
    elif sizes_set & set(['l', 'xl', 'xxl']):
        return "has big"
    else:
        return "other"

 