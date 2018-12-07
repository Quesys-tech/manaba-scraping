# manaba scraping tool

This is a script that scrape assignments which haven't been submitted, and notify if deadline is close.

## install

It requires these libraries.

- beautifulsoup4
- lxml
- pytz
- requests

### instalation of libraries using conda

```:shell
conda install beautifulsoup4 lxml pytz requests
```

### instalation of libraries using pip

```:shell
pip install beautifulsoup4 lxml pytz requests
```

### ID and password

First, Create `secret.txt` in a directory which contains `scraping.py`.
Scond, Write ID in first row and password in second row.