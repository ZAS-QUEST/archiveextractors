import sys
import pprint
import glob
import json
from lxml.html.soupparser import fromstring

class Record():
    def fulltext(self, el):
        return ''.join(el.itertext())

    def findtext(self, root, querystring):
        try:
            return root.find(querystring).text.strip() 
        except AttributeError:
            return ''
        
    def __init__(self,root):
        self.names = dict([(x.find('th').text, x.find('.//div/div/div').text) 
                       for x 
                       in root.findall('.//table[@class="field-group-format group_table_name table table-condensed"]/tbody/tr')
                       ])
        
        self.language_comment = self.fulltext(root.find('.//language_comment'))
        self.references = [li.text for li in root.findall('.//div[@class="field field-name-field-al-references field-type-text-long field-label-above"]/div/div/ul/li')]
        self.status = self.findtext(root, './/div[@class="field field-name-field-al-status field-type-list-text field-label-above"]/div/div')
        self.state = self.findtext(root, './/div[@class="field field-name-field-state-territory field-type-list-text field-label-above"]/div/div')
        self.location_information = self.fulltext(root.find('.//div[@class="field field-name-field-al-location-info field-type-text-long field-label-above"]/div/div'))
        self.maps = [self.fulltext(x) for x in root.findall('.//div[@class="field field-name-field-al-maps-ozbib field-type-text-long field-label-above"]/div/div/ul/li')]
        self.links = [(a.attrib["href"],a.text) for a in root.findall('.//div[@class="field field-name-field-al-links field-type-link-field field-label-hidden"]/div/div/a')]
        self.activities = self.findtext(root, './/div[@class="field field-name-field-al-activities field-type-text-long field-label-above"]/div/div')
        self.people = self.findtext(root, './/div[@class="field field-name-field-al-people field-type-text-long field-label-above"]/div/div')
        self.indigenous_organisations = self.findtext(root, './/div[@class="field field-name-field-al-indig-orgs field-type-text-long field-label-above"]/div/div')        
        self.speaker_numbers =  [(tr.find('td[1]').text, tr.find('td[2]').text, tr.find('td[3]').text) 
                                 for tr 
                                 in root.findall('.//div[@class="field field-name-ds-code-austlang-speaker-data field-type-ds field-label-hidden"]/div/div/div/table/tbody/tr')[1:]
                                 ]
        documentation = [{'type':self.fulltext(tr.find('th')), 
                          'size': tr.find('td[1]').text, 
                          'grade': tr.find('td[2]').text} 
                         for tr 
                         in root.findall('.//div[@class="field field-name-field-al-documentation-table field-type-text-long field-label-hidden"]/div/div/div/table/tbody/tr')[1:]]        
        self.manuscript_note = self.findtext(root, './/div[@class="field field-name-field-al-manuscript-note field-type-text-long field-label-above"]/div/div')
        self.grammar = self.findtext(root, './/div[@class="field field-name-field-al-grammar field-type-text-long field-label-above"]/div/div')          
        self.dictionary = self.findtext(root, './/div[@class="field field-name-field-al-dictionary field-type-text-long field-label-above"]/div/div')

        

        
    def csv():
        pass
    
    def json():
        pass
    
    def haraldhammarstroem():
        pass
    
        
        
if __name__ == "__main__":
    filenames = glob.glob('*')
    records = {}
    for filename in filenames:
        if filename.endswith('py'):
            continue
        with open(filename) as file_:
            try:
                record = Record(fromstring(file_.read()))
            except AttributeError:
                print("could not parse", filename)
                continue
            records[filename] = record.__dict__
    jrecords = json.dumps(records, sort_keys=True, indent=4)
    with open('out.json','w') as out:
        out.write(jrecords)
        #record.csv()
        #record.json()
        #record.haraldhammarstroem()
        
