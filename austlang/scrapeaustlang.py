import sys
import pprint
from lxml.html.soupparser import fromstring

class Record():
    def fulltext(self,el):
        return ''.join(el.itertext())
    
    def __init__(self,root):
        self.names = dict([(x.find('th').text, x.find('.//div/div/div').text) 
                       for x 
                       in root.findall('.//table[@class="field-group-format group_table_name table table-condensed"]/tbody/tr')
                       ])
        
        self.language_comment = ''.join(root.find('.//language_comment').itertext())
        self.references = [li.text for li in root.findall('.//div[@class="field field-name-field-al-references field-type-text-long field-label-above"]/div/div/ul/li')]
        self.status = root.find('.//div[@class="field field-name-field-al-status field-type-list-text field-label-above"]/div/div').text
        self.state = root.find('.//div[@class="field field-name-field-state-territory field-type-list-text field-label-above"]/div/div').text
        self.location_information = ''.join(root.find('.//div[@class="field field-name-field-al-location-info field-type-text-long field-label-above"]/div/div').itertext())
        self.maps = [self.fulltext(x) for x in root.findall('.//div[@class="field field-name-field-al-maps-ozbib field-type-text-long field-label-above"]/div/div/ul/li')]
        self.links = [(a.attrib["href"],a.text) for a in root.findall('.//div[@class="field field-name-field-al-links field-type-link-field field-label-hidden"]/div/div/a')]
        self.activities = root.find('.//div[@class="field field-name-field-al-activities field-type-text-long field-label-above"]/div/div').text
        self.people = root.find('.//div[@class="field field-name-field-al-people field-type-text-long field-label-above"]/div/div').text
        self.indigenous_organisations = root.find('.//div[@class="field field-name-field-al-indig-orgs field-type-text-long field-label-above"]/div/div').text        
        #self.speaker_numbers =  [(tr.find('td[1]').text, tr.find('td[2]').text, tr.find('td[3]').text) 
                                 #for tr 
                                 #in root.find('.//div[@class="field field-name-ds-code-austlang-speaker-data field-type-ds field-label-hidden"]/div/div/div/table/tbody/tr')[1:]
                                 #]
        documentation = [{'type':self.fulltext(tr.find('th')), 
                          'size': tr.find('td[1]').text, 
                          'grade': tr.find('td[2]').text} 
                         for tr 
                         in root.findall('.//div[@class="field field-name-field-al-documentation-table field-type-text-long field-label-hidden"]/div/div/div/table/tbody/tr')[1:]]        
        self.manuscript_note = root.find('.//div[@class="field field-name-field-al-manuscript-note field-type-text-long field-label-above"]/div/div').text        
        self.grammar = root.find('.//div[@class="field field-name-field-al-grammar field-type-text-long field-label-above"]/div/div').text            
        self.dictionary = root.find('.//div[@class="field field-name-field-al-dictionary field-type-text-long field-label-above"]/div/div').text     
        
    def csv():
        pass
    
    def json():
        pass
    
    def haraldhammarstroem():
        pass
    
        
        
if __name__ == "__main__":
    filename = sys.argv[1]
    root = fromstring(open(filename).read())
    record = Record(root)
    pprint.pprint(record.__dict__)
    #record.csv()
    #record.json()
    #record.haraldhammarstroem()
    
