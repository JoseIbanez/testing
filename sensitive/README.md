# Masking customer file

The propouse of this code is to anonymize a customers file in csv format.

The first line of the file, should contain the collumn names. Collumns names define if the value is sensitive, and should be masked in the output.

The code generates a new file in the current path with a fix name: masked_clients.csv

Two type or masking is performed, as the type of the collumn, TEXT, or NUMERIC. Character sustitituion, or average calculations.


## Usage:

Usage example:
````bash
% ls -l
total 48
-rw-r--r--  1 ibanez  staff  1873 May 22 11:56 README.md
-rw-r--r--  1 ibanez  staff   275 May 21 21:53 customers 3.csv
-rw-r--r--  1 ibanez  staff  4689 May 22 12:00 masking.py
%
% cat "./customers 3.csv"
ID,Name,Email,Billing,Location
1,John Smith,john@mail.com,15000,New York
2,Kelly Lawrence Gomez,Kelly@your-mail.com,20000,Washington
3,Carl Winslow,carl-wins@mail-bot.com, ,Seattle
4,Roger Rogers,doubleR@mailer.com,12400.27,Boston
5,Gerald Frances, gf@jmail.com,53000,Dallas
%
% python3 ./masking.py 
Input filename: ./customers 3.csv
Name: Max. 20, Min. 10, Avg. 13.6
Billing: Max. 53000.0, Min. 0, Avg. 20080.054
%
% cat masked_clients.csv 
ID,Name,Email,Billing,Location
1,XXXX XXXXX,XXXX@XXXX.XXX,15000.0,New York
2,XXXXX XXXXXXXX XXXXX,XXXXX@XXXXXXXXX.XXX,20000.0,Washington
3,XXXX XXXXXXX,XXXXXXXXX@XXXXXXXX.XXX,0.0,Seattle
4,XXXXX XXXXXX,XXXXXXX@XXXXXX.XXX,12400.27,Boston
5,XXXXXX XXXXXXX,XX@XXXXX.XXX,53000.0,Dallas
%
````

## Program configurationd:

I defined some global constants to modify the code behavior and provide extra flexibility:

### SENSITIVE_FIELDS_TEXT

This define the list of SENTIVIVE collumns to managed as text columns, you can add more columns if a new format file needs that

Default: SENSITIVE_FIELDS_TEXT = [ "Name", "Email"]

### SENSITIVE_FIELDS_NUMBER

Same as before, list of SENTITIVE collumns, but for numeric management, avg. calculation 

Default: SENSITIVE_FIELDS_NUMBER = [ "Billing" ] 

### SPECIAL_CHARS

We want to not mask some characters of sensitive text fieds, statement says about "@", and ".", I added also space " ", I think this is nice for name collumn. This constant has the list of characters to keep.

Default: SPECIAL_CHARS = "@. "

### REPORT_COLUMNS 

As optinal, we want some statistics for several collumns, here is the list of collumns to generate a proccess report

Note: Numeric columns of the report must be included as SENSITIVE collumns

Default: REPORT_COLUMNS = ["Name","Billing"]


### STRIP_OUTPUT = True

I see some extra spaces, at the begining or at the end, in some cells of the example file. Maybe is good idea to remove those extra spaces. This constant define this behavior, remove or not remove extra spaces in the values before mask them.


Default: STRIP_OUTPUT = True



### Owner 
Jose Ibañez Vela