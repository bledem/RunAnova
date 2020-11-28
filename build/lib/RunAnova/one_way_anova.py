from numpy.core.defchararray import capitalize
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle
import scipy.stats as stats

from RunAnova import *
# from RunAnova import create_color, run_one_way_anova

class OneWayAnova(dict):
    def __init__(self, df, resp_var, treatments, stack=False):
        self.resp_var = resp_var
        self.treatment = treatments
        self.stack = stack
        # Reform the dataframe 
        if stack: # TO DO: create a self.df
            self.stack_df = df
            dict_ = {} 
            for treat in df[treatments].unique():
                dict_.update({treat: df.loc[df[treatments] == treat, resp_var].values})
            self.df = pd.DataFrame.from_dict(dict_)
        else:
            self.df = df
            stack_df = self.df.stack().reset_index()
            self.stack_df = stack_df.rename(columns={'level_0': 'id',
                                                'level_1': self.treatment,
                                                0 : self.resp_var})
        self.treatments = self.df.columns
        self.sample_size_dict = {treat: len(self.df[treat]) for treat in self.df}
        self.create_color()
        self.compute_indep_ci(loc= 0.95, show=True)

    def create_color(self):
        self.colors = create_color(self.treatments)

    def show_distribution(self):
        handles = [Rectangle((0,0),1,1,color=c,ec="k") for c in self.colors]
        plt.legend(handles, self.treatments)
        for i, sample in enumerate(self.df):
            plt.hist(self.df[sample], color=self.colors[i])
        plt.title(f'Distribution of {self.resp_var} by {self.treatment}')
        plt.show()
        ax = sns.displot(self.stack_df, x=self.resp_var,
                         hue=self.treatment, kind="kde", fill=True)
        plt.title("KDE estimate")
        plt.show()

        ax = sns.boxplot(y=self.stack_df[self.resp_var], x=self.stack_df[self.treatment])
        ax.set_title('Boxplot of treatment samples')
        plt.show()

    def compute_dep_ci(self):
        pass

    def compute_indep_ci(self, loc, show=False, kde=True):
        """
        args: c (float): level of confidence
        return: dataframe
        Is similar from the external package:
        import researchpy as rp
        rp.summary_cont(exp_df)
        """
        # Compute CI as if considering each sample independant
        CI_df = compute_indep_ci(self.df)
        self.CI_df = CI_df.sort_values(by=['Mean'])
        print(f'For a level of confidence of {loc}')
        display(self.CI_df)
        if show:
            for i, treat in enumerate(self.df):
                sub_df = self.df[treat]
                CI = self.CI_df.loc[self.CI_df.Treatment==treat]['CI'].values[0]
                if kde:
                    graph = sns.displot(sub_df, kind="kde", fill=True, color=self.colors[i])
                else:
                    graph = sns.displot(sub_df, kde=False, fill=True, color=self.colors[i])
                plt.axvline(CI[0],  linestyle='--', color=self.colors[i])
                plt.axvline(CI[1],  linestyle='--', color=self.colors[i])
                plt.title(f'KDE {treat} with confidence interval')
                plt.show()

    def normality_test(self, test_type):
        """
        Test of normality.
        Args: test_type (str) ``qqplot``, ``shapiro``.
        Possible extension with D’Agostino’s K^2 Test or Anderson-Darling Test
        """
        print(f'###### Run {test_type.capitalize()} test ###### \n')

        if test_type == "qqplot":

            run_qqplot(self.df)
            
        elif test_type == "shapiro":
            # Test hypothesis where null hypothesis assume that the sample are taken from 
            # Gaussian distribution.
            # p <= alpha: reject H0, not normal.
            # p > alpha: fail to reject H0, normal.
            # Shapiro-Wilk test
            # if p > 0.05 we fail to reject null hypoteshsi -> Gaussian
            print('If p > 0.05 we fail to reject null hypoteshsi -> Gaussian')
            run_shapiro(self.df)
           
        elif test_type == "levene":
            print('If p-value >0.05 non-statistically significant difference in their varability')
            # Levene test for homogeneity of variance
            run_levene(self.df)
            # if p-value >0.05 non-statistically significant difference in their varability
    
    def run_anova(self, simple=True, loc=0.95):
        """ 
        Compute pre-package ANOVA or every steps of ANOVA table
        #SSE = "How spread is the data inside this sampme compare with the sample mean" (dive-in-view)
        #SST = "How each sample mean varies wrt to the grand mean" (global view)
        # Total variation = "How each data point varies wtr from the grand mean is composed from the \
        # variation of this data point from the sample mean + the variation of the sample mean wrt the grand mean"
        """
        if simple:
            list_treat = [self.df[treat] for treat in self.df]
            F, p = stats.f_oneway(*list_treat)
            print(f'F stat: {F:.2}, p-value: {p:.2f}')
        else:
            # ANOVA the hard way
            run_one_way_anova(self.df)
           

if __name__ == "__main__":
    resp_var = 'age'
    treatment = 'company'
    experiment = {'NASA' : [18,19,20,21,22,23,18,19,20,21],
                'Tesla' : [18,20,16,20,21,20,18,19,17,13], 
                'Orange' : [21,22,17,18,22,19,21,20,18,23]}

    exp_df = pd.DataFrame(experiment)
    exp_df.index.name = "observation"
    anova_proc = Anov(exp_df, resp_var=resp_var, treatment=treatment)
