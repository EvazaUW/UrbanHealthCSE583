import data_preprocessing as dp
import pandas as pd
import os

raw_data = pd.read_csv("Dataset/UpdateMetropolitanCensusTractsData.csv")

data = dp.metro_data_preprocessing(raw_data)

seattle_index_means, seattle_index_rank_means = dp.get_city_ind_avg('Seattle', data)
dp.get_city_life_exp('Seattle', data)

dp. get_city_life_exp('Jacksonville', data)

print(seattle_index_means, seattle_index_rank_means)