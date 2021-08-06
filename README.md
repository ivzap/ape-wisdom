# ape-wisdom

### Usage:

##### Description:  > ape-wisdom uses **pagination** so we use the requests library to 'request' the data
```python
subreddit = 'wallstreetbets'
url = 'https://apewisdom.io/api/v1.0/filter/' + subreddit + '/'
import requests
requests.get(pagination_url)
```
