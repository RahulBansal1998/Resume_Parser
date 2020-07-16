# -*- coding: utf-8 -*-
from pyresparser import ResumeParser
import argparse
import subprocess
import time
import pandas as pd
import pandas as pd
import os

#Argument Parser
def Argument_Parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath',help='path to resume file')
    parser.add_argument('--directory',help="directory containing all the resumes to be extracted")
    parser.add_argument('--excel',required=True,help='Excel Filename')
    args = parser.parse_args()
    FileName = args.filepath
    Excel_Filename = args.excel 
    Directory_Name = args.directory
    Argument_list = [FileName,Excel_Filename,Directory_Name]
    return Argument_list


argument_list = Argument_Parser()                                #Argument_List
FileName = argument_list[0]                                      #FileName_Argument
Excel_Filename = argument_list[1]                                #Excel_Argument
Directory_Name = argument_list[2]                                #Directory_Argument

if FileName:                                                    #If User Enters file
    def Document_to_pdf(FileName):                              #doc and docx converter to pdf
        if FileName.endswith('.doc') or FileName.endswith('.docx'):
            subprocess.call(['soffice', '--headless', '--convert-to', 'pdf', FileName])
            time.sleep(4)
            FileName = FileName.split('/')[-1]
            FileName = FileName.split('.')[-2]
            FileName = FileName + ".pdf"  
        return FileName

    FileName = Document_to_pdf(FileName)  

    try:
        Resume_Data = ResumeParser(FileName).get_extracted_data()
        for key in Resume_Data:
            if (key=="skills"):
                key.replace("skills","Top Skills")
        Resume_Dataframe = pd.DataFrame.from_dict(Resume_Data ,orient='index')       #DataFrame from Dict
        Resume_Dataframe = Resume_Dataframe.transpose()                              #Transpose
        writer = pd.ExcelWriter(Excel_Filename, engine='xlsxwriter')
        Resume_Dataframe.to_excel(writer, sheet_name='Sheet1')
        writer.save()
    except:
        print("Enter Correct Path")


if Directory_Name:                                                              #If User Enters Directory
    Resumes_Dataframe = pd.DataFrame()
    files = os.listdir(Directory_Name)
    for i in files:
        i = Directory_Name + "/" + i
        def Document_to_pdf(FileName):
            if FileName.endswith('.doc') or FileName.endswith('.docx'):
                subprocess.call(['soffice', '--headless', '--convert-to', 'pdf', FileName])
                time.sleep(5)
                FileName = FileName.split('/')[-1]
                FileName = FileName.split('.')[-2]
                FileName = FileName + ".pdf"  
            return FileName

        FileName = Document_to_pdf(i)

        try:
            Resume_Data = ResumeParser(FileName).get_extracted_data()
            for key in Resume_Data:
                if (key=="skills"):
                    key.replace("skills","Top Skills")
            Resume_Dataframe = pd.DataFrame.from_dict(Resume_Data ,orient='index')
            Resume_Dataframe = Resume_Dataframe.transpose()
            Resumes_Dataframe = Resumes_Dataframe.append(Resume_Dataframe)                     #appending all resumedataframe into main
        except:
            print("Enter Correct Directory")
    writer = pd.ExcelWriter(Excel_Filename, engine='xlsxwriter')                                #write to excel
    Resumes_Dataframe.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    

               





    




    



    
  