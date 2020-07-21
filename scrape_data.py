from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np
import re

def replace_regex(var):
	if re.match('.*[DNB$|\*|\-]',var):
		return 1
	else:
		return 0

def get_yearwise_record(df):
	df = df.groupby(['Year'])[['Runs','acc_inn']].sum().reset_index()
	df['avg'] = df['Avg'] = df['Runs']/df['acc_inn']
	return df

def get_record_by_innings(url, type='frame'):

	driver = webdriver.Chrome("C:\\ChromeDriver\\chromedriver")
	driver.get(url)
	content = driver.page_source

	bs = BeautifulSoup(content)

	table_class = bs.find_all("table",{"class":"engineTable"})[3]

	rows = table_class.find_all('th')
	#print(rows)
	header = []
	for row in rows:
		for a in row.findAll('a'):
	 		header.append(a.text)

	table_body=bs.find_all('tbody')[3]
	rows = table_body.find_all('tr')
	data = np.array([])

	for row in rows:
		cols=row.find_all('td')
		cols=np.array([x.text.strip() for x in cols])
		if data.size == 0:
			data = np.append(data,cols)
		else:
			data = np.vstack([data,cols])

	df = pd.DataFrame(data)
	df = df.drop(7,1)
	df.columns =  header[:(len(header)-1)] + ['Opposition','Ground','StartDate','Test']
	df['Year'] = df['StartDate'].apply(lambda x:x.split(' ')[2])
	replacements = {r'-':0}
	df['Runs'] = df['Runs'].replace(replacements,regex=True)
	df['Runs'] = df['Runs'] .astype(int)
	# df.loc[(df['Bat1'] == '-'), 'Bat1'] = 'DNB' 
	# df.loc[(df['Bat2'] == '-'), 'Bat2'] = 'DNB'
	df['NotOuts'] = df['Bat1'].apply(lambda x : replace_regex(x)) + \
					df['Bat2'].apply(lambda x : replace_regex(x))
	df['acc_inn'] = 2 - df['NotOuts']
	if type == 'json':
		return df.to_json()
	else:
		return df
	



