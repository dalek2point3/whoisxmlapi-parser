whoisxmlapi-parser
==================

- A python parser for the whoisxml api(http://whoisxmlapi.com/), which esentially stores WHOIS JSON response and produces a CSV flatfile for analysis.

- Data description documentation is here: https://www.whoisxmlapi.com/documentation/whoisapi_documentation/index.html

- Tested on python2.7

## How to Use

1. create auth.txt with two lines with authentication details for your WHOISXMLAPI details
username
password

2. create a list of domains you want to get data for in domains.csv and a "data" folder for cached json data.

3. execute the following command
`python parser.py`




