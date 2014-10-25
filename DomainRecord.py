import json
import requests
import os
import re

class ContactBlock:

    def __init__(self, blocktype):
        self.fields = ['city', 'country','name','email','organization','postalCode','state', 'street1', 'street2', 'telephone']
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

        self.fields = ['createdDate', 'updatedDate', 'registrarName', 'registrarIANAID', 'parseCode']
        for field in self.fields:
            setattr(self, field, "")

        self.contacts = ['administrativeContact', 'billingContact','registrant','technicalContact','zoneContact']
        for contact in self.contacts:
            setattr(self, contact, ContactBlock(contact))

        self.sdata = sdata

    def parse(self):

        for field in self.fields:
            if field in self.sdata:
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
        self.whois = ""
        self.registrydata = ""

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
            self.whois.parse()

        if 'registryData' in self.data['WhoisRecord']:
            self.registrydata = SubRecord("registryData",  self.data['WhoisRecord']['registryData'])
            self.registrydata.parse()


    def make_lines(self):
    # this converts the entire data structure into multiple lines, one each for sub-record / contact combo

        subrecords = ["whois", "registrydata"]
        lines = []

        for sr in subrecords:
            if getattr(self,sr) != "":
                        sub_record = getattr(self,sr)
                        items1 = [self.domain, sr, sub_record.createdDate, sub_record.updatedDate,sub_record.registrarName, sub_record.registrarIANAID, sub_record.parseCode]

                        for c in sub_record.contacts:
                            cnt = getattr(sub_record, c)
                            items2 = [c]

                            notempty_flag = 0
                            for f in cnt.fields:
                                items2.append(getattr(cnt,f))
                                # if not empty, set flag to 1
                                if getattr(cnt,f) != "":
                                    notempty_flag = max(notempty_flag, 1)

                            if notempty_flag > 0:
                                items = items1 + items2
                                lines.append(items)

        return lines
