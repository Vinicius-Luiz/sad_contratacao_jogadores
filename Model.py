import pandas as pd

def df_input():
    return pd.read_csv('data\data_input.csv', low_memory=False)

def df_output():
    return pd.read_csv('data\data_output.csv', low_memory=False)