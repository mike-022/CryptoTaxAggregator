import pandas as pd
import glob


def get_column_value(df, columns):
    for column in columns:
        if column in df:
            return df[column]
    return None

def map_csv_columns_and_write_to_file(input_df):

    input_df.columns = input_df.columns.str.title()
    mapped_rows = []

    for index, row in input_df.iterrows():
        mapped_row = {}

        mapped_row['Product'] = get_column_value(row,
                                                 ['Product', 'Asset'])

        mapped_row['Size Unit'] = get_column_value(row, ['Size Unit', 'Asset'])

        mapped_row['Side'] = get_column_value(row,
                                              ['Transaction Type', 'Side'])
        mapped_row['Created At'] = get_column_value(
            row, ['Timestamp', 'Created At'])
        mapped_row['Size'] = get_column_value(row,
                                              ['Quantity Transacted', 'Size'])
        mapped_row['Price'] = get_column_value(row,['Spot Price At Transaction'
                                                   ,'Price'])
        fee = get_column_value(
            row, ['Fees And/Or Spread', 'Fee'])
        mapped_row['Fee'] = fee if fee else 0

        total = get_column_value(row,[
            'Total (Inclusive Of Fees And/Or spread)', 'Total'])
        mapped_row['Total'] = total if total else 0
        mapped_row['Price/Fee/Total Unit'] = get_column_value(row,[
            'Spot Price Currency', 'Price/Fee/Total Unit'])

        mapped_row['Side'] = mapped_row['Side'].upper()
        mapped_rows.append(mapped_row)

    mapped_df = pd.DataFrame(mapped_rows)
    return mapped_df

# Takes in a list of dataframes and merges them
def mergeTradesAndFilter(trade_dfs):
    merged_trade_file = 'output/MergedTrades.csv'

    # Merge trade data frames
    merged_df = pd.concat(trade_dfs)
    # sort the dataframe by the "created_at" column
    merged_df = merged_df.sort_values(by='Created At')

    # reset the index
    merged_df = merged_df.reset_index(drop=True)

    #Filter response

    merged_df = merged_df[(merged_df['Side'] == 'BUY') | (merged_df['Side'] == 'SELL')]
    # write the filtered data to a new csv file

    merged_df = merged_df.dropna(axis=1, how='all')

    merged_df['Total'] = abs(merged_df['Total'])

    print("Merged Trades and filtered for buy and sell transactions. See - " +
          merged_trade_file)
    return merged_df



def processTradeFiles():
    trade_files = []
    path = './input/*.csv'
    files = glob.glob(path)
    print(files)
    for file in files:
        trade_df = pd.read_csv(file)
        mapped_df = map_csv_columns_and_write_to_file(trade_df)
        trade_files.append(mapped_df)

    return trade_files


def processTradeDataFrames(trade_dfs):
    processed_trade_dfs = []
    for df in trade_dfs:
        mapped_df = map_csv_columns_and_write_to_file(df)
        processed_trade_dfs.append(mapped_df)

    return mergeTradesAndFilter(processed_trade_dfs)

# trade_dfs = processTradeFiles()
# mergeTradesAndFilter(trade_dfs)
