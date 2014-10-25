import json
import requests
import os
import re

def get_auth(infile='auth.txt'):
    auth = dict()
    with open(infile) as f:
        auth['username'] = f.readline().strip()
        auth['pwd'] = f.readline().strip()
    return auth

def readlist(fname = "domains.csv"):

    domains = []
    with open(fname) as f:
        for line in f:
            # domains ideally in format, google.com, not www.google.com or http://www.google.com/
            domains.append(line.strip())
        
    return domains


class DomainRecord:

    def __init__(self, domain):
        self.domain = domain
        self.createdDate = ""
        self.org = ""
        self.street1 = ""
        self.street2 = ""
        self.street3 = ""
        self.city = ""
        self.postalCode = ""
        self.country = ""
        self.state = ""
        self.email = ""
        self.telephone = ""
        self.name = ""
        self.fname = "data/" + domain + ".json"

    def handle_audit(self):
        
        if 'WhoisRecord' in self.data:

            result = self.data['WhoisRecord']
            if 'audit' in result:
                if 'createdDate' in result['audit']:
                    if '$' in result['audit']['createdDate']:
                        result['audit']['createdDate'] = result['audit']['createdDate']['$']
                if 'updatedDate' in result['audit']:
                    if '$' in result['audit']['updatedDate']:
                        result['audit']['updatedDate'] = result['audit']['updatedDate']['$']
                        
            return result
        else:
            print "no WHOIS RECORD in " + self.domain

    def getdata(self):

        outputFormat = 'json'
        user = 'dalek2point3'
        password = 'quark'

        url = "http://www.whoisxmlapi.com/whoisserver/WhoisService?domainName=" + self.domain + "&da=2&outputFormat=" + outputFormat + "&username=" + user + "&password=" + password
        
        if not os.path.exists(self.fname):
            r= requests.get(url)
            if r.status_code == 200:

                try:
                    self.data = json.loads(r.text)
                except:
                    print self.domain
                    return

                with open(self.fname, 'w') as f:
                    f.write(r.text.encode('utf-8'))
                    print "wrote data to " + self.fname
            else:
                self.data = ""
        else:
            with open(self.fname) as f:
                print "exists: " + self.fname
                self.data = json.loads(f.read().decode('utf8'))
                self.data = self.handle_audit()

    def parse(self):

        registrant = []
        result = self.data

        if result == None:
            return
            
        #if 'audit' in result:
        #    if 'createdDate' in result['audit']:
        #        self.createdDate = result['audit']['createdDate']

        # TODO: if multiple of these exist, choose the best one
        if 'registrant' in result:
            registrant = result['registrant']
        elif 'registryData' in result:
            if 'registrant' in result['registryData']:
                registrant = result['registryData']['registrant']
            elif 'technicalContact' in result['registryData']:
                registrant = result['registryData']['technicalContact']
            elif 'zoneContact' in result['registryData']:
                registrant = result['registryData']['zoneContact']
            elif 'administrativeContact' in result['registryData']:
                registrant = result['registryData']['administrativeContact']
        else:
            print self.domain + ": registrant not found"
            return

        if 'createdDate' in registrant:
            self.createdDate = registrant['createdDate']
        elif 'createdDate' in result:
            self.createdDate = result['createdDate']
        elif 'createdDate' in result['registryData']:
            self.createdDate = result['registryData']['createdDate']

        if 'organization' in registrant:
            self.org = registrant['organization']

        if 'name' in registrant:
            self.name = registrant['name']

        if 'organization' in registrant:
            self.org = registrant['organization']

        if 'street1' in registrant:
            self.street1 = registrant['street1']

        if 'street2' in registrant:
            self.street2 = registrant['street2']

        if 'street3' in registrant:
            self.street3 = registrant['street3']

        if 'city' in registrant:
            self.city = registrant['city']

        if 'postalcode' in registrant:
            self.postalcode = registrant['country']

        if 'state' in registrant:
            self.state = registrant['state']

        if 'country' in registrant:
            self.country = registrant['country']

        if 'email' in registrant:
            self.email = registrant['email']

        if 'telephone' in registrant:
            self.telephone = registrant['telephone']

        if 'postalCode' in registrant:
            self.postalCode = registrant['postalCode']

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def writedata(domainrecords, outfile = "data.csv"):
    
    header = "\t".join(["domain", "createdDate", "name", "org", "street1", "street2", "street3", "city", "state", "postalCode", "country", "email", "telephone"]) + "\n"
    with open(outfile, 'w') as f:
        f.write(header)
        for d in domainrecords:
            d.parse()
            print "writing " + d.domain

            items = [d.domain, d.createdDate, d.name, d.org, d.street1, d.street2, d.street3, d.city, d.state, d.postalCode, d.country, d.email, d.telephone] 

            # items = [re.sub(r'[^\x00-\x7F\n\t]+', '', x) for x in items]
            items = [strip_non_ascii(x) for x in items]
            items = [re.sub(r'[\n\t]+', '', x) for x in items]

            row = "\t".join(items) + "\n"
            f.write(row)

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


def test_domain(domain):
    d = DomainRecord(domain)
    d.getdata()
    d.parse()
    
    items = [d.org, d.street1, d. name, d. country, d.createdDate]
    items = [re.sub(r'[\n\t]+', '', x) for x in items]
    print "----------"
    print items
    print "----------"

if __name__ == "__main__":

    domains = readlist()
    print domains
    #domains = domains[0:500]
    print 
    print "fetching data"
    print "..."
    # domainrecords = getdata(domains)
    
    # print "writing data"
    # writedata(domainrecords, "data2.csv")

    # testing
    # domains = ["www.creativedistrict.com"]
    # domains = ["www.cows.de", "www.ipeen.com.tw", "www.spotted.de", "www.csscorp.com"]
    # domains = ["www.ipeen.com.tw"]
    # for domain in domains:
    #    test_domain(domain)
    

