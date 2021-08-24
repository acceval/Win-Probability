import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import json

from Model import Model


model = Model('local')

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('list', type=list)


@app.route('/')
def hello():

	return jsonify('Welcome to Win Probability')

@app.route('/size_model', methods=['POST'])
def size_model():

	ABC = parser.parse_args()
	data_decoded = request.data.decode("utf-8")

	#convert to json
	data_json = json.loads(data_decoded)

	# print(data_json)

	if 'file' in data_json:
		file = data_json['file']
	else:
		file = ''

	if 'msrp' in  data_json:
		msrp = data_json['msrp']
	else:
		msrp = ''

	if 'unitcost' in  data_json:
		unitcost = data_json['unitcost']
	else:
		unitcost = ''

	if 'unitprice' in  data_json:
		unitprice = data_json['unitprice']
	else:
		unitprice = ''

	if 'win' in  data_json:
		win = data_json['win']
	else:
		win = ''

	if 'units' in  data_json:
		units = data_json['units']
	else:
		units = ''

	if 'government' in  data_json:
		government = data_json['government']
	else:
		government = ''


	if file!='' and msrp!='' and unitcost!='' and unitprice!='' and win!='' and units!='' and government!='':

		output = model.size_model(file,msrp,unitcost,unitprice,win,units,government)

		return jsonify(output)

	else:

		status = 0
		error = 'There is a problem on the parameters'
		data = None

		output = dict()
		output["status"] = status
		output["error"] = error
		output["data"] = None
		output = json.dumps(output)
		return jsonify(output)


@app.route('/segmented_model', methods=['POST'])
def segmented_model():

	ABC = parser.parse_args()
	data_decoded = request.data.decode("utf-8")

	#convert to json
	data_json = json.loads(data_decoded)

	# print(data_json)

	if 'file' in data_json:
		file = data_json['file']
	else:
		file = ''

	if 'msrp' in  data_json:
		msrp = data_json['msrp']
	else:
		msrp = ''

	if 'unitcost' in  data_json:
		unitcost = data_json['unitcost']
	else:
		unitcost = ''

	if 'unitprice' in  data_json:
		unitprice = data_json['unitprice']
	else:
		unitprice = ''

	if 'win' in  data_json:
		win = data_json['win']
	else:
		win = ''

	if 'units' in  data_json:
		units = data_json['units']
	else:
		units = ''

	if 'government' in  data_json:
		government = data_json['government']
	else:
		government = ''


	if file!='' and msrp!='' and unitcost!='' and unitprice!='' and win!='' and units!='' and government!='':

		output = model.segmented_model(file,msrp,unitcost,unitprice,win,units,government)

		return jsonify(output)

	else:

		status = 0
		error = 'There is a problem on the parameters'
		data = None

		output = dict()
		output["status"] = status
		output["error"] = error
		output["data"] = None
		output = json.dumps(output)
		return jsonify(output)


@app.route('/price_model', methods=['POST'])
def choice_model():

	ABC = parser.parse_args()
	data_decoded = request.data.decode("utf-8")

	#convert to json
	data_json = json.loads(data_decoded)


	# python main.py --env local --file fleet_sales.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --model price_model

	print(data_json)

	if 'file' in data_json:
		file = data_json['file']
	else:
		file = ''

	if 'msrp' in  data_json:
		msrp = data_json['msrp']
	else:
		msrp = ''

	if 'unitcost' in  data_json:
		unitcost = data_json['unitcost']
	else:
		unitcost = ''

	if 'unitprice' in  data_json:
		unitprice = data_json['unitprice']
	else:
		unitprice = ''

	if 'win' in  data_json:
		win = data_json['win']
	else:
		win = ''

	if 'units' in  data_json:
		units = data_json['units']
	else:
		units = ''


	if file!='' and msrp!='' and unitcost!='' and unitprice!='' and win!='' and units!='':

		output = model.price_model(file,msrp,unitcost,unitprice,win,units)

		return jsonify(output)

	else:

		status = 0
		error = 'There is a problem on the parameters'
		data = None

		output = dict()
		output["status"] = status
		output["error"] = error
		output["data"] = None
		output = json.dumps(output)
		return jsonify(output)



if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5050))
	app.run(host='0.0.0.0', port = port, debug=True)

	# local
	# app.run(host='127.0.0.1', port = port, debug=True)
