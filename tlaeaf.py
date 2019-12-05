import sys
import time 
import requests 
import json


if __name__ == "__main__": 
    #log into TLA in your webbrowser and copy the cookie. 
    #use that cookie as first argument    
    
    #Limit how many files to download
    LIMIT = 999999
    #LIMIT = 5
    
    #prepare URLS
    with open("tla.json") as jsonfile:
        jsond = json.loads(jsonfile.read())
        
    for url in list(jsond.keys())[:LIMIT]:     
        eafname = jsond[url][0] 
        cookie = {'SESSecb87833daadde0850c5ab0b67590059': sys.argv[1]} 
        print("downloading %s" % url)
        with requests.Session() as s:  
            r = s.post(url, cookies=cookie) 
            eafcontent = r.text 
            #abort if fetched data is HTML because this is an error message
            if eafcontent.startswith("<!DOCTYPE html>"): #no access
                print("no access")
                continue
            with open("tlaeafs/%s" % eafname.strip(),'w') as localeaf: 
                localeaf.write(eafcontent)                
            print("success")  
