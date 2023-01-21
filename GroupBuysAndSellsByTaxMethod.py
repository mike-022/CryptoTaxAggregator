import pandas as pd
import numpy as np


# def tax_calculation_method(tax_calculation_method):
#     # read in the buys csv
#     buys_df = pd.read_csv("output/buys.csv")
#     buys_df['Created At'] = pd.to_datetime(buys_df['Created At'])

#     # read in the sells csv
#     sells_df = pd.read_csv("output/sells.csv")

#     buys_df['Created At'] = pd.to_datetime(buys_df['Created At'])
#     buys_df = buys_df.set_index('Created At')

#     buys_df = buys_df.reset_index()

#     buys_df.index = pd.to_datetime(buys_df.index)
#     buys_df = buys_df.loc[(buys_df['Total'] > 0)]
#     buys_df = buys_df[buys_df.columns]


#     sells_df['Created At'] = pd.to_datetime(sells_df['Created At'])
#     sells_df = sells_df.set_index('Created At')

#     sells_df = sells_df.reset_index()

#     sells_df.index = pd.to_datetime(sells_df.index)
#     sells_df = sells_df.loc[(sells_df['Total'] > 0)]
#     sells_df = sells_df[sells_df.columns]


#     buys_df.to_csv("output/grouped_buys.csv", index=False)
#     sells_df.to_csv("output/grouped_sells.csv", index=False)


def separate_transactions(csv_file, buys_file, sells_file,
                          tax_calculation_method):
    # read in the csv file
    df = pd.read_csv(csv_file)
    # create separate dataframes for buys and sells
    buys_df = df[df['Side'] == 'BUY']
    buys_df = buys_df.set_index('Created At')

    buys_df = buys_df.reset_index()

    buys_df.index = pd.to_datetime(buys_df.index)
    # buys_df = buys_df.loc[(buys_df['Total'] > 0)]
    buys_df = buys_df[buys_df.columns]

    sells_df = df[df['Side'] == 'SELL']
    sells_df = sells_df.sort_values(by=['Created At'], ascending=False)
    sells_df = sells_df.set_index('Created At')

    sells_df = sells_df.reset_index()

    sells_df.index = pd.to_datetime(sells_df.index)
    sells_df = sells_df.loc[(sells_df['Total'] > 0)]
    sells_df = sells_df[sells_df.columns]

    if tax_calculation_method == 'HIFO':
        buys_df = buys_df.sort_values(by='Price', ascending=False)

    # write the dataframes to separate csv files
    buys_df.to_csv(buys_file, index=False)

    sells_df.to_csv(sells_file, index=False)

# example usage
tax_method = "HIFO"
separate_transactions('output/MergedTrades.csv', 'output/buys.csv',
                      'output/sells.csv',tax_method)
print("Separated buys and sells.")

print("Finished grouping transactions - see output/buys.csv, output/sells.csv")