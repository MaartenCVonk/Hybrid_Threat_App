import numpy as np
from pulp import *

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
        self.pay_off, self.pay_off_matrix, self.det_costs, self.att_costs = pay_off, pay_off_matrix, det_costs, att_costs
        self.attlen, self.detlen, self.pay_offlen = self.pay_off_matrix.shape
        self.det_strat= det_strat if det_strat is not None else np.eye(self.detlen)[0]
        self.att_strat= att_strat if att_strat is not None else np.eye(self.detlen)
        self.logger = logging.getLogger(__name__)
        assert np.array_equal(np.sum(self.att_strat, axis=0), np.ones(self.detlen)),\
            "Probabilities Attack Strategy should sum up to one"
        assert np.sum(self.det_strat) == 1,\
            "Probabilities Det Strategy should sum up to one"
        assert np.array_equal(np.sum(self.pay_off_matrix, axis=2),np.ones([self.attlen, self.detlen])), \
            "Probabilities Pay-off should sum up to one"


    def deterrence_LP(self):
        """
        This solves all the LP steps, prints the problem status and returns the variable results
        """

        strat = {}
        for x in range(0, self.detlen):
            strat[x] = LpVariable(f"d[{x+1}]", lowBound=0, upBound=1, cat="Continuous")
        prob = LpProblem("Max pay-off", LpMaximize)
        # Creates the objective function
        prob.setObjective(sum(self.pay_off[y] * self.att_strat[t,x]*self.pay_off_matrix[t,x,y]*strat[x] for y in range(self.pay_offlen)
                                                                          for t in range(self.attlen)
                                                                          for x in range(self.detlen))
                         +sum(self.det_costs[x]*strat[x]                 for x in range(self.detlen)))
        prob += lpSum([strat[i] for i in range(self.detlen)]) <= 1
        prob += lpSum([strat[i] for i in range(self.detlen)]) >= 1
        # Solve ILP
        prob.solve()
        return prob.variables(), value(prob.objective)

    def attack_LP(self):
        """
        This solves all the LP steps, prints the problem status and returns the variable results
        """
        alp = {}
        for i in range(self.attlen):
            alp[i] = LpVariable(f"a[{i+1}]", lowBound=0, upBound=1, cat="Binary")
        prob = LpProblem("Min pay-off", LpMinimize)
        # Creates the objective function
        prob.setObjective(sum(self.pay_off[y]* alp[i]*self.pay_off_matrix[i,j,y]*self.det_strat[j] for y in range(self.pay_offlen)
                                                                          for i in range(self.attlen)
                                                                          for j in range(self.detlen))
                                            + sum(alp[i]*self.att_costs[i] for i in range(self.attlen)))
        prob += lpSum([alp[i] for i in range(self.attlen)]) <= 1
        prob += lpSum([alp[i]  for i in range(self.attlen)]) >= 1
        # Solve ILP
        prob.solve()
        return prob.variables(), value(prob.objective)

