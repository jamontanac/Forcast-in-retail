"""
This is a boilerplate pipeline 'reporting'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline
from .nodes import evaluate_model, feature_importance

def create_pipeline(**kwargs) -> Pipeline:
    pipeline_instance= pipeline([
        node(func=evaluate_model,
             inputs=["Pipeline","X_train","y_train","X_test","y_test"],
             outputs="metrics",
             name= "Reporting_metrics"
             ),
        node(func=feature_importance,
             inputs=["Pipeline","X_train","y_train","X_test","y_test"],
             outputs="figure",
             name="Plot_Feature_Importance")

    ],outputs=["metrics","figure"])

    Germany_pipeline = pipeline(
        pipe = pipeline_instance,
        inputs= {"Pipeline":"Germany_modeling_pipeline",
                 "X_train":"Germany_X_train_forTrain",
                 "y_train":"Germany_y_train_forTrain",
                 "X_test":"Germany_X_test_forTrain",
                 "y_test":"Germany_y_test_forTrain"},
        outputs= {"metrics":"metrics_germany",
                  "figure":"germany_feature_importance"},
        namespace="Germany_Reporting"
    )
    Austria_pipeline = pipeline(
        pipe = pipeline_instance,
        inputs= {"Pipeline":"Austria_modeling_pipeline",
                 "X_train":"Austria_X_train_forTrain",
                 "y_train":"Austria_y_train_forTrain",
                 "X_test":"Austria_X_test_forTrain",
                 "y_test":"Austria_y_test_forTrain"
                 },
        outputs= {"metrics":"metrics_austria",
                  "figure":"austria_feature_importance"},
        namespace="Austria_Reporting"
    )
    France_pipeline = pipeline(
        pipe = pipeline_instance,
        inputs= {"Pipeline":"France_modeling_pipeline",
                 "X_train":"France_X_train_forTrain",
                 "y_train":"France_y_train_forTrain",
                 "X_test":"France_X_test_forTrain",
                 "y_test":"France_y_test_forTrain"
                 },
        outputs= {"metrics":"metrics_france",
                  "figure":"france_feature_importance"},
        namespace="France_Reporting"
    )
    return Germany_pipeline + Austria_pipeline + France_pipeline
    #return pipeline([])

