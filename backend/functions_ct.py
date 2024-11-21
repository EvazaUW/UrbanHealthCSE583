import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_white"
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from math import sqrt

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



def print_coefficients(model, features):
    """
    This function takes in a model column and a features column. 
    And prints the coefficient along with its feature name.
    """
    feats = list(zip(features, model.coef_))
    print(*feats, sep = "\n")

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
    test_rmse_ridge = sqrt(mean_squared_error(test_life_exp.values, ridge_model.predict(test_df)))   # test_rmse_ridge
    print('L2 Penalty',  best_l2)
    print('Test RSME', test_rmse_ridge)
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
    best_l1 = ridge_data.loc[index]['l1_penalty']
    test_rmse_ridge = sqrt(mean_squared_error(test_life_exp.values, ridge_model.predict(test_df)))   # test_rmse_ridge
    print('L1 Penalty',  best_l1)
    print('Test RSME', test_rmse_ridge)
    print_coefficients(best_model, features)

  else:
    raise ValueError("Invalid model type. Choose 'ridge' or 'lasso'.")

  return best_model, scaler

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
    # if (city_name != None):
    #     plt.savefig(f'Feature importance for {city_name}.png')  # Saves the figure to a file
    # else:
    #     plt.savefig(f'Feature importance for all census tracts.png')  # Saves the figure to a file
    plt.show()
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

# all_features = [
#     'Life Expectancy',
#     'Ave Economic Diversity',
#     'Ave Physical Activity',
#     'Average Distance to Transit', 
#     'Ave Road Network Density', 
#     'Walkability Index', 
#     'Ave Percent People With Health Insurance', 
#     'Ave Population Density', 
#     'Ave Percent People Employed']

