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

First, Create `settings.json` in a directory which contains `scraping.py`.
Scond, Write ID in first row and password as follows.

```json
{
    "base":{
        "user":"1234567890123",
        "pass":"password",
        "criteria_hours":168
    },
    "line":{
        "is_enabled":true,
        "token":"line-token-from-line-notify"
    },
    "slack":{
        "is_enabled":true,
        "token":"slack-token-from-custom-integration"
    }
}
```