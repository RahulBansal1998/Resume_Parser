# -*- coding: utf-8 -*-
import subprocess
import time
import pandas as pd
import os
from pyresparser import ResumeParser      
import numpy as np
import googlesheets



def Document_to_pdf(FileName):
    ''' converting to pdf 
    when user entered doc and docx'''
    if FileName.endswith('.doc') or FileName.endswith('.docx'): 
        subprocess.call(['soffice', '--headless', '--convert-to', 'pdf','--outdir', 'PDF', FileName])       #calling subprocess
        time.sleep(4)
        FileName = FileName.split('/')[-1]
        FileName = FileName.split('.')[-2]
        FileName = "PDF/" + FileName + ".pdf"  
        return FileName
    if FileName.endswith('.pdf'):
        return FileName
    else:
        raise Exception("Enter only pdf doc and docx format resumes only")


def dataframe_for_Directory(Directory_Name):
    Resume_Dataframe = pd.DataFrame()
    files = os.listdir(Directory_Name)
    for i in files:
        i = Directory_Name + "/" + i
        FileName = Document_to_pdf(i)
        Resume_Data = ResumeParser(FileName).get_extracted_data()                                            #call to resume_parser file in pyresparser  
        Resume_dataframe = pd.DataFrame.from_dict(Resume_Data ,orient='index',)
        Resume_dataframe = Resume_dataframe.transpose()
        Resume_Dataframe = Resume_Dataframe.append(Resume_dataframe, ignore_index=True)                      #appending all resumedataframe into main
        Resume_Dataframe = Resume_Dataframe.replace(np.nan,"")
    return Resume_Dataframe


def main():                                                 #main function to write to google sheets
    os.chdir('./drive_cli/Resumes')
    # boolean = True  
    # if boolean:
    #     os.system("drive login")
    #     os.system("drive add_remote")
    #     boolean = False

    os.system("drive pull")
    os.chdir('../..')
    Resume_Dataframe = dataframe_for_Directory("drive_cli/Resumes")
    googlesheets.sheets_upload(Resume_Dataframe)

if __name__ == "__main__":
    main()
    

               





    




    



    
  