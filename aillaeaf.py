import sys
import time 
import requests  

if __name__ == "__main__": 
    #log into AILLA in your webbrowser and copy the cookie. 
    #use that cookie as first argument
    cookie = {'SSESS64f35ecaf4903fe271ed0b0c15ee2bce': sys.argv[1]} 
    
    #Limit how many files to download
    LIMIT = 999999
    #LIMIT = 5
    
    with open("aillaeaf.tsv") as csvfile:
        lines = csvfile.readlines()    
    for line in lines[:LIMIT]:     
        listed_url, eafname = line.split('\t')
        #in order to proceed to download, AILLA requires we append to the path
        url = listed_url + "/datastream/OBJ/download" 
        print("downloading %s" % url)
        with requests.Session() as s:  
            r = s.post(url, cookies=cookie) 
            eafcontent = r.text 
            if eafcontent.startswith("<!DOCTYPE html>"): #no access
                print("no access")
                continue
            with open("aillaeafs/%s" % eafname.strip(),'w') as localeaf: 
                localeaf.write(eafcontent)                
            print("success")  
