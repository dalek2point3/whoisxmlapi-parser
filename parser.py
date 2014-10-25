import json
import requests
import os
import re

def readlist(fname = "domains.csv"):

    domains = []
    with open(fname) as f:
        for line in f:
            # domains ideally in format, google.com, not www.google.com or http://www.google.com/
            domains.append(line.strip())
    return domains

class ContactBlock:

    def __init__(self, blocktype):
        self.fields = ['city', 'country','name','email','organization','postalCode','state', 'street1', 'street2', 'telephone', 'name']
        for field in self.fields:
            setattr(self, field, "")
        self.blocktype = blocktype

    def get_fields(self, data):
        for field in self.fields:
            if field in data:
                setattr(self, field, data[field])


class SubRecord:

    def __init__(self, recordtype, sdata):

        self.recordtype = recordtype

        self.fields = ['createdDate', 'updatedDate', 'registrarName', 'registrarIANAID']
        for field in self.fields:
            setattr(self, field, "")

        self.contacts = ['administrative', 'billing','registrant','technical','zone']
        for contact in self.contacts:
            setattr(self, contact, ContactBlock(contact))

        self.sdata = sdata

    def parse(self):

        for field in self.fields:
            if field in self.data:
                setattr(self, field, self.sdata[field])

        # TODO: make this shorter using getattr
        if 'administrativeContact' in self.sdata:
            self.administrativeContact.get_fields(self.sdata['administrativeContact'])

        if 'billingContact' in self.sdata:
            self.billingContact.get_fields(self.sdata['billingContact'])

        if 'registrant' in self.sdata:
            self.registrant.get_fields(self.sdata['registrant'])

        if 'technicalContact' in self.sdata:
            self.technicalContact.get_fields(self.sdata['technicalContact'])

        if 'zoneContact' in self.sdata:
            self.registrant.get_fields(self.sdata['zoneContact'])


class DomainRecord:

    def __init__(self, domain):
        self.domain = domain
        self.fname = "data/" + domain + ".json"

    def get_auth(self, infile='auth.txt'):
    # helper function of get username / pwd for WHOISXMLAPI
        auth = dict()

        with open(infile,'r') as f:
            auth['username'] = f.readline().strip()
            auth['pwd'] = f.readline().strip()
        return auth

    def handle_audit(self):
    # helper function of fix audit records
        if 'WhoisRecord' in self.data:

            result = self.data
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


    def get_data(self):

        outputFormat = 'json'
        auth = self.get_auth()
        user = auth['username']
        password = auth['pwd']

        url = "http://www.whoisxmlapi.com/whoisserver/WhoisService?domainName=" + self.domain + "&da=2&outputFormat=" + outputFormat + "&username=" + user + "&password=" + password
        
        if not os.path.exists(self.fname):

            # get data because it does not seem to exist
            r= requests.get(url)
            if r.status_code == 200:

                try:
                    self.data = json.loads(r.text)
                except:
                    print self.domain + " does not seem to have json data"
                    return

                with open(self.fname, 'w') as f:
                    f.write(r.text.encode('utf-8'))
                    print "fetched data to " + self.fname
            else:
                print self.domain + "  -- error getting data"
                self.data = ""
                return
        else:
            # read data that we have saved before
            with open(self.fname) as f:
                print "exists: " + self.fname
                self.data = json.loads(f.read().decode('utf8'))

        self.data = self.handle_audit()
        return


    def parse_data(self):

        if self.data == None:
            return

        if 'WhoisRecord' in self.data:
            self.whois = SubRecord("whois", self.data['WhoisRecord'])
            print "parsing whois"
            self.whois.parse()

        if 'registryData' in self.data['WhoisRecord']:
            self.registrydata = SubRecord("whois",  self.data['WhoisRecord']['registryData'])
            print "parsing rdata"
            self.registrydata.parse()


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

    # print "writing data"
    # writedata(domainrecords, "data2.csv")

    # testing
    # domains = ["www.creativedistrict.com"]
    # domains = ["www.cows.de", "www.ipeen.com.tw", "www.spotted.de", "www.csscorp.com"]
    # domains = ["www.ipeen.com.tw"]
    # for domain in domains:
    #    test_domain(domain)
    

