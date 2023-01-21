import csv
from datetime import datetime
from dateutil import parser


def calculate_amount_sold(csv_file1, csv_file2, start_date, end_date):
    # Initialize variables to store current holding and cost
    amount_sold = {}
    total_usd = {}
    # Convert start_date and end_date to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Read in first CSV file
    with open(csv_file1, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = row['product']
            side = row['side']
            size = float(row['size'])
            price = float(row['price'])
            timestamp = parser.parse(row['created at']).replace(tzinfo=None)
            if start_date <= timestamp <= end_date:
                if side == 'SELL':
                    if product in amount_sold:
                        amount_sold[product] += size
                        total_usd[product] += price * size
                    else:
                        amount_sold[product] = size
                        total_usd[product] = price * size
    # Read in second CSV file
    with open(csv_file2, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = row['product']
            side = row['side']
            size = float(row['size'])
            price = float(row['price'])
            timestamp = parser.parse(row['created at']).replace(tzinfo=None)
            if start_date <= timestamp <= end_date:
                if side == 'SELL':
                    if product in amount_sold:
                        amount_sold[product] += size
                        total_usd[product] += price * size
                    else:
                        amount_sold[product] = size
                        total_usd[product] = price * size
    return {'amount_sold': amount_sold, 'total_usd': total_usd}


# Example usage
amount_sold = calculate_amount_sold('input/CoinbaseProTrades.csv',
                                    'input/CoinbaseTrades.csv', '2022-01-01',
                                    '2022-12-31')
print(amount_sold)
