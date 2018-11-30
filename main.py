from flask import Flask,render_template
import json,urllib.request
from alpha_vantage.timeseries import TimeSeries
from helpers import getStockClusters

ts = TimeSeries(key='YOUR_API_KEY', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')

app = Flask(__name__)

@app.route("/")
def landingPage():
    return "Landing Page"

@app.route("/stocks/<symbol>")
def stocksForSymbol(symbol):
    #data = urllib.request.urlopen("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=full&apikey=GZ78DWYK4UQOVQ83").read()
    #output = json.loads(data)
    #print(output)
    clusters=getStockClusters(symbol);
    print(clusters);
    return render_template('index.html', title='Home', symbol=symbol,output=clusters);
