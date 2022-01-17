## Scraping Indeed website

Using BeautifulSoup and requests, I scrape different data scientist job posts.
Different values like title, date, job snippet, links are scraped.

## Saving data

1. Using sqlite3, I create a database called *indeed.db*, in which I create a table named *dataScientistJobs*.
See *scrape_indeed_save_df.py*
2. Using pandas, I save the data in a dataframe *scrape_indeed_save_df.py*.
