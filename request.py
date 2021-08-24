import requests
import json
import config, utils
from config import var
import argparse
from pathlib import Path
import curlify
from Model import Model 

	
def curl_request(url,method,headers,payloads):
    # construct the curl command from request
    command = "curl -v -H {headers} {data} -X {method} {uri}"
    data = "" 
    if payloads:
        payload_list = ['"{0}":"{1}"'.format(k,v) for k,v in payloads.items()]
        data = " -d '{" + ", ".join(payload_list) + "}'"
    header_list = ['"{0}: {1}"'.format(k, v) for k, v in headers.items()]
    header = " -H ".join(header_list)
    print(command.format(method=method, headers=header, data=data, uri=url))



if __name__ == '__main__':

	# local url
	url = config.LOCAL_URL
	# url = config.HEROKU_URL
	# url = config.DEV_URL

	method = 'POST'
	headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

	env = 'prod'

	# default vars
	file = 'https://raw.githubusercontent.com/acceval/Win-Probability/main/fleet_sales.csv'
	msrp = 'MSRP'
	unit_cost = 'Unit_Cost'
	unit_price = 'Unit_Price'
	win = 'Win'
	units = 'Units'
	government = 'Government'

	function = 'price_model' 
	url_ = url+function 

	data = '{"file" :"'+str(file)+'", "msrp":"'+str(msrp)+'", "unitcost":"'+str(unit_cost)+'", "unitprice":"'+str(unit_price)+'", "win":"'+str(win)+'", "units":"'+units+'"}'
	data = data.replace("'",'"')
	data_json = json.loads(data)

	print(url_,	data)

	send_request = requests.post(url_, data, headers=headers, verify=False)

	print(curlify.to_curl(send_request.request))

	if send_request.status_code == 200:

		print(send_request.json())
	else:
		print('There is an error occurs')


	print('==================================================================================================')

	
	file = 'https://raw.githubusercontent.com/acceval/Win-Probability/main/segmented_model.csv'

	function = 'segmented_model' 
	url_ = url+function 

	data = '{"file" :"'+str(file)+'", "msrp":"'+str(msrp)+'", "unitcost":"'+str(unit_cost)+'", "unitprice":"'+str(unit_price)+'", "win":"'+str(win)+'", "units":"'+units+'", "government":"'+str(government)+'"}'
	data = data.replace("'",'"')
	data_json = json.loads(data)

	print(url_,	data)

	send_request = requests.post(url_, data, headers=headers, verify=False)

	print(curlify.to_curl(send_request.request))

	if send_request.status_code == 200:

		print(send_request.json())
	else:
		print('There is an error occurs')


	print('==================================================================================================')

	file = 'https://raw.githubusercontent.com/acceval/Win-Probability/main/size_model.csv'

	function = 'size_model' 
	url_ = url+function 

	data = '{"file" :"'+str(file)+'", "msrp":"'+str(msrp)+'", "unitcost":"'+str(unit_cost)+'", "unitprice":"'+str(unit_price)+'", "win":"'+str(win)+'", "units":"'+units+'", "government":"'+str(government)+'"}'
	data = data.replace("'",'"')
	data_json = json.loads(data)

	print(url_,	data)

	send_request = requests.post(url_, data, headers=headers, verify=False)

	print(curlify.to_curl(send_request.request))

	if send_request.status_code == 200:

		print(send_request.json())
	else:
		print('There is an error occurs')

	

