"""
This is a boilerplate pipeline 'Modeling'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline
from .nodes import create_pipeline_modeling


def create_pipeline(**kwargs) -> Pipeline:
    pipeline_instance= pipeline([
        node(func=create_pipeline_modeling,
             inputs=["X_train", "y_train","X_test","y_test", "params:model_options"],
             outputs="pipeline",
             name= "Generation_of_data_pipelining"
             ),
    ])

    Germany_pipeline = pipeline(
        pipe = pipeline_instance,
        inputs= {"X_train":"Germany_X_train_forTrain",
                 "y_train":"Germany_y_train_forTrain",
                 "X_test":"Germany_X_test_forTrain",
                 "y_test":"Germany_y_test_forTrain"},
        outputs= {"pipeline":"Germany_modeling_pipeline"},
        parameters={"params:model_options":"params:train_evaluation"},
        namespace="Germany_pipeline"
    )
    Austria_pipeline = pipeline(
        pipe = pipeline_instance,
        inputs= {"X_train":"Austria_X_train_forTrain",
                 "y_train":"Austria_y_train_forTrain",
                 "X_test":"Austria_X_test_forTrain",
                 "y_test":"Austria_y_test_forTrain"},
        parameters={"params:model_options":"params:train_evaluation"},
        #parameters={"params:any":"params:FeatureEngineering.parameters"},
        outputs= {"pipeline":"Austria_modeling_pipeline"},
        namespace="Austria_pipeline"
    )
    France_pipeline = pipeline(
        pipe = pipeline_instance,
        inputs= {"X_train":"France_X_train_forTrain",
                 "y_train":"France_y_train_forTrain",
                 "X_test":"France_X_test_forTrain",
                 "y_test":"France_y_test_forTrain"},
        parameters={"params:model_options":"params:train_evaluation"},
        #parameters={"params:any":"params:FeatureEngineering.parameters"},
        outputs= {"pipeline":"France_modeling_pipeline"},
        namespace="France_pipeline"
    )
    return Germany_pipeline + Austria_pipeline + France_pipeline
