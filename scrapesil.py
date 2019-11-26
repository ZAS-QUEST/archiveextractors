import sys
import pprint
import glob
import json
import csv
from lxml.html.soupparser import fromstring

class Record():        
    def __init__(self,root):
        def _get_text(el, field):
            try:
                return ''.join(el.find('span[@class="views-field views-field-%s"]/span'%field).itertext())
            except AttributeError:
                return ''
            
        fieldnames = [
                        'field-reap-edition',
                        'field-reap-fieldofwork',
                        'field-reap-series',
                        'field-reap-sortdate',
                        'title',
                        'views-ifempty'
                     ]
        self.refs = [{f:_get_text(div ,f) for f in fieldnames} for div in root.findall('.//div[@class="view-content"]/div')] 
        
if __name__ == "__main__":
    filenames = glob.glob('*')
    records = {}
    for filename in filenames:
        if filename.endswith('py'):
            continue
        with open(filename) as file_: 
            record = Record(fromstring(file_.read()))
            records[filename.split('.')[0]] = record.refs
            
    with open('sil.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        for record in records:
            for ref in records[record]:
                writer.writerow([record]+list(ref.values()))
            
    jrecords = json.dumps(records, sort_keys=True, indent=4)
    with open('out.json','w') as out:
        out.write(jrecords)
        
