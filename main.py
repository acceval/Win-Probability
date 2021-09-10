import os,sys,inspect,getopt,io
from pathlib import Path
import argparse

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from log import Log
import config, utils

import pandas as pd
import numpy as np
import json
import string

from Model import Model 


if __name__== '__main__':

	log = Log()		

	msg = __name__+'.'+utils.get_function_caller()
	log.print_(msg)


	start = utils.get_time()
	print(start)
	
	today = None

	# input files
	# player names
	# features 


	parser = argparse.ArgumentParser()	
	parser.add_argument("--env", "-e", help="State the environment", required=True)	
	parser.add_argument("--file", "-f", help="Specify path to input files", required=True)	
	parser.add_argument("--msrp", "-ms", help="Specify the MSRP feature.", required=True)	
	parser.add_argument("--unitcost", "-uc", help="Specify the unit cost.", required=True)	
	parser.add_argument("--unitprice", "-up", help="Specify the unit price.", required=True)	
	parser.add_argument("--win", "-w", help="Specify the win.", required=True)
	parser.add_argument("--units", "-u", help="Specify the units.", required=True)	
	parser.add_argument("--model", "-m", help="Specify the model.", required=True)	
	parser.add_argument("--government", "-g", help="Specify the government.", required=False)	
	parser.add_argument("--cons", "-c", help="Specify the constraint.", required=False)		
	parser.add_argument("--margin_threshold", "-t", help="Specify the constraint margin_threshold.", required=False)		

	# parser.add_argument("--size", "-s", help="Specify the size.", required=False)		
	args = parser.parse_args()

	env = 'local'
	if args.env is None:
		print("State the environment!!")
	else:
		env = args.env
	
	file = None
	if args.file is None:
		print("State the input file!!")
	else:
		file = args.file

	msrp = None
	if args.msrp is None:
		print("State the msrp!!")
	else:
		msrp = args.msrp

	unit_cost = None
	if args.unitcost is None:
		print("State the unitcost!!")
	else:
		unit_cost = args.unitcost

	unit_price = None
	if args.unitprice is None:
		print("State the unitprice!!")
	else:
		unit_price = args.unitprice

	win = None
	if args.win is None:
		print("State the win!!")
	else:
		win = args.win

	units = None
	if args.units is None:
		print("State the units!!")
	else:
		units = args.units

	model = None
	if args.model is None:
		print("State the model!!")
	else:
		model = args.model

	government = None
	if args.government is None:
		print("State the government!!")
	else:
		government = args.government

	cons = None
	if args.cons is None:
		print("State the constraint!!")
	else:
		cons = args.cons

	margin_threshold = None
	if args.margin_threshold is None:
		print("State the margin_threshold!!")
	else:
		margin_threshold = args.margin_threshold
	

	# size = None
	# if args.size is None:
	# 	print("State the size!!")
	# else:
	# 	size = args.size

	print('env:',env)
	print('file:',file)
	print('msrp:',msrp)
	print('unit_cost:',unit_cost)
	print('unit_price:',unit_price)
	print('win:',win)
	print('units:',units)
	print('model:',model)	
	print('government:',government)
	print('constraint:',cons)
	print('margin_threshold:',margin_threshold)	
	# print('size:',size)
	print('-------------------------------------------')
	
	if file is not None and msrp is not None and unit_cost is not None and unit_price is not None and win is not None and units is not None and model is not None:

		if model=='price_model':

			model = Model(env)		
			output = model.price_model(file,msrp,unit_cost,unit_price,win,units,cons,margin_threshold)
			print(type(output))
			print(output)		

		if model=='segmented_model':

			model = Model(env)		
			output = model.segmented_model(file,msrp,unit_cost,unit_price,win,units,government,cons,margin_threshold)
			print(type(output))
			print(output)		

		if model=='size_model':

			model = Model(env)		
			output = model.size_model(file,msrp,unit_cost,unit_price,win,units,government,cons,margin_threshold)
			print(type(output))
			print(output)		


			

	else:
		
		print('Error !!')



	print('-------------------------------------------')

	end = utils.get_time()
	print(end)

	print(end - start)


	msg = 'start:',start
	log.print_(msg)

	msg = 'end:',end
	log.print_(msg)

	msg = 'total:',end-start
	log.print_(msg)	
	