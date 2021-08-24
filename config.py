import os

## SERVER
# PATH_TO_FOLDER = '/home/cst/Jixie/source code/unit_forecasting/'
PATH_TO_FOLDER = str(os.getcwd())+'/'


VERSION = '0.1.0'

RANDOM_STATE = 42

DEFAULT_ZERO = 0.0000001
CONS = 5
INC = 0.01

LOCAL_URL = 'http://127.0.0.1:5050/'
HEROKU_URL = 'https://choice-model.herokuapp.com/'
DEV_URL = 'http://office.smarttradzt.com:8080/'


# env: local
# file: size_model.csv
# msrp: MSRP
# unit_cost: Unit_Cost
# unit_price: Unit_Price
# win: Win
# units: Units
# model: size_model
# government: Government
# size: Units


var = {}

var['local'] = {}
var['local']['file'] = 'fleet_sales.csv'
var['local']['msrp'] = 'MSRP'
var['local']['unit_cost'] = 'Unit_Cost'
var['local']['unit_price'] = 'Unit_Price'
var['local']['win'] = 'Win'
var['local']['units'] = 'Units'
var['local']['government'] = 'Government'

 

var['prod'] = {}
var['prod']['file'] = 'https://raw.githubusercontent.com/acceval/Win-Probability/main/fleet_sales.csv'
var['prod']['msrp'] = 'MSRP'
var['prod']['unit_cost'] = 'Unit_Cost'
var['prod']['unit_price'] = 'Unit_Price'
var['prod']['win'] = 'Win'
var['prod']['units'] = 'Units'
var['prod']['government'] = 'Government'