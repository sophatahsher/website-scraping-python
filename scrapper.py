import argparse
import requests
import psycopg2
from click import echo

# create command arg
parser = argparse.ArgumentParser(description="Please see the commands below to start to use this application: ", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--create_db", action="store_true", help="Initialize database")
parser.add_argument("--create_table", action="store_true", help="Create database table")

args = parser.parse_args()
config = vars(args)
print(config)

def create_db():
    commands = (
        """
        CREATE DATABASE scrape_db
        """
    )
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(host="127.0.0.1", port ="5432", user="postgres", password='admin')
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        echo('Initialized the database!')   
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def create_table():
    commands = (
        """
        CREATE TABLE scraping_properties (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            cover VARCHAR(255) NULL,
            type VARCHAR(50) NULL,
            price MONEY,
            details JSONB
        )
        """
    )

    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(host="127.0.0.1", port ="5432", user="postgres", password="postgres", database="scrape_db")
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        echo('scraping_properties table has been created!')  
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()    

def start_scraping():
    r = requests.get('https://www.signature.co.nz/house-land/')
    print(r.text)

    # Establish db connection
    conn = psycopg2.connect(host="127.0.0.1", port ="5432", user="postgres", password="postgres", database="scrape_db")

    # db cursor
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO properties(id, title, property_cover, property_type, price, details) 
                VALUES(%s, %s, %s, %s)
                """,
                (

                )
            )

    # commit the data
    conn.commit()

    # close connection
    cur.close()
    conn.close()

if __name__ == '__main__':

    if args.create_db:
        create_db()

    if args.create_table:
        create_table(model=args.m)