#!/bin/bash

# source /home/ubuntu/scripts/religion/env/bin/activate
# cd /home/ubuntu/scripts/religion

# local
python main.py --env local --file fleet_sales.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --model price_model

python main.py --env local --file segmented_model.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --government Government --model segmented_model

python main.py --env local --file size_model.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --government Government --model size_model #--size Units 

python main.py --env local --file random.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --model price_model
