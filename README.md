# ape-wisdom

### Usage:

> ape-wisdom uses **pagination** so we use the requests library to 'request' the data
```python
subreddit = 'wallstreetbets'
url = 'https://apewisdom.io/api/v1.0/filter/' + subreddit + '/'
import requests
requests.get(pagination_url)
```
### Documentation:
> Click https://apewisdom.io/api/ to view ape-wisdom's simple api documentation

### Cron Job:
```
*/15 * * * * (cd project_location && interpreter_location project_name.py) >> /project_path/cron_logs/cron.log 2>&1

```
