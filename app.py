from flask import Flask, Response, send_from_directory
from web3 import Web3
from time import sleep
from flask_cors import CORS

app = Flask(__name__, static_folder="./client/build/static")
CORS(app)


alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/91d8RE0MuWCIHIFye2RYykFcUtK5ROjK"
w3 = Web3(Web3.HTTPProvider(alchemy_url))
latest_block = w3.eth.block_number

def get_block_data(latest_block):
   
    # Get the latest block number
    transactions = latest_block['transactions']     
    transaction_list = []
    for t in transactions:
        transaction_data = {}

        transaction = w3.eth.get_transaction(t)
        value = transaction["value"]
        converted_to_eth = w3.from_wei(value, 'ether')
        transaction_data.update({"Block:": latest_block["number"], "To": transaction["to"], "From": transaction["from"], "Value (ETH)": converted_to_eth})

        transaction_list.append(transaction_data)
    return transaction_list


    # print(w3.is_connected())
    # block_data = get_block_data()
    # df = pd.DataFrame(block_data)
    # html_table = df.to_html(justify='left')

@app.route('/stream')
def stream():

    def get_data():
        while True:
            block = w3.eth.get_block('latest')
            transactions = get_block_data(block)
            # df = pd.DataFrame(transactions)
            yield f'data: {transactions} \n\n'
            sleep(10)
    return Response(get_data(),mimetype='text/event-stream')

@app.route('/')
def index():
    return send_from_directory('./client/build', 'index.html')

if __name__ == '__main__':
    app.run(port=5001)