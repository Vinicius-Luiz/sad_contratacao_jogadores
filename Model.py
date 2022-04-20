import pandas as pd

def df():
    return pd.read_csv('data\data_input.csv', low_memory=False)