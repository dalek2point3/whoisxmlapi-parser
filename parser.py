#!/usr/bin/env python
from DomainRecord import *

"""parse.py: This program reads a list of domains from domains.csv, gets WHOIS data and stores in data/ folder and then converts this data to csv and writes it to a file -- data.csv."""

__author__ = "dalek2point3"
__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"

def readlist(fname = "domains.csv"):
    domains = []
    with open(fname) as f:
        for line in f:
            # domains ideally in format, google.com, not www.google.com or http://www.google.com/
            domains.append(line.strip())
    return domains

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def makeline(items):

    vals = []
    # TODO: fix ugly unicode hack
    for x in items:
        if type(x) == int:
            vals.append(str(x))
        else:
            vals.append(strip_non_ascii(x))

    ##items = [strip_non_ascii(str(x)) for x in items]
    vals = [re.sub(r'[\n\t]+', '', x) for x in vals]
    row = "\t".join(vals) + "\n"
    return row

def writedata(drecords, outfile = "data.csv"):
    cols1 = ['domain', 'subrecord','created','updated','registrarname','registrarid','parsecode', 'contacttype']
    fields = ['city', 'country','name','email','organization','postalCode','state', 'street1', 'street2', 'telephone']
    cols = cols1 + fields

    with open(outfile, 'w') as outf:
        outf.write(makeline(cols))
        for d in drecords:
            lines = d.make_lines()
            for items in lines:
                outf.write(makeline(items))

    return

def get_data(domains):
    drecords = []
    count = 0
    for domain in domains:
        print "getting " + str(count)
        count+=1
        d = DomainRecord(domain)
        d.get_data()
        d.parse_data()
        drecords.append(d)
    return drecords

def test_record(d):
    for x in d.whois.fields:
        print x, getattr(d.whois, x)

if __name__ == "__main__":

    domains = readlist("domains.csv")
    drecords = get_data(domains)
    writedata(drecords)

    #test_record(drecords[0])



