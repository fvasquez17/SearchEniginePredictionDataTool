from tkinter import*
import pandas as pd
import numpy as np
import boto3
import requests 
import json
import AWS_ComprehendAPI
import BingSearchAPI
import GoogleSearchAPI
from tkinter import filedialog
import os.path


root = Tk()
root.title("Search Prediction Scraper")
root.geometry("400x700")

#Group of parallel arrays linear time complexity
GoogleResults=[]
BingResults=[]
GoogleKeyWordCounter=[]
BingKeyWordCounter=[]
googleLang=[]
bingLang=[]
print("im here")

def openSheetsWindow():
    
    newWindow = Toplevel(root)
    newWindow.title("Google Sheets Graber")
    newWindow.geometry("500x300")

    def url_builder(DOC_ID, SHEET_ID):
        return f'https://docs.google.com/spreadsheets/d/{DOC_ID}/export?format=csv&gid={SHEET_ID}'

    def get_csv(df, file_name):
        df.to_csv(file_name,index=False)
        
    def GoogleSheetDocID():
        userGSheetsDocID = Label(newWindow, text="Google Sheet Doc ID :"+ doc_id.get())
        userGSheetsDocID.pack()
        global DOC_ID
        DOC_ID = doc_id.get()

    def GoogleSheetGidID():
        userGSheetsGidID = Label(newWindow, text="Google Sheet GID ID :"+ gid_id.get())
        userGSheetsGidID.pack()
        global SHEET_ID
        SHEET_ID = gid_id.get()

    def GoogleSheetGrabber():
        try:
            URL = url_builder(DOC_ID, SHEET_ID)
            df = pd.read_csv(URL)
            file_name = "KeyWords.csv"#Enter any name for the file followed by ".csv"
        except:
            errorLabel = Label(newWindow, text="Google Sheet NOT FOUND! Try entering ID information again!")
            errorLabel.pack()
        else:
            get_csv(df, file_name)
            successLabel = Label(newWindow, text="Google Sheet has succesfully been downloaded")
            successLabel.pack()


    
    doc_id = Entry(newWindow, width=80)
    doc_id.pack()

    idButton = Button(newWindow, text="Enter the Doc ID", command= GoogleSheetDocID)
    idButton.pack()


    gid_id = Entry(newWindow, width=80)
    gid_id.pack()


    gidButton = Button(newWindow, text="Enter the Gid ID", command= GoogleSheetGidID)
    gidButton.pack()




    GetKeywords = Button(newWindow, text="Get Keywords from Sheets", command = GoogleSheetGrabber)
    GetKeywords.pack()

    newWindow.mainloop()



def csvReader ():
    try:
        filepath= filedialog.askopenfilename(initialdir='D:/Users/')
        file = open(filepath,'r')
        df = pd.read_csv(file,names=['KeyWord',
                                    'Language'])
    except:
        errorLabel = Label(root, text="File NOT FOUND or File NOT SELECTED!")
        errorLabel.pack()

    else:
        global keywords
        global kwLanguages

        keywords = df['KeyWord'].to_numpy()
        kwLanguages = df['Language'].to_numpy()
        successLabel = Label(root, text="Keywords have been retrieved from CSV File Successfully!")
        successLabel.pack()
        print(keywords,"  ",kwLanguages)

def googlePredictions ():
    for i in range(len(keywords))[1:]:
        #print("Scraping suggestions on Google for KeyWord: ",keywords[i]) 
        google_keywords, google_suggestions, google_languages=GoogleSearchAPI.suggestion(keywords[i],kwLanguages[i])
        GoogleResults.extend(google_suggestions)
        GoogleKeyWordCounter.extend(google_keywords)
        googleLang.extend(google_languages)
    completeLabel = Label(root, text="Google Auto Predictions have been collected!").pack()
    #print(GoogleResults)
    
def bingPredictions ():
    for i in range(len(keywords))[1:]:
        #print("Scraping suggestions on Bing for KeyWord: ",keywords[i])
        bing_keywords,bing_suggestions,bing_languages=BingSearchAPI.makeBingRequest(keywords[i],kwLanguages[i])
        BingResults.extend(bing_suggestions)
        BingKeyWordCounter.extend(bing_keywords)
        bingLang.extend(bing_languages)
    completeLabel = Label(root, text="Bing Auto Predictions have been collected!").pack()
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
    completeLabel = Label(root, text="Google Suggestions Sentimental Analysis is complete!").pack()
    
def sentimentBing ():
    for a in range(len(BingResults)):
        engine="Bing"
        df2=AWS_ComprehendAPI.analysis(BingKeyWordCounter[a],BingResults[a],bingLang[a],engine)
        global df1
        df1 = pd.concat([df1, df2], ignore_index = True)
        #print("Bing Search suggestion is: ",BingResults[a])
    completeLabel = Label(root, text="Bing Suggestions Sentimental Analysis is complete!").pack()
def DownloadCSV():

    if os.path.isfile('Results.csv'):
        df = pd.read_csv('Results.csv')
        df = pd.concat([df, df1], ignore_index = True)
        appendLabel = Label(root, text="New Data has been added to Results.csv").pack()
    else:
        df1.to_csv('Results.csv',index=False)
        completeLabel = Label(root, text="The Data collection has been saved as Results.csv").pack()

#def RunAutomation():
 #   import PyAutomator
    #PyAutomator.job()


    
sheetLabel = Label(root, text="Download the LATEST Google Sheet Keyword File as CSV if Needed").pack()
sheetWindow = Button(root, text="Save KeyWords from Google Sheets as CSV", command= openSheetsWindow)
sheetWindow.pack()

readLabel = Label(root, text="Open the CSV File with the Keywords for Data Collection").pack()
readKeywordCSV = Button(root, text="Read KeyWords from CSV File", command= csvReader)
readKeywordCSV.pack()

googleLabel = Label(root, text="Scrape Google Auto Predictions Manually").pack()
googleSugg = Button(root, text="Scrape Google Search Auto Predictions", command= googlePredictions)
googleSugg.pack()

bingLabel = Label(root, text="Scrape Bing Auto Predictions Manually").pack()
bingSugg = Button(root, text="Scrape Bing Search Auto Predictions", command= bingPredictions)
bingSugg.pack()

googleS_Label = Label(root, text="Get Sentimental Data for Google Predictions").pack()
googleSenti = Button(root, text="Google Sentimental Data", command= sentimentGoogle)
googleSenti.pack()

bingS_Label = Label(root, text="Get Sentimental Data for Bing Predictions").pack()
bingSenti = Button(root, text="Bing Sentimental Data", command= sentimentBing)
bingSenti.pack()

dfLabel = Label(root, text="Download the DataFrame with all the Data as CSV").pack()
dataFrame = Button(root, text="Download DataFrame CSV", command= DownloadCSV)
dataFrame.pack()

#autoLabel = Label(root, text="This will make the data collection run daily in the background").pack()
#auto = Button(root, text="Automate Data Collection", command= RunAutomation)
#auto.pack()


root.mainloop()




