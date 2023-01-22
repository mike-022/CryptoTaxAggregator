import os, sys
import subprocess

sys.path.append(sys.path)

if __name__ == '__main__':
    subprocess.run(['python3', 'MergeTradeFiles.py'])
    subprocess.run(['python3', 'GroupBuysAndSellsByTaxMethod.py'])
    subprocess.run(['python3', 'CalculateCapitalGains.py'])
    subprocess.run(['python3', 'AggregateTransactions.py'])
