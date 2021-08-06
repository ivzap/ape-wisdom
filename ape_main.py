import datetime as dt 
import pandas as pd
import requests

#Description: Gets number of pages in pagination
def get_ape_wisdom_pages(subreddit):
	url = 'https://apewisdom.io/api/v1.0/filter/' + subreddit + '/'
	pages = range(1, requests.get(url).json()['pages'] + 1)
	return pages

#Description: Gets the data from pagination
def get_ape_wisdom(subreddit, pages):
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

# Querrys two wisdoms for comparison seperated by X minutes
def querry(minutes, subreddit, pages):
    seconds = minutes * 60 # convert to seconds
    wisdoms = []
    for run in tqdm(range(0,2)):
        pages = get_ape_wisdom_pages(subreddit)
        wisdom = get_ape_wisdom(subreddit, pages)
        wisdoms.append(wisdom)
        time.sleep(seconds)
    return wisdoms

subreddit = 'wallstreetbets'
pages = get_ape_wisdom_pages()


wisdom = get_ape_wisdom(subreddit, pages)
print(wisdom)

