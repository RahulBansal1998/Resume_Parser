import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g


def sheets_upload(Resume_Dataframe):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("MYDOC").sheet1
    spreadsheet_key = '1ngPWdIS4r0ZV5MeqJu3ISpVfEPFX9CJTEvlGFvXpTCY'
    wks_name = 'Test'
    d2g.upload(Resume_Dataframe, spreadsheet_key, wks_name, credentials=creds, row_names=True)