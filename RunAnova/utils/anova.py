
import numpy as np
import scipy.stats as stats

def run_one_way_anova(dataframe, loc=0.95):
    list_n = dataframe.count().values
    try:
        assert np.all(list_n == list_n[0])
    except:
        print('Warning: Samples are not of equal size')
    k = len(dataframe.iloc[0]) # Number of columns
    n = np.sum(list_n)
    alpha = 1 - loc
    gd_mean = dataframe.mean().mean()

    # sum all value from all groups and divide it by sum of observation from all (the three) samples
    CM = (dataframe.sum().sum())**2 / n 
    # print('CM', CM)
    # total SS 
    TSS = (dataframe**2).sum().sum() - CM
    dof_tss = n - 1

    # SST between
    SST = ((dataframe.sum()**2).values / list_n).sum() - CM
    dof_sst = k - 1
    MST = SST / dof_sst 
    # SSE within
    SSE = TSS - SST
    dof_sse = n - k
    MSE = SSE / dof_sse

    # Test statistic
    F = MST/ MSE
    # F alpha
    F_alpha = stats.f.ppf(q=1-alpha, dfn=dof_sst, dfd=dof_sse)
    # p-value
    p = stats.f.sf(F, dof_sst, dof_sse)

    # Eta 
    et_sq = SST / TSS
    # Omega squared 
    om_sq = SST - (dof_sst * MSE) / (TSS + MSE)

    DOF = [dof_tss, dof_sst, dof_sse]
    print('##### Decomposition of variance #####')
    print('Grand Mean {:.2f}'.format(gd_mean))
    print('SST: {:.2f}, dof k-1:  {}, MST: {:.2f}'.format(SST, dof_sst, MST))
    print('SSE: {:.2f}, dof n-k:  {}, MSE: {:.2f}'.format(SST, dof_sse, MSE))

    print('TSS=SST+SSE total variation: {:.2f}, DOF: {}'.format(TSS, dof_tss))
    print('##### Testing #####')
    print('Test statistic: F=MST/MSE={:.2f}'.format(F))
    print('F_alpha: {:.2f} for a level of confidence of {:.2f}'.format(F_alpha,alpha))
    print('We reject Ho!') if F_alpha<F else print('We fail to reject the null hypothesis')
    if F_alpha<F:
        print('We failed to reject Ho: one mean is different from the others!')
    print('P-value: {:.4f}'.format(p))
    print('eta squared: {:.2f} omega_squared: {:.2f}'.format(et_sq, om_sq))



def compute_two_way_critic_val(dataframe, f0, f1, loc=0.95):
    """
    Compute critical values of the F ditribution for a for a two-way ANOVA.
    Args: 
        dataframe: contains the output values for each treatment.
        f0 (string): name of the first factor of interest.
        f1 (string): name of the second factor of interest.
        loc (float): level of confidence. 
    """
    ### Factor A has two levels so () Dof_sst = DFN = a -1 = 1
    a = len(set(dataframe[f0]))
    dfn1 = a -1
    ### Factor B Dof_sst = DFN = a - 1
    b = len(set(dataframe[f1]))
    dfn2 = b -1
    ## Factor AxB (interaction)
    dfn3 = (a-1) * (b-1)
    ## Denominator
    n  =  len(set(dataframe[f0])) #????? number of subject in each group
    dfd = a*b*(n-1)

    f_cv_a = stats.f.ppf(loc, dfn1, dfd)
    f_cv_b = stats.f.ppf(loc, dfn2, dfd) ## A and B factor critical value is different when they have 
    # different level of factors
    f_cv_ab = stats.f.ppf(loc, dfn3, dfd)
    print(f'Critical value for {f0}:', f_cv_a)
    print(f'Critical value for {f1}:', f_cv_b)
    print('Critical value for interaction:', f_cv_ab)

    F_critical = [f_cv_b, f_cv_a, f_cv_ab]
    return F_critical
    