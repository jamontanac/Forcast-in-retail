"""
This is a boilerplate pipeline 'reporting'
generated using Kedro 0.18.12
"""
import pandas as pd
from sklearn.pipeline import Pipeline
from typing import Dict, Tuple, Any
from sklearn.metrics import mean_absolute_error, max_error, r2_score
from sklearn.inspection import permutation_importance
import logging
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def evaluate_model(regressor:Pipeline,X_train: pd.DataFrame,y_train: pd.DataFrame,X_test: pd.DataFrame,y_test: pd.DataFrame)->Dict[str,float]:
    logger = logging.getLogger(__name__)
    logger.info(f" {X_test.shape}, {y_test.shape}")
    logger.info(f" columns_used test= {X_test.columns}")
    y_pred = regressor.predict(X_train)
    y_pred_test = regressor.predict(X_test)
    score = r2_score(y_train,y_pred)
    score_test = r2_score(y_test, y_pred_test)
    logger.info("Model has a coefficient R^2 of %.3f on train data.", score)
    logger.info("Model has a coefficient R^2 of %.3f on test data.", score_test)
    logger.info("Model has a oob score of %.3f on test data.",regressor["regressor"].oob_score_ )
    mae = mean_absolute_error(y_train, y_pred)
    me = max_error(y_train, y_pred)
    mae_test = mean_absolute_error(y_test, y_pred_test)
    me_test = max_error(y_test, y_pred_test)

    experiment_result ={"oob_score":regressor["regressor"].oob_score_,"r2_score":score,"mae":mae,"me":me,"r2_score_test": score_test, "mae_test": mae_test, "max_error_test": me_test}
    #return pipe, flat_model_params
    return experiment_result

def feature_importance(regressor:Pipeline,X_train: pd.DataFrame,y_train: pd.DataFrame,X_test:pd.DataFrame,y_test: pd.DataFrame)-> go.Figure:
    features_names=X_train.columns.values
    result_train = permutation_importance(regressor, X_train, y_train, n_repeats=10, random_state=42, n_jobs=2)
    result_test =  permutation_importance(regressor, X_test, y_test, n_repeats=10, random_state=42, n_jobs=2) 
    
    forest_importances_train = pd.Series(result_train.importances_mean, index=features_names)
    importances_std_train = result_train.importances_std
    
    forest_importances_test = pd.Series(result_test.importances_mean, index=features_names)
    importances_std_test = result_test.importances_std
    

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Importance in Train", "Importance in Test"))

    bar_trace_train = go.Bar(x=forest_importances_train.index, y=forest_importances_train.values, error_y=dict(type='data', array=importances_std_train),name="Train Data")

    bar_trace_test = go.Bar(x=forest_importances_test.index, y=forest_importances_test.values, error_y=dict(type='data', array=importances_std_test),name="Test Data")
    fig.add_trace(bar_trace_train, row=1, col=1)
    fig.add_trace(bar_trace_test, row=1, col=2)

    fig.update_layout(title='Feature importances using permutation on the full model',
                      yaxis_title='Mean Importance')
    return fig

