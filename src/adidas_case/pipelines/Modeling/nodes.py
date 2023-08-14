"""
This is a boilerplate pipeline 'Modeling'
generated using Kedro 0.18.12
"""

import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler, PowerTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, max_error,r2_score
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
import pandas as pd
from typing import Tuple, Dict, Any
import importlib
import logging

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

def create_pipeline_modeling(X_train:pd.DataFrame, y_train:pd.DataFrame,X_test:pd.DataFrame, y_test:pd.DataFrame, model_options:Dict[str, Any]) -> Pipeline:
    # Define the possible categories for the bucketized variable
    bucket_categories = ['has it all', 'has small', 'has big', 'has medium', 'other']
    # Define the custom transformer for the bucketized variable
    bucket_transformer = CustomBucketizer(categories=bucket_categories)

    features_preprocessor = ColumnTransformer(
        transformers= [
            ('numerical', StandardScaler(),model_options["features_to_use"]["numerical"]),
            ('categorical', OneHotEncoder(handle_unknown="infrequent_if_exist"),model_options["features_to_use"]["categorical"]),
            ('bucketized', bucket_transformer,model_options["features_to_use"]["bucket"]),
            ('invariants','passthrough', model_options["features_to_use"]["invariant"])
        ])
    model_module = model_options["model_options"]["module"]
    model_type = model_options["model_options"]["class"]
    model_arguments = model_options["model_options"]["kwargs"]
    regressor_class = getattr(importlib.import_module(model_module), model_type)
    regressor_instance = regressor_class(**model_arguments)

    logger = logging.getLogger(__name__)
    logger.info(f"Fitting model of type {type(regressor_instance)}")


    pipe = Pipeline(steps=[('preprocessor',features_preprocessor),('regressor',regressor_instance)])
    pipe.fit(X_train,y_train)


    flat_model_params = {**{"model_type":model_type},**model_arguments}
    logger.info(flat_model_params)
    logger.info(f" {X_test.shape}, {y_test.shape}")
    logger.info(f" columns_used test= {X_test.columns}, columns_used train = {X_train.columns}")
    # y_pred_val = regressor.predict(X_val)
    y_pred_test = pipe.predict(X_test)
    score_test = r2_score(y_test, y_pred_test)
    # score_val = regressor.score(y_val, y_pred_val)
    
    logger.info("Model has a coefficient R^2 of %.3f on test data.", score_test)
    # logger.info("Model has a coefficient R^2 of %.3f on validation data.", score_val)
    logger.info("Model has a oob score of %.3f on test data.",pipe["regressor"].oob_score_ )
    mae_test = mean_absolute_error(y_test, y_pred_test)
    me_test = max_error(y_test, y_pred_test)
    # mae_val = mean_absolute_error(y_val, y_pred_val)
    # me_val = max_error(y_val, y_pred_val)

    experiment_result ={"oob_score":pipe["regressor"].oob_score_,"r2_score_test": score_test, "mae_test": mae_test, "max_error_test": me_test}
    logger.info(experiment_result)
    #return pipe, flat_model_params
    return pipe
