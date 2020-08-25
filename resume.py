# -*- coding: utf-8 -*-
import argparse
import subprocess
import time
import pandas as pd
import os
import xlsxwriter
from pyresparser import ResumeParser      #call to resume_parser file from pyresparser folder
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
import numpy as np




#Argument Parser
def Argument_Parser():
    '''Taking arguments from user '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath',help='path to resume file')         #Taking arguments
    parser.add_argument('--directory',help="directory containing all the resumes to be extracted") #Taking arguments
    args = parser.parse_args()
    FileName = args.filepath
    Directory_Name = args.directory
    Argument_list = [FileName,Directory_Name]
    return Argument_list                                                 #returning argument list

def Document_to_pdf(FileName):
    ''' converting to pdf 
    when user entered doc and docx'''
    if FileName.endswith('.doc') or FileName.endswith('.docx'): 
        subprocess.call(['soffice', '--headless', '--convert-to', 'pdf','--outdir', 'PDF', FileName])       #calling subprocess
        time.sleep(5)
        FileName = FileName.split('/')[-1]
        FileName = FileName.split('.')[-2]
        FileName = "PDF/" + FileName + ".pdf"  
        return FileName
    if FileName.endswith('.pdf'):
        return FileName
    else:
        raise Exception("Enter only pdf doc and docx format resumes only")



def dataframe_for_filepath(FileName):
    '''creating dataframe  and calling 
    get_extrcated_data() function from 
    resume_parser.py file inside in pyresparser folder '''
    Resume_Data = ResumeParser(FileName).get_extracted_data()            
    Resume_Dataframe = pd.DataFrame.from_dict(Resume_Data ,orient='index')                #DataFrame from Dict
    Resume_Dataframe = Resume_Dataframe.transpose()                                       #Transpose of dataframe
    Resume_Dataframe = Resume_Dataframe.replace(np.nan,"")
    return Resume_Dataframe


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


def main():                                                 #main function to write to excel

    argument_list = Argument_Parser()                       #Argument_List
    FileName = argument_list[0]                             #FileName_Argument
    Directory_Name = argument_list[1]                       #Directory_Argument      
    if FileName:
        FileName = Document_to_pdf(FileName)
        Resume_Dataframe = dataframe_for_filepath(FileName)
    if Directory_Name:
        Resume_Dataframe = dataframe_for_Directory(Directory_Name)

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("resume_data").sheet1
    spreadsheet_key = '1Gvsv0KbLZn_d6TcZfJio6OcjZ3un3uLdExGzt9W5hkI'
    wks_name = 'Resumee_Dataaaaa'
    d2g.upload(Resume_Dataframe, spreadsheet_key, wks_name, credentials=creds, row_names=True)



if __name__ == "__main__":
    main()
    

               





    




    



    
  