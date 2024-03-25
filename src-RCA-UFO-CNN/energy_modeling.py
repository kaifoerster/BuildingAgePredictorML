import os
import logging

from sklearn import metrics
import numpy as np
import pandas as pd

import dataset

logger = logging.getLogger(__name__)


def calculate_energy_error(y_true, y_predict, labels=None):
    y_true = assign_heating_energy_demand(y_true, labels)
    y_predict = assign_heating_energy_demand(y_predict, labels)

    #logger.info(f"Columns in y_true: {y_true.columns}")
    #logger.info(f"Columns in y_predict: {y_predict.columns}")

    ids = y_true.index.intersection(y_predict.index)
    y_true = y_true.loc[ids]
    y_predict = y_predict.loc[ids]

    r2 = metrics.r2_score(y_true['heating_demand'], y_predict['heating_demand'])
    mape = metrics.mean_absolute_percentage_error(y_true['heating_demand'], y_predict['heating_demand'])
    mae = metrics.mean_absolute_error(y_true['heating_demand'], y_predict['heating_demand'])
    rmse = np.sqrt(metrics.mean_squared_error(y_true['heating_demand'], y_predict['heating_demand']))

    logger.info(f'Energy need for heating in kWh/(m²a) R2: {r2:.4f}')
    logger.info(f'Energy need for heating in kWh/(m²a) MAPE: {mape:.4f}')
    logger.info(f'Energy need for heating in kWh/(m²a) MAE: {mae:.2f}')
    logger.info(f'Energy need for heating in kWh/(m²a) RMSE: {rmse:.2f}')

    return r2, mape


def assign_heating_energy_demand(df, labels=None):
    tabula_energy_path = os.path.join(dataset.METADATA_DIR, 'TABULA_heating_demand.csv')
    tabula_energy_df = pd.read_csv(tabula_energy_path)
    countries = tabula_energy_df['country'].unique()

    column_names = df.columns
    # print(column_names)
    if 'country_label' in column_names:
        df.rename(columns={'country_label': 'country'}, inplace=True)
    if 'residential_type_label' in column_names:
        df.rename(columns={'residential_type_label': 'residential_type'}, inplace=True)   


    df = df.dropna(subset=['country', 'residential_type'])
    # Replace all country names in df that are not in countries with 'Europe'
    df['country'] = df['country'].apply(lambda x: 'Europe' if x not in countries else x)

    n_buildings = len(df)
    index = df.index
    

    if labels:
        # matching on existing age bins (classification)
        class_to_label = dict(enumerate(labels))
        df['age_bin'] = df['age'].map(class_to_label)
        df = pd.merge(df, tabula_energy_df,  how='left', on=['country', 'residential_type', 'age_bin']).set_index('Unnamed: 0', drop=False)
    else:
        # binning continuous age (regression)
        df = pd.merge(df, tabula_energy_df,  how='left', on=['country', 'residential_type']).set_index('Unnamed: 0', drop=False)
        df[f'{dataset.AGE_ATTRIBUTE}'] = pd.to_numeric(df[f'{dataset.AGE_ATTRIBUTE}'], errors='coerce').fillna(0).astype('int64')
        #df = df[df[f'{dataset.AGE_ATTRIBUTE}'] == 0]
        df['age_min'] = df['age_min'].astype('int64')
        df['age_max'] = df['age_max'].astype('int64')
        df = df.query(f'age_min <= {dataset.AGE_ATTRIBUTE} < age_max')
        
    df = df.drop_duplicates(subset='Unnamed: 0', keep='last')
    if n_buildings != len(df):
        logger.error(f'Assigning heating energy demand failed. Number of building changed during merge of TABULA data from {n_buildings} to {len(df)}. Dropped buildings include:\n{list(index.difference(df.index))[:10]}')

    return df
