import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_white"
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from math import sqrt
from joblib import dump, load

def clean_data(df):
    df['FGEOIDCT10'] = df['FGEOIDCT10'].astype(str).str.zfill(11)
    df = df.dropna(inplace=False)
    return df

def get_city_data_by_city(df, city_name):
    city_data = df[df['City'] == city_name]
    city_data = clean_data(city_data)
    return city_data
def get_city_data_by_ct_geoid(df, geoid):
    # df = clean_data(df)
    tract_data = df[df['FGEOIDCT10'] == geoid]
    if tract_data.empty:
        print(f"Census tract with FGEOID10 '{geoid}' not found.")
        return
    city = tract_data['City'].iloc[0]
    city_data = df[df['City'] == city]
    return city_data

def df_feature_reverse_for_ml(df):
    df['Ave Percent People With Health Insurance'] = df['Ave Percent People Without Health Insurance'].apply(lambda x: 100 - x)
    df['Ave Physical Activity'] = df['Ave Physical Inactivity'].apply(lambda x: 100 - x)
    df['Ave Percent People Employed'] = df['Ave Percent People Unemployed'].apply(lambda x: 100 - x)
    df = df.drop(['Ave Percent People Without Health Insurance', 'Ave Physical Inactivity', 'Ave Percent People Unemployed'], axis=1)
    return df

def generate_correlation_matrix(df):
    correlation_matrix = df.corr()
    # Creating a heatmap using seaborn
    plt.figure(figsize=(8, 7))
    sns.heatmap(correlation_matrix, annot=True, cmap='BrBG', center=0, fmt=".2f")
    plt.title('Correlation Matrix Heatmap of Health and Urban Indicators')
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor")  # Improve label readability
    plt.yticks(rotation=0)
    plt.tight_layout()  # Adjust layout to make room for label rotation
    plt.savefig('correlation_matrix.png')  # Saves the figure to a file
    plt.show()
    # plt.close()  # Close the figure to free up memory


def print_coefficients(model, features):
    """
    This function takes in a model column and a features column. 
    And prints the coefficient along with its feature name.
    """
    feats = list(zip(features, model.coef_))
    print(*feats, sep = "\n")
def save_model(model, scaler, model_name):
    dump(model, f'{model_name}.joblib')
    dump(scaler, f'std_scaler_{model_name}.bin', compress=True)
def load_model(model_name):
    model = load(f'{model_name}.joblib')
    scaler = load(f'std_scaler_{model_name}.bin')
    return model, scaler

def train_regression_model(df, features, target='Life Expectancy', model_type='ridge'):
  """Trains a regression model for a specific city.

  Args:
    df: DataFrame containing data for a city or for all census tracts.
    features: List of feature column names.
    target: Name of the target column.
    model_type: Type of regression model to train ('ridge' or 'lasso').

  Returns:
    Trained regression model.
  """

  # Split data into train, validation, and test sets
  life_exp = df[target]
  df = df[features]
  train_and_val_df, test_df, train_and_val_life_exp, test_life_exp = \
      train_test_split(df, life_exp, test_size=0.2)
  train_df, val_df, train_life_exp, val_life_exp = \
      train_test_split(train_and_val_df, train_and_val_life_exp, test_size=.125)

  # Standardize features
  scaler = StandardScaler().fit(train_df)
  train_df = scaler.transform(train_df)
  val_df = scaler.transform(val_df)
  test_df = scaler.transform(test_df)

  if model_type == 'ridge':
    # Train Ridge Regression model
    l2_lambdas = np.logspace(-5, 5, 11, base=10)
    ridgeData = []
    for i in range(11):
        ridge_model = Ridge(alpha=l2_lambdas[i])
        ridge_model.fit(train_df, train_life_exp)
        train_life_exp_true = train_life_exp.values
        train_life_exp_pred = ridge_model.predict(train_df)
        train_rmse = sqrt(mean_squared_error(train_life_exp_true, train_life_exp_pred))
        val_life_exp_true = val_life_exp.values
        val_life_exp_pred = ridge_model.predict(val_df)
        val_rmse = sqrt(mean_squared_error(val_life_exp_true, val_life_exp_pred))
        ridgeData.append({
            'l2_penalty': l2_lambdas[i],
            'model': ridge_model,
            'train_rmse': train_rmse,
            'val_rmse': val_rmse
        })
    ridge_data = pd.DataFrame(ridgeData)
    index = ridge_data['val_rmse'].idxmin()
    best_model = ridge_data.loc[index]['model']
    best_l2 = ridge_data.loc[index]['l2_penalty']
    test_rmse = sqrt(mean_squared_error(test_life_exp.values, ridge_model.predict(test_df)))   # test_rmse
    print('L2 Penalty',  best_l2)
    print('Test RSME', test_rmse)
    print_coefficients(best_model, features)

  elif model_type == 'lasso':
    # Train Lasso Regression model
    l1_lambdas = np.logspace(-5, 5, 11, base=10)
    lassoData = []
    for i in range(11):
        lasso_model = Lasso(alpha=l1_lambdas[i])
        lasso_model.fit(train_df, train_life_exp)
        train_life_exp_true = train_life_exp.values
        train_life_exp_pred = lasso_model.predict(train_df)
        train_rmse = sqrt(mean_squared_error(train_life_exp_true, train_life_exp_pred))
        val_life_exp_true = val_life_exp.values
        val_life_exp_pred = lasso_model.predict(val_df)
        val_rmse = sqrt(mean_squared_error(val_life_exp_true, val_life_exp_pred))
        lassoData.append({
            'l1_penalty': l1_lambdas[i],
            'model': lasso_model,
            'train_rmse': train_rmse,
            'val_rmse': val_rmse
        })
    lasso_data = pd.DataFrame(lassoData)
    index = lasso_data['val_rmse'].idxmin()
    best_model = lasso_data.loc[index]['model']
    best_l1 = lasso_data.loc[index]['l1_penalty']
    test_rmse = sqrt(mean_squared_error(test_life_exp.values, ridge_model.predict(test_df)))   # test_rmse
    print('L1 Penalty',  best_l1)
    print('Test RSME', test_rmse)
    print_coefficients(best_model, features)

  else:
    raise ValueError("Invalid model type. Choose 'ridge' or 'lasso'.")

  return best_model, scaler, test_rmse

def generate_feature_importance_graph(model, features, city_name = None):
    flag = False
    feature_importance = model.coef_
    # features = model.feature_names_in_
    # feats_coef_list = list(zip(features, feature_importance))

    # Create a bar chart of feature importance
    plt.figure(figsize=(5, 6))  # Adjust figure size as needed

    bar_width = 0.5  # Set the width of the bars

    bars = plt.bar(features, abs(feature_importance), width=bar_width, 
                  edgecolor=(0, 60/255, 48/255), linewidth=1)  # Pink border

    # Add a gradient color to the bars based on importance
    for bar, importance in zip(bars, feature_importance):
        # if importance < 0:
        #     bar.set_facecolor((0.2, 0, 1, abs(importance) / max(abs(feature_importance))))  # Red for negative values
        # else:
        bar.set_facecolor((0, 150/255, 150/255, abs(importance) / max(abs(feature_importance))))  # Blue for positive values

    plt.xlabel('Features')
    plt.ylabel('Importance')
    plt.title('Feature Importance for Life Expectancy Prediction')
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add grid lines to the background
    plt.ylim(top=1.4)
    plt.tight_layout()
    if (city_name != None):
        plt.savefig(f'Feature importance for {city_name}.png')  # Saves the figure to a file
    else:
        plt.savefig(f'Feature importance for all census tracts.png')  # Saves the figure to a file
    # plt.show()
    # plt.close()  # Close the figure to free up memory
    flag = True
    return flag

def generate_ct_life_exp_posi_in_city_distribution(df, geoid):
    """
    Shows a census tract's life expectancy performance in its city.

    Args:
        df: DataFrame containing census tract data, including 'FGEOID10', 'Life Expectancy', and 'City'.
        geoid: The FGEOID10 of the census tract to highlight.
    """
    try:
        # Find the census tract's data
        city_data = get_city_data_by_ct_geoid(df, geoid)
        tract_data = df[df['FGEOIDCT10'] == geoid]
        tract_life_expectancy = tract_data['Life Expectancy'].iloc[0]
        city_name = tract_data['City'].iloc[0]

        # Calculate cumulative distribution
        city_life_expectancy = city_data['Life Expectancy']
        city_life_expectancy_sorted = np.sort(city_life_expectancy)
        cumulative_percentages = np.arange(1, len(city_life_expectancy_sorted) + 1) / len(city_life_expectancy_sorted) * 100

        # Create the cumulative distribution plot
        plt.figure(figsize=(10, 6))
        plt.plot(city_life_expectancy_sorted, cumulative_percentages, marker='', linestyle='-', color=(0, 150/255, 150/255))
        plt.xlabel("Life Expectancy")
        plt.ylabel("Cumulative Percentage")
        plt.title(f"Life Expectancy Distribution in {city_name} (Census Tract {geoid})")
        plt.fill_between(city_life_expectancy_sorted, 0, cumulative_percentages, color=(0, 150/255, 150/255), alpha=0.2)  # Adjust alpha for transparency

        # Mark the position of the given census tract
        x = tract_life_expectancy
        y = round(np.interp(tract_life_expectancy, city_life_expectancy_sorted, cumulative_percentages), 1)
        annotation_text = f"({x} yrs, {y} %)"
        plt.axvline(x=x, color='purple', linestyle=':', label=f'Census Tract {geoid}', linewidth = 2)
        plt.axhline(y=y, color='purple', linestyle=':', linewidth = 2)
        plt.plot(x, y, 'o', markeredgecolor='purple', markerfacecolor='purple', markersize=5)  # 'ro' for red circle marker
        plt.annotate(annotation_text, (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontsize='x-large', color = "purple")
        plt.xlim(70, 86)

        plt.legend()
        plt.grid(axis='y')  # Add grid lines to the background
        plt.tight_layout()
        plt.show()

    except (KeyError, IndexError) as e:
        print(f"Error: {e}. Please ensure the DataFrame has the necessary columns.")

def generate_ct_ind_posi_in_all_distribution(df, geoid, feature):
    """
    Shows a census tract's life expectancy performance in its city.

    Args:
        df: DataFrame containing census tract data, including 'FGEOID10', 'Life Expectancy', and 'City'.
        geoid: The FGEOID10 of the census tract to highlight.
    """
    try:
        # Find the census tract's data
        ### city_data = get_city_data_by_ct_geoid(df, geoid)
        tract_data = df[df['FGEOIDCT10'] == geoid]
        tract_ind = tract_data[feature].iloc[0]

        # Calculate cumulative distribution
        df_ind = df[feature]
        df_ind_sorted = np.sort(df_ind)
        cumulative_percentages = np.arange(1, len(df_ind_sorted) + 1) / len(df_ind_sorted) * 100

        # Create the cumulative distribution plot
        plt.figure(figsize=(5, 3))
        plt.plot(df_ind_sorted, cumulative_percentages, marker='', linestyle='-', color=(0, 150/255, 150/255))
        plt.xlabel(feature)
        plt.ylabel("Cumulative Percentage")
        plt.title(f"{feature} Distribution for Census Tract {geoid}")
        plt.fill_between(df_ind_sorted, 0, cumulative_percentages, color=(0, 150/255, 150/255), alpha=0.2)  # Adjust alpha for transparency

        # Mark the position of the given census tract
        x = tract_ind
        y = round(np.interp(tract_ind, df_ind_sorted, cumulative_percentages), 1)
        annotation_text = f"({x} yrs, {y} %)"
        plt.axvline(x=x, color='purple', linestyle=':', label=f'Census Tract {geoid}', linewidth = 2)
        plt.axhline(y=y, color='purple', linestyle=':', linewidth = 2)
        plt.plot(x, y, 'o', markeredgecolor='purple', markerfacecolor='purple', markersize=5)  # 'ro' for red circle marker
        plt.annotate(annotation_text, (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontsize='x-large', color = "purple")
        # plt.xlim(70, 86)

        plt.legend()
        plt.grid(axis='y')  # Add grid lines to the background
        plt.tight_layout()
        plt.savefig(f'distribution_{feature}_{geoid}.png')
        plt.show()

    except (KeyError, IndexError) as e:
        print(f"Error: {e}. Please ensure the DataFrame has the necessary columns.")

def get_census_tract_inds_info(df, geoid, features):
    """
    Returns a map of the census tract's {indicator : [value, eval]}

    Args:
        df: DataFrame containing census tract data.
        geoid: The FGEOID10 of the census tract.
    """
    try:
        tract_data = df[df['FGEOIDCT10'] == geoid]
        tract_inds = {}
        if 'Ave Physical Activity' not in df.columns:
            df = df_feature_reverse_for_ml(df)
        for feature in features:
            value = tract_data[feature].iloc[0]
            all_ct_feature = df[feature]
            all_ct_feature_sorted = np.sort(all_ct_feature)
            cumulative_percentages = np.arange(1, len(all_ct_feature_sorted) + 1) / len(all_ct_feature_sorted) * 100
            eval = np.interp(value, all_ct_feature_sorted, cumulative_percentages)
            if (feature == 'Average Distance to Transit'):
                eval = round(100-eval, 1)
            else: eval = round(eval, 1)
            tract_inds[feature] = [value, eval]
        return tract_inds

    except (KeyError, IndexError) as e:
        print(f"Error: {e}. Please ensure the DataFrame has the necessary columns.")


# helper function: get_improved_features
def get_improved_features(df, geoid, features, feature_importance, improve_rate, bound):
    scaled_feature_importances = []
    for i in range(len(features)):
        scaled_feature_importances.append(round(feature_importance[i] * len(feature_importance) / sum(feature_importance), 2))
    improve_rates = []  # percentage
    for i in range(len(features)):
        improve_rates.append(improve_rate * scaled_feature_importances[i])

    improved_features = []
    cur_features_dict = get_census_tract_inds_info(df, geoid, features)
    for i in range(len(features)):
        cur_feature_eval = cur_features_dict[features[i]][1]
        if features[i] == 'Average Distance to Transit':
            improved_feature_eval = max(cur_feature_eval - improve_rates[i], bound[0])
        elif improve_rates[i] < 0:
            improved_feature_eval = max(cur_feature_eval + improve_rates[i], bound[0])
        else:
            improved_feature_eval = min(cur_feature_eval + improve_rates[i], bound[1])
        imrpoved_feature_value = np.percentile(df[features[i]], improved_feature_eval)
        improved_features.append(imrpoved_feature_value)
    return improved_features


# Get the recommended indicator values and performance for census tract
# input df is the cleaned df which include column 'FGEOIDCT10', 'Life Expectancy', 'life_exp_pred', and 8 features
def get_recommendations(df, geoid, features):
    if (geoid not in df['FGEOIDCT10'].values):
        print(f"Census tract with FGEOID10 '{geoid}' not enough data available.")
        return None
    feature_all = features.copy()
    feature_all.insert(0, 'Life Expectancy')
    cur_inds_info_dict = get_census_tract_inds_info(df, geoid, feature_all)
    # load model_default
    model_default, scaler = load_model('ridge_default')
    feature_importance_general = model_default.coef_
    # importance option 1:
    feature_importance = feature_importance_general
    # importance option 2:
    # feature_importance_city = model_city.coef_
    # feature_importance = (feature_importance_city + feature_importance_general) / 2
    
    # improve features:
    # performance improvement between: improve 3 years / be in first half / 30% --> choose the bigest one (the new life expectancy target value). 
    # change the factors based on importance

    # define target value:
    life_exp_pred = df[df['FGEOIDCT10'] == geoid]['life_exp_pred'].iloc[0]
    if (life_exp_pred > cur_inds_info_dict['Life Expectancy'][0] + 2):
        target_life_exp = min(life_exp_pred + 1, np.percentile(df['Life Expectancy'], 95))
    else:
        target_life_exp = max(
            cur_inds_info_dict['Life Expectancy'][0] + 3, 
            patched_df['Life Expectancy'].median(), 
            np.percentile(df['Life Expectancy'], min(cur_inds_info_dict['Life Expectancy'][1] + 30, 95)))
    # try different rate of getting improved features
    ### df[df['FGEOIDCT10'] == geoid][features]
    ct_data_for_predict = []
    for improve_rate in range(5, 41):
        improved_features = get_improved_features(df, geoid, features, feature_importance, improve_rate, [5, 95])
        ct_data_for_predict.append(improved_features)
    ct_df_for_predict = pd.DataFrame(ct_data_for_predict, columns = features)
    ct_df_for_predict_sc = scaler.transform(ct_df_for_predict)
    result_life_exp = model_default.predict(ct_df_for_predict_sc)
    result_life_exp_df = pd.DataFrame(result_life_exp, columns = ['life_exp_pred'])
    ct_df_for_predict = pd.DataFrame(ct_df_for_predict, columns = features)
    result_ct_df = pd.concat([ct_df_for_predict, result_life_exp_df], axis=1)
    # find the first result_life_exp that is larger than target_life_exp
    select_df_row = pd.DataFrame()
    print(select_df_row.shape)
    for i in range(result_ct_df.shape[0]):
        if result_life_exp_df['life_exp_pred'][i] >= target_life_exp :
            select_df_row = result_ct_df.iloc[i]
            break
    if select_df_row.shape[0] == 0:
        select_df_row = result_ct_df.iloc[result_ct_df.shape[0]-1]
    select_df_row['Life Expectancy'] = select_df_row['life_exp_pred']
    select_df_row['FGEOIDCT10'] = geoid
    select_df_row = select_df_row.to_frame()
    select_df_row = select_df_row.T
    select_df_row = select_df_row.astype({
        'Life Expectancy' : 'float64',
        'Ave Economic Diversity' : 'float64',
        'Ave Physical Activity' : 'float64',
        'Average Distance to Transit' : 'float64', 
        'Ave Road Network Density' : 'float64', 
        'Walkability Index' : 'float64', 
        'Ave Percent People With Health Insurance' : 'float64',
        'Ave Population Density' : 'float64', 
        'Ave Percent People Employed' : 'float64',
        'life_exp_pred' : 'float64'
    })
    select_df_row = select_df_row.round(2)
    # print("Select_df_row: ", select_df_row)
    df2 = df.drop(df[df['FGEOIDCT10'] == geoid].index)
    df2 = df2.reset_index(drop=True)
    df2 = pd.concat([df2, select_df_row], ignore_index=True)
    features.insert(0, 'Life Expectancy')
    improved_inds_info_dict = get_census_tract_inds_info(df2, geoid, features)
    return cur_inds_info_dict, improved_inds_info_dict

def generate_indicator_comparison_plot(cur, improved, geoid):
    """Plots a horizontal bar graph comparing current and improved indicator values."""

    indicators = list(cur.keys())
    cur_values = [cur[ind][1] for ind in indicators]
    improved_values = [improved[ind][1] for ind in indicators]

    x_pos = np.arange(len(indicators))

    fig, ax = plt.subplots(figsize=(4, 10))  # Adjust figure size as needed

    width = 0.2  # Width of each bar

    ax.barh(x_pos + width / 1.5, cur_values, height=width, label='Current', align='center', color = (0.6, 0.6, 1))
    ax.barh(x_pos - width / 1.5, improved_values, height=width, label='Improved', align='center', color = (0, 150/255, 150/255))

    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('lightgrey')
    ax.spines['right'].set_color('white')

    ax.set_yticks(x_pos)
    # ax.set_yticklabels(indicators)
    for i in range(len(indicators)):
        # ax.text(cur_values[i] + 2, x_pos[i] + width, indicators[i], va='center', fontsize='large')
        if i == 6:
            indicators[i] = 'Ave Per Health Insurance'
        ax.annotate(indicators[i], (0, x_pos[i] + width), textcoords="offset points", xytext=(0, 10), ha='left', fontsize='large', color = (0, 0, 100/255))
        ax.annotate('Current', (0, x_pos[i] + width/1.5), textcoords="offset points", xytext=(0, -2), ha='left', fontsize='small', color = (1,1,1))
        ax.annotate('Improved', (0, x_pos[i] - width/1.5), textcoords="offset points", xytext=(0, -2), ha='left', fontsize='small', color = (1,1,1))
        ax.annotate(f'{cur_values[i]}%', (cur_values[i], x_pos[i] + width/1.5), textcoords="offset points", xytext=(1, -2), ha='left', fontsize='small', color = (0.6, 0.5, 1))
        ax.annotate(f'{improved_values[i]}%', (improved_values[i], x_pos[i] - width/1.5), textcoords="offset points", xytext=(1, -2), ha='left', fontsize='small', color = (0,100/255,70/255))
    ax.set_xlabel(f"Indicator Ranking (Percentage) for CT: {geoid}", loc='left', color = 'lightgrey')
    ax.set_yticklabels([])
    ax.set_title("Comparison of Current and Improved\nIndicator performance (Ranking)", loc = 'left', ha='left', fontsize='x-large', pad=20, color = (0.1, 0.2, 0.8))
    ax.legend(loc='upper right', bbox_to_anchor=(1, 0.746))
    ax.set_xlim(0, 100)
    plt.tight_layout()
    plt.savefig(f'plot_indicator_performance_comparison_{geoid}.png')
    plt.show()



## example fewtures
# all_features = [
#     'FGEOIDCT10',
#     'Life Expectancy',
#     'Ave Economic Diversity',
#     'Ave Physical Activity',
#     'Average Distance to Transit', 
#     'Ave Road Network Density', 
#     'Walkability Index', 
#     'Ave Percent People With Health Insurance',
#     'Ave Population Density', 
#     'Ave Percent People Employed',
#     'life_exp_pred'
# ]
# features = all_features[2:10]
## example census tract GEOID: '04013082008'