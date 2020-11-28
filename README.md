# RunAnova

This library run ANOVA one way and two way experiments.
RunAnova will detail the computation steps (Mean Square, Degree of Freedom), to help you understand the results. 

## Install the package (optinal)
If you want to install the package in your environment:
```shell script
conda create --name anova python=3.7
pip install dist/RunAnova-1.0a0-py3-none-any.whl
```

## Run example notebooks

### One way using RunAnova
 - example_oneway_breakfast_test.ipynb

### One way using classic packages
- example_without_library.ipynb


### Two ways using RunAnova
- two_ways_test.ipynb


## Results


### Example of results for one way configuration:
![1](imgs/df_oneway)
```python
resp_var = 'attention_span'
treatments = "meal_quantity"
anov = OneWayAnova(df=exp_df, resp_var=resp_var , treatments=treatments)
anov.show_distribution()
```
You obtain nice displays like
![2](imgs/display_oneway)

```python
anov.run_anova(simple=True)
anov.run_anova(simple=False)
```

The output of ANOVA is either simple:
```F stat: 4.9, p-value: 0.03```
or detailed:
```python
##### Decomposition of variance #####
Grand Mean 12.13
SST: 58.53, dof k-1:  2, MST: 29.27
SSE: 58.53, dof n-k:  12, MSE: 5.93
TSS=SST+SSE total variation: 129.73, DOF: 14
##### Testing #####
Test statistic: F=MST/MSE=4.93
F_alpha: 3.89 for a level of confidence of 0.05
We reject Ho!
We failed to reject Ho: one mean is different from the others!
P-value: 0.0273
eta squared: 0.45 omega_squared: 58.45
```

### Example of results for two way configuration:
![3](imgs/df_twoway)

and obtain by running:



```python
from RunAnova import two_way_anova
factors_levels = {'wheel':[], 'gas':[]}
anova_proc = TwoWayAnova(df, resp_var='consumption', factors_levels=factors_levels)
anova_proc()
```
```
##### Decomposition of variance #####
Grand Mean 12.13
SST: 58.53, dof k-1:  2, MST: 29.27
SSE: 58.53, dof n-k:  12, MSE: 5.93
TSS=SST+SSE total variation: 129.73, DOF: 14
##### Testing #####
Test statistic: F=MST/MSE=4.93
F_alpha: 3.89 for a level of confidence of 0.05
We reject Ho!
We failed to reject Ho: one mean is different from the others!
P-value: 0.0273
eta squared: 0.45 omega_squared: 58.45
```