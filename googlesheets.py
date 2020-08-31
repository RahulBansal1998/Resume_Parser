import pygsheets
from pygsheets.datarange import DataRange


def sheets_upload(Resume_Dataframe):
    client = pygsheets.authorize(service_account_file='client_secret.json')
    sheet = client.open('MYDOC')
    wks = sheet.worksheet_by_title('Sheet3')
    model_cell = wks.cell("A1")
    model_cell.set_text_format('bold', True)
    model_cell.set_text_format('fontSize',10)
    wks.adjust_column_width(start=1, end=16, pixel_size=200)
    wks.adjust_column_width(start=17, end=18, pixel_size=450)
    wks.adjust_column_width(start=19, end=23, pixel_size=200)   
    DataRange('A1','Y1', worksheet=wks).apply_format(model_cell)
    # dataframe_two = wks.get_as_df()
    # roww = dataframe_two.shape[0]
    # print(roww)
    wks.set_dataframe(Resume_Dataframe, start=(1,1),extend = True)


