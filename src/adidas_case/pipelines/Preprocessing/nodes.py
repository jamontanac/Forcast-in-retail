"""
This is a boilerplate pipeline 'Preprocessing'
generated using Kedro 0.18.12
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import webcolors
import holidays
import matplotlib.pylab as plt
from sklearn.preprocessing import PowerTransformer
from scipy import stats
import matplotlib.figure

Holidays = {"France":holidays.FR(),"Germany":holidays.DE(), "Austria":holidays.AT()}


def _get_nearest_color(rgb:List[int]):
    min_colors={}
    for key, name in webcolors.CSS21_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb[0])**2
        gd = (g_c) - rgb[1]**2
        bd = (b_c) - rgb[2]**2
        min_colors[(rd+gd+bd)] = name
    return min_colors[min(min_colors.keys())]

def _get_closest_first_color(df:pd.DataFrame):
    r,g,b = df['rgb_r_main_col'], df['rgb_g_main_col'],	df['rgb_b_main_col']
    return _get_nearest_color([r,g,b])

def _get_closest_sec_color(df:pd.DataFrame):
    r,g,b = df['rgb_r_sec_col'], df['rgb_g_sec_col'],	df['rgb_b_sec_col']
    return _get_nearest_color([r,g,b])


def merge_datasets_split(df_sales:pd.DataFrame,df_articles:pd.DataFrame,parameters: Dict)->List[pd.DataFrame]:
    # we ignore the missing element (IO7646) because we are using inner join
    new_df = pd.merge(df_sales,df_articles, on= 'article')
    new_df['main_color'] = new_df.apply(_get_closest_first_color, axis=1)
    new_df['sec_color'] = new_df.apply(_get_closest_sec_color, axis=1)
    countries_df = []
    for country in parameters["countries"]:
        countries_df.append(new_df.query(f"country == '{country}'")
                            .sort_values(by=parameters['date_column'])
                            .reset_index(drop=True))
    return countries_df

def _is_holiday(date,country):
    if date in Holidays[country]:
        return True
    return False

def extract_holidays(df:pd.DataFrame,parameters: Dict)->pd.DataFrame:
    country_name = df['country'].unique()[0]
    is_holiday = pd.Series(df[parameters["date_column"]]).apply(lambda x: _is_holiday(x,country_name))
    is_holiday.name = "Holiday"
    return pd.concat([df,is_holiday],axis=1)

def _normalise_rgb(df):
    names=df.index
    total_sum = df[names[0]] + df[names[1]] + df[names[2]]
    return  df[names[0]]/total_sum , df[names[1]]/total_sum , df[names[2]]/total_sum

def normalise_rgb_of_all(Germany:pd.DataFrame,Austria:pd.DataFrame,France:pd.DataFrame)->Tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame]:
    # normalise primary color
    tmp_germany=Germany.filter(regex="(rbg.*main_col)")
    tmp_austria=Austria.filter(regex="(rbg.*main_col)")
    tmp_france=France.filter(regex="(rbg.*main_col)")
    #print(tmp_france.columns,tmp_germany.columns)
    Germany[tmp_germany.columns] = tmp_germany.apply(_normalise_rgb,axis=1).apply(pd.Series).values
    Austria[tmp_austria.columns] = tmp_austria.apply(_normalise_rgb,axis=1).apply(pd.Series).values
    France[tmp_france.columns] = tmp_france.apply(_normalise_rgb,axis=1).apply(pd.Series).values
    #normalise secondary color
    tmp_germany=Germany.filter(regex="(rbg.*sec_col)")
    tmp_austria=Austria.filter(regex="(rbg.*sec_col)")
    tmp_france=France.filter(regex="(rbg.*sec_col)")
    Germany[tmp_germany.columns] = tmp_germany.apply(_normalise_rgb,axis=1).apply(pd.Series).values
    Austria[tmp_austria.columns] = tmp_austria.apply(_normalise_rgb,axis=1).apply(pd.Series).values
    France[tmp_france.columns] = tmp_france.apply(_normalise_rgb,axis=1).apply(pd.Series).values
    return Germany.drop("country",axis=1),Austria.drop("country",axis=1), France.drop("country",axis=1)

def Generate_normality_report_sales(Germany:pd.DataFrame,Austria:pd.DataFrame,France:pd.DataFrame)->Tuple[matplotlib.figure.Figure,matplotlib.figure.Figure,matplotlib.figure.Figure]:
    return _power_transform(Germany,"Germany"),_power_transform(Austria,"Austria"),_power_transform(France,"France")
def _power_transform(df,title): 
    pt = PowerTransformer()

    sales_data = pt.fit_transform(df.sales.values.reshape(-1,1))
    sales_data=np.ravel(sales_data)

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 6))
    fig.suptitle(title)
    axes[1,0].hist(sales_data, bins=40, edgecolor='black')
    axes[1,0].set_xlabel("Value")
    axes[1,0].set_ylabel("Frequency")

    axes[1,1].hist(df.sales, bins=40, edgecolor="black")
    axes[1,1].set_xlabel("Value")
    axes[1,1].set_ylabel("Frequency")

    stats.probplot(sales_data, dist='norm', plot=axes[0,0])
    axes[0,0].set_title("Q-Q plot")

    sorted_data = np.sort(sales_data)

    # Calculate the cumulative probabilities for the observed data
    observed_cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

    # Calculate the cumulative probabilities for the normal distribution
    normal_cdf = stats.norm.cdf(sorted_data, loc=np.mean(sales_data), scale=np.std(sales_data))
    # Plot the P-P plot
    axes[0,1].plot(normal_cdf, observed_cdf, 'o')
    axes[0,1].plot([0, 1], [0, 1], 'k--') # Diagonal line
    axes[0,1].set_xlabel("Theoretical CDF")
    axes[0,1].set_ylabel("Observed CDF")
    axes[0,1].set_title("P-P Plot")
    plt.tight_layout()
    return fig
    