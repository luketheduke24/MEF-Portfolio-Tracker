from flask import Flask, render_template, Response
import concurrent.futures
import time
import yfinance as yf

app = Flask(__name__)

# Simulated portfolio value
Portfolio = [
{'ticker':'GOOG', 'shares':1.0}, 
{'ticker':'AAPL', 'shares':1.0},
{'ticker':'ARRY', 'shares':1.0},
{'ticker':'AZPN', 'shares':1.0}, 
{'ticker':'AY', 'shares':1.0}, 
{'ticker':'CG', 'shares':1.0},
{'ticker':'DKS', 'shares':1.0},
{'ticker':'LOCO', 'shares':1.0},
{'ticker':'EHC', 'shares':1.0},
{'ticker':'ES', 'shares':1.0},
{'ticker':'FMC', 'shares':1.0},
{'ticker':'FOXF', 'shares':1.0},
{'ticker':'GLPI', 'shares':1.0},
{'ticker':'GNTX', 'shares':1.0},
{'ticker':'GOOD', 'shares':1.0},
{'ticker':'GMED', 'shares':1.0},
{'ticker':'HGV', 'shares':1.0},
{'ticker':'HOLX', 'shares':1.0},
{'ticker':'ICE', 'shares':1.0},
{'ticker':'J', 'shares':1.0},
{'ticker':'JNJ', 'shares':1.0},
{'ticker':'JNPR', 'shares':1.0},
{'ticker':'MTZ', 'shares':1.0},
{'ticker':'OUT', 'shares':1.0},
{'ticker':'QLYS', 'shares':1.0},
{'ticker':'RS', 'shares':1.0},
{'ticker':'RVTY', 'shares':1.0},
{'ticker':'SRE', 'shares':1.0},
{'ticker':'SCI', 'shares':1.0},
{'ticker':'SHW', 'shares':1.0},
{'ticker':'SUM', 'shares':1.0},
{'ticker':'TFX', 'shares':1.0},
{'ticker':'TJX', 'shares':1.0},
{'ticker':'VRNT', 'shares':1.0},
{'ticker':'VST', 'shares':1.0},
{'ticker':'VOYA', 'shares':1.0},
{'ticker':'WAL', 'shares':1.0},
{'ticker':'ZI', 'shares':1.0}]



def position_value(stock):
   data = yf.Ticker(stock['ticker']).info
   return float(data['currentPrice'] * stock['shares'])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/liveportfoliovalue")
def update_portfolio_value():
    def generate():
        while True:
            value = 0
            with concurrent.futures.ProcessPoolExecutor(10) as executor:
                results = [executor.submit(position_value, stock) for stock in Portfolio]
                for result in concurrent.futures.as_completed(results):
                    value += result.result()
            print(value)
            yield f'data: {value:.02f}\n\n'
            time.sleep(100)

    return Response(generate(), content_type="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True)