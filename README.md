# scraper

To use this scraper follow below steps

### Redis Setup
- Ensure Redis is up and running below steps are for Mac OSX, similar steps can be googled for your environment
- `brew install redis`
- `redis-server`  
  
### Service Setup    
Run Below Commands
- `pip install -r requirements.txt`
- `cd scraping_tool`
- `fastapi run`

Once server is up, you can hit API localhost:8000/scrape through Postman etc
Example curl

```
curl --location --request POST 'localhost:8000/scrape?base_url=https%3A%2F%2Fdentalstall.com%2Fshop%2F&max_pages=2' \
--header 'Authorization: Bearer STATIC_TOKEN'
```

base_url - required parameter, the website to scrape  
max_pages - max number of pages to scrape, default value is 2  