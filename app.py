from flask import Flask, jsonify
from web3 import Web3, IPCProvider
import pandas as pd 
import time

app = Flask(__name__)

alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/91d8RE0MuWCIHIFye2RYykFcUtK5ROjK"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# def get_block_data(latest_block):
   
#     # Get the latest block number
#     transactions = latest_block['transactions']     
#     transaction_list = []
#     for t in transactions:
#         transaction_data = {}

#         transaction = w3.eth.get_transaction(t)
#         value = transaction["value"]
#         converted_to_eth = w3.from_wei(value, 'ether')
#         transaction_data.update({"Block:": latest_block["number"], "To": transaction['to'], "From": transaction["from"], "Value (ETH)": converted_to_eth})

#         transaction_list.append(transaction_data)
#     return transaction_list

def get_transactions(block_number):
    block = w3.eth.get_block(block_number)
    transactions = []
    for tx in block.transactions:
        tx_data = w3.eth.get_transaction(tx)
        tx_info = {
            'hash': tx.hex(),
            'from': tx_data['from'],
            'to': tx_data['to'],
            'value': w3.fromWei(tx_data['value'], 'ether'),
            'gas_price': tx_data['gasPrice'],
            'gas_used': tx_data['gas'],
            'nonce': tx_data['nonce'],
        }
        transactions.append(tx_info)
    return transactions


@app.route('/')
def hello_world():
    block_data = get_block_data()
    df = pd.DataFrame(block_data)
    html_table = df.to_html(justify='left')
    
    return html_table

if __name__ == '__main__':
    app.run()