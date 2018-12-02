# manaba scraping tool

This is a script that scrape assignments which haven't been submitted, and notify if deadline is close.

## install

It requires these softwares.

- webdriver
- selenium
- beautifulsoup4
- lxml

### webdriver
Install webdriver which adopts your web browser.

- Chrome : [ChromeDriver](http://chromedriver.chromium.org/downloads)
- Firefox : [geckodriver](https://github.com/mozilla/geckodriver/releases)
- other borwser : do yourself(Author don't know).

### using conda

```:shell
conda install selenium beautifulsoup4 lxml
```

### using pip

```:shell
pip install selenium beautifulsoup4 lxml
```

### ID and password

First, Create `secret.txt` in a directory which contains `scraping.py`.
Scond, Write ID in first row and password in second row.