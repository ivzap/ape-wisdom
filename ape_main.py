import datetime as dt 
import pandas as pd
import requests
import os


#Description: Gets number of pages in pagination
def get_ape_wisdom_pages(subreddit: str) -> int:
	url = 'https://apewisdom.io/api/v1.0/filter/' + subreddit + '/'
	pages = range(1, requests.get(url).json()['pages'] + 1)
	return pages


#Description: Gets the data from pagination
def get_ape_wisdom(subreddit: str, pages: int) -> pd.DataFrame:
	current = str(dt.datetime.now())
	wisdom = pd.DataFrame()
	for page in pages:  
	    url = 'https://apewisdom.io/api/v1.0/filter/' + subreddit + '/page/' + str(page)
	    # request data
	    pagination_data = requests.get(url).json()
	    tempData = pd.DataFrame(pagination_data['results'])
	    tempData['timestamp'] = current
	    # concat to data
	    wisdom = pd.concat([tempData, wisdom])
	wisdom = wisdom.fillna(0)
	wisdom = wisdom.drop_duplicates('ticker', keep='first')
	wisdom = wisdom.sort_values(by='rank')
	wisdom = wisdom.reset_index(drop=True)
	return wisdom


# Description: writes wisdom to current day csv
def wisdom_to_csv(wisdom: pd.DataFrame, write_dateDT: dt.datetime):
	cwd = os.getcwd()
	# Check if we need to write a header to our csv when appending/writing
	try:
	# means read was succesful and we already listed the headers in the csv
	with open(cwd + '/wisdom/' + 'ape_wisdom_' + str(write_dateDT.date()) + '.csv', mode='r') as f:
	    pass
	wisdom.to_csv(cwd + '/wisdom/' +  'ape_wisdom_' + str(write_dateDT.date()) + '.csv', mode='a', index=False, header=False)
	except:
	# means file not found and this is the first write so header is needed
	wisdom.to_csv('ape_wisdom_' + str(write_dateDT.date()) + '.csv', mode='w', index=False)

	
if __name__ == "__main__":
	subreddit = 'wallstreetbets'
	pages = get_ape_wisdom_pages(subreddit)
	
	# get new data
	new_wisdom, write_dateDT = get_ape_wisdom(subreddit, pages)
	new_wisdom = new_wisdom[['timestamp','ticker', 'name', 'rank', 'mentions','upvotes','rank_24h_ago', 'mentions_24h_ago']]
	
	# append/write new wisdom to csv
	wisdom_to_csv(new_wisdom, write_dateDT)
