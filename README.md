# Apartment Hunting

Scrape apartment data from websites to make Apartment Hunting easier.

## How it works
Every day, run this script from your local machine. It can't be run headless due to scraping restrictions imposed by the apartment management companies. 

For every apartment building listed in `main.py`, the script will list out all the apartments that are available and dump them into a SQL DB.

Query the DB to your heart's desire. The simpliest usage pattern is "what's available today?" but you can get much more complex by looking at specific units and how their price has changed over time.

## Environment
  - Python3 w/ `bs4`, `selenium`, `mysql` installed
  - MySQL server
    - Database: `apt_hunting`
    - Table: `info` (with all the columns enumerated below)

## Working SQL Query:
```
SELECT
  building,
  price,
  sqFt,
  beds,
  details,
  aptId,
  available
FROM
  info
WHERE
  (
    beds = 1
    OR beds = 2
  )
  AND date = curdate()
  AND ((available > "2024-04-20" AND available < "2024-05-07") OR available IS NULL OR available = curdate())
  AND sqFt > 600
ORDER BY
  price

```
