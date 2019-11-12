import glob 
import json
from collections import defaultdict
from lxml import etree  
from lxml.html.soupparser import fromstring

BASEURL = "https://catalog.paradisec.org.au"

if __name__ == "__main__": 
    prefix = ''
    offset = 0 
    limit = 999999
    d = defaultdict(list)
    records = glob.glob("paradisec/items/%s*"%prefix)[offset:limit]
    for i, record in enumerate(records):
        with open(record, "r") as file_: 
            contents = file_.read() 
            try:
                root = fromstring(contents)
            except ValueError as e: 
                root = fromstring(contents.replace('\x0b',' '))
            trs = root.findall("body/div/div/div/fieldset/table/tbody/tr")
            for tr in trs: 
                td = tr.find('td')        
                if td.text.endswith('eaf'):
                    collectionlink = root.find(".//body/div/div/div/fieldset/table//tr[6]/td/a")
                    print("%s%s : %s"%(BASEURL, collectionlink.attrib["href"], td.text))
                    d[collectionlink.attrib["href"]].append(td.text)
                    
    with open("paradisec.json","w") as out:
        out.write(json.dumps(d, sort_keys=True, indent=4))
                
