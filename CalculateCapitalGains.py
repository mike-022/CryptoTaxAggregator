import pandas as pd
import numpy as np


# read in the buys csv
buys_df = pd.read_csv("output/buys.csv")

#Format created date time to tax reportable
buys_df['Created At'] = pd.to_datetime(buys_df['Created At'])
buys_df['Year'] = buys_df['Created At'].dt.year

# read in the sells csv
sells_df = pd.read_csv("output/sells.csv")

#Format created date time to tax reportable
sells_df['Created At'] = pd.to_datetime(sells_df['Created At'])
sells_df['Year'] = sells_df['Created At'].dt.year

# create a dictionary to store the capital gains for each year
gains = {}
losses = {}
proceedsforyear ={}
sell_calculations = []
long_gains = []
short_gains = []
tax_form = []
buy_fees = 0
sell_fees = 0

# loop through the sells dataframe
for index, sell in sells_df.iterrows():
    # get the current year of the sell
    current_year = sell['Created At'].year
    # initialize the capital gains for the current year if it doesn't exist in the dictionary
    if current_year not in gains:
        gains[current_year] = 0
    if current_year not in losses:
        losses[current_year] = 0
    if current_year not in proceedsforyear:
        proceedsforyear[current_year] = 0

    # get the sell details
    product = sell['Product']
    sell_size = sell['Size']
    sell_total = sell['Total']
    created_at = sell['Created At']
    size_unit = sell['Size Unit']
    sell_price = sell['Price']
    sell_fee = sell['Fee']
    # check if there are enough buys to match the sell

    sell_fees += sell_fee

    # loop through the buys for the current year
    totalAmountToSell = sell_size

    #Looping through all the buys and using each buy until exhaused against the cost basis
    for i, buy in buys_df.iterrows():
        size_realized = 0
        # check if the buy is for the same size unit
        if buy['Size Unit'] == size_unit and created_at > buy['Created At']:
            gain_in_this_transaction = 0
            if totalAmountToSell >= buy['Size']:
                # update the buy size and remove it from the dataframe if it's fully sold
                buys_df = buys_df.drop(i)
                size_realized = buy['Size']
                cost_basis = size_realized * buy['Price']
                proceeds = size_realized * sell_price
                gain_in_this_transaction = proceeds - cost_basis
                totalAmountToSell -= size_realized
                buy_fee = buy['Fee']

            elif totalAmountToSell < buy['Size']:
                size_realized = totalAmountToSell
                buys_df.at[i, 'Size'] -= size_realized
                buy_fee = (totalAmountToSell / buy['Size']) * buy['Fee']
                buys_df.at[i, 'Fee'] -= buy_fee
                cost_basis = size_realized * buy['Price']
                proceeds = size_realized * sell_price
                gain_in_this_transaction = proceeds - cost_basis
                totalAmountToSell = 0

            buy_fees += buy_fee
            # calculate the holding period
            holding_period = (created_at - buy['Created At']).days

            tax_rate = ''
            if gain_in_this_transaction > 0:
                gains[current_year] += gain_in_this_transaction
            else:
                losses[current_year] += gain_in_this_transaction

            calculation = {
                "Sold": pd.to_datetime(created_at).strftime('%m/%d/%Y'),
                "Product": product,
                "Sell Id": index,
                "Buy Id realized": i,
                "Year": current_year,
                "Dates Of Acquisition": buy['Created At'],
                "Gain": gain_in_this_transaction,
                "Amount To Sell": totalAmountToSell + size_realized,
                "Size Realized": size_realized,
                "Left To Sell": totalAmountToSell,
                "Amount Written Off": size_realized,
                "Buy Price Off": (buy['Price']),
                "Sell Date": sell['Created At'],
                "Buy Written Off Date": buy['Created At'],
                "Sell Price": sell_price,
                "Buy Price": buy['Price'],
                "Buy Fee": buy_fee,
                "Sell Fee": sell_fee,
                "Cost Basis": cost_basis
            }

            if holding_period > 365:
                calculation['Tax Rate'] = "LONG"
                long_gains.append(calculation)
            else:
                calculation['Tax Rate'] = "SHORT"
                short_gains.append(calculation)


            proceedsforyear[current_year] += gain_in_this_transaction


            if totalAmountToSell == 0 :
                break




# print the capital gains for each year
print("Gains:")
print(gains)
print("Losses")
print(losses)
print("fees")
print("proceeds")
print(proceedsforyear)
print("buy fees:" + str(buy_fees) + "sell fees:" + str(sell_fees))


long_gains_df = pd.DataFrame(long_gains)
long_gains_df.to_csv("output/Long_Gain_Calculation.csv")
short_gains_df = pd.DataFrame(short_gains)
short_gains_df.to_csv("output/Short_Gain_Calculation.csv")

print("Calculated long and short gains for all transaction data.")