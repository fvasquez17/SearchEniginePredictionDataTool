import pandas as pd
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
import gspread_dataframe as gd
import warnings
warnings.filterwarnings("ignore")

SERVICE_ACCOUNT_FILE = 'key.json'
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scopes= scope)
spreadsheet_key = '1mQ2OfZj_X9D56nfC5f3LmdhMlGqtptZ9_WAJWVbvxK8'
gs=gspread.authorize(creds)
    


def addData(df, sheet_name, range) :
    d2g.upload(df, spreadsheet_key, sheet_name, credentials=creds, row_names=True, start_cell = range)

def appendData(df,sheet_name, range ):
    sheet = gs.open(spreadsheet_key)
    params = {'valueInputOption': 'USER_ENTERED'}
    body = {'values': df.values.tolist()}
    sheet.values_append(f'{sheet_name}!{range}', params, body)

def appendData2(df):
    
    


