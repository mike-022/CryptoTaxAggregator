import pandas as pd
import numpy as np

def separate_transactions(merged_df,
                          tax_calculation_method):
    # create separate dataframes for buys and sells
    buys_df = merged_df[merged_df['Side'] == 'BUY']
    buys_df = buys_df.set_index('Created At')

    buys_df = buys_df.reset_index()

    buys_df.index = pd.to_datetime(buys_df.index)
    # buys_df = buys_df.loc[(buys_df['Total'] > 0)]
    buys_df = buys_df[buys_df.columns]

    sells_df = merged_df[merged_df['Side'] == 'SELL']
    sells_df = sells_df.sort_values(by=['Created At'], ascending=False)
    sells_df = sells_df.set_index('Created At')

    sells_df = sells_df.reset_index()

    sells_df.index = pd.to_datetime(sells_df.index)
    sells_df = sells_df.loc[(sells_df['Total'] > 0)]
    sells_df = sells_df[sells_df.columns]

    if tax_calculation_method == 'HIFO':
        buys_df = buys_df.sort_values(by='Price', ascending=False)

    return buys_df, sells_df





print("Separated buys and sells.")
print("Finished grouping transactions - see output/buys.csv, output/sells.csv")