#!/bin/bash

# source /home/ubuntu/scripts/religion/env/bin/activate
# cd /home/ubuntu/scripts/religion

# local
# python main.py --env local --file fleet_sales.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --model price_model 

# python main.py --env local --file fleet_sales.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --model price_model --margin_threshold 50

# python main.py --env local --file fleet_sales.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --model price_model --cons "prob > 0.6" --margin_threshold 50

# python main.py --env local --file fleet_sales.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --model price_model --cons "prob > 0.6" 

# python main.py --env local --file segmented_model.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --government Government --model segmented_model --cons "prob > 0.75" --margin_threshold 50

# python main.py --env local --file segmented_model.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --government Government --model segmented_model --cons "prob > 0.75" 

# python main.py --env local --file size_model.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --government Government --model size_model --cons "prob > 0.8" --margin_threshold 50 #--size Units  

# python main.py --env local --file size_model.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --government Government --model size_model --cons "prob > 0.8" 

# python main.py --env local --file random.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --model price_model

# python main.py --env local --file segmented_model.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --model price_model --government Government --model segmented_model --cons "i > you" --margin_threshold "123"

python main.py --env local --file segmented_model.csv --msrp MSRP --unitcost Unit_Cost --unitprice Unit_Price --win Win --units Units --model price_model --government Government --model segmented_model --cons "prob > 0.8" --margin_threshold "123"
