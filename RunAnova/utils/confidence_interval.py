
import pandas as pd
import numpy as np
import scipy.stats as stats

def compute_indep_ci(df, loc=0.95):
    mean_list, std_list, ci_list = [], [], []
    for col_name in df:
        col_values = df[col_name].values
        sample_size = len(col_values)
        degrees_freedom = sample_size - 1
        sample_mean = np.mean(col_values)
        # Standard error of the mean (SEM) = sigma / sqrt(n)
        sample_standard_error = stats.sem(col_values)
        confidence_interval = stats.t.interval(alpha=loc,
                                            df=degrees_freedom,
                                            loc=sample_mean,
                                            scale=sample_standard_error)
        std_list.append(np.array(sample_standard_error).round(2))
        ci_list.append(np.array(confidence_interval).round(2))
        mean_list.append(sample_mean)
        
    CI_df = pd.DataFrame([df.columns.values,
                         mean_list,
                         std_list,
                          ci_list]).transpose().round(2)

    CI_df.columns = ['Treatment',
                    'Mean',
                    'Std error',
                    'CI']
    return CI_df