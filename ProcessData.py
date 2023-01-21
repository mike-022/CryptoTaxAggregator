import os, sys
import subprocess

sys.path.append(sys.path)

# list of scripts to call
scripts = [
    'MergeTradeFiles.py', 'GroupBuysAndSellsByTaxMethod.py',
    'CalculateCapitalGains.py', 'AggregateTransactions.py'
]

# loop through the list of scripts
for script in scripts:
    subprocess.run(['python3', script])
