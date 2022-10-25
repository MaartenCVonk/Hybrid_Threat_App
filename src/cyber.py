import streamlit as st
import numpy as np
import src.LP as model

def cyber():
    counter_hybrid_measures = ['counter hybrid by setting red lines', 'counter hybrid by resiliance',
                           'counter hybrid by collaboration','no counter hybrid measure']
    attack_measures = ['a hybrid attack', 'no hybrid attack']

    st.subheader("""Cyber Counter Hybrid Game""")
    st.write("""The goal of the cyber counter hybrid game is to deter the adversary from conducting a cyber attack.
     However, the resources for counter hybrid measures are not unlimited. Therefore 
    we would find out the counter hybrid measures that maximizes the total pay-off that includes possible consequences 
    of a hybrid attack under deep uncertainty and potential costs of the corresponding counter hybrid measure. 
    Please read the context of the scenario and the profiles of the deterrer and the adversary. Provide the input for
    the model accordingly. In order to prevent future attacks, we consider the following counter hybrid measures:
    """)
    st.markdown("""1) Invest in constituting a clear definition of kinetic cyber attacks. Set and communicate clear red lines to the 
    adversary. (counter hybrid by setting red lines)""")
    st.markdown("""2) Enhance resiliance by requiring companies and public entities operating in critical sectors to take adequate
     cybersecurity measures and to report to the competent authority within a short period of time of any 
     cyber incident or attack suffered. (counter hybrid by resiliance)""")
    st.markdown("""3) Along with partners, openly attribute the attack to the adversary. Leverage the membership of a supranational organisation 
    and push for collective attribution. Improve joint situational awareness through enhanced cooperation and information-sharing among countries.
    (counter hybrid by collaboration)""")
    st.markdown("""4) Decide to the nothing at all. (No counter hybrid)
            """)
    st.markdown("""For now we assume that each counter-hybrid measure is a deterrence measure to deter future attacks.
            """)
    st.subheader("""Counter Hybrid Measure Costs""")
    st.markdown("""Each of the counter-hybrid measures described above bring certain costs. These costs include the financial
    resources costs to enhance, update, audit and manage technical capabilities or costs of hiring qualified experts. However,
    the costs also include political capital for international support, costs for balancing open economic principles with security concerns,
    or costs due to the number of critical infrastructure parties to coordinate with. The only costs that are NOT included
    are costs that come with effectiveness of the counter hybrid measure. Please rate the counter hybrid measure costs on a scale from 0-100.
               """)
    gamma_1 = st.slider("What are my costs for {}?".format(counter_hybrid_measures[0]),0,100, value= 20, step=10)
    gamma_2 = st.slider("What are my costs for {}?".format(counter_hybrid_measures[1]),0,100, value= 30, step=10)
    gamma_3 = st.slider("What are my costs for {}?".format(counter_hybrid_measures[2]),0,100, value= 10, step=10)
    gamma_4 = st.slider("What are my costs for {}?".format(counter_hybrid_measures[3]),0,100, value= 0, step=10)
    st.write("The costs for the counter hybrid measures are {}, {}, {} and {} respectively.".format(gamma_1, gamma_2, gamma_3, gamma_4))

    st.subheader("""Possible Pay-offs""")
    st.write("""Later we will evaluate what the probabilities are for potential pay-off values. But first we will define
    the potential pay-off. When the adversary decides to conducts a hybrid attack (or not) despite (because of) counter hybrid efforts,
    there are three possibilities for pay-offs. Please, rate on a 
    scale from -100-100 the advantage the adversary could gain relative to the losses of the deterring agent (zero-sum-game)""")
    st.markdown("""Positive values correspond to a gain of the adversary compared to the loss of the deterring agent (e.g. when despite
    deterring efforts the hybrid conduct is very effective, this value is highly positive)""")
    st.markdown("""Contrary, negative values correspond to a gain of the deterring agent compared to the loss of the adversary agent 
    (when the hybrid conduct was not very effective, but the deterring agent was able to rally many allies to collaborate with
    , this value can be negative)""")

    st.write("""_Reasoning default: When the adversary managed to exploit vulnerabilities that the deterring agent is not
    aware off, the pay-off is very bad (70). A hybrid attack can also be effective while still being detected (35). 
    When the hybrid effort is not effective at all, the pay-off is 0._
     """)

    st.markdown("""When constructing potential pay-off, please relativize them to the counter hybrid costs previously determined""")
    theta_1 = st.slider("What is the first possible pay-off?",-100,100, value= 70, step= 5)
    theta_2 = st.slider("What is the second possible pay-off?",-100,100, value= 35, step= 5)
    theta_3 = st.slider("What is the third possible pay-off?",-100,100, value= 0, step= 5)

    st.subheader("""Conditional Probabilities for Pay-offs""")
    st.write("""Hybrid conducts entail many uncertain elements. A failure of detection of the hybrid conduct can result
     in disastrous effects by letting the adversary commit in deep reconnaissance activities without being aware. Similarly,
     a failure in attribution can result in a lack of success in gaining enough political support to take effective counter-measures.
     Because the nature of a hybrid conduct is to remain under the threshold for detection and attribution and one can never
     be 100% certain that we detect or attribute correctly, the possible outcomes should be modeled probabilistically.
    """)
    st.write("""For each possible combination of counter-hybrid measure and hybrid conduct we assign probability values to
    the earlier defined pay-off options. Note that a probability of 20% means unlikely while 100% means certain.
    Please be aware that the total probability of EVERY combination should sum to 100%.  
    """)

    st.write("""_Reasoning default: setting red lines is only effective in deterring, but you are almost as vulnerable as
    doing nothing. However, exploring red lines might help detection of vulnerabilities. Conclusion 50% worst pay-off and 50% bad pay-off._
    """)

    w111 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
                     .format(theta_1, counter_hybrid_measures[0],attack_measures[0] ), 0,100, 50, step=10)
    w112 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
                     .format(theta_2, counter_hybrid_measures[0],attack_measures[0] ), 0,100, 50,  step=10)
    w113 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
                     .format(theta_3, counter_hybrid_measures[0],attack_measures[0] ), 0,100, 0, step=10)

    st.write("Probability of each of the pay-off values when deterrer commits to {} and attacker conducts {}. Pay-offs should sum up to 100%.".format(counter_hybrid_measures[1],attack_measures[0]))

    st.write("""_Reasoning default: enhancing resiliance might be very costly, but it very effective when being attacked.
    It would be considerably harder to exploit vulnerabilities with a counter hybrid measure because of the high defense,
    but it can still happen._
    """)

    w211 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
                     .format(theta_1, counter_hybrid_measures[1],attack_measures[0] ), 0,100, 10, step=10)
    w212 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
                     .format(theta_2, counter_hybrid_measures[1],attack_measures[0] ), 0,100, 20, step=10)
    w213 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
                     .format(theta_3, counter_hybrid_measures[1],attack_measures[0] ), 0,100, 70, step=10)

    st.write("Probability of each of the pay-off values when deterrer commits to {} and attacker conducts {}. Pay-offs should sum up to 100%.".format(counter_hybrid_measures[2],attack_measures[0]))

    st.write("""_Reasoning default: collaborating with international stakeholders mainly helps with deterring because when
    conducting a hybrid attack, the adversary gets more isolated. Also, sharing information and collaborating can help reducing
    the most exploitable vulnerabilities substantially and allies will alert me if this happens._
    """)

    w311 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
                     .format(theta_1, counter_hybrid_measures[2],attack_measures[0] ), 0,100, 30, step=10)
    w312 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
                     .format(theta_2, counter_hybrid_measures[2],attack_measures[0] ), 0,100, 70, step=10)
    w313 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
                     .format(theta_3, counter_hybrid_measures[2],attack_measures[0] ), 0,100, 0, step=10)

    st.write("Probability of each of the pay-off values when deterrer commits to {} and attacker conducts {}. Pay-offs should sum up to 100%.".format(counter_hybrid_measures[3],attack_measures[0]))

    st.write("""_Doing nothing at all is free of costs. However, it opens the door to free exploitation of vulnerabilities 
    by the adversary._
    """)

    w411 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
                     .format(theta_1, counter_hybrid_measures[3],attack_measures[0] ), 0,100, 80, step=10)
    w412 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
                     .format(theta_2, counter_hybrid_measures[3],attack_measures[0] ), 0,100, 20, step=10)
    w413 = st.slider("What is the likelihood of pay-off loss  {} when deterrer commits to {} and attacker conducts {}?"
                     .format(theta_3, counter_hybrid_measures[3],attack_measures[0] ), 0,100, 0, step=10)

    # st.write("Probability of each of the pay-off values when deterrer commits to {} and attacker conducts {}. Pay-offs should sum up to 100%.".format(counter_hybrid_measures[0],attack_measures[1]))
    #
    # w121 = st.slider("What is the likelihood of pay-off loss{} when deterrer commits to {} and attacker conducts {}?"
    #                  .format(theta_1, counter_hybrid_measures[0],attack_measures[1] ), 0,100, 0, step=10)
    # w122 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
    #                  .format(theta_2, counter_hybrid_measures[0],attack_measures[1] ), 0,100, 0, step=10)
    # w123 = st.slider("What is the likelihood of pay-off loss  {} when deterrer commits to {} and attacker conducts {}?"
    #                  .format(theta_3, counter_hybrid_measures[0],attack_measures[1] ), 0,100, 100, step=10)
    #
    # st.write("Probability of each of the pay-off values when deterrer commits to {} and attacker conducts {}. Pay-offs should sum up to 100%.".format(counter_hybrid_measures[1],attack_measures[1]))
    #
    # w221 = st.slider("What is the likelihood of pay-off loss{} when deterrer commits to {} and attacker conducts {}?"
    #                  .format(theta_1, counter_hybrid_measures[1],attack_measures[1] ), 0,100, 0, step=10)
    # w222 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
    #                  .format(theta_2, counter_hybrid_measures[1],attack_measures[1] ), 0,100, 0, step=10)
    # w223 = st.slider("What is the likelihood of pay-off loss  {} when deterrer commits to {} and attacker conducts {}?"
    #                  .format(theta_3, counter_hybrid_measures[1],attack_measures[1] ), 0,100, 100, step=10)
    #
    # st.write("Probability of each of the pay-off values when deterrer commits to {} and attacker conducts {}. Pay-offs should sum up to 100%.".format(counter_hybrid_measures[2],attack_measures[1]))
    #
    # w321 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
    #                  .format(theta_1, counter_hybrid_measures[2],attack_measures[1] ), 0,100, 0, step=10)
    # w322 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
    #                  .format(theta_2, counter_hybrid_measures[2],attack_measures[1] ), 0,100, 0, step=10)
    # w323 = st.slider("What is the likelihood of pay-off loss  {} when deterrer commits to {} and attacker conducts {}?"
    #                  .format(theta_3, counter_hybrid_measures[2],attack_measures[1] ), 0,100, 100, step=10)
    #
    # st.write("Probability of each of the pay-off values when deterrer commits to {} and attacker conducts {}. Pay-offs should sum up to 100%.".format(counter_hybrid_measures[3],attack_measures[1]))
    #
    # w421 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
    #                  .format(theta_1, counter_hybrid_measures[3],attack_measures[1] ), 0,100, 0, step=10)
    # w422 = st.slider("What is the likelihood of pay-off loss {} when deterrer commits to {} and attacker conducts {}?"
    #                  .format(theta_2, counter_hybrid_measures[3],attack_measures[1] ), 0,100, 0, step=10)
    # w423 = st.slider("What is the likelihood of pay-off loss  {} when deterrer commits to {} and attacker conducts {}?"
    #                  .format(theta_3, counter_hybrid_measures[3],attack_measures[1] ), 0,100, 100, step=10)

    st.subheader("""Probability of succeeding in deterring""")
    st.write("""_For each of the counter hybrid measure taken, we should assess its effectiveness in terms of its successfulness
             in deterring the next attack. Therefore we make an assessment of the likelihood of a hybrid attack based
             on each of the counter-hybrid measures._""")
    st.write("Probability of effectiveness in counter hybrid measure in countering a hybrid attack.")

    a_1 = st.slider("How effective is {}".format(counter_hybrid_measures[0]), 0,100, 60, step = 10)*0.01
    a_2 = st.slider("How effective is {}".format(counter_hybrid_measures[1]), 0,100, 20, step = 10)*0.01
    a_3 = st.slider("How effective is {}".format(counter_hybrid_measures[2]), 0,100, 30, step = 10)*0.01
    a_4 = st.slider("How effective is {}".format(counter_hybrid_measures[3]), 0,100, 10, step = 10)*0.01


    # Boundary Conditions:
    theta = np.array([-theta_1,-theta_2,-theta_3, 0, 0]) #Pay_off rewards
    pay_off = np.array([[[w111, w112, w113, 0, 0], [w211, w212, w213, 0, 0], [w311, w312, w313, 0, 0], [w411, w412, w413, 0, 0]],
      #                  [[w121, w122, w123, 0, 0], [w221, w222, w223, 0, 0], [w321, w322, w323, 0, 0], [w421, w422, w423, 0, 0]]])*0.01
                         [[0, 0, 100, 0, 0], [0, 0, 100, 0, 0], [0, 0, 100, 0, 0],  [0, 0, 100, 0, 0]]])*0.01  # Pay_off probabilities
    gamma = np.array([-gamma_1,-gamma_2 ,-gamma_3,-gamma_4]) # Deterrence cost gamma_1, gamma_2, gamma_3, gamma_4
    alpha1 = np.array([[1-a_1,1-a_2,1-a_3,1-a_4],[a_1,a_2,a_3,a_4]])#deterrer thinks d_1 det by punishment is effective
    H = np.array([2.5,0]) # The Attack cost eta_1, eta_2


    st.header("""Optimal Solution""")

    LP_instance = model.LP(pay_off=theta, pay_off_matrix=pay_off, det_costs=gamma, att_costs=H, det_strat=None, att_strat=alpha1)
    variables, objective = LP_instance.deterrence_LP()

    st.write()

    for i, variable in enumerate(variables):
        if variable.varValue>0:
            st.write("The optimal solution is to conduct **{}** with optimal solution {}. ".format(counter_hybrid_measures[i], round(objective,2)))
