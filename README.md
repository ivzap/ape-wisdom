# ape-wisdom

### Usage:

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
