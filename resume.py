# -*- coding: utf-8 -*-
import subprocess
import time
import pandas as pd
import os
from pyresparser import ResumeParser      
import numpy as np
import googlesheets
import shutil
import glob
import file_tracker



def Document_to_pdf(FileName):
    ''' converting to pdf 
    when user entered doc and docx'''
    if FileName.endswith('.doc') or FileName.endswith('.docx'): 
        subprocess.call(['soffice', '--headless', '--convert-to', 'pdf', FileName])                     #calling subprocess
        time.sleep(4)
  


def dataframe_for_Directory(Directory_Name):
    pdf_list = file_tracker.pdf_documents()
    list_diff = (list(list(set(pdf_list[0])-set(pdf_list[1])) + list(set(pdf_list[1])-set(pdf_list[0])))) 
    Resume_Dataframe = pd.DataFrame()
    files = os.listdir(Directory_Name)
    for i in files:
        if i.endswith('.pdf') and i in list_diff:
            i = Directory_Name + "/" + i
            Resume_Data = ResumeParser(i).get_extracted_data()                                                   #call to resume_parser file in pyresparser  
            Resume_dataframe = pd.DataFrame.from_dict(Resume_Data ,orient='index')
            Resume_dataframe = Resume_dataframe.transpose()
            Resume_Dataframe = Resume_Dataframe.append(Resume_dataframe, ignore_index=True)                      #appending all resumedataframe into main
            Resume_Dataframe = Resume_Dataframe.replace(np.nan,"")

    print(Resume_Dataframe)
    return Resume_Dataframe


def doc_to_pdf(cli_dir):
    doc_list = file_tracker.doc_documents()
    list_diffs = (list(list(set(doc_list[0])-set(doc_list[1])) + list(set(doc_list[1])-set(doc_list[0])))) 
    files = os.listdir(cli_dir)
    os.chdir(cli_dir)
    for i in files :
        if i.endswith('.doc') or i.endswith('.docx') and i in list_diffs:
            Document_to_pdf(i)


def drive_pull():
    os.chdir('./drive_cli/Resumes')
    # os.system("drive login")
    # os.system("drive add_remote")
    os.system("drive pull")
    os.chdir('../../')


def main(): 
    drive_pull()
    doc_to_pdf('./drive_cli/Resumes')
    os.chdir('../../')
    Resume_Dataframe = dataframe_for_Directory("./drive_cli/Resumes")
    googlesheets.sheets_upload(Resume_Dataframe)

if __name__ == "__main__":
    main()
    

               





    




    



    
  