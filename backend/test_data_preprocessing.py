import data_preprocessing as dp

# data = pd.read_csv("../Dataset/CleanedMetropolitanCensusTractsData.csv")

dp.get_city_ind_avg('Seattle', data)

dp.get_city_life_exp('Seattle', data)
# get_city_life_exp('Jacksonville', data)

# get_city_life_exp_dist('Seattle', data)