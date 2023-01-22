import pandas as pd
import numpy as np
from datetime import datetime


def agregateTransactions(input_df,output,year):

    grouped_df = input_df.groupby('Sell Id').agg({
        "Sold":
        'first',
        'Product':
        'first',
        'Dates Of Acquisition':
        lambda x: set(x.apply(lambda y: pd.to_datetime(y).strftime('%m/%d/%Y'))
                      ),
        'Gain':
        'sum',
        'Cost Basis':
        'sum',
        'Sell Fee':
        'mean',
        'Buy Fee':
        'sum'
    }).reset_index()

    grouped_df['Total Fees'] = grouped_df['Sell Fee'] + grouped_df['Buy Fee']
    grouped_df['Total Fees'] = np.around(grouped_df['Total Fees'], decimals=2)
    grouped_df['Gain'] = np.around(grouped_df['Gain'], decimals=2)
    grouped_df['Cost Basis'] = np.around(grouped_df['Cost Basis'], decimals=2)
    grouped_df['Buy Fee'] = np.around(grouped_df['Buy Fee'], decimals=2)
    grouped_df['Sell Fee'] = np.around(grouped_df['Sell Fee'], decimals=2)


    grouped_df.pop('Buy Fee')
    grouped_df.pop('Sell Fee')
    grouped_df.pop('Sell Id')

    sum_df = grouped_df.select_dtypes(include='float').sum().to_frame().T
    sum_df = sum_df.applymap(lambda x: np.around(x, decimals=2)
                            if isinstance(x, (int, float)) else x)

    grouped_df = pd.concat([grouped_df, sum_df], axis=0)

    grouped_df.to_csv(output)
    return grouped_df


def calculateCapitalGainsFilesByYear(short_gains_df, long_gains_df):
    cap_gains_by_year_dfs = []
    # Calculating long gains for each year
    for year_to_calculate in long_gains_df["Year"].unique():
        long_gains_df = long_gains_df.loc[long_gains_df["Year"] ==
                                        year_to_calculate]
        long_gain_output_file = "output/Long_Gain_" + str(year_to_calculate) + ".csv"
        grouped_df = agregateTransactions(long_gains_df,long_gain_output_file,
                                       year_to_calculate)
        cap_gains_by_year_dfs.append(grouped_df)
        print("Created Sample Capital Gains tax form refer to " +
            long_gain_output_file + ".")

    # Calculating short gains for each year
    for year_to_calculate in short_gains_df["Year"].unique():
        short_gains_df = short_gains_df.loc[short_gains_df["Year"] ==
                                            year_to_calculate]
        short_gain_output_file = "output/Short_Gain_" + str(
            year_to_calculate) + ".csv"
        grouped_df = agregateTransactions(short_gains_df,short_gain_output_file,
                                          year_to_calculate)
        cap_gains_by_year_dfs.append(grouped_df)

        print("Created Sample Capital Gains tax form refer to " +
            short_gain_output_file + ".")
    return cap_gains_by_year_dfs