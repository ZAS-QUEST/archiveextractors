import sys
import pprint
import glob
import json
from lxml.html.soupparser import fromstring

class Record():
    def fulltext(self, el):
        try:
            return ''.join(el.itertext())
        except AttributeError:
            return ''

    def findtext(self, root, querystring):
        try:
            return root.find(querystring).text.strip() 
        except AttributeError:
            return ''
        
    def striptext(self, el):
        try:
            return el.text.strip()
        except AttributeError:
            return ''
        
    def __init__(self, filename, geodic, root):
        self.names = dict([(self.striptext(x.find('th')), self.striptext(x.find('.//div/div/div'))) 
                       for x 
                       in root.findall('.//table[@class="field-group-format group_table_name table table-condensed"]/tbody/tr')
                       ])
        
        self.name = self.findtext(root, './/div[@class="field field-name-field-al-reference-name field-type-text field-label-inline clearfix"]/div/div')
        self.language_comment = self.fulltext(root.find('.//language_comment'))
        self.references = [self.striptext(li) for li in root.findall('.//div[@class="field field-name-field-al-references field-type-text-long field-label-above"]/div/div/ul/li')]
        self.status = self.findtext(root, './/div[@class="field field-name-field-al-status field-type-list-text field-label-above"]/div/div')
        self.state = self.findtext(root, './/div[@class="field field-name-field-state-territory field-type-list-text field-label-above"]/div/div')
        self.location_information = self.fulltext(root.find('.//div[@class="field field-name-field-al-location-info field-type-text-long field-label-above"]/div/div'))
        self.maps = [self.fulltext(x) for x in root.findall('.//div[@class="field field-name-field-al-maps-ozbib field-type-text-long field-label-above"]/div/div/ul/li')]
        self.links = [(a.attrib["href"], self.striptext(a)) for a in root.findall('.//div[@class="field field-name-field-al-links field-type-link-field field-label-hidden"]/div/div/a')]
        self.activities = self.findtext(root, './/div[@class="field field-name-field-al-activities field-type-text-long field-label-above"]/div/div')
        self.people = self.findtext(root, './/div[@class="field field-name-field-al-people field-type-text-long field-label-above"]/div/div')
        self.indigenous_organisations = self.findtext(root, './/div[@class="field field-name-field-al-indig-orgs field-type-text-long field-label-above"]/div/div')        
        self.speaker_numbers =  [(self.striptext(tr.find('td[1]')), self.striptext(tr.find('td[2]')), self.striptext(tr.find('td[3]'))) 
                                 for tr 
                                 in root.findall('.//div[@class="field field-name-ds-code-austlang-speaker-data field-type-ds field-label-hidden"]/div/div/div/table/tbody/tr')[1:]
                                 ]
        self.documentation = [{'type':self.fulltext(tr.find('th')), 
                          'size': self.striptext(tr.find('td[1]')), 
                          'grade': self.striptext(tr.find('td[2]'))} 
                         for tr 
                         in root.findall('.//div[@class="field field-name-field-al-documentation-table field-type-text-long field-label-hidden"]/div/div/div/table/tbody/tr')[1:]]        
        self.manuscript_note = self.findtext(root, './/div[@class="field field-name-field-al-manuscript-note field-type-text-long field-label-above"]/div/div')
        self.grammar = self.findtext(root, './/div[@class="field field-name-field-al-grammar field-type-text-long field-label-above"]/div/div')          
        self.dictionary = self.findtext(root, './/div[@class="field field-name-field-al-dictionary field-type-text-long field-label-above"]/div/div')
        try:
            self.geo = geodic[filename] 
        except KeyError:
            self.geo = None
            print("no geodata for", filename)
        
if __name__ == "__main__":
    with open("austlang-compl.csv") as geocsv:
        lines = geocsv.readlines()
        geodic = {}
        for line in lines:
            ID, name, latitude, longitude =  line.strip().split('\t')
            geodic[ID.lower()] = (latitude,longitude) 
    filenames = glob.glob('austlang/*')
    records = {}
    for filename in filenames:
        with open(filename) as file_: 
            strippedfilename = filename.split('/')[-1]
            record = Record(strippedfilename, geodic, fromstring(file_.read()))
            records[strippedfilename] = record.__dict__
    jrecords = json.dumps(records, sort_keys=True, indent=4)
    with open('austlang.json','w') as out:
        out.write(jrecords)
