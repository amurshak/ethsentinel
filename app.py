import os
import json
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from decimal import Decimal
from time import sleep
from web3 import Web3
from flask import Flask, Response, send_from_directory
from flask_cors import CORS

#Initialize app and configuration
app = Flask(__name__, static_folder="./client/build/static")
CORS(app)
app.config['FLASK_DEBUG'] = os.getenv('FLASK_DEBUG')
app.secret_key = os.getenv('APP_SECRET_KEY')

#Get API keys from local environment
ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY')
WEBSOCKET_URI = os.getenv('ALCHEMY_WEBSOCKETS_URI')
COINMARKETCAP_API_KEY = os.getenv('COINMARKETCAP_API_KEY')

#Establish Alchemy connection
ALCHEMY_URL = "https://eth-mainnet.g.alchemy.com/v2/" + ALCHEMY_API_KEY
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))


#Set up request for CoinMarketCap
coinmarket_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  'symbol': 'ETH'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
}


#For retrieving pricing information from CoinMarketCap
def get_eth_pricing():
    try:
        response = requests.get(coinmarket_url, headers=headers, params=parameters)
        eth_price = response.json()['data']['ETH']['quote']['USD']['price']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    return eth_price


#For extracting and sorting latest block data
def get_block_data(latest_block):
    
    transaction_list = []
    
    # Get all block transactions
    transactions = latest_block['transactions']
    #Get current ETH pricing
    eth_price = get_eth_pricing()
    count = 0
    for t in transactions:
        transaction_data = {}
        if count == 0:
            print(t)
            count +=1
        transaction = w3.eth.get_transaction(t)
        value = transaction["value"]

        #Convert current value from Wei to ETH & USD
        converted_to_eth = float(w3.from_wei(value, 'ether'))
        converted_to_usd = float(w3.from_wei(value, 'ether') * Decimal(eth_price))
        
        #Create new transaction dictionary to append to list
        transaction_data.update({"Block": latest_block["number"], "To": transaction["to"], "From": transaction["from"], "Eth": converted_to_eth, "Usd": converted_to_usd})
        transaction_list.append(transaction_data)
        
    return transaction_list


#For streaming data from new blocks
@app.route('/stream', methods=['GET', 'POST'])
def stream():

    def get_data():
        while True:
            #Fetch latest block
            try:
                block = w3.eth.get_block('latest')
            except Exception as e:
                print(e)
                pass
            #Format latest block data, send as JSON
            try:
                transactions = get_block_data(block)
                json_transactions = json.dumps(transactions)
                yield f'data: {json_transactions} \n\n'
            except Exception as e:
                print(e)
                pass
 
            sleep(10)

    return Response(get_data(),mimetype='text/event-stream')


@app.route('/', methods=['GET'])
def index():
    return send_from_directory('./client/build', 'index.html')

if __name__ == '__main__':
    app.run()