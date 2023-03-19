# ethsentinel
A simple web-app for monitoring transactions on the latest Ethereum block.

Getting started:

Clone the repo
`git clone https://github.com/amurshak/ethsentinel.git`

Cd into the root directory
`cd ethsentinel`

Create, then activate, the local virtual environment
`python3 venv env`
`source ./env/bin/activate`

Install dependencies
`pip3 install -r requirements.txt`
`cd ./client`
`npm install`

Set environment variables:

`export FLASK_DEBUG=true`
`export FLASK_ENV=development`
`export FLASK_APP=app.py`
`export SECRET_KEY='XXXXXXXXXXXXXXX'`
`export ALCHEMY_API_KEY='XXXXXXXXXXXXXXX'`
`export COINMARKETCAP_API_KEY='XXXXXXXXXXXXXXX'`