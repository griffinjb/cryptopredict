import cryptocompare as cc 
import numpy as np 
import matplotlib.pyplot as plt
import requests
import pandas as pd
import scipy.signal as ss

def get_current_data(	from_sym='BTC', 
						to_sym='USD', 
						exchange=''):

	url = 'https://min-api.cryptocompare.com/data/price'    
	
	parameters = {'fsym': from_sym,
				  'tsyms': to_sym }
	
	if exchange:
		print('exchange: ', exchange)
		parameters['e'] = exchange
		
	# response comes as json
	response = requests.get(url, params=parameters)   
	data = response.json()
	
	return data   

def get_hist_data(	from_sym='BTC', 
					to_sym='USD', 
					timeframe = 'day', 
					limit=500, 
					aggregation=1, 
					date='2019-08-21',
					exchange=''):
	
	url = 'https://min-api.cryptocompare.com/data/v2/histo'
	url += timeframe
	
	parameters = {'fsym': from_sym,
				  'tsym': to_sym,
				  'limit': limit,
				  'aggregate': aggregation,
				  'date': date}

	if exchange:
		print('exchange: ', exchange)
		parameters['e'] = exchange    
	
	print('baseurl: ', url) 
	print('timeframe: ', timeframe)
	print('parameters: ', parameters)
	
	# response comes as json
	response = requests.get(url, params=parameters)
	
	data = response.json()['Data']['Data']
	
	return(data_to_dataframe(data))


def data_to_dataframe(data):
	#data from json is in array of dictionaries
	df = pd.DataFrame.from_dict(data)
	
	# time is stored as an epoch, we need normal dates
	df['time'] = pd.to_datetime(df['time'], unit='s')
	df.set_index('time', inplace=True)
	print(df.tail())
	
	return df

# def btc_gen(start_date,precision):



# each day may be modelled as a mixture
	# a set of agents
	# have a system determining buy/sell
	# the price differential




if __name__ == '__main__':

	CID = 'BTC'

	df = get_hist_data(	from_sym=CID,
						timeframe='day',
						limit=2000
						)

	plt.figure('hist')
	df.high.hist(bins=100)
	plt.figure('diff_hist')
	df.high.diff().hist(bins=100)
	plt.figure('diff')
	df.high.diff().plot()

	plt.figure('diff_spect')
	# plt.specgram(df.high.diff().values)

	f,t,Sxx = ss.spectrogram(df.high.diff().values,nperseg=32)
	plt.pcolormesh(f,t,np.log10(Sxx.T),shading='gouraud')

	plt.show()















#