import os,sys,inspect,getopt,io 
from pathlib import Path
import argparse

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


from log import Log
import config, utils

import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import json
import string
from scipy.optimize import minimize

class Model:

	def __init__(self, env):

		self.log = Log()		

		self.env = env


	def data_cleaning(self,dataframe:pd.DataFrame):

		for col in dataframe.columns:
    
		    dataframe[col] = dataframe[col].apply(lambda x: ''.join([n for n in str(x) if n.isdigit()]) )
		    dataframe[col] = dataframe[col].astype(float)
	
		return dataframe

	def size_model(self,file,msrp,unit_cost,unit_price,win,units,government,cons=None,margin_threshold=None):

		msg = self.__class__.__name__+'.'+utils.get_function_caller()
		self.log.print_(msg)
		print(msg)

		return_ = dict()
		result = dict()

		if isinstance(file,str) and isinstance(msrp,str) and isinstance(unit_cost,str) and isinstance(unit_price,str) and isinstance(win,str) and isinstance(units,str) and isinstance(government,str):

			cols = []

			try:

				dataframe = pd.read_csv(file)			

			except Exception as e:

				msg = 'Error when read the file.'
				self.log.print_(msg)
				print(msg)
				print(e)

				status = 0	
				error = msg

			else: 

				cols = list(dataframe.columns)


				check, error = self.check(cols,msrp,unit_cost,unit_price,win,units,cons,margin_threshold,government)

				if check==0:

					msg = error
					self.log.print_(msg)
					print(msg)

					status = 0				

				else:


					try:

						dataframe = self.data_cleaning(dataframe)

						if margin_threshold is not None:
							margin_threshold = float(margin_threshold)



					except Exception as e:

						msg = 'Error when perform modeling.'
						self.log.print_(msg)
						print(msg)
						print(e)

						status = 0	
						error = msg

					else:

						dataframe['Discount_Pctg'] = (dataframe[msrp]-dataframe[unit_price])/dataframe[msrp]
						dataframe['Unit_Margin'] = dataframe[unit_price]-dataframe[unit_cost]
						dataframe['Units_Sold'] = dataframe[win]*dataframe[units]
						dataframe['Total_Margin'] = dataframe['Units_Sold']*dataframe['Unit_Margin']
						dataframe['Price_Ratio'] = dataframe[unit_price]/dataframe[msrp]

						def f(x):
		    
						    win_probability = 1/(1+np.exp(x[0]+dataframe['Price_Ratio']*x[1]+dataframe[units]*x[2]))    				    
						    likelihood = (dataframe[win]*win_probability)+(1-dataframe[win])*(1-win_probability)
						    ln_likelihood = np.where(dataframe[government]==1,np.log(likelihood),0)
						    sse = ln_likelihood.sum()
						    return sse				  
						    
						def objective(x):
						    # minus sign means the opposite of minimize
						    return -f(x)

						x0 = np.array([1,1,1])
						sol = minimize(objective,x0,options={'disp':True})
						xOpt = sol.x
						# print(xOpt)

						msrp = dataframe[msrp]
						unit_cost = dataframe[unit_cost]

						msrp_ = msrp.unique()[0]
						unit_cost_ = unit_cost.unique()[0]

						xs = np.arange(0.5,1.1,config.INC)
						probs = [1/(1+np.exp(xOpt[0]+(xOpt[1]*x)+(xOpt[2]*config.CONS))) for x in xs]
						margin_per_unit = [ ((x*msrp_)-unit_cost_)*prob for x, prob in zip(xs,probs)]

						df = pd.DataFrame([xs,probs,margin_per_unit]).T
						df.columns = ['price_ratio','prob','unit_margin']

						# print(df)

						if cons is not None:

							self.query(df,xOpt,msrp_,unit_cost_,cons,margin_threshold)							

							optimal_price_ratio, actual_price, probability, margin = self.query(df,xOpt,msrp_,unit_cost_,cons,margin_threshold)							

						else:

							optimal_price_ratio = df.loc[df['unit_margin']==df['unit_margin'].max()]['price_ratio'].values[0]
							actual_price = optimal_price_ratio*msrp_
							probability = 1/(1+np.exp(xOpt[0]+(xOpt[1]*optimal_price_ratio)))
							margin = (actual_price-unit_cost_)*probability


						# print('optimal_price_ratio:',optimal_price_ratio)
						# print('actual_price:',actual_price)
						# print('probability:',probability)
						# print('margin:',margin)

						result['government'] = dict()

						result['government']['parameters'] = dict()
						result['government']['parameters']['intercept'] = xOpt[0]
						result['government']['parameters']['price'] = xOpt[1]
						result['government']['parameters']['size'] = xOpt[2]

						result['government']['constraint'] = cons
						result['government']['margin_threshold'] = margin_threshold						

						result['government']['suggestion'] = dict()
						result['government']['suggestion']['optimal_price_ratio'] = optimal_price_ratio
						result['government']['suggestion']['actual_price'] = actual_price
						result['government']['suggestion']['probability'] = probability
						result['government']['suggestion']['margin'] = margin

						def f(x):
		    
						    win_probability = 1/(1+np.exp(x[0]+dataframe['Price_Ratio']*x[1]+dataframe[units]*x[2]))   
						    likelihood = (dataframe[win]*win_probability)+(1-dataframe[win])*(1-win_probability)
						    ln_likelihood = np.where(dataframe[government]!=1,np.log(likelihood),config.DEFAULT_ZERO)
						    sse = ln_likelihood.sum()
						    return sse
						 
						    
						def objective(x):
						    # minus sign means the opposite of minimize
						    return -f(x)

						x0 = np.array([1,1,1])
						# f(x0)

						sol = minimize(objective,x0,options={'disp':True})

						xOpt = sol.x
						# print(xOpt)

						xs = np.arange(0.5,1.1,config.INC)
						probs = [1/(1+np.exp(xOpt[0]+(xOpt[1]*x)+(xOpt[2]*config.CONS))) for x in xs]	
						margin_per_unit = [ ((x*msrp_)-unit_cost_)*prob for x, prob in zip(xs,probs)]

						df = pd.DataFrame([xs,probs,margin_per_unit]).T
						df.columns = ['price_ratio','prob','unit_margin']

						# print(df)

						if cons is not None:

							optimal_price_ratio, actual_price, probability, margin = self.query(df,xOpt,msrp_,unit_cost_,cons,margin_threshold)														

						else:

							optimal_price_ratio = df.loc[df['unit_margin']==df['unit_margin'].max()]['price_ratio'].values[0]
							actual_price = optimal_price_ratio*msrp_
							probability = 1/(1+np.exp(xOpt[0]+(xOpt[1]*optimal_price_ratio)))
							margin = (actual_price-unit_cost_)*probability



						# print('optimal_price_ratio:',optimal_price_ratio)
						# print('actual_price:',actual_price)
						# print('probability:',probability)
						# print('margin:',margin)

						result['corporate'] = dict()

						result['corporate']['parameters'] = dict()
						result['corporate']['parameters']['intercept'] = xOpt[0]
						result['corporate']['parameters']['price'] = xOpt[1]
						result['corporate']['parameters']['size'] = xOpt[2]				

						result['corporate']['constraint'] = cons
						result['corporate']['margin_threshold'] = margin_threshold						

						result['corporate']['suggestion'] = dict()
						result['corporate']['suggestion']['optimal_price_ratio'] = optimal_price_ratio
						result['corporate']['suggestion']['actual_price'] = actual_price
						result['corporate']['suggestion']['probability'] = probability
						result['corporate']['suggestion']['margin'] = margin


						# print(result)

						# # # result = json.dumps(result)

						status = 1	
						error = None

		else:

			msg = 'Error on data type.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg


		return_["status"] = status
		return_["error"] = error
		return_["data"] = [result]

		return_json = json.dumps(return_)

		return return_json



	def segmented_model(self,file,msrp,unit_cost,unit_price,win,units,government,cons=None,margin_threshold=None):

		msg = self.__class__.__name__+'.'+utils.get_function_caller()
		self.log.print_(msg)
		print(msg)

		return_ = dict()
		result = dict()

		if isinstance(file,str) and isinstance(msrp,str) and isinstance(unit_cost,str) and isinstance(unit_price,str) and isinstance(win,str) and isinstance(units,str) and isinstance(government,str):

			cols = []

			try:

				dataframe = pd.read_csv(file)			

			except Exception as e:

				msg = 'Error when read the file.'
				self.log.print_(msg)
				print(msg)
				print(e)

				status = 0	
				error = msg

			else: 

				cols = list(dataframe.columns)

				check, error = self.check(cols,msrp,unit_cost,unit_price,win,units,cons,margin_threshold,government)

				if check==0:

					msg = error
					self.log.print_(msg)
					print(msg)

					status = 0					


				else:


					try:

						dataframe = self.data_cleaning(dataframe)

						if margin_threshold is not None:
							margin_threshold = float(margin_threshold)


					except Exception as e:


						msg = 'Error when perform modeling.'
						self.log.print_(msg)
						print(msg)
						print(e)

						status = 0	
						error = msg

					else:

						dataframe['Discount_Pctg'] = (dataframe[msrp]-dataframe[unit_price])/dataframe[msrp]
						dataframe['Unit_Margin'] = dataframe[unit_price]-dataframe[unit_cost]
						dataframe['Units_Sold'] = dataframe[win]*dataframe[units]
						dataframe['Total_Margin'] = dataframe['Units_Sold']*dataframe['Unit_Margin']
						dataframe['Price_Ratio'] = dataframe[unit_price]/dataframe[msrp]

						def f(x):
		    
						    win_probability = 1/(1+np.exp(x[0]+dataframe['Price_Ratio']*x[1]))    
						    likelihood = (dataframe[win]*win_probability)+(1-dataframe[win])*(1-win_probability)
						    ln_likelihood = np.where(dataframe[government]==1,np.log(likelihood),0)
						    sse = ln_likelihood.sum()
						    return sse				  
						    
						def objective(x):
						    # minus sign means the opposite of minimize
						    return -f(x)

						x0 = np.array([1,1])
						sol = minimize(objective,x0,options={'disp':True})
						xOpt = sol.x
						print(xOpt)

						msrp = dataframe[msrp]
						unit_cost = dataframe[unit_cost]

						msrp_ = msrp.unique()[0]
						unit_cost_ = unit_cost.unique()[0]

						xs = np.arange(0.5,1.1,config.INC)
						probs = [1/(1+np.exp(xOpt[0]+(xOpt[1]*x))) for x in xs]
						margin_per_unit = [ ((x*msrp_)-unit_cost_)*prob for x, prob in zip(xs,probs)]

						df = pd.DataFrame([xs,probs,margin_per_unit]).T
						df.columns = ['price_ratio','prob','unit_margin']

						if cons is not None:

							optimal_price_ratio, actual_price, probability, margin = self.query(df,xOpt,msrp_,unit_cost_,cons,margin_threshold)							

						else:

							optimal_price_ratio = df.loc[df['unit_margin']==df['unit_margin'].max()]['price_ratio'].values[0]
							actual_price = optimal_price_ratio*msrp_
							probability = 1/(1+np.exp(xOpt[0]+(xOpt[1]*optimal_price_ratio)))
							margin = (actual_price-unit_cost_)*probability


						# print('optimal_price_ratio:',optimal_price_ratio)
						# print('actual_price:',actual_price)
						# print('probability:',probability)
						# print('margin:',margin)

						result['government'] = dict()

						result['government']['parameters'] = dict()
						result['government']['parameters']['intercept'] = xOpt[0]
						result['government']['parameters']['price'] = xOpt[1]

						result['government']['constraint'] = cons						
						result['government']['margin_threshold'] = margin_threshold
					
						result['government']['suggestion'] = dict()
						result['government']['suggestion']['optimal_price_ratio'] = optimal_price_ratio
						result['government']['suggestion']['actual_price'] = actual_price
						result['government']['suggestion']['probability'] = probability
						result['government']['suggestion']['margin'] = margin

						def f(x):
		    
						    win_probability = 1/(1+np.exp(x[0]+dataframe['Price_Ratio']*x[1]))    
						    likelihood = (dataframe[win]*win_probability)+(1-dataframe[win])*(1-win_probability)
						    ln_likelihood = np.where(dataframe[government]!=1,np.log(likelihood),0)
						    sse = ln_likelihood.sum()
						    return sse
						 
						    
						def objective(x):
						    # minus sign means the opposite of minimize
						    return -f(x)

						x0 = np.array([1,1])
						# f(x0)

						sol = minimize(objective,x0,options={'disp':True})

						xOpt = sol.x
						# print(xOpt)

						xs = np.arange(0.5,1.1,config.INC)
						probs = [1/(1+np.exp(xOpt[0]+(xOpt[1]*x))) for x in xs]
						margin_per_unit = [ ((x*msrp_)-unit_cost_)*prob for x, prob in zip(xs,probs)]

						df = pd.DataFrame([xs,probs,margin_per_unit]).T
						df.columns = ['price_ratio','prob','unit_margin']

						if cons is not None:

							optimal_price_ratio, actual_price, probability, margin = self.query(df,xOpt,msrp_,unit_cost_,cons,margin_threshold)							

						else:

							optimal_price_ratio = df.loc[df['unit_margin']==df['unit_margin'].max()]['price_ratio'].values[0]
							actual_price = optimal_price_ratio*msrp_
							probability = 1/(1+np.exp(xOpt[0]+(xOpt[1]*optimal_price_ratio)))
							margin = (actual_price-unit_cost_)*probability

						# print('optimal_price_ratio:',optimal_price_ratio)
						# print('actual_price:',actual_price)
						# print('probability:',probability)
						# print('margin:',margin)

						result['corporate'] = dict()

						result['corporate']['parameters'] = dict()
						result['corporate']['parameters']['intercept'] = xOpt[0]
						result['corporate']['parameters']['price'] = xOpt[1]

						result['corporate']['constraint'] = cons
						result['corporate']['margin_threshold'] = margin_threshold

						result['corporate']['suggestion'] = dict()
						result['corporate']['suggestion']['optimal_price_ratio'] = optimal_price_ratio
						result['corporate']['suggestion']['actual_price'] = actual_price
						result['corporate']['suggestion']['probability'] = probability
						result['corporate']['suggestion']['margin'] = margin


						# print(result)

						# # result = json.dumps(result)

						status = 1	
						error = None
			


		else:

			msg = 'Error on data type.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg


		return_["status"] = status
		return_["error"] = error
		return_["data"] = [result]

		return_json = json.dumps(return_)

		return return_json


	def price_model(self,file,msrp,unit_cost,unit_price,win,units,cons=None,margin_threshold=None):

		msg = self.__class__.__name__+'.'+utils.get_function_caller()
		self.log.print_(msg)
		print(msg)

		return_ = dict()
		result = dict()

		if isinstance(file,str) and isinstance(msrp,str) and isinstance(unit_cost,str) and isinstance(unit_price,str) and isinstance(win,str) and isinstance(units,str):			


			cols = []

			try:

				dataframe = pd.read_csv(file)			

			except Exception as e:

				msg = 'Error when read the file.'
				self.log.print_(msg)
				print(msg)
				print(e)

				status = 0	
				error = msg

			else: 

				cols = list(dataframe.columns)

				check, error = self.check(cols,msrp,unit_cost,unit_price,win,units,cons,margin_threshold)

				if check==0:

					msg = error
					self.log.print_(msg)
					print(msg)

					status = 0					

				else:

					try:

						dataframe = self.data_cleaning(dataframe)						
					
						print(dataframe)

						if margin_threshold is not None:
							margin_threshold = float(margin_threshold)

						print('margin_threshold:',margin_threshold)

					except Exception as e:


						msg = 'Error when perform modeling.'
						self.log.print_(msg)
						print(msg)
						print(e)

						status = 0	
						error = msg

					else:

						dataframe['Discount_Pctg'] = (dataframe[msrp]-dataframe[unit_price])/dataframe[msrp]
						dataframe['Unit_Margin'] = dataframe[unit_price]-dataframe[unit_cost]
						dataframe['Units_Sold'] = dataframe[win]*dataframe[units]
						dataframe['Total_Margin'] = dataframe['Units_Sold']*dataframe['Unit_Margin']
						dataframe['Price_Ratio'] = dataframe[unit_price]/dataframe[msrp]

						def f(x):
			    
						    win_probability = 1/(1+np.exp(x[0]+dataframe['Price_Ratio']*x[1]))    
						    likelihood = (dataframe[win]*win_probability)+(1-dataframe[win])*(1-win_probability)
						    ln_likelihood = np.log(likelihood)
						    sse = ln_likelihood.sum()
						    return sse
						  

						    
						def objective(x):
						    # minus sign means the opposite of minimize
						    return -f(x)

						x0 = np.array([1,1])
						sol = minimize(objective,x0,options={'disp':True})
						xOpt = sol.x

						# print('xOpt:')
						# print(xOpt)

						# dataframe['win_probability'] = 1/(1+np.exp(xOpt[0]+dataframe['Price_Ratio']*xOpt[1]))    
						# dataframe['likelihood'] = (dataframe[win]*dataframe[win])+(1-dataframe[win])*(1-dataframe['win_probability'])
						# dataframe['ln_likelihood'] = np.log(dataframe['likelihood'])

						# print(dataframe)
						# print(dataframe['ln_likelihood'].sum())

						msrp = dataframe[msrp]
						unit_cost = dataframe[unit_cost]

						msrp_ = msrp.unique()[0]
						unit_cost_ = unit_cost.unique()[0]

						xs = np.arange(0.5,1.1,config.INC)
						probs = [1/(1+np.exp(xOpt[0]+(xOpt[1]*x))) for x in xs]
						margin_per_unit = [ ((x*msrp_)-unit_cost_)*prob for x, prob in zip(xs,probs)]

						df = pd.DataFrame([xs,probs,margin_per_unit]).T
						df.columns = ['price_ratio','prob','unit_margin']

						# print(df)
						# df.to_csv('df.csv',index=False)

						if cons is not None:

							optimal_price_ratio, actual_price, probability, margin = self.query(df,xOpt,msrp_,unit_cost_,cons,margin_threshold)							

						else:

							optimal_price_ratio = df.loc[df['unit_margin']==df['unit_margin'].max()]['price_ratio'].values[0]
							actual_price = optimal_price_ratio*msrp_
							probability = 1/(1+np.exp(xOpt[0]+(xOpt[1]*optimal_price_ratio)))
							margin = (actual_price-unit_cost_)*probability


						print('optimal_price_ratio:',optimal_price_ratio)
						print('actual_price:',actual_price)
						print('probability:',probability)
						print('margin:',margin)

						result['parameters'] = dict()					
						result['parameters']['intercept'] = xOpt[0]
						result['parameters']['price'] = xOpt[1]

						result['constraint'] = cons
						result['margin_threshold'] = margin_threshold

						result['suggestion'] = dict()
						result['suggestion']['optimal_price_ratio'] = optimal_price_ratio
						result['suggestion']['actual_price'] = actual_price
						result['suggestion']['probability'] = probability
						result['suggestion']['margin'] = margin

						# result = json.dumps(result)

						status = 1	
						error = None
					



		else:

			msg = 'Error on data type.'
			self.log.print_(msg)
			print(msg)

			status = 0	
			error = msg

		return_["status"] = status
		return_["error"] = error
		return_["data"] = [result]

		return_json = json.dumps(return_)

		return return_json

	def check(self,cols,msrp,unit_cost,unit_price,win,units,cons=None,margin_threshold=None,government=None):

		msg = self.__class__.__name__+'.'+utils.get_function_caller()
		self.log.print_(msg)
		print(msg)

		if msrp not in cols and cols is not None:

			msg = msrp+' does not exist.'
			self.log.print_(msg)
			print(msg)				

			return 0, msg

		if unit_cost not in cols and cols is not None:

			msg = unit_cost+' does not exist.'
			self.log.print_(msg)
			print(msg)				

			return 0, msg

		if unit_price not in cols and cols is not None:

			msg = unit_price+' does not exist.'
			self.log.print_(msg)
			print(msg)				

			return 0, msg

		if win not in cols and cols is not None:

			msg = win+' does not exist.'
			self.log.print_(msg)
			print(msg)				

			return 0, msg

		if units not in cols and cols is not None:

			msg = units+' does not exist.'
			self.log.print_(msg)
			print(msg)				

			return 0, msg

		if government is not None and government not in cols and cols is not None:

			msg = government+' does not exist.'
			self.log.print_(msg)
			print(msg)				

			return 0, msg

		if margin_threshold is not None and cons is None:

			msg = 'Constraint is needed.'
			self.log.print_(msg)
			print(msg)				

			return 0, msg

		if margin_threshold is not None and not (isinstance(margin_threshold,str) or isinstance(margin_threshold,int) or isinstance(margin_threshold,float)):

			msg = str(margin_threshold)+' is invalid.'
			self.log.print_(msg)
			print(msg)				

			return 0, msg

		if cons is not None:


			if not isinstance(cons,str):

				msg = str(cons)+' is invalid.'
				self.log.print_(msg)
				print(msg)				

				return 0, msg

			if len(cons.split(' '))!=3:

				msg = cons+' is invalid.'
				self.log.print_(msg)
				print(msg)				

				return 0, msg

			if not (cons.split(' ')[0]=='prob' and cons.split(' ')[1] in ['<','<=','>=','>'] and (utils.is_float(cons.split(' ')[2]) or utils.is_int(cons.split(' ')[2]))) :

				msg = str(cons)+' is invalid.'
				self.log.print_(msg)
				print(msg)				

				return 0, msg


			# elif not(margin_threshold is not None and (not isinstance(margin_threshold,str) or not isinstance(margin_threshold,int) or not isinstance(margin_threshold,float))):

			# 	msg = 'Margin Threshold must be a numeric.'
			# 	self.log.print_(msg)
			# 	print(msg)				
				
			# 	return 0, msg

		else:

			pass

		return 1, ''			




	def query(self,df,params,msrp_,unit_cost_,cons=None,margin_threshold=None):

		msg = self.__class__.__name__+'.'+utils.get_function_caller()
		self.log.print_(msg)
		print(msg)

		optimal_price_ratio = None
		actual_price = None
		probability = None
		margin = None

		try:

			field = cons.split(' ')[0]
			opt = cons.split(' ')[1]
			val = cons.split(' ')[2]

			_str = "df[(df['"+str(field)+"'] "+str(opt)+" "+str(val)+")]"

			df = pd.eval(_str)

			if df.shape[0]>0:

				optimal_price_ratio = df.loc[df['unit_margin']==df['unit_margin'].max()]['price_ratio'].values[0]
				actual_price = optimal_price_ratio*msrp_
				probability = 1/(1+np.exp(params[0]+(params[1]*optimal_price_ratio)))
				margin = (actual_price-unit_cost_)*probability

				if margin_threshold is not None:

					lower_margin = margin-margin_threshold

					df_ = df[df['unit_margin']>=lower_margin]

					if df_.shape[0]>0:

						optimal_price_ratio = df_.loc[df_['prob']==df_['prob'].max()]['price_ratio'].values[0]
						actual_price = optimal_price_ratio*msrp_
						probability = 1/(1+np.exp(params[0]+(params[1]*optimal_price_ratio)))
						margin = (actual_price-unit_cost_)*probability

			# print(optimal_price_ratio, actual_price, probability, margin)

			return optimal_price_ratio, actual_price, probability, margin

		except Exception as e:

			msg = 'Error when query dataset.'
			self.log.print_(msg)
			self.log.print_(e)

			print(msg)
			print(e)