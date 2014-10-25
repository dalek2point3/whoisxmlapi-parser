from DomainRecord import *

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

def writedata(drecords, outfile = "data.csv"):
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
        domainrecords.append(d)
    return drecords

def test_record(d):
    for x in d.whois.fields:
        print x, getattr(d.whois, x)

if __name__ == "__main__":

    domains = readlist("domains.csv")
    drecords = get_data(domains)




