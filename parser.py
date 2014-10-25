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

def makeline(items):
    items = [strip_non_ascii(str(x)) for x in items]
    items = [re.sub(r'[\n\t]+', '', x) for x in items]
    row = "\t".join(items) + "\n"
    return row

def writedata(drecords, outfile = "data.csv"):

    fields = ['city', 'country','name','email','organization','postalCode','state', 'street1', 'street2', 'telephone']
    cols1 = ['domain', 'subrecord','created','updated','registrarname','registrarid','parsecode', 'contacttype']

    cols = cols1 + fields

    subrecords = ["whois", "registrydata"]
    contacts = ['administrativeContact', 'billingContact','registrant','technicalContact','zoneContact']

    with open(outfile, 'w') as outf:
        outf.write(makeline(cols))

        for d in drecords:
            if d.domain != "":
                for sr in subrecords:
                    if getattr(d,sr) != "":
                        sub_record = getattr(d,sr)
                        items1 = [d.domain, sr, sub_record.createdDate, sub_record.updatedDate,sub_record.registrarName, sub_record.registrarIANAID, sub_record.parseCode]

                        for c in contacts:
                            cnt = getattr(sub_record, c)
                            items2 = [c]
                            for f in fields:
                                items2.append(getattr(cnt,f))

                            items = items1 + items2
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



