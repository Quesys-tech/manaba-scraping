# manaba scraping tool

This is a script that scrape assignments which haven't been submitted, and notify if deadline is close.

## install

It requires these libraries.

- webdriver
- selenium
- beautifulsoup4
- lxml
- pytz

### webdriver

Install webdriver which adopts your web browser.

- Chrome : [ChromeDriver](http://chromedriver.chromium.org/downloads)
- Firefox : [geckodriver](https://github.com/mozilla/geckodriver/releases)
- other borwser : do yourself(Author don't know).

### instalation of libraries using conda

```:shell
conda install selenium beautifulsoup4 lxml pytz
```

### instalation of libraries using pip

```:shell
pip install selenium beautifulsoup4 lxml pytz
```

### ID and password

First, Create `secret.txt` in a directory which contains `scraping.py`.
Scond, Write ID in first row and password in second row.

### add path to webdriver

Overwirte the path of webdriver to `webdriver_path` in `scraping.py`.