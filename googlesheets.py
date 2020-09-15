import pygsheets
import pandas as pd
from pygsheets.datarange import DataRange
import csv


def sheets_upload(Resume_Dataframe):
    client = pygsheets.authorize(service_account_file='client_secret.json')
    sheet = client.open('MYDOC')
    wks = sheet.worksheet_by_title('Sheet23')
    model_cell = wks.cell("A1")
    model_cell.set_text_format('bold', True)
    model_cell.set_text_format('fontSize',10)
    wks.adjust_column_width(start=1, end=4, pixel_size=200)
    wks.adjust_column_width(start=5, pixel_size=450)
    wks.adjust_column_width(start=6, end=16, pixel_size=200)
    wks.adjust_column_width(start=17, end=18, pixel_size=450)
    wks.adjust_column_width(start=19, end=23, pixel_size=200)   
    DataRange('A1','Y1', worksheet=wks).apply_format(model_cell)

    # wks.set_dataframe(Resume_Dataframe, start=(1,1), copy_index=False, fit=False)

    # col_list = ['val']
    # value = pd.read_csv('val.csv',usecols=col_list)
    # val = value['val']
    # val = val.astype(int)
    # print(type(val))
    with open('val.csv') as f1:
        reader = csv.reader(f1)
        data = list(reader)
    
    val = [ i for row in data for i in row]

    val = int(val[0])
    print(val)
    if val == 0:
        wks.set_dataframe(Resume_Dataframe, start=(1,1), copy_index=False, fit=False)
    if val!=0:
        wks.set_dataframe(Resume_Dataframe, start=(val+1,1), copy_index=False,copy_head=False)
    val= val + Resume_Dataframe.shape[0]
    print (val)
    val = str(val)
    with open('val.csv', 'w') as f:
        f.write(val)




