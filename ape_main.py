import datetime as dt
import pandas as pd
import requests
import os


#Description: Gets number of pages in pagination
def get_ape_wisdom_pages(subreddit):
    url = 'https://apewisdom.io/api/v1.0/filter/' + subreddit + '/'
    pages = range(1, requests.get(url).json()['pages'] + 1)
    return pages


#Description: Gets the data from pagination
def get_ape_wisdom(subreddit, pages):
    current = dt.datetime.strftime(dt.datetime.now(), format='%Y-%m-%d %H:%M:%S')
    currentDT = dt.datetime.strptime(current,'%Y-%m-%d %H:%M:%S')
    wisdom = pd.DataFrame()
    for page in pages:
        url = 'https://apewisdom.io/api/v1.0/filter/' + subreddit + '/page/' + str(page)
        
        # request data
        pagination_data = requests.get(url).json()
        tempData = pd.DataFrame(pagination_data['results'])
        tempData['timestamp'] = current
        
        # concat to data
        wisdom = pd.concat([tempData, wisdom])
    wisdom = wisdom.drop_duplicates('ticker', keep='first')
    wisdom = wisdom.sort_values(by='rank')
    wisdom = wisdom.reset_index(drop=True)

    return wisdom, currentDT


# Description: writes wisdom to current day csv
def wisdom_to_csv(wisdom, write_dateDT, dirpath):
    file_name = 'ape_wisdom_' + str(write_dateDT.date()) + '.csv'
    
    # Check if we need to write a header to our csv when appending/writing
    if os.path.isfile(os.path.join(dirpath, file_name))
        # means read was succesful and we already listed the headers in the csv
        wisdom.to_csv(os.path.join(share_mnt_path, file_name), mode='a', index=False, header=False)
    else:
        # means file not found and this is the first write so header is needed
        wisdom.to_csv(os.path.join(share_mnt_path, file_name), mode='w', index=False)


if __name__ == "__main__":
    # get subreddit and pages  
    subreddit = 'wallstreetbets'
    pages = get_ape_wisdom_pages(subreddit)
    
    # get new data
    new_wisdom, write_dateDT = get_ape_wisdom(subreddit, pages)
    new_wisdom = new_wisdom[['timestamp','ticker', 'name', 'rank', 'mentions','upvotes','rank_24h_ago', 'mentions_24h_ago']]
    
    # append/write new wisdom to csv
    dirpath = 'somepath'
    wisdom_to_csv(new_wisdom, write_dateDT, dirpath)                                             
