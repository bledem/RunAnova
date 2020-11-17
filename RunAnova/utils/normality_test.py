from statsmodels.graphics.gofplots import qqplot
from scipy.stats import shapiro
import scipy.stats as stats
import matplotlib.pyplot as plt

def run_qqplot(dataframe):
    for treat in dataframe:
        qqplot(dataframe[treat].values, line='s')
        plt.title(treat)
        plt.show()

def run_shapiro(dataframe):
    for col, val in dataframe.iteritems():
        print(col, end=' ')
        stat, p = shapiro(val)
        print('statistics=%.3f, p=%.3f' % (stat, p))

def run_levene(dataframe):
    list_treat = [dataframe[treat] for treat in dataframe]
    stat, p = stats.levene(*list_treat)
    print('statistics=%.3f, p=%.3f' % (stat, p))
