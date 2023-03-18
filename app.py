from flask import Flask, Response, send_from_directory
from web3 import Web3
import json
from time import sleep
from flask_cors import CORS
from decimal import Decimal

app = Flask(__name__, static_folder="./client/build/static")
CORS(app)
app.config['FLASK_DEBUG'] = os.getenv('FLASK_DEBUG')
app.secret_key = os.getenv('APP_SECRET_KEY')


ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY')
alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/" + ALCHEMY_API_KEY
w3 = Web3(Web3.HTTPProvider(alchemy_url))
latest_block = w3.eth.block_number


COINMARKETCAP_API_KEY = os.getenv('COINMARKETCAP_API_KEY')
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  'symbol': 'ETH'
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
}

# session = Session()
# session.headers.update(headers)


def get_eth_pricing():
    try:
        response = requests.get(url, headers=headers, params=parameters)
        eth_price = response.json()['data']['ETH']['quote']['USD']['price']
        print(f"The current Ethereum price is {eth_price: .2f} USD.")
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    return eth_price


def get_block_data(latest_block):
   
    # Get the latest block number
    transactions = latest_block['transactions']     
    transaction_list = []
    eth_price = get_eth_pricing()
    for t in transactions:
        transaction_data = {}

        transaction = w3.eth.get_transaction(t)
        value = transaction["value"]

        converted_to_eth = float(w3.from_wei(value, 'ether'))
        converted_to_usd = float(w3.from_wei(value, 'ether') * Decimal(eth_price))

        transaction_data.update({"Block": latest_block["number"], "To": transaction["to"], "From": transaction["from"], "Eth": converted_to_eth, "Usd": converted_to_usd})

        transaction_list.append(transaction_data)
    return transaction_list


@app.route('/stream')
def stream():

    def get_data():
        while True:
            block = w3.eth.get_block('latest')
            try:
                transactions = get_block_data(block)
                trans = json.dumps(transactions)
                yield f'data: {trans} \n\n'
            except Exception as e:
                print(e)
                pass

            # df = pd.DataFrame(transactions)
            
            
            sleep(10)
    return Response(get_data(),mimetype='text/event-stream')

@app.route('/')
def index():
    return send_from_directory('./client/build', 'index.html')

if __name__ == '__main__':
    app.run(port=5001)