########## This script contains functions for data transformation and city-level data analysis #############

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load the data
data = pd.read_csv("Dataset/UpdateMetropolitanCensusTractsData.csv")


#########################################################################
######### Functions needed for preprocessing ###############

metro_area_dict = {
    'NY': 'New York',
    'AZ': 'Phoenix',
    'IL': 'Chicago',
    'TX': 'Houston',
    'MA': 'Boston',
    'WA': 'Seattle',
    'DC': 'DC',
    'VA': 'DC',
    'FL': 'Jacksonville'
}

ten_metro = pd.Categorical(
    ['Seattle', 'New York', 'Boston','Chicago', "DC", "Los Angeles", 
     "San Francisco", "Phoenix", "Houston", "Jacksonville"]
)


def assign_metro_area(row):
    if row['stateid'] == "06" and row['countyid'] == '037':
        return 'Los Angeles'
    elif row['stateid'] == "06" and (row['countyid'] == '001' or row['countyid'] == '075') :
        return 'San Francisco'
    else:
        # use the mapping dictionary for states other than CA
        return metro_area_dict.get(row['Sits in State'])


def metro_data_preprocessing(df): 
    """
    This function takes in the UrbanHealthCSE583/Dataset/UpdateMetropolitanCensusTractsData.csv,
    makes the following transformations:
      - create a new variable that indicates metro area based on FGEOIDCT10
      - create a new variable for life expectancy level
      - create a new variable for percentile ranks for each urban indicator (8 in total)
    
    and returns an updated df
    """ 
    # wrangle the state and county codes
    df['FGEOIDCT10'] = df['FGEOIDCT10'].astype(str).str.zfill(11)
    df['stateid'] = df.iloc[:, 0].astype(str).str[:-9]
    df['countyid'] = df.iloc[:, 0].astype(str).str[-9:-6]
    
    # Create a new variable that indicates metro area 
    df['metro'] = df.apply(assign_metro_area, axis =1)
    df['metro'] = df['metro'].astype('category')

    # Data transformation for health and urban indices 
    df['Life Expectancy level'] = pd.cut(df['Life Expectancy'], 
                                         bins = [0, 70, 75, 80, 85, 100], 
                                         labels = ['poor', 'Fair', 'Average', 'Good', 'Excellent'])
    
    urban_indicators = ['Average Distance to Transit', 'Ave Economic Diversity', 
                        'Ave Road Network Density', 'Walkability Index',
                        'Ave Percent People Without Health Insurance', 'Ave Population Density',
                        'Ave Percent People Unemployed', 'Ave Physical Inactivity']
    
    for indicator in urban_indicators:  # transform into percentile ranks
        non_na_values = len(data[indicator].dropna())
        col_name = indicator + "_Rank"
        df[col_name] = df[indicator].rank(na_option = 'keep')/non_na_values *100
    
    return df


# All of the functions below takes in a city (category), and the processed data as input

def get_city_ind_avg(city, df):
    """
    This function returns two pandas Series objects.
    0 - a series that contains the mean values for the 8 urban indices for a selected city.
    1 - a series that contains the mean percentile ranks for the 8 urban indices for a selected city. 
    The indices should be in the same order. 
    
    usage:
    index_values, index_ranks = get_city_ind_avg()
    """

    if city not in ten_metro:
        raise ValueError("Not in the ten metro areas. ")
    else:
        data_subset = df[df['metro'] == city]
        urban_index_means = data_subset.loc[:,'Average Distance to Transit':'Ave Physical Inactivity'].mean()
        urban_index_rank_means = data_subset.loc[:,'Average Distance to Transit_Rank':'Ave Physical Inactivity_Rank'].mean()

        # check if the two series have the same order of urban indices
        check = urban_index_means.index == urban_index_rank_means.index.astype(str).str[:-5] 
        
        if check.all():
            pass
        else:
            raise ValueError("The order of indices do not match. ")

    return (urban_index_means, urban_index_rank_means)

def get_city_life_exp(city, df):
    """
    This function returns a set of metrics around the life expectancy of a selected city.
    0 - the mean life expectancy of a metro area across all census tracts,
    1 - the level (poor, fair, ave, good, excellent) of the mean life expectancy,
    2 - a data frame with 5 census tracts with the lowest life expectancy.
    """
    if city not in ten_metro:
        raise ValueError("Not in the ten metro areas. ")
    else:
        data_subset = df[df['metro'] == city]
        
        mean_life_exp_by_metro = df.groupby('metro')['Life Expectancy'].mean()
        life_exp_mean = mean_life_exp_by_metro.loc[city].round(2)
        
        life_exp_level = (
            "Very Poor" if life_exp_mean < 72 else
            "Poor" if 72 <= life_exp_mean < 76 else
            "Fair" if 76 <= life_exp_mean < 79.5 else
            "Good" if 79.5 <= life_exp_mean < 82 else
            "Excellent"
        )

        life_exp_level_num = (
            1 if life_exp_mean < 72 else
            2 if 72 <= life_exp_mean < 76 else
            3 if 76 <= life_exp_mean < 79.5 else
            4 if 79.5 <= life_exp_mean < 82 else
            5
        )
        
        highest_life_exp = data_subset['Life Expectancy'].max()
        mid_life_exp = data_subset['Life Expectancy'].median()
        lowest_tracts = data_subset.nsmallest(5, 'Life Expectancy').loc[:, ["FGEOIDCT10", "Life Expectancy", "Life Expectancy level"]]
    
    return (life_exp_mean, life_exp_level, life_exp_level_num, highest_life_exp, mid_life_exp, lowest_tracts)

def get_city_life_exp_dist_plot(city, df):
    if city not in ten_metro:
        raise ValueError("Not in the ten metro areas. ")
    else:
        data_subset = df[df['metro'] == city]

        fig, ax = plt.subplots()
        sns.histplot(data_subset, x= 'Life Expectancy', kde = True)

    return fig
