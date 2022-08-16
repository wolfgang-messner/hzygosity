import hzygosity as hz
import pandas as pd

df = pd.read_csv('../data/Testdata2.csv', na_values=['N/A', ' '])  # CHANGE FILE NAME & PATH
# Compute heterozygosity index
H = hz.hetzyg(df, calcmeth='vectorized')
print(f'Heterozygosity index H = {H}')

# print(hz.__name__)
# print(dir(hz))