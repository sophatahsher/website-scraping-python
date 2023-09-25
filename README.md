# Scraping Web Page With BeautifulSoup, Python
Web Scraping With Python By Using Requests & BeautifulSoup

Beautiful Soup is a Python package for parsing HTML and XML documents. It creates a parse tree for parsed pages that can be used to extract data from HTML, which is useful for web scraping. 

To get to know about Beautiful Soup, please see details:
[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) 

## Features

- Command create Database & Table in Postgresql
- Command to execute scrape script & save data into database ( The content of scraping is from website url example)

### Installation

```bash
$ cd python-scraping-webpage
```

### Create Virtual Environment
I'm going to run python in virtual environment by running the command below:

```bash
$ python3 -m venv venv
```
### Active Environment
```bash
$ source venv/bin/active
```

### Install dependencies

```bash
$ pip install -r requirements.txt
```

## Commands
- Create database `python scrapper.py --create_database`
- Create table `python scrapper.py --create_table`
- Start Scraping `python scrapper.py --start_scraping`

### Stop Working on Environment
```bash
$ deactivate
```
