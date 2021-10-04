# Ape Wisdom API Wrapper
![image](https://user-images.githubusercontent.com/64557487/135900885-7b48c43d-bac5-42fb-8a54-3c97bbad6856.png)



> Parameters

| Name   |     Type      | Description  |
| -------------       | ------------- |------------- |
| subreddit  | String     | the subreddit to request total pages of data available on Ape wisdoms API |


```python
def get_ape_wisdom_pages(subreddit)
```

> Parameters
> 
| Name   |     Type      | Description  |
| -------------       | ------------- |------------- |
| subreddit  | String     | the subreddit to request data from Ape wisdoms API |
| pages  | Int     | number of available pages to request |

```python
def get_ape_wisdom(subreddit, pages)
```



> Parameters

| Name   |     Type      | Description  |
| -------------       | ------------- |------------- |
| wisdom  | String     | the data collected from Ape wisdoms API|
| write_dateDT  | datetime.Datetime()     | time as datetime object that we requested data from Ape wisdoms API|
| dirpath  | String     | the path to write in csv format all our wisdom|

```python
def wisdom_to_csv(wisdom, write_dateDT, dirpath)
```

### Usage Example:

> note: ape wisdoms api uses **pagination** so we use the requests library to 'request' the data
```python
# set subreddit to be searched and get pages
subreddit = 'wallstreetbets'
pages = get_ape_wisdom_pages(subreddit)

# get new data
new_wisdom, write_dateDT = get_ape_wisdom(subreddit, pages)
new_wisdom = new_wisdom[['timestamp','ticker', 'name', 'rank', 'mentions','upvotes','rank_24h_ago', 'mentions_24h_ago']]

# append/write new wisdom to csv
dirpath = 'somedirpath'
wisdom_to_csv(new_wisdom, write_dateDT, dirpath)

```
### Documentation:
> Click https://apewisdom.io/api/ to view ape-wisdom's simple api documentation

### Cron Job:
```
*/15 * * * * /home/interns/miniconda3/bin/python3 /home/interns/ape_wisdom/ape-wisdom/ape_main.py >> ~/cron.log 2>&1

```
