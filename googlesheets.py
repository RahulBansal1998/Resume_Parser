import pygsheets
import pandas as pd
from pygsheets.datarange import DataRange
import csv

def sheets_upload(Resume_Dataframe,arguments_data):
    ''' 
    Resume_Dataframe : Dataframe to be write
    argument_data : json argument for mapping 
    '''
    client = pygsheets.authorize(service_account_file='client_secret.json')
    sheet = client.open(arguments_data["sheets_title"])
    wks = sheet.worksheet_by_title(arguments_data["sheets"])
    model_cell = wks.cell("A1")
    model_cell.set_text_format('bold', True)
    model_cell.set_text_format('fontSize',10)
    wks.adjust_column_width(start=1, end=4, pixel_size=200)
    wks.adjust_column_width(start=5, pixel_size=450)
    wks.adjust_column_width(start=6, end=16, pixel_size=200)
    wks.adjust_column_width(start=17, end=18, pixel_size=450)
    wks.adjust_column_width(start=19, end=23, pixel_size=200)   
    DataRange('A1','Y1', worksheet=wks).apply_format(model_cell)
    
    with open(arguments_data["sheets_row"]) as f1:
        reader = csv.reader(f1)
        data = list(reader)

    val = [ i for row in data for i in row]
    val = int(val[0])
    try:
        if val == 0:
            wks.set_dataframe(Resume_Dataframe, start=(1,1), copy_index=False, fit=False)
        if val!=0:
            wks.set_dataframe(Resume_Dataframe, start=(val+1,1), copy_index=False,copy_head=False)
            print("succesfully inserted to", arguments_data["sheets_title"] , "Sheets with sheet reference", arguments_data["sheets"])
        val= val + Resume_Dataframe.shape[0]
        val = str(val)
        with open(arguments_data["sheets_row"], 'w') as f:
            f.write(val)
    except:
        print("please insert new files to The Folder")





