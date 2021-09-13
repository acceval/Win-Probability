import os
import pytest
from Model import Model 
import json
import requests
from config import var
import pandas as pd

env = 'prod'

# default vars
file = var[env]['file']
msrp = var[env]['msrp']
unit_cost = var[env]['unit_cost']
unit_price = var[env]['unit_price']
win = var[env]['win']
units = var[env]['units']
government = var[env]['government']
cons = var[env]['cons']
margin_threshold = var[env]['margin_threshold']

model = Model(env)      
    

# happy path
def test_price_model():

    output = model.price_model(file,msrp,unit_cost,unit_price,win,units)
    print(type(output))
    print(output)       
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''

    assert len(output_json['data'][0])==4

    assert 'parameters' in output_json['data'][0].keys()    
    assert 'constraint' in output_json['data'][0].keys()
    assert 'margin_threshold' in output_json['data'][0].keys()
    assert 'suggestion' in output_json['data'][0].keys()

    assert len(output_json['data'][0]['parameters'].keys()) == 2
    assert len(output_json['data'][0]['suggestion'].keys()) == 4

def test_price_model_cons():

    output = model.price_model(file,msrp,unit_cost,unit_price,win,units,cons)
    print(type(output))
    print(output)       
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''
    
    assert len(output_json['data'][0])==4

    assert 'parameters' in output_json['data'][0].keys()    
    assert 'constraint' in output_json['data'][0].keys()
    assert 'margin_threshold' in output_json['data'][0].keys()
    assert 'suggestion' in output_json['data'][0].keys()


    assert len(output_json['data'][0]['parameters'].keys()) == 2
    assert len(output_json['data'][0]['suggestion'].keys()) == 4

def test_price_model_cons_margin_threshold():

    output = model.price_model(file,msrp,unit_cost,unit_price,win,units,cons,margin_threshold)
    print(type(output))
    print(output)       
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''
    
    assert len(output_json['data'][0])==4

    assert 'parameters' in output_json['data'][0].keys()    
    assert 'constraint' in output_json['data'][0].keys()
    assert 'margin_threshold' in output_json['data'][0].keys()
    assert 'suggestion' in output_json['data'][0].keys()


    assert len(output_json['data'][0]['parameters'].keys()) == 2
    assert len(output_json['data'][0]['suggestion'].keys()) == 4

    

def test_segmented_model():

    file = 'https://raw.githubusercontent.com/acceval/Win-Probability/main/segmented_model.csv'
    output = model.segmented_model(file,msrp,unit_cost,unit_price,win,units,government)
    print(type(output))
    print(output)       
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''

    assert len(output_json['data'][0])==2

    assert 'parameters' in output_json['data'][0]['government'].keys()    
    assert 'constraint' in output_json['data'][0]['government'].keys()
    assert 'margin_threshold' in output_json['data'][0]['government'].keys()
    assert 'suggestion' in output_json['data'][0]['government'].keys()

    assert 'parameters' in output_json['data'][0]['corporate'].keys()    
    assert 'constraint' in output_json['data'][0]['corporate'].keys()
    assert 'margin_threshold' in output_json['data'][0]['corporate'].keys()
    assert 'suggestion' in output_json['data'][0]['corporate'].keys()

    assert 'government' in output_json['data'][0].keys()
    assert 'corporate' in output_json['data'][0].keys()

    assert len(output_json['data'][0]['government'].keys())==4
    assert len(output_json['data'][0]['corporate'].keys())==4

    assert len(output_json['data'][0]['government']['parameters']) == 2
    assert len(output_json['data'][0]['corporate']['parameters']) == 2


def test_segmented_model_cons():

    file = 'https://raw.githubusercontent.com/acceval/Win-Probability/main/segmented_model.csv'
    output = model.segmented_model(file,msrp,unit_cost,unit_price,win,units,government,cons)
    print(type(output))
    print(output)       
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''

    assert len(output_json['data'][0])==2

    assert 'parameters' in output_json['data'][0]['government'].keys()    
    assert 'constraint' in output_json['data'][0]['government'].keys()
    assert 'margin_threshold' in output_json['data'][0]['government'].keys()
    assert 'suggestion' in output_json['data'][0]['government'].keys()

    assert 'parameters' in output_json['data'][0]['corporate'].keys()    
    assert 'constraint' in output_json['data'][0]['corporate'].keys()
    assert 'margin_threshold' in output_json['data'][0]['corporate'].keys()
    assert 'suggestion' in output_json['data'][0]['corporate'].keys()

    assert 'government' in output_json['data'][0].keys()
    assert 'corporate' in output_json['data'][0].keys()

    assert len(output_json['data'][0]['government'].keys())==4
    assert len(output_json['data'][0]['corporate'].keys())==4

    assert len(output_json['data'][0]['government']['parameters'])==2
    assert len(output_json['data'][0]['corporate']['parameters'])==2

def test_segmented_model_cons_margin_threshold():

    file = 'https://raw.githubusercontent.com/acceval/Win-Probability/main/segmented_model.csv'
    output = model.segmented_model(file,msrp,unit_cost,unit_price,win,units,government,cons,margin_threshold)
    print(type(output))
    print(output)       
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''

    assert len(output_json['data'][0])==2

    assert 'parameters' in output_json['data'][0]['government'].keys()    
    assert 'constraint' in output_json['data'][0]['government'].keys()
    assert 'margin_threshold' in output_json['data'][0]['government'].keys()
    assert 'suggestion' in output_json['data'][0]['government'].keys()

    assert 'parameters' in output_json['data'][0]['corporate'].keys()    
    assert 'constraint' in output_json['data'][0]['corporate'].keys()
    assert 'margin_threshold' in output_json['data'][0]['corporate'].keys()
    assert 'suggestion' in output_json['data'][0]['corporate'].keys()

    assert 'government' in output_json['data'][0].keys()
    assert 'corporate' in output_json['data'][0].keys()

    assert len(output_json['data'][0]['government'].keys())==4
    assert len(output_json['data'][0]['corporate'].keys())==4

    assert len(output_json['data'][0]['government']['parameters'])==2
    assert len(output_json['data'][0]['corporate']['parameters'])==2



def test_size_model():

    file = 'https://raw.githubusercontent.com/acceval/Win-Probability/main/size_model.csv'
    output = model.size_model(file,msrp,unit_cost,unit_price,win,units,government)
    print(type(output))
    print(output)       
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''

    assert len(output_json['data'][0])==2

    assert 'parameters' in output_json['data'][0]['government'].keys()    
    assert 'constraint' in output_json['data'][0]['government'].keys()
    assert 'margin_threshold' in output_json['data'][0]['government'].keys()
    assert 'suggestion' in output_json['data'][0]['government'].keys()

    assert 'parameters' in output_json['data'][0]['corporate'].keys()    
    assert 'constraint' in output_json['data'][0]['corporate'].keys()
    assert 'margin_threshold' in output_json['data'][0]['corporate'].keys()
    assert 'suggestion' in output_json['data'][0]['corporate'].keys()


    assert 'government' in output_json['data'][0].keys()
    assert 'corporate' in output_json['data'][0].keys()

    assert len(output_json['data'][0]['government'].keys())==4
    assert len(output_json['data'][0]['corporate'].keys())==4

    assert len(output_json['data'][0]['government']['parameters'])==3
    assert len(output_json['data'][0]['corporate']['parameters'])==3


def test_size_model_cons():

    file = 'https://raw.githubusercontent.com/acceval/Win-Probability/main/size_model.csv'
    output = model.size_model(file,msrp,unit_cost,unit_price,win,units,government,cons)
    print(type(output))
    print(output)       
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''

    assert len(output_json['data'][0])==2
    
    assert 'parameters' in output_json['data'][0]['government'].keys()    
    assert 'constraint' in output_json['data'][0]['government'].keys()
    assert 'margin_threshold' in output_json['data'][0]['government'].keys()
    assert 'suggestion' in output_json['data'][0]['government'].keys()

    assert 'parameters' in output_json['data'][0]['corporate'].keys()    
    assert 'constraint' in output_json['data'][0]['corporate'].keys()
    assert 'margin_threshold' in output_json['data'][0]['corporate'].keys()
    assert 'suggestion' in output_json['data'][0]['corporate'].keys()


    assert 'government' in output_json['data'][0].keys()
    assert 'corporate' in output_json['data'][0].keys()

    assert len(output_json['data'][0]['government'].keys())==4
    assert len(output_json['data'][0]['corporate'].keys())==4

    assert len(output_json['data'][0]['government']['parameters'])==3
    assert len(output_json['data'][0]['corporate']['parameters'])==3


def test_size_model_cons_margin_threshold():

    file = 'https://raw.githubusercontent.com/acceval/Win-Probability/main/size_model.csv'
    output = model.size_model(file,msrp,unit_cost,unit_price,win,units,government,cons,margin_threshold)
    print(type(output))
    print(output)       
    
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''

    assert len(output_json['data'][0])==2
    
    assert 'parameters' in output_json['data'][0]['government'].keys()    
    assert 'constraint' in output_json['data'][0]['government'].keys()
    assert 'margin_threshold' in output_json['data'][0]['government'].keys()
    assert 'suggestion' in output_json['data'][0]['government'].keys()

    assert 'parameters' in output_json['data'][0]['corporate'].keys()    
    assert 'constraint' in output_json['data'][0]['corporate'].keys()
    assert 'margin_threshold' in output_json['data'][0]['corporate'].keys()
    assert 'suggestion' in output_json['data'][0]['corporate'].keys()


    assert 'government' in output_json['data'][0].keys()
    assert 'corporate' in output_json['data'][0].keys()

    assert len(output_json['data'][0]['government'].keys())==4
    assert len(output_json['data'][0]['corporate'].keys())==4

    assert len(output_json['data'][0]['government']['parameters'])==3
    assert len(output_json['data'][0]['corporate']['parameters'])==3



# sad path

def test_file():

    output = model.price_model('file.csv',msrp,unit_cost,unit_price,win,units)

    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    output = model.segmented_model('file.csv',msrp,unit_cost,unit_price,win,units,government)
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    output = model.segmented_model('file.csv',msrp,unit_cost,unit_price,win,units,government)
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''



def test_msrp():

    file = 'https://raw.githubusercontent.com/acceval/Win-Probability/main/fleet_sales.csv'
    output = model.price_model(file,'msrp',unit_cost,unit_price,win,units)

    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    file = 'https://raw.githubusercontent.com/acceval/Win-Probability/main/segmented_model.csv'
    output = model.segmented_model(file,'msrp',unit_cost,unit_price,win,units,government)
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    file = 'https://raw.githubusercontent.com/acceval/Win-Probability/main/size_model.csv'
    output = model.segmented_model(file,'msrp',unit_cost,unit_price,win,units,government)
    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''
    
    
def test_unit_cost():

    output = model.price_model(file,msrp,'unit_cost',unit_price,win,units)

    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    output = model.segmented_model('segmented_model.csv',msrp,'unit_cost',unit_price,win,units,government)
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    output = model.segmented_model('size_model.csv',msrp,'unit_cost',unit_price,win,units,government)
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''
    
    
def test_unit_price():

    output = model.price_model(file,msrp,unit_cost,'unit_price',win,units)

    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    output = model.segmented_model('segmented_model.csv',msrp,unit_cost,'unit_price',win,units,government)
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    output = model.segmented_model('size_model.csv',msrp,unit_cost,'unit_price',win,units,government)
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''
    
    

def test_win():

    output = model.price_model(file,msrp,unit_cost,unit_price,'win',units)

    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    output = model.segmented_model('segmented_model.csv',msrp,unit_cost,unit_price,'win',units,government)
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    output = model.segmented_model('size_model.csv',msrp,unit_cost,unit_price,'win',units,government)
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''
    
    

def test_units():

    output = model.price_model(file,msrp,unit_cost,unit_price,win,'units')

    assert isinstance(output, str)

    output_json = json.loads(output)
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    output = model.segmented_model('segmented_model.csv',msrp,unit_cost,unit_price,win,'units',government)
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    output = model.segmented_model('size_model.csv',msrp,unit_cost,unit_price,win,'units',government)
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''
    

def test_government():

    output = model.segmented_model('segmented_model.csv',msrp,unit_cost,unit_price,win,units,'gov')
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    output = model.segmented_model('size_model.csv',msrp,unit_cost,unit_price,win,units,'gov')
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    output = model.segmented_model('segmented_model.csv',msrp,unit_cost,unit_price,win,units,['gov'])
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    output = model.segmented_model('size_model.csv',msrp,unit_cost,unit_price,win,units,['gov'])
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''
    

def test_cons():

    output = model.segmented_model('segmented_model.csv',msrp,unit_cost,unit_price,win,units,government,'cons')
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

    output = model.segmented_model('segmented_model.csv',msrp,unit_cost,unit_price,win,units,government,['cons'])
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    output = model.segmented_model('segmented_model.csv',msrp,unit_cost,unit_price,win,units,government,'abc 2 3')
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''

def test_margin_threshold():

    output = model.segmented_model('segmented_model.csv',msrp,unit_cost,unit_price,win,units,government,cons,'123')
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==1
    assert output_json['error'] is None or output_json['error'] == ''

    output = model.segmented_model('segmented_model.csv',msrp,unit_cost,unit_price,win,units,government,cons,['123'])
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''


    output = model.segmented_model('segmented_model.csv',msrp,unit_cost,unit_price,win,units,government,cons,'abc')
    assert isinstance(output, str)

    output_json = json.loads(output)    
    assert isinstance(output_json, dict)

    assert output_json['status']==0
    assert output_json['error'] is not None or output_json['error'] != ''
    

