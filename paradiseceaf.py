import sys 
import requests  
import json

if __name__ == "__main__":  
    #Log in to paradisec in your browser and get the cookie value. 
    #Provide this value as first argument
    cookie = {'_session_id':  sys.argv[1]} 
    
    #get urls from paradisec.json
    with open("paradisec.json") as pjson:
        dico = json.loads(pjson.read())
            
    #compute urls to use
    #PARADISEC has a naming scheme for URLs which can be inferred
    #from eaf file names. 
    archive_url = "http://catalog.paradisec.org.au/repository/%s/%s/%s"
    #Assemble all download URLs
    urls = []
    for collection in dico.keys():
        for filename in dico[collection]:
            first, second, thirdthrowaway = filename.split('-')     
            urls.append(archive_url%(first, second, filename))  

    s = requests.Session() 
    for url in urls: 
        print(url)
        outfilename = url.split('/')[-1]
        eafcontent = s.post(url, cookies=cookie).text
        #abort if fetched data is HTML because this is an error message
        if eafcontent.startswith("<!DOCTYPE html>"):
            print("no access")
            continue
        #save eaf XML data
        with open("paradiseceafs/%s" % outfilename,'w') as localeaf: 
            localeaf.write(eafcontent) 
