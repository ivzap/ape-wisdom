import datetime as dt 
import pandas as pd
import requests


#Description: Gets number of pages in pagination
def get_ape_wisdom_pages(subreddit) -> int:
	url = 'https://apewisdom.io/api/v1.0/filter/' + subreddit + '/'
	pages = range(1, requests.get(url).json()['pages'] + 1)
	return pages


#Description: Gets the data from pagination
def get_ape_wisdom(subreddit, pages) -> pd.DataFrame():
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

	wisdom = wisdom.sort_values(by='rank')
	wisdom = wisdom.reset_index(drop=True)
	return wisdom


# Description: Gets a concated dataframe of last two ape requests and sort it by X
def get_ape_wisdom_changes(wisdoms, sort_by) -> pd.DataFrame():
	# sort_by options: mentions_change, upvotes_change
	first_req = wisdoms[0]
	second_req = wisdoms[1]
	data = pd.concat([first_req, second_req])
	data['mentions_change'] = second_req.mentions.astype(int).sub(first_req.mentions.astype(int), axis=0, fill_value=0)
	data['upvotes_change'] = second_req.upvotes.astype(int).sub(first_req.upvotes.astype(int), axis=0, fill_value=0)
	data = data.drop_duplicates(['ticker'], keep='first')
	data.sort_values(sort_by, inplace=True)
	data.reset_index(drop=True, inplace=True)
	data = data[
			['timestamp',
			'ticker',
			'rank',
			'name',
			'mentions',
			'upvotes',
			'rank_24h_ago',
			'mentions_24h_ago',
			'mentions_change',
			'upvotes_change']
			]
	return data


# Description: writes wisdom to a database
def write_wisdom(wisdom, path: str):
	current_day = str(datetime.datetime.now().date())
	wisdom.to_csv(path + 'ape_wisdom_' + current_day + '.csv', index=False, mode='a')


# Description: Gets only the stocks that have changed rank since the last data request(USE: RESEARCH)
def get_ape_wisdom_diff(wisdoms) -> pd.DataFrame():
	first_req = wisdoms[0]
	second_req = wisdoms[1]
	rank_change = second_req['ticker'].astype(str) != first_req['ticker'].astype(str)
	result = second_req[rank_change]
	result.reset_index(drop=True, inplace=True)
	result.sort_values('rank', inplace=True)
	return result


# Querrys two wisdoms for comparison seperated by X minutes
def query(minutes, subreddit, pages) -> pd.DataFrame():
    seconds = minutes * 60 # convert to seconds
    wisdoms = []
    for run in tqdm(range(0,2)):
        pages = get_ape_wisdom_pages(subreddit)
        wisdom = get_ape_wisdom(subreddit, pages)
        wisdoms.append(wisdom)
        time.sleep(seconds)
    return wisdoms


if __name__ == "__main__":
	subreddit = 'wallstreetbets'
	pages = get_ape_wisdom_pages(subreddit)

	wisdoms = []
	for run in range(0,2):
		wisdom = get_ape_wisdom(subreddit, pages)
		wisdoms.append(wisdom)

	data = get_ape_wisdom_changes(wisdoms, 'mentions_change')
	print(data)
