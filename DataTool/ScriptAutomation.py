
import pandas as pd
import numpy as np
import boto3
import requests 
import json
import AWS_ComprehendAPI
import BingSearchAPI
import GoogleSearchAPI
import os.path

#Group of parallel arrays linear time complexity
GoogleResults=[]
BingResults=[]
GoogleKeyWordCounter=[]
BingKeyWordCounter=[]
googleLang=[]
bingLang=[]


def get_csv(df, file_name):
    df.to_csv(file_name,index=False)

def csvReader ():
    try:
        df = pd.read_csv('KeyWords.csv',names=['KeyWord',
                                             'Language'])
    except:
        print("File NOT FOUND")
        

    else:
        global keywords
        global kwLanguages

        keywords = df['KeyWord'].to_numpy()
        kwLanguages = df['Language'].to_numpy()
        print(keywords,"  ",kwLanguages)

def googlePredictions ():
    for i in range(len(keywords))[1:]:
        #print("Scraping suggestions on Google for KeyWord: ",keywords[i]) 
        google_keywords, google_suggestions, google_languages=GoogleSearchAPI.suggestion(keywords[i],kwLanguages[i])
        GoogleResults.extend(google_suggestions)
        GoogleKeyWordCounter.extend(google_keywords)
        googleLang.extend(google_languages)
       #print(GoogleResults)

def bingPredictions ():
    for i in range(len(keywords))[1:]:
        #print("Scraping suggestions on Bing for KeyWord: ",keywords[i])
        bing_keywords,bing_suggestions,bing_languages=BingSearchAPI.makeBingRequest(keywords[i],kwLanguages[i])
        BingResults.extend(bing_suggestions)
        BingKeyWordCounter.extend(bing_keywords)
        bingLang.extend(bing_languages)
    #print(BingResults)

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
df1 = pd.DataFrame(columns=['KeyWord',
                        'Search Engine',
                        'Query',
                        'Language',
                        'Sentiment',
                        'Mixed',
                        'Negative',
                        'Neutral',
                        'Positive',
                        'Date'])

def sentimentGoogle ():
    for i in range(len(GoogleResults)):
        engine="Google"
        # print("Google Search suggestion is: ",GoogleResults[i])
        df2=AWS_ComprehendAPI.analysis(GoogleKeyWordCounter[i],GoogleResults[i],googleLang[i],engine)
        global df1
        df1 = pd.concat([df1, df2], ignore_index = True)

def sentimentBing ():
    for a in range(len(BingResults)):
        engine="Bing"
        df2=AWS_ComprehendAPI.analysis(BingKeyWordCounter[a],BingResults[a],bingLang[a],engine)
        global df1
        df1 = pd.concat([df1, df2], ignore_index = True)
        #print("Bing Search suggestion is: ",BingResults[a])

def DownloadCSV():

    if os.path.isfile('Results.csv'):
        df = pd.read_csv('Results.csv')
        df = pd.concat([df, df1], ignore_index = True)
        df.to_csv('Results.csv',index=False)
    else:
        df1.to_csv('Results.csv',index=False)
        

def run():
    csvReader ()
    googlePredictions ()
    bingPredictions ()
    sentimentGoogle ()
    sentimentBing ()
    DownloadCSV()

