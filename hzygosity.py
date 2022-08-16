"""
Compute heterozygosity index H

Created: 08 Jun 2022
Updated: 08 Jun 2022
Version: 0.1
Authors: Wolfgang Messner and Chrisogonas O. Odhiambo, University of South Carolina

# Citation: Messner, W. (2022). Cultural heterozygosity: Towards a new measure of within-country cultural diversity.
# Journal of World Business, 57/4, 1-17. DOI: 10.1016/j.jwb.2022.101346
"""

# IMPORT LIBRARIES
# ================
import pandas as pd
from math import sqrt


# HETZYG: HETEROZYGOSITY INDEX
# ============================
def hetzyg(df, calcmeth='vectorized'):
    """
    This function calculates the heterozygosity index, which is a measure of how different data is. Unlike the standard
    deviation, it is a distribution-free algorithm comparing all data across a number of variables with each other.

    Input:
      :param df: An array of data (data in the rows, variables in the columns)
      :param calcmeth: Calculation method (vectorized default)

    Output:
      :return: Heterozygosity index H

    Source: Messner, W. (2022). Cultural heterozygosity: Towards a new measure of within-country cultural diversity.
    Journal of World Business, 57/4, 1-17. DOI: 10.1016/j.jwb.2022.101346
    """

    rows = df.shape[0]
    cols = df.shape[1]

    dd_sum = 0
    my_vals = [0 for i in range(cols)]

    if calcmeth == 'vectorized':
        # First calculation method: Vectorization
        # Loop through all respondents - For each row, iterate each column (vector)
        for row in range(rows):
            for col in range(cols):
                a_sum = df.iloc[:, col].loc[lambda s: s > df.iloc[row, col]].sum()
                a_count = df.iloc[:, col].loc[lambda s: s > df.iloc[row, col]].count()

                b_sum = df.iloc[:, col].loc[lambda s: s < df.iloc[row, col]].sum()
                b_count = df.iloc[:, col].loc[lambda s: s < df.iloc[row, col]].count()

                my_vals[col] = ((abs(a_sum - a_count * df.iloc[row, col]) + abs(
                    b_sum - b_count * df.iloc[row, col])) / (
                                        rows - 1)) ** 2

            dd_sum += sqrt(sum(my_vals))
        return dd_sum / rows
    if calcmeth == 'nestedloop':  # Second calculation method: Double loop
        my_vals_rows = [0] * rows

        for row in range(rows):
            my_vals_a = [0] * cols
            my_counts_a = my_vals_a.copy()
            my_vals_b = my_vals_a.copy()
            my_counts_b = my_vals_a.copy()
            my_vals_sum = my_vals_a.copy()

            # for each respondent
            for row_2 in range(rows):

                # for each attribute/feature, run the computation
                for col in range(cols):
                    if df.iloc[row_2, col] > df.iloc[row, col]:
                        my_vals_a[col] += df.iloc[row_2, col]
                        my_counts_a[col] += 1
                    if df.iloc[row_2, col] < df.iloc[row, col]:
                        my_vals_b[col] += df.iloc[row_2, col]
                        my_counts_b[col] += 1

                    my_vals_sum[col] = ((abs(my_vals_a[col] - my_counts_a[col] * df.iloc[row, col]) + abs(
                        my_vals_b[col] - my_counts_b[col] * df.iloc[row, col])) / (
                                                rows - 1))
            # sum up the squared values
            my_vals_rows[row] = sqrt(sum(map(lambda x: x ** 2, my_vals_sum)))

        return sum(my_vals_rows) / rows
    else:
        print('Calculation method specified for hetzyg not valid. Program aborted.')
        exit(999)