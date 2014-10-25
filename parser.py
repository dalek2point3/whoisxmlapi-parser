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

def writedata(domainrecords, outfile = "data.csv"):
    return

def getdata(domains):
    domainrecords = []
    count = 0
    for domain in domains:
        print "getting " + str(count)
        count+=1
        d = DomainRecord(domain)
        d.getdata()
        domainrecords.append(d)
    return domainrecords


if __name__ == "__main__":

    domains = readlist("domains.csv")

    d = DomainRecord(domains[0])
    d.get_data()
    d.parse_data()

    for x in d.whois.fields:
        print x, getattr(d.whois, x)

    # print "writing data"
    # writedata(domainrecords, "data2.csv")

    # testing
    # domains = ["www.creativedistrict.com"]
    # domains = ["www.cows.de", "www.ipeen.com.tw", "www.spotted.de", "www.csscorp.com"]
    # domains = ["www.ipeen.com.tw"]
    # for domain in domains:
    #    test_domain(domain)
    

