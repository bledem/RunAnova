import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle
import scipy.stats as stats
from statsmodels.formula.api import ols
import statsmodels.api as sm

from RunAnova import compute_two_way_critic_val

class TwoWayAnova(dict):
    def __init__(self, df, resp_var, factors_levels):
        self.df = df
        self.resp_var = resp_var
        self.factors_levels = factors_levels
        self.init()
    
    def init(self):
        for col in self.df.columns:
            if col in self.factors_levels:
                self.factors_levels[col] = list(self.df[col].unique())
        # each combination of different levels from each factor is one treatment
        self.factors = [f for f in self.factors_levels]
        self.mean_table = self.df.groupby(self.factors).mean()
        display(self.mean_table)
        self.n = len(self.df) # a * b * r

    def plot_interaction_response(self):
        
        sns.lineplot(data=self.mean_table,
                    x=self.factors[0],
                    y=self.resp_var,
                    hue=self.factors[1],
                    style='gas', markers=True, dashes=False)
        plt.title('Interaction plot for response')

    def run_anova(self, simple=True, loc=0.95):
        """ 
        Run two-ways anova (=with two factors). 
        """
        list_treat = [self.df[treat] for treat in self.df]
        f0 = self.factors[0]
        f1 = self.factors[1]
        model = ols(f'{self.resp_var} ~ C({f0}) + C({f1}) + C({f0}):C({f1})', data=self.df).fit()
        anov_results = sm.stats.anova_lm(model, typ=2)
        F_critical = compute_two_way_critic_val(self.df, f0, f1)
        print(anov_results)
        ## Verdict
        for i in range(len(F_critical)):
            F_test = anov_results["F"].iloc[i]
            F_cri = F_critical[i]

            if F_test > F_cri:
                print('We reject the null hypothesis for', anov_results.index[i])
            else:
                print('We fail to reject the null hypothesis for', anov_results.index[i])   
           
