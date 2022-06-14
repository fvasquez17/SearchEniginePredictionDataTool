import requests 
import json
import os
import time
from tkinter import filedialog
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
import boto3

def suggestion(q,l):
    autoResults=[]
    keyword=[]
    languages=[]
    params = {
    'output': 'toolbar',
    'client': 'chrome',
    'q': 'test ',
    'hl': 'en',
    'gl': 'us'
    }
    language=l
    query=q
    query.replace(" ","+")
    params['hl'] = language
    params['q'] = query
    url = "http://suggestqueries.google.com/complete/search"
    response = requests.get(url,params)

    suggestions = json.loads(response.text)
  
    for word in suggestions[1]:
        #generated= Label(root, text=word)
        #generated.pack()
        autoResults.append(word)
        keyword.append(q.strip())
        languages.append(l)
        #print(word,language)

    return keyword,autoResults,languages;
