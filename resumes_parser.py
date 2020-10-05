# -*- coding: utf-8 -*-
import subprocess
import time
import pandas as pd
import os
from pyresparser import ResumeParser      
import numpy as np
import googlesheets
import glob
import file_tracker


def Document_to_pdf(FileName):
    '''
    :param : filename to be converted to pdf 
     converting to pdf when user entered doc and docx 
    '''
    if FileName.endswith('.doc') or FileName.endswith('.docx'): 
        subprocess.call(['soffice', '--headless', '--convert-to', 'pdf', FileName])                     #calling subprocess
        time.sleep(4)
  
def dataframe_for_Directory(arguments_data):
    '''
    :param:json parameter
     creating dataframe for writing to the google sheet 
    '''
    Directory_Name = arguments_data["Directory"]
    pdf_list = file_tracker.pdf_documents(arguments_data)
    list_diff = (list(list(set(pdf_list[0])-set(pdf_list[1])) + list(set(pdf_list[1])-set(pdf_list[0])))) #calculating list diff 
    Resume_Dataframe = pd.DataFrame()
    files = os.listdir(Directory_Name)
    for i in sorted(files):
        if i.endswith('.pdf') and i in list_diff:
            i = Directory_Name + "/" + i
            Resume_Data = ResumeParser(i,arguments_data).get_extracted_data()                                                   #call to resume_parser file in pyresparser  
            Resume_dataframe = pd.DataFrame.from_dict(Resume_Data ,orient='index')
            Resume_dataframe = Resume_dataframe.transpose()
            Resume_Dataframe = Resume_Dataframe.append(Resume_dataframe, ignore_index=True)                      #appending all resumedataframe into main
            Resume_Dataframe = Resume_Dataframe.replace(np.nan,"")
    

    return Resume_Dataframe


def doc_to_pdf(arguments_data):
    cli_dir = arguments_data["Directory"]
    doc_list = file_tracker.doc_documents(arguments_data)
    list_diffs = (list(list(set(doc_list[0])-set(doc_list[1])) + list(set(doc_list[1])-set(doc_list[0])))) 
    files = os.listdir(cli_dir)
    os.chdir(cli_dir)
    print(list_diffs)
    for i in files :
        if i.endswith('.doc') or i.endswith('.docx'):
            if i in list_diffs:
                Document_to_pdf(i)


def main(arguments_data): 
    '''
     main function getting arguments
     from gem_resume_parser.py file 
    '''
    doc_to_pdf(arguments_data)
    os.chdir(arguments_data["root"])
    Resume_Dataframe = dataframe_for_Directory(arguments_data)
    Resume_Dataframe.to_csv('Resume_Dataframes.csv')
    googlesheets.sheets_upload(Resume_Dataframe,arguments_data)    # calling google sheet


    

               





    




    



    
  