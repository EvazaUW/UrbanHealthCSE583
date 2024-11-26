import data_preprocessing as dp
import pandas as pd
import os

data = pd.read_csv("Dataset/UpdateMetropolitanCensusTractsData.csv")

# dp.get_city_ind_avg('Seattle', data)

# dp.get_city_life_exp('Seattle', data)
# get_city_life_exp('Jacksonville', data)

# get_city_life_exp_dist('Seattle', data)

print(data)

print(dp.metro_data_preprocessing(data))