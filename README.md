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
 - ```example_oneway_breakfast_test.ipynb```

### One way using classic packages
- ```example_without_library.ipynb```


### Two ways using RunAnova
- ```two_ways_test.ipynb```


## Results

### Example of results for one way configuration:
For the following example dataframe:

| No breakfast | Light breakfast | Full breaskfast | 
| ------------- | ------------- | ------------- |
| 8  | 14  | 10 |
| 7  | 16  | 12 | 
| 9 | 12| 16 | 
| 13 | 17 | 15 | 
| 10 | 11 | 12| 

Init and call a OneWayAnova object:
```python
from RunAnova import OneWayAnova
resp_var = 'attention_span'
treatments = "meal_quantity"
anov = OneWayAnova(df=exp_df, resp_var=resp_var , treatments=treatments)
anov(simple=True)
anov(simple=False)
```

The output of ANOVA is either simple:
```
F stat: 4.9, p-value: 0.03
```
or detailed:
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

### Example of results for two way configuration:


Init and call a TwoWayAnova class object:

```python
from RunAnova import TwoWayAnova
factors_levels = {'wheel':[], 'gas':[]}
df = pd.DataFrame({'wheel': np.tile(['two', 'four'], 4),
                   'gas': np.tile(['regular', 'octane', 'octane', 'regular'],2),
                   'consumption': [26.7, 26.1, 32.3, 28.6,
                          25.2, 24.2, 32.8, 29.3]})      
for col in df.columns:
    if col in factors_levels:
        factors_levels[col] = list(df[col].unique())
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