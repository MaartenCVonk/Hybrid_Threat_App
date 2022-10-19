import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import math
import requests
from IPython.core.pylabtools import figsize
import matplotlib.pyplot as plt
import scipy.stats as stats
import requests

def load_data():
    # Get Uncomtrade data
    url = 'https://comtrade.un.org/api/get/plus?max=50000&type=C&freq=A&px=HS&ps=2017%2C2018%2C2019%2C2020%2C2016&r=643&p=all&rg=1%2C2&cc=27'
    un_data = requests.get(url)
    result = pd.json_normalize(un_data.json(), "dataset")
    return result

raw_data = load_data()
data = data = raw_data[(raw_data['cstDesc']=='TOTAL CPC')& (raw_data['motDesc']=='TOTAL MOT')&(raw_data['pt3ISO']!='W00')&(raw_data['pt3ISO2']=='W00')]
unique_countries = np.array(sorted(data['pt3ISO'].unique()))
selected_countries = ['NLD', 'ESP', 'DEU', 'GBR', 'PRT', 'BEL', 'FRA', 'IRL']


#Filtering Data
df = data[data['pt3ISO']=="NLD"].sort_values(by=['yr'])
print(df)
df2 = df.groupby(['rt3ISO','rgDesc'], as_index=False).agg(lambda x: list(x))['TradeValue'].apply(lambda x: pd.Series(x)).transpose()
df2['year'] = df['yr'].unique()
df2.set_index('year', inplace=True)
df2.columns = ['Russian Import', 'Russian Export']
print(df2)