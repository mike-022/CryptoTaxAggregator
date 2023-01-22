from flask import Flask, request, send_file, Response
from celery import Celery
import subprocess
import pandas as pd
import MergeTradeFiles
import GroupBuysAndSellsByTaxMethod
import CalculateCapitalGains
import AggregateTransactions
import zipfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
celery = Celery('tasks', broker='redis://localhost:6379/0')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files')
    tax_method = "HIFO" 

    file_dfs = []
    for file in files:
        df = pd.read_csv(file)
        file_dfs.append(df)
    cap_gains_by_year_dfs = process_csv(file_dfs,tax_method)

    i=0
    with zipfile.ZipFile('CapitalGains1.zip', 'w') as zf:
        for df in cap_gains_by_year_dfs:
            df.to_csv('sample' + str(i) + '.csv',
                index=None,
                sep=",",
                header=True,
                encoding='utf-8-sig')
            zf.write('sample' + str(i) + '.csv')
            i+=1

    return Response(
        open('CapitalGains1.zip', 'rb'),
        mimetype='application/zip',
        headers={'Content-disposition': 'attachment; filename=CapitalGains.zip'})



@celery.task
def process_csv(trade_dfs,tax_method):
    print("processing...")
    merged_df = MergeTradeFiles.processTradeDataFrames(trade_dfs)

    buys_df, sells_df = GroupBuysAndSellsByTaxMethod.separate_transactions(
        merged_df,
        tax_method)
    short_gains_df,long_gains_df = CalculateCapitalGains.calculateCaptitalGains(buys_df, sells_df)
    cap_gains_by_year_dfs = AggregateTransactions.calculateCapitalGainsFilesByYear(
        short_gains_df, long_gains_df)
    return cap_gains_by_year_dfs

# callback function
@celery.task
def print_result(result):
    print(result)


if __name__ == '__main__':
    subprocess.call(['python3', '-m', 'celery', '-A', '__main__.celery', 'worker', '--loglevel=info'])
    app.run(debug=True)
