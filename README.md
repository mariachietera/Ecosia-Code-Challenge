### BI Analyst with Python Experience - Ecosia

#### Requirements

Create a Python program that does the following:

1. Programmatically load json from url. ✔
2. Upload to s3 a csv file with the following columns: ```age```, ```device```, ```date```, ```count```, ```sum```. ✔
3. Group on ```gender```, ```age```, ```device``` and ```date``` of ```client_time```. ✔
4. Convert the ```date``` column to *YYYY-MM-DD* format. ✔
5. Populate ```count``` column as entries' count. ✔
6. Populate ```sum``` column as the sum of the ```amount``` key values. ✔
7. Calculates entries for female and Californian users. ✔
8. Provide location of .csv output file. ✔

#### Usage
```
> cd ecosia
> ./ecosia
```
#### Output
```
> Running...
> =============
> Please find total_events.csv at https://s3.eu-central-1.amazonaws.com/maryte.test/total_events.csv
> =============
```


### Implementation details

The project has been written in Python 2.7.
The script is articulated in 3 parts: loading of the json file from url, data processing, uploading the requested .csv file on s3.

I loaded the json file from url using the ```json.loads()``` method.

In order to process the provided data, I choose to populate a ```sqlite``` table with the json keys relevant to the query I was asked to perform, namely ```gender```, ```age```, ```device```, ```date```, ```state```, ```amount```.
Once I stored the entries in this way, the performing of the operation had been a simple SQL query - please see the ```main.query_session_table()``` method.
I found the requirement #7 not clear in terms of which kind of calculation to perform only on female and Californian users, so I decided to encode that through an HAVING statement filtering records to be processed by the SUM and COUNT aggregate functions.
I chose to follow the SQL-table-approach mainly because of its cleanliness and to prove my skills in handling different kind of data format and in formulating SQL statements.
Another simpler approach I could have followed would have been looping over the json entries and taking track of the requested information making use of counters.


Once aggregated the data as requested, I converted the query result in a .csv format string and uploaded that as the ```Body``` parameter of the ```boto3.client('s3').put_object()``` method.

### External resources

* ```json``` and ```urllib```: used to programmatically load the provided json file from url
* ```sqlite3```: used to save the sessions data in a RAM based table and make aggregation and operations on entries easier
* ```datetime.datetime```: used to shape the client_time in the *%Y-%m-%d* format.
* ```boto3```: Amazon Web Services SDK allowing the uploading of the .csv to S3

#### Possible improvements

* encode hard-coded parameters such as URL, BUCKET, REGION, KEY_NAME in a config file.
* create a ```Data Access Object``` to encapsulate database communication
* introduce unittests
  
