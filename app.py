from flask import Flask, render_template, Response
import concurrent.futures
import time
from datetime import datetime
import yfinance as yf

app = Flask(__name__)


Portfolio = [
{'ticker':'GOOG', 'shares':200.0}, 
{'ticker':'AAPL', 'shares':100.0},
{'ticker':'ARRY', 'shares':550.0},
{'ticker':'AZPN', 'shares':23.0}, 
{'ticker':'AY', 'shares':200.0}, 
{'ticker':'CRL', 'shares':41.0},
{'ticker':'DKS', 'shares':120.0},
{'ticker':'LOCO', 'shares':500.0},
{'ticker':'EHC', 'shares':112.0},
{'ticker':'ES', 'shares':91.0},
{'ticker':'FMC', 'shares':70.0},
{'ticker':'FOXF', 'shares':90.0},
{'ticker':'GLPI', 'shares':260.0},
{'ticker':'GNTX', 'shares':280.0},
{'ticker':'GOOD', 'shares':724.0},
{'ticker':'GMED', 'shares':145.0},
{'ticker':'HGV', 'shares':180.0},
{'ticker':'HOLX', 'shares':130.0},
{'ticker':'ICE', 'shares':50.0},
{'ticker':'J', 'shares':75.0},
{'ticker':'JNJ', 'shares':36.0},
{'ticker':'JNPR', 'shares':230.0},
{'ticker':'MTZ', 'shares':140.0},
{'ticker':'OUT', 'shares':640.0},
{'ticker':'QLYS', 'shares':85.0},
{'ticker':'RS', 'shares':70.0},
{'ticker':'RVTY', 'shares':70.0},
{'ticker':'SRE', 'shares':40.0},
{'ticker':'SCI', 'shares':130.0},
{'ticker':'SWK', 'shares':47.0},
{'ticker':'SUM', 'shares':406.0},
{'ticker':'TFX', 'shares':22.0},
{'ticker':'CG', 'shares':270.0},
{'ticker':'SHW', 'shares':37.0},
{'ticker':'TJX', 'shares':202.0},
{'ticker':'VRNT', 'shares':140.0},
{'ticker':'VST', 'shares':200.0},
{'ticker':'VOYA', 'shares':65.0},
{'ticker':'WAL', 'shares':70.0},
{'ticker':'ZI', 'shares':320.0}]

def current_position_value(stock):
   data = yf.Ticker(stock['ticker']).info
   return float(data['currentPrice'] * stock['shares'])

def opening_position_value(stock):
   data = yf.Ticker(stock['ticker']).info
   return float(data['previousClose'] * stock['shares'])

def style(current_value, abs_change, per_change):
    current_value = "{:,.2f}".format(float(current_value))
    if abs_change < 0:
        abs_change = f'-{"{:,.2f}".format(float(abs_change))}'
        per_change = f'-{"{:.2f}".format(float(per_change))}%'
    else:
        abs_change = f'+{"{:,.2f}".format(float(abs_change))}'
        per_change = f'+{"{:.2f}".format(float(per_change))}%'
    return current_value, abs_change, per_change

def opening_thread():
    opening_value = 18589.21
    with concurrent.futures.ProcessPoolExecutor(10) as executor:
        results = [executor.submit(opening_position_value, stock) for stock in Portfolio]
        for result in concurrent.futures.as_completed(results):
            opening_value += result.result()
    return opening_value

def current_thread():
    current_value = 18589.21
    with concurrent.futures.ProcessPoolExecutor(10) as executor:
        results = [executor.submit(current_position_value, stock) for stock in Portfolio]
        for result in concurrent.futures.as_completed(results):
            current_value += result.result()
    return current_value

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/liveportfoliovalue")
def update_portfolio_value():
    def generate():
        while True:
            executors_list = []
            with concurrent.futures.ProcessPoolExecutor(10) as executor:
                executors_list.append(executor.submit(opening_thread))
                executors_list.append(executor.submit(current_thread))
    
            opening_value = executors_list[0].result()
            current_value = executors_list[1].result()

            abs_change = float(current_value - opening_value)
            per_change = float(((current_value - opening_value)/current_value)*100)

            current_value, abs_change, per_change = style(current_value, abs_change, per_change)

            yield f'data: {{"value": "{current_value}", "asof": "{datetime.now().replace(microsecond=0).strftime("%I:%M:%S %p")}", "abs_change":"{abs_change} ({per_change})"}}\n\n'
            time.sleep(10)

    return Response(generate(), content_type='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)