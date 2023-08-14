"""
This is a boilerplate pipeline 'Preprocessing'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import merge_datasets_split, extract_holidays, normalise_rgb_of_all,Generate_normality_report_sales

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(func=merge_datasets_split,
                 inputs=['Sales','Articles',"params:parameters"],
                 outputs=['Germany','Austria','France'],
                 name="merge_split"),
            
             node(func=extract_holidays,
                 inputs=['Germany',"params:parameters"],
                 outputs='Germany_holidays',
                 name="Get_Hollidays_Germany"),

            node(func=extract_holidays,
                 inputs=['Austria',"params:parameters"],
                 outputs='Austria_holidays',
                 name="Get_Hollidays_Austria"),

            node(func=extract_holidays,
                 inputs=['France',"params:parameters"],
                 outputs='France_holidays',
                 name="Get_Hollidays_France"),

            node(func=normalise_rgb_of_all,
                 inputs=['Germany_holidays','Austria_holidays','France_holidays'],
                 outputs=['Germany_Final','Austria_Final','France_Final'],
                 name="RGB_Normalisation"),
            node(func=Generate_normality_report_sales,
                 inputs=['Germany_holidays','Austria_holidays','France_holidays'],
                 outputs=['Germany_Normality_Report','Austria_Normality_Report','France_Normality_Report'],
                 name="Normality_Report")
        ], 
        inputs=['Sales','Articles'],
        outputs=['Germany_Normality_Report','Austria_Normality_Report','France_Normality_Report','Germany_Final','Austria_Final','France_Final'],
        namespace='Preprocessing'
        )
