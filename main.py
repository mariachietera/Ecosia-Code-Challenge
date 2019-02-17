#! /usr/bin/env python

import json
import sqlite3
import urllib
from datetime import datetime
import boto3

s3 = boto3.client('s3')

URL = "https://raw.githubusercontent.com/localytics/data-viz-challenge/master/data.json"
BUCKET = 'maryte.test'
REGION = 'eu-central-1'
KEY_NAME = 'total_events.csv'


def main():
    """
    lead json file, process data and load output csv file to s3
    :return: Bool
    """
    print("Running...")
    data = load_data_from_url(URL)
    total_events = process_data(data)
    output_file = upload_csv_to_s3(total_events)
    print("=============\nPlease find the output file {} at {}\n=============".format(KEY_NAME, output_file))
    return True


def process_data(data):
    """
    populate table with json entries, perform query and convert result in csv format string
    :param data: json
    :return: string
    """
    db = sqlite3.connect(':memory:')
    cursor = db.cursor()
    populate_session_table(data, cursor)
    rows = query_session_table(cursor)
    db.commit()
    db.close()
    total_events = encode_result_as_csv(rows)
    return total_events


def upload_csv_to_s3(total_events_csv_format):
    """
    upload csv file to s3 and returns file location
    :param total_events_csv_format: string
    :return: string
    """
    s3.put_object(Bucket=BUCKET, Key=KEY_NAME, Body=total_events_csv_format, ContentType='text/csv',
                  ACL='public-read-write')
    output_file = "https://s3.{}.amazonaws.com/{}/{}".format(REGION, BUCKET, KEY_NAME)
    return output_file


def encode_result_as_csv(results):
    """
    convert sql query result in csv shaped string
    :param results: sql result
    :return: string
    """
    total_events_csv_format = "age,device,date,count,sum\r\n"
    for result in results:
        total_events_csv_format = total_events_csv_format + \
                                  "{},{},{},{},{}\r\n".format(result[0], result[1], result[2], result[3], result[4])
    return total_events_csv_format


def query_session_table(cursor):
    """
    query over table
    :param cursor: sql cursor
    :return: sql result
    """
    cursor.execute(
        '''SELECT age, device, date, COUNT(*), SUM(amount)
        FROM session 
        GROUP BY gender, age, device, date 
        HAVING gender="F" AND state="CA"''')
    results = cursor.fetchall()
    return results


def populate_session_table(data, cursor):
    """
    create and populate table
    :param data: json
    :param cursor: sql cursor
    :return: None
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS session(id INTEGER PRIMARY KEY, gender TEXT,
                           age TEXT, device TEXT, date INTEGER, state TEXT, amount INTEGER)
    ''')
    for session in data["data"]:
        cursor.execute('''INSERT INTO session(gender, age, device, date, state, amount)
                          VALUES(?,?,?,?,?,?)''', (session["gender"],
                                                   session["age"],
                                                   session["device"],
                                                   convert_unix_to_datatime(session["client_time"]),
                                                   session["location"]["state"],
                                                   session.get('amount', 0)))


def load_data_from_url(url):
    """
    lead json from web url
    :param url: string
    :return: json
    """
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data


def convert_unix_to_datatime(param):
    """
    convert data to datatime format
    :param param:
    :return:
    """
    ts = int(param)
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')


if __name__ == "__main__":
    main()
