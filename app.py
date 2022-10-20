import numpy as np
import streamlit as st
import src.LP as model
import src.cyber as cyber
import src.information as information

st.title('Hybrid Threat Simulator')

st.markdown(""" 
This simulator calculates the optimal strategy to deter the adversary from conducting a hybrid attack under deep
uncertainty. The user will be asked to express certain uncertainty levels and boundary conditions. 
There are two different scenarios: the cyber and the information hybrid threat.
Please choose a game on the left-hand side.
""")
page = st.sidebar.selectbox('Select Game',['Cyber Counter-Hybrid Game','Information Counter-Hybrid Game'])

if page == 'Cyber Counter-Hybrid Game':
    cyber.cyber()
else:
    information.information()