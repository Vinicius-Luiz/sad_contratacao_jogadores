import pandas as pd

def df_input():
    df = pd.read_csv('data\data_input.csv', low_memory=False)
    df['value_eur'] = df['value_eur']//100
    df['wage_eur'] = df['wage_eur']//100
    df['release_clause_eur'] = df['release_clause_eur']//100
    return df

def df_output():
    return pd.read_csv('data\data_output.csv', low_memory=False)