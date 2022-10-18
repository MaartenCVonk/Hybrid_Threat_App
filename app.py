import numpy as np
import pandas as pd
import streamlit as st
import requests
from pulp import *

st.title('Hybrid Threat Monitor')

st.markdown("""
This app calculates the optimal strategy based on boundary conditions and a probability assessment of the adversary
* **Python libraries:** base64, pandas, streamlit, numpy, Pulp
* **Data source:** (None).
Todo:
* Cleaner function for sourcing data (API)
""")


def extract_data_API():
    params = {'cc':'27', 'freq':'A', 'px':'HS', 'r':'643' ,'p':'all', 'type':'C',
              'ps': ','.join(['2016','2017','2018','2019','2020']), 'rg': ','.join(['1','2']) }
    url = 'http://comtrade.un.org/api/get?parameters'
    url = 'https://comtrade.un.org/api/get/plus?'
    un_data = requests.get(url, params=params)
    result = pd.json_normalize(un_data.json(), "dataset")
    return result


# Extract API
raw_data = extract_data_API()
data = data = raw_data[(raw_data['cstDesc']=='TOTAL CPC')& (raw_data['motDesc']=='TOTAL MOT')&(raw_data['pt3ISO']!='W00')&(raw_data['pt3ISO2']=='W00')]

#
#Sidebar Country
unique_countries = np.array(sorted(data['pt3ISO'].unique()))
print(unique_countries)
selected_countries = ['NLD', 'ESP', 'DEU', 'GBR', 'PRT', 'BEL', 'FRA', 'IRL']
country = st.sidebar.selectbox('Countries', selected_countries)

# Transform data based on country
df = data[data['pt3ISO']==country].sort_values(by=['yr'])
df2 = df.groupby(['rt3ISO','rgDesc'], as_index=False).agg(lambda x: list(x))['TradeValue'].apply(lambda x: pd.Series(x)).transpose()
df2['year'] = df['yr'].unique()
df2.set_index('year', inplace=True)
df2.columns = ['Russian Import', 'Russian Export']


st.write("""## Russian Trade Exports to """, country)
st.subheader("""Mineral fuels, mineral oils and products of their distillation; bituminous substances; mineral waxes""")
st.bar_chart(df2)

deterrence_measures = ['deterrence by punishment', 'deterrence by threat', 'deterrence by denial','no deterrence measure']
attack_measures = ['hybrid attack', 'no hybrid attack']

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

class LP:
    """
    Class function to run the LP for deterrence and defender an spit out the results
    Attributes:
    -  Calculate Optimal Strategy for Deterrer
    -  Calculate Optimal Strategy for Attacker
    """

    def __init__(self, pay_off, pay_off_matrix, det_costs, att_costs, det_strat=None, att_strat=None):
        """
        Initiate data and logger and validates input
        :data (pd.Dataframe) : to be converted data
        """
            # Create logger
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
        logging.basicConfig(format=log_format, level=logging.INFO, stream=sys.stdout)
        logger = logging.getLogger()
        self.pay_off, self.pay_off_matrix, self.det_costs, self.att_costs = pay_off, pay_off_matrix, det_costs, att_costs
        self.det_strat= det_strat if det_strat is not None else None
        self.att_strat= att_strat if att_strat is not None else None
        self.logger = logging.getLogger(__name__)

        if self.att_strat is not None:
          if not np.array_equal(np.sum(self.att_strat, axis=0) ,np.ones(len(self.att_strat[0]))):
             raise ValueError("Probabilities Attack Strategy should sum up to one")
        if self.det_strat is not None:
          if not round(np.sum(self.det_strat, axis=0),4) == 1:
              raise ValueError("Probabilities Det Strategy should sum up to one")
        if not np.array_equal(np.sum(self.pay_off_matrix, axis=2) ,np.ones([pay_off_matrix.shape[0],self.pay_off_matrix.shape[1]])):
            raise ValueError("Probabilities Pay-off should sum up to one")

    def deterrence_LP(self):
        """
        This solves all the LP steps, prints the problem status and returns the variable results
        """
        strat = {}
        for x in range(4):
          strat[x]= LpVariable(f"d[{x+1}]", lowBound=0, upBound=1, cat="Continuous")
        prob = LpProblem("Max pay-off", LpMaximize)
        # Creates the objective function
        prob.setObjective(sum(self.pay_off[y] * self.att_strat[t,x]*self.pay_off_matrix[t,x,y]*strat[x] for y in range(0,len(self.pay_off_matrix[0,0]))
                                                                          for t in range(0,len(self.att_strat))
                                                                          for x in range(4))
                          +sum(self.det_costs[x]*strat[x]                 for x in range(4)))
        prob += lpSum([strat[i]  for i in range(len(strat))]) <= 1
        prob += lpSum([strat[i]  for i in range(len(strat))]) >= 1
        # Solve ILP
        prob.solve()
        #print(LpStatus[prob.status])
        self.variables = prob.variables()
        return self.variables, value(prob.objective)

    def attack_LP(self):
        """
        This solves all the LP steps, prints the problem status and returns the variable results
        """
        alp = {}
        for i in range(2):
           alp[i]= LpVariable(f"a[{i+1}]", lowBound=0, upBound=1, cat="Binary")
        prob = LpProblem("Min pay-off", LpMinimize)
        # Creates the objective function
        prob.setObjective(sum(self.pay_off[y]* alp[i]*self.pay_off_matrix[i,j,y]*self.det_strat[j] for y in range(0,len(self.pay_off_matrix[0,0]))
                                                                          for i in range(2)
                                                                          for j in range(4))
        +                 sum(alp[i]*self.att_costs[i]                    for i in range(2)  ))
        prob += lpSum([alp[i] for i in range(2)]) <= 1
        prob += lpSum([alp[i]  for i in range(2)]) >= 1
        # Solve ILP
        prob.solve()
        #print(LpStatus[prob.status])
        self.variables = prob.variables()
        return self.variables, value(prob.objective)
st.subheader("""Boundary Conditions""")
st.subheader("""Counter Hybrid Measure Costs""")

gamma_1 = st.slider("What are my costs for {}?".format(deterrence_measures[0]),0,1000, value= 100, step=10)  #TODO modify when deterrence measure is determined,
gamma_2 = st.slider("What are my costs for {}?".format(deterrence_measures[1]),0,1000, value= 40, step=10)  #TODO modify when deterrence measure is determined,
gamma_3 = st.slider("What are my costs for {}?".format(deterrence_measures[2]),0,1000, value= 150, step=10)  #TODO modify when deterrence measure is determined,
gamma_4 = st.slider("What are my costs for {}?".format(deterrence_measures[3]),0,1000, value= 0, step=10)  #TODO modify when deterrence measure is determined,
st.write("The costs for the deterrence measures are {}, {}, {} and {} respectively.".format(gamma_1, gamma_2, gamma_3, gamma_4))

st.subheader("""Possible Pay-offs""")
st.write("""Possible Pay-offs are the pay-off the adversary gains when committing a hybrid threat relative to what the defender loses. 
            When it is negative, the pay-off is in favor of the adversary. When it is positive, it is in favor of the deterrer.""")
theta_1 = st.slider("What is the first possible pay-off?",-1000,1000, value= -400, step= 20)  #TODO modify when deterrence measure is determined,
theta_2 = st.slider("What is the second possible pay-off?",-1000,1000, value= -200, step= 20)  #TODO modify when deterrence measure is determined,
theta_3 = st.slider("What is the third possible pay-off?",-1000,1000, value= 0, step= 20)  #TODO modify when deterrence measure is determined,

st.subheader("""Conditional Probabilities for Pay-offs""")
st.write("Probability of each of the pay-off values when deterrer commits to {} and attacker conducts a {}. Pay-offs should sum up to 100%.".format(deterrence_measures[0],attack_measures[0]))

w111 = st.slider("What is the likelihood of pay-off {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_1, deterrence_measures[0],attack_measures[0] ), 0,100, 50, step=10)
w112 = st.slider("What is the likelihood of pay-off  {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_2, deterrence_measures[0],attack_measures[0] ), 0,100, 0,  step=10)
w113 = st.slider("What is the likelihood of pay-off   {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_3, deterrence_measures[0],attack_measures[0] ), 0,100, 50, step=10)

st.write("Probability of each of the pay-off values when deterrer commits to {} and attacker conducts a {}. Pay-offs should sum up to 100%.".format(deterrence_measures[1],attack_measures[0]))

w211 = st.slider("What is the likelihood of pay-off {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_1, deterrence_measures[1],attack_measures[0] ), 0,100, 50, step=10)
w212 = st.slider("What is the likelihood of pay-off  {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_2, deterrence_measures[1],attack_measures[0] ), 0,100, 50, step=10)
w213 = st.slider("What is the likelihood of pay-off   {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_3, deterrence_measures[1],attack_measures[0] ), 0,100, 0, step=10)

st.write("Probability of each of the pay-off values when deterrer commits to {} and attacker conducts a {}. Pay-offs should sum up to 100%.".format(deterrence_measures[2],attack_measures[0]))

w311 = st.slider("What is the likelihood of pay-off {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_1, deterrence_measures[2],attack_measures[0] ), 0,100, 0, step=10)
w312 = st.slider("What is the likelihood of pay-off  {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_2, deterrence_measures[2],attack_measures[0] ), 0,100, 20, step=10)
w313 = st.slider("What is the likelihood of pay-off   {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_3, deterrence_measures[2],attack_measures[0] ), 0,100, 80, step=10)

st.write("Probability of each of the pay-off values when deterrer commits to {} and attacker conducts a {}. Pay-offs should sum up to 100%.".format(deterrence_measures[3],attack_measures[0]))

w411 = st.slider("What is the likelihood of pay-off {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_1, deterrence_measures[3],attack_measures[0] ), 0,100, 80, step=10)
w412 = st.slider("What is the likelihood of pay-off  {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_2, deterrence_measures[3],attack_measures[0] ), 0,100, 20, step=10)
w413 = st.slider("What is the likelihood of pay-off   {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_3, deterrence_measures[3],attack_measures[0] ), 0,100, 0, step=10)

st.write("Probability of each of the pay-off values when deterrer commits to {} and attacker conducts a {}. Pay-offs should sum up to 100%.".format(deterrence_measures[0],attack_measures[1]))

w121 = st.slider("What is the likelihood of pay-off {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_1, deterrence_measures[0],attack_measures[1] ), 0,100, 0, step=10)
w122 = st.slider("What is the likelihood of pay-off  {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_2, deterrence_measures[0],attack_measures[1] ), 0,100, 0, step=10)
w123 = st.slider("What is the likelihood of pay-off   {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_3, deterrence_measures[0],attack_measures[1] ), 0,100, 100, step=10)

st.write("Probability of each of the pay-off values when deterrer commits to {} and attacker conducts a {}. Pay-offs should sum up to 100%.".format(deterrence_measures[1],attack_measures[1]))

w221 = st.slider("What is the likelihood of pay-off {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_1, deterrence_measures[1],attack_measures[1] ), 0,100, 0, step=10)
w222 = st.slider("What is the likelihood of pay-off  {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_2, deterrence_measures[1],attack_measures[1] ), 0,100, 0, step=10)
w223 = st.slider("What is the likelihood of pay-off   {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_3, deterrence_measures[1],attack_measures[1] ), 0,100, 100, step=10)

st.write("Probability of each of the pay-off values when deterrer commits to {} and attacker conducts a {}. Pay-offs should sum up to 100%.".format(deterrence_measures[2],attack_measures[1]))

w321 = st.slider("What is the likelihood of pay-off {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_1, deterrence_measures[2],attack_measures[1] ), 0,100, 0, step=10)
w322 = st.slider("What is the likelihood of pay-off  {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_2, deterrence_measures[2],attack_measures[1] ), 0,100, 0, step=10)
w323 = st.slider("What is the likelihood of pay-off   {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_3, deterrence_measures[2],attack_measures[1] ), 0,100, 100, step=10)

st.write("Probability of each of the pay-off values when deterrer commits to {} and attacker conducts a {}. Pay-offs should sum up to 100%.".format(deterrence_measures[3],attack_measures[1]))

w421 = st.slider("What is the likelihood of pay-off {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_1, deterrence_measures[3],attack_measures[1] ), 0,100, 0, step=10)
w422 = st.slider("What is the likelihood of pay-off  {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_2, deterrence_measures[3],attack_measures[1] ), 0,100, 0, step=10)
w423 = st.slider("What is the likelihood of pay-off   {} when deterrer commits to {} and attacker conducts a {}?"
                 .format(theta_3, deterrence_measures[3],attack_measures[1] ), 0,100, 100, step=10)




st.subheader("""Probability of succeeding in deterring""")
st.write("Probability of effectiveness in deterrence measure in deterring a hybrid attack.")

a_1 = st.slider("How Effective is {}".format(deterrence_measures[0]), 0,100, 70, step = 10)*0.01
a_2 = st.slider("How Effective is {}".format(deterrence_measures[1]), 0,100, 60, step = 10)*0.01
a_3 = st.slider("How Effective is {}".format(deterrence_measures[2]), 0,100, 70, step = 10)*0.01
a_4 = st.slider("How Effective is {}".format(deterrence_measures[3]), 0,100, 60, step = 10)*0.01


# Boundary Conditions:
theta = np.array([theta_1,theta_2,theta_3, 0, 0]) #Pay_off rewards
pay_off = np.array([[[w111, w112, w113, 0, 0], [w211, w212, w213, 0, 0], [w311, w312, w313, 0, 0], [w411, w412, w413, 0, 0]],
                    [[w121, w122, w123, 0, 0], [w221, w222, w223, 0, 0], [w321, w322, w323, 0, 0], [w421, w422, w423, 0, 0]]])*0.01 #Pay_off probabilities

gamma = np.array([-gamma_1,-gamma_2 ,-gamma_3,-gamma_4]) # Deterrence cost gamma_1, gamma_2, gamma_3, gamma_4
alpha1 = np.array([[1-a_1,1-a_2,1-a_3,1-a_4],[a_1,a_2,a_3,a_4]])#deterrer thinks d_1 det by punishment is effective
H = np.array([2.5,0]) # The Attack cost eta_1, eta_2


st.header("""Optimal Solution""")

LP_instance = LP(pay_off=theta, pay_off_matrix=pay_off, det_costs=gamma, att_costs=H, det_strat=None, att_strat=alpha1)
variables, objective = LP_instance.deterrence_LP()

for variable in variables:
    st.write("Counter hybrid Measure",variable.name, round(variable.varValue,2))
st.write("Optimal Solution", objective)