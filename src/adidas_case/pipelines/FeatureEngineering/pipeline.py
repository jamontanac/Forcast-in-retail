"""
This is a boilerplate pipeline 'FeatureEngineering'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import Train_test_split, preprocess_colors, set_date_as_index


def create_pipeline(**kwargs) -> Pipeline:
    pipeline_instance= pipeline([
        node(func=preprocess_colors,
             inputs=["data","params:any"],
             outputs="data_with_standard_color",
             name= "Standar_color"
             ),
        node(func=set_date_as_index,
             inputs="data_with_standard_color",
             outputs="Data_as_timeSeries",
             name= "Setting_date_time"
             ),
        node(
            func = Train_test_split,
            inputs = ["Data_as_timeSeries","params:any"],
            outputs = ["X_train","X_val", "X_test", "y_train", "y_val", "y_test"],
            name = "Train_test_split"
        ),
    ])
    Germany_pipeline = pipeline(
        pipe = pipeline_instance,
        inputs= {"data":"Germany_Final"},
        parameters={"params:any":"params:FeatureEngineering.parameters"},
        outputs= {"X_train":"Germany_X_train",
                  "X_val":"Germany_X_val",
                  "X_test":"Germany_X_test",
                  "y_train":"Germany_y_train",
                  "y_val":"Germany_y_val",
                  "y_test":"Germany_y_test"},
        namespace="Germany_split"
    )
    Austria_pipeline = pipeline(
        pipe = pipeline_instance,
        inputs= {"data":"Austria_Final"},
        parameters={"params:any":"params:FeatureEngineering.parameters"},
        outputs= {"X_train":"Austria_X_train",
                  "X_val":"Austria_X_val",
                  "X_test":"Austria_X_test",
                  "y_train":"Austria_y_train",
                  "y_val":"Austria_y_val",
                  "y_test":"Austria_y_test"},
        namespace="Austria_split"
    )
    France_pipeline = pipeline(
        pipe = pipeline_instance,
        inputs= {"data":"France_Final"},
        parameters={"params:any":"params:FeatureEngineering.parameters"},
        outputs= {"X_train":"France_X_train",
                  "X_val":"France_X_val",
                  "X_test":"France_X_test",
                  "y_train":"France_y_train",
                  "y_val":"France_y_val",
                  "y_test":"France_y_test"},
        namespace="France_split"
    )
    return Germany_pipeline + Austria_pipeline + France_pipeline
