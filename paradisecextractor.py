import glob
import json
from collections import defaultdict
#from lxml import etree
from lxml.html.soupparser import fromstring

BASEURL = "https://catalog.paradisec.org.au"

if __name__ == "__main__":
    PREFIX = ''
    OFFSET = 0
    LIMIT = 999999
    dico = defaultdict(list)
    RECORDS = glob.glob("paradisec/items/%s*"%PREFIX)[OFFSET:LIMIT]
    for i, record in enumerate(RECORDS):
        with open(record, "r") as file_:
            contents = file_.read()
            try:
                root = fromstring(contents)
            except ValueError:
                root = fromstring(contents.replace('\x0b', ' '))
            trs = root.findall("body/div/div/div/fieldset/table/tbody/tr")
            for tr in trs:
                td = tr.find('td')
                if td.text.endswith('eaf'):
                    collectionlink = root.find(".//body/div/div/div/fieldset/table//tr[6]/td/a")
                    print("%s%s : %s"%(BASEURL, collectionlink.attrib["href"], td.text))
                    dico[collectionlink.attrib["href"]].append(td.text)

    with open("paradisec.json", "w") as out:
        out.write(json.dumps(dico, sort_keys=True, indent=4))
