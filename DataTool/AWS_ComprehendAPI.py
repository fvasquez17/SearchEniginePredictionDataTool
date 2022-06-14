import boto3
import requests 
import json
import pandas as pd
from datetime import date

def analysis(keyword,s,l,engine):



    today = date.today().strftime("%B %d, %Y")
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    df = pd.DataFrame(columns=['KeyWord',
                                'Search Engine',
                                'Query',
                                'Language',
                                'Sentiment',
                                'Mixed',
                                'Negative',
                                'Neutral',
                                'Positive',
                                'Date'])
    searchEngine=engine
    kw=keyword
    lang=l
    text=s
    #print('Running Sentimental Analysis: ',text)
    data=json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode=lang), sort_keys=True, indent=4)
    parser=json.loads(data)
    parser2=parser['SentimentScore']
    df_new_row = pd.DataFrame({'KeyWord':[kw],
                               'Search Engine':[engine],
                               'Query':[s],
                               'Language':[lang],
                               'Sentiment':[parser['Sentiment']],
                               'Mixed':[parser2['Mixed']],
                               'Negative':[parser2['Negative']],
                               'Neutral':[parser2['Neutral']],
                               'Positive':[parser2['Positive']],
                               'Date':[today]
                               })



    #print(df[['Query','Language','Sentiment','Mixed','Negative','Neutral','Positive']])
    #print('End of DetectSentiment\n')        
    df = pd.concat([df, df_new_row], ignore_index=True)
    return df;



