import os
import pytest
import json
import requests
import config
from config import var
from Model import Model 
from app import app

env = 'prod'

# default vars
file = 'size_model.csv'
msrp = 'MSRP'
unit_cost = 'Unit_Cost'
unit_price = 'Unit_Price'
win = 'Win'
units = 'Units'
government = 'Government'
cons = 'prob > 0.8'
margin_threshold = 50


# local url
url = config.LOCAL_URL
# url = config.HEROKU_URL


def test_price_model(app, client):

    
    function = 'price_model' 
    url_ = url+function 
    data = '{"file" :"'+str(file)+'", "msrp":"'+str(msrp)+'", "unitcost":"'+str(unit_cost)+'", "unitprice":"'+str(unit_price)+'", "win":"'+str(win)+'", "units":"'+units+'"}'
    data = data.replace("'",'"')

    send_request = client.post(url_, data=data, follow_redirects=True)    

    assert send_request.status_code == 200

def test_segmented_model(app, client):

    
    function = 'segmented_model' 
    url_ = url+function 
    data = '{"file" :"'+str(file)+'", "msrp":"'+str(msrp)+'", "unitcost":"'+str(unit_cost)+'", "unitprice":"'+str(unit_price)+'", "win":"'+str(win)+'", "units":"'+units+'", "government":"'+str(government)+'","cons":"'+str(cons)+'","margin_threshold":"'+str(margin_threshold)+'"}'
    data = data.replace("'",'"')

    send_request = client.post(url_, data=data, follow_redirects=True)    

    assert send_request.status_code == 200


def test_size_model(app, client):

    
    function = 'size_model' 
    url_ = url+function 
    data = '{"file" :"'+str(file)+'", "msrp":"'+str(msrp)+'", "unitcost":"'+str(unit_cost)+'", "unitprice":"'+str(unit_price)+'", "win":"'+str(win)+'", "units":"'+units+'", "government":"'+str(government)+'","cons":"'+str(cons)+'","margin_threshold":"'+str(margin_threshold)+'"}'
    data = data.replace("'",'"')

    send_request = client.post(url_, data=data, follow_redirects=True)    

    assert send_request.status_code == 200

