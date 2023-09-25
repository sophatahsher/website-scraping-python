import re
import argparse
import requests
import psycopg2
from click import echo
from bs4 import BeautifulSoup
from html.parser import HTMLParser


# create command arg
parser = argparse.ArgumentParser(description="Please see the commands below to start to use this application: ", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--create_db", action="store_true", help="Initialize database")
parser.add_argument("--create_table", action="store_true", help="Create database table")
parser.add_argument("--start_scraping", action="store_true", help="Scrape data from url")


args = parser.parse_args()
config = vars(args)
print(config)

def create_db():
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(host="127.0.0.1", port ="5432", user="postgres", password='postgres')
        
        conn.autocommit = True

        # Creating a cursor object using the cursor() method  
        cur = conn.cursor()

        # Preparing query to create a database
        command = '''CREATE database scraping_db'''

        cur.execute(command)

        # close communication with the PostgreSQL database server
        cur.close()

        echo("Database created successfully!") 
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def create_table():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE scraping_properties (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            cover VARCHAR(255) NULL,
            type VARCHAR(50) NULL,
            price VARCHAR NULL,
            details JSONB
        )
        """)

    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(host="127.0.0.1", port ="5432", user="postgres", password="postgres", database="scraping_db")
        cur = conn.cursor()
        
        # Doping EMPLOYEE table if already exists.
        cur.execute("DROP TABLE IF EXISTS scraping_properties")

        # create table one by one
        cur.execute(commands)

        # close communication with the PostgreSQL database server
        cur.close()

        # commit the changes
        conn.commit()
        echo('scraping_properties table has been created!')  

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()    

def start_scraping():
    r = requests.get('https://www.signature.co.nz/house-land/')

    soup = BeautifulSoup(r.content, 'html.parser')

    # Page Title
    print('Package Title: \n' + soup.title.string + '\n')

    # All Links in current page
    total_links = len(soup.find_all('a'))
    print(f"There are {total_links} links in this page")

    # Property DOM
    property_items = soup.find("div", {"class": "lister-grid"})
    property_data = []

    # Establish db connection
    conn = psycopg2.connect(host="127.0.0.1", port ="5432", user="postgres", password="postgres", database="scraping_db")

    # db cursor
    cur = conn.cursor()

    # 
    all_properties = property_items.find_all("div", {"class": "property u-bg-tint"})
    
    for child_div in all_properties:
        child = child_div.find('h3', { "class": "u-gap-v u-pad-h u-font3"})
        title = child.get_text()
        property_cover = child_div.select_one("div > div:nth-of-type(1) > div:nth-of-type(2) > picture > img").get('src')
        property_type = child_div.select_one("a:nth-of-type(2) > div > div").string
        property_price = child_div.select_one("a:nth-of-type(2) > div > div:nth-of-type(4)").string
        data = {
            "title": title,
            "type": property_type,
            "price": property_price,
            "cover": property_cover
        }

        cur.execute(
            """
            INSERT INTO scraping_properties(title, type, cover, price) 
            VALUES(%s, %s, %s, %s)
            """,
            (
                [title, property_type, property_cover, property_price]
            )
        )

        property_data.append(data)
    
    if( len(property_data) > 0 ):
        echo('scraping_properties  data and saving into table, has been successful!')  

    # commit the data
    conn.commit()

    # close connection
    cur.close()
    conn.close()

def get_html_text(html: str):
    parser = HTMLParser()
    parser.text = ''
    parser.feed(html)

    return parser.text.strip()

if __name__ == '__main__':

    if args.create_db:
        create_db()

    if args.create_table:
       create_table()

    if args.start_scraping:
       start_scraping()