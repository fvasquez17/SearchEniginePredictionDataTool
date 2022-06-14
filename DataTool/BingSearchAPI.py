import requests
import xmltodict

def makeBingRequest(query,market):
    lang=market
    mkt=lang+"-US"
    URL = "https://api.bing.com/qsml.aspx"
    PARAMS = {"Market":mkt,
            "query":query}
    headers = {'User-agent':'Mozilla/5.0'}
    response = requests.get(URL, params=PARAMS, headers=headers)
    if response.status_code == 200:
        obj = None
        obj = xmltodict.parse(response.content)
        suggestList = []
        keywordCounter=[]
        languages=[]
        if obj['SearchSuggestion']['Section'] != None:
            suggests = obj['SearchSuggestion']['Section']['Item']
            if len(suggests)==1:
                suggests = [suggests]
            for suggest in suggests:
                _s = suggest['Text']
                suggestList.append(_s)
                keywordCounter.append(query.strip())
                languages.append(lang)
                
        return keywordCounter,suggestList,languages;
    else:
        return ""


#str =makeBingRequest("covid est ","es-US")
#print(str)
