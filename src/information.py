import streamlit as st
import numpy as np
import src.LP as model


def information():
    counter_hybrid_measures = ['Threatening with Political Attribution', 'Media Restrictions',
                               'Boosting Cyber Resilience at the Wider Societal Level', 'Proactive Resilience',
                               'Open Deterrence Messaging']
    attack_measures = ['a hybrid attack', 'no hybrid attack']

    st.subheader("""Cyber Counter Hybrid Game""")
    st.write("""The goal of the cyber counter hybrid game is to deter the adversary from foreign election meddling.
    However, the resources for counter hybrid measures are not unlimited. Therefore 
    we would like to find out the counter hybrid measures that optimize the total pay-off. This pay-off includes possible 
    consequences of a hybrid attack under uncertainty and potential costs of the corresponding counter hybrid measure. 
    In order to prevent future attacks, we consider the following deterrence measures:
    """)
    st.markdown("""1) Threatening with Political Attribution: threaten to attribute publicly and collectively. This is intended to exert
    international pressure, shape public opinion and unlock further multilateral action.""")
    st.markdown("""2) Introduce restrictions on certain media within one’s own territory. Design specific legislation 
     without incurring the risk of undermining your own core values (e.g., freedom of speech and information) """)
    st.markdown("""3) Boost Cyber Resilience at the Wider Societal Level: In both cyber and information domains, 
     it has become clear that individuals play a central role in achieving resilience.  """)
    st.markdown("""4) Proactive resilience in the information domain. Invest sufficient resources in scanning, 
     verifying and debunking fake news and other information available to domestic audiences  """)
    st.markdown("""5) Open deterrence messaging through strategic communications. Being transparent with the hostile 
     actor regarding one's own strategic strengths and possible actions. This increases the possibility of a better 
     informed decision by the hostile actor.""")
    st.markdown("""For now we assume that each counter-hybrid measure is a deterrence measure. The measures are abstract
    and therefore scalable.
    Please concretize the measures so that they are tailor-made to the scenario and the profiles and fill out the data
     accordingly.
            """)

    st.subheader("""The impact of a the hybrid attack""")
    st.write("""First we are going to assess how damaging the threat of the adversary could be. 
     Please, carefully read the scenario, profile
      of the adversary and profile of the defender to assess what are the most damaging impact, the tolerable damaging impact,
      and the least damaging possible impact when the adversary conducts a hybrid threat. Rate the results on a pay-off
       scale for 0-100, where 0 is the least damaging impact for the deterring agent and 100 the most damaging impact.""")

    theta_1 = st.slider("What is the most damaging impact?", 0, 100, value=100, step=5)
    theta_2 = st.slider("What is the tolerable damaging impact?", 0, 100, value=50, step=5)
    theta_3 = st.slider("What is the least damaging impact", 0, 100, value=0, step=5)


    st.subheader("""Counter Hybrid Measure Costs""")
    st.markdown("""Each of the counter-hybrid measures described above bring certain costs. These costs include the financial
    resources needed to boost cyber resilience or costs of hiring qualified experts. However, the costs also include 
    political capital for international support, or economic fallback when imposing market restrictions.
    The only costs that are *NOT* included are costs that come with effectiveness of the counter hybrid measure. Please, 
    carefully read the scenario, profile of the adversary and profile of the defender to assess costs for each of the 
    deterrence measures. Please rate the cost from 0-100 and relate them to the damaging impact above.
               """)

    gamma_1 = st.slider("What are my costs for {}?".format(counter_hybrid_measures[0]), 0, 100, value=5, step=5)
    gamma_2 = st.slider("What are my costs for {}?".format(counter_hybrid_measures[1]), 0, 100, value=5, step=5)
    gamma_3 = st.slider("What are my costs for {}?".format(counter_hybrid_measures[2]), 0, 100, value=15, step=5)
    gamma_4 = st.slider("What are my costs for {}?".format(counter_hybrid_measures[3]), 0, 100, value=10, step=5)
    gamma_5 = st.slider("What are my costs for {}?".format(counter_hybrid_measures[4]), 0, 100, value=15, step=5)

    st.write(
        "The costs for the counter hybrid measures are {}, {}, {}, {} and {} respectively.".format(gamma_1, gamma_2,
                                                                                                   gamma_3, gamma_4,
                                                                                                   gamma_5))

    st.subheader("""Conditional Probabilities for the Damaging Impacts""")
    st.write("""Hybrid conducts entail many uncertain elements. A failure of detection of the hybrid conduct can result
     in disastrous effects by letting the adversary pursue strategic goals without being aware. Similarly,
     a failure in attribution can result in a lack of success in gaining enough political support to take effective counter-measures.
     Because the nature of a hybrid conduct is to remain under the threshold for detection and attribution and one can never
     be 100% certain that we detect or attribute correctly, the possible outcomes should be modeled probabilistically.
    """)
    st.write("""In the next section we assume that the deterrence has failed and the adversary follows with a hybrid conduct.
    For each possible counter-hybrid measure and hybrid conduct we assign probability values to
    the earlier defined damaging impacts. Note that a probability of 0% means impossible while 100% means certain, as described in 
    the probability standards used by intelligence services.
    Please be aware that the total probability of EVERY combination should sum to 100%. 
    """)
    st.subheader("""Probability of Damaging Impacts when {}""".format(counter_hybrid_measures[0]))
    w111 = st.slider("What is the probability of the most damaging impact ({}) when the deterrer commits to {} and "
                     "the attacker conducts {}? "
                     .format(theta_1, counter_hybrid_measures[0], attack_measures[0]), 0, 100, 50, step=10)
    w112 = st.slider("What is the probability of the tolerable damaging impact ({}) when the deterrer commits to {} and "
                     "the attacker conducts {}? "
                     .format(theta_2, counter_hybrid_measures[0], attack_measures[0]), 0, 100, 50, step=10)
    w113 = st.slider("What is the probability of the least damaging impact ({}) when the deterrer commits to {} and "
                     "the attacker conducts {}? "
                     .format(theta_3, counter_hybrid_measures[0], attack_measures[0]), 0, 100, 0, step=10)


    st.subheader("""Probability of Damaging Impacts when {}""".format(counter_hybrid_measures[1]))
    st.write(
        "Probability of each of the damaging impacts when the deterrer commits to {} and the attacker conducts {}. Probabilities "
        "should sum up to 100%.".format(
            counter_hybrid_measures[1], attack_measures[0]))

    w211 = st.slider("What is the probability of the most damaging impact ({}) when the the deterrer commits to {} and "
                     "the attacker conducts {}? "
                     .format(theta_1, counter_hybrid_measures[1], attack_measures[0]), 0, 100, 20, step=10)
    w212 = st.slider("What is the probability of the tolerable damaging impact ({}) when the deterrer commits to {} and "
                     "the attacker conducts {}? "
                     .format(theta_2, counter_hybrid_measures[1], attack_measures[0]), 0, 100, 50, step=10)
    w213 = st.slider("What is the probability of the least damaging impact ({}) when the deterrer commits to {} and "
                     "the attacker conducts {}? "
                     .format(theta_3, counter_hybrid_measures[1], attack_measures[0]), 0, 100, 30, step=10)


    st.subheader("""Probability of Damaging Impacts when {}""".format(counter_hybrid_measures[2]))
    st.write(
        "Probability of each of the damaging impacts when the deterrer commits to {} and the attacker conducts {}. Probabilities "
        "should sum up to 100%.".format(
            counter_hybrid_measures[2], attack_measures[0]))

    w311 = st.slider("What is the probability of the most damaging impact ({}) when the deterrer commits to {} and "
                     "the attacker conducts {}? "
                     .format(theta_1, counter_hybrid_measures[2], attack_measures[0]), 0, 100, 30, step=10)
    w312 = st.slider("What is the probability of the tolerable damaging impact ({}) when the deterrer commits to {} and "
                     "the attacker conducts {}? "
                     .format(theta_2, counter_hybrid_measures[2], attack_measures[0]), 0, 100, 70, step=10)
    w313 = st.slider("What is the probability of the least damaging impact ({}) when the deterrer commits to {} and "
                     "the attacker conducts {}? "
                     .format(theta_3, counter_hybrid_measures[2], attack_measures[0]), 0, 100, 0, step=10)


    st.subheader("""Probability of Damaging Impacts when {}""".format(counter_hybrid_measures[3]))

    st.write(
        "Probability of each of the damaging impacts when the deterrer commits to {} and the attacker conducts {}. Probabilities should sum up to 100%.".format(
            counter_hybrid_measures[3], attack_measures[0]))

    w411 = st.slider("What is the probability of the most damaging impact ({}) when the deterrer commits to {} and "
                     "the attacker conducts {}? "
                     .format(theta_1, counter_hybrid_measures[3], attack_measures[0]), 0, 100, 20, step=10)
    w412 = st.slider("What is the probability of the tolerable damaging impact ({}) when the deterrer commits to {} and "
                     "the attacker conducts {}? "
                     .format(theta_2, counter_hybrid_measures[3], attack_measures[0]), 0, 100, 50, step=10)
    w413 = st.slider("What is the probability of the least damaging impact ({}) when the deterrer commits to {} and "
                     "the attacker conducts {}? "
                     .format(theta_3, counter_hybrid_measures[3], attack_measures[0]), 0, 100, 30, step=10)


    st.subheader("""Probability of Damaging Impacts when {}""".format(counter_hybrid_measures[4]))
    st.write(
        "Probability of each of the damaging impacts when the deterrer commits to {} and the attacker conducts {}. Probabilities should sum up to 100%.".format(
            counter_hybrid_measures[4], attack_measures[0]))

    w511 = st.slider("What is the probability of the most damaging impact ({}) when the deterrer commits to {} and "
                     "the attacker conducts {}? "
                     .format(theta_1, counter_hybrid_measures[4], attack_measures[0]), 0, 100, 50, step=10)
    w512 = st.slider("What is the probability of the tolerable damaging impact ({}) when the deterrer commits to {} and "
                     "the attacker conducts {}? "
                     .format(theta_2, counter_hybrid_measures[4], attack_measures[0]), 0, 100, 50, step=10)
    w513 = st.slider("What is the probability of the least damaging impact ({}) when the deterrer commits to {} and "
                     "the attacker conducts {}? "
                     .format(theta_3, counter_hybrid_measures[4], attack_measures[0]), 0, 100, 0, step=10)


    st.subheader("""Probability of succeeding in deterring""")
    st.write("""For each of the counter hybrid measure taken, we should assess its effectiveness in terms of successfully
    deterring the attack. Therefore we make an assessment of the likelihood of a hybrid attack based
             on each of the counter-hybrid measures.""")
    st.write("Probability of effectiveness of the corresponding counter hybrid measure in deterring a hybrid attack.")

    a_1 = st.slider("How effective is {}".format(counter_hybrid_measures[0]), 0, 100, 40, step=10) * 0.01
    a_2 = st.slider("How effective is {}".format(counter_hybrid_measures[1]), 0, 100, 20, step=10) * 0.01
    a_3 = st.slider("How effective is {}".format(counter_hybrid_measures[2]), 0, 100, 20, step=10) * 0.01
    a_4 = st.slider("How effective is {}".format(counter_hybrid_measures[3]), 0, 100, 40, step=10) * 0.01
    a_5 = st.slider("How effective is {}".format(counter_hybrid_measures[4]), 0, 100, 10, step=10) * 0.01

    # Boundary Conditions:
    theta = np.array([-theta_1, -theta_2, -theta_3, 0, 0])  # Pay_off rewards
    pay_off = np.array([[[w111, w112, w113, 0, 0], [w211, w212, w213, 0, 0], [w311, w312, w313, 0, 0],
                         [w411, w412, w413, 0, 0], [w511, w512, w513, 0, 0]],
                        [[0, 0, 100, 0, 0], [0, 0, 100, 0, 0], [0, 0, 100, 0, 0], [0, 0, 100, 0, 0],
                         [0, 0, 100, 0, 0]]]) * 0.01  # Pay_off probabilities
    gamma = np.array(
        [-gamma_1, -gamma_2, -gamma_3, -gamma_4, -gamma_5])  # Deterrence cost gamma_1, gamma_2, gamma_3, gamma_4
    alpha1 = np.array([[1 - a_1, 1 - a_2, 1 - a_3, 1 - a_4, 1 - a_5],
                       [a_1, a_2, a_3, a_4, a_5]])  # deterrer thinks d_1 det by punishment is effective
    H = np.array([2.5, 0])  # The Attack cost eta_1, eta_2

    st.header("""Optimal Solution""")

    LP_instance = model.LP(pay_off=theta, pay_off_matrix=pay_off, det_costs=gamma, att_costs=H, det_strat=None,
                           att_strat=alpha1)
    variables, objective = LP_instance.deterrence_LP()

    st.write()

    for i, variable in enumerate(variables):
        if variable.varValue > 0:
            st.write("The optimal measure is to conduct **{}** (with optimal solution {}). ".format(
                counter_hybrid_measures[i], round(objective, 2)))

    st.write("""The number of the optimal solution refers to the costs of the chosen deterrence measure weighted against
    the possible impact under uncertainty.""")