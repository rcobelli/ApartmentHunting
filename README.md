# Apartment Hunting

Scrape apartment data from websites.

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