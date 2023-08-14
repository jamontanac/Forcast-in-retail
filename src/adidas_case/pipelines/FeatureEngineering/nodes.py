"""
This is a boilerplate pipeline 'FeatureEngineering'
generated using Kedro 0.18.12
"""
import pandas as pd
from typing import Dict, Tuple
import logging

def preprocess_colors(df:pd.DataFrame,parameters:Dict)-> pd.DataFrame:
    df["main_rgb"] = 0.3*df[parameters["main_colors"][0]]+ 0.6*df[parameters["main_colors"][1]]+0.11*df[parameters["main_colors"][2]]
    df["sec_rgb"] = 0.3*df[parameters["sec_colors"][0]]+ 0.6*df[parameters["sec_colors"][1]]+0.11*df[parameters["sec_colors"][2]] 
    return df
def set_date_as_index(df:pd.DataFrame)->pd.DataFrame:
    df["retailweek"] = pd.to_datetime(df["retailweek"], format="%Y-%m-%d")
    df=df.sort_values(by="retailweek").set_index("retailweek")
    return df
def Train_test_split(df:pd.DataFrame,parameters:Dict) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    categorical = ['productgroup', 'gender', 'category', 'style']
    bucket=['sizes']
    invariant = ['promo1', 'promo2','ratio']
    target = ['sales']
    numerical = ['regular_price','current_price','main_rgb','sec_rgb'] 
    logger = logging.getLogger(__name__)
    logger.info(
        f"Splitting data for the following independent variables "
        f"{categorical + bucket + invariant + numerical} against the target of '{target}' "
        f"with a test from 2017-01-01"
    )

    X,y = df[invariant+categorical+numerical+bucket],df[target]
    # split 80 -20
    new_X, X_test, new_y, y_test = X.loc[X.index <parameters["test_date"]], X.loc[X.index > parameters["test_date"]],y.loc[y.index < parameters["test_date"]], y.loc[y.index > parameters["test_date"]] 
    # split 80-20
    X_train, X_val, y_train, y_val = new_X.loc[new_X.index<parameters["test_date"]], new_X.loc[new_X.index>parameters["test_date"]], new_y.loc[new_y.index<parameters["test_date"]], new_y.loc[new_y.index >parameters["test_date"]]
    return X_train,X_val,X_test, y_train, y_val, y_test