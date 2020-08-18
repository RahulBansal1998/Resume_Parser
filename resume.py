# -*- coding: utf-8 -*-
import argparse
import subprocess
import time
import pandas as pd
import os
import xlsxwriter
from pyresparser import ResumeParser      #call to resume_parser file from pyresparser folder


#Argument Parser
def Argument_Parser():
    '''Taking arguments from user '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath',help='path to resume file')         #Taking arguments
    parser.add_argument('--directory',help="directory containing all the resumes to be extracted") #Taking arguments
    parser.add_argument('--excel',required=True,help='Excel Filename')   #Taking arguments
    args = parser.parse_args()
    FileName = args.filepath
    Excel_Filename = args.excel 
    Directory_Name = args.directory
    Argument_list = [FileName,Excel_Filename,Directory_Name]
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
    return Resume_Dataframe


def dataframe_for_Directory(Directory_Name):
    Resume_Dataframe = pd.DataFrame()
    files = os.listdir(Directory_Name)
    for i in files:
        i = Directory_Name + "/" + i
        FileName = Document_to_pdf(i)
        Resume_Data = ResumeParser(FileName).get_extracted_data()                                            #call to resume_parser file in pyresparser  
        Resume_dataframe = pd.DataFrame.from_dict(Resume_Data ,orient='index')
        Resume_dataframe = Resume_dataframe.transpose()
        Resume_Dataframe = Resume_Dataframe.append(Resume_dataframe, ignore_index=True)                      #appending all resumedataframe into main
    return Resume_Dataframe

def main():                                                 #main function to write to excel
    argument_list = Argument_Parser()                       #Argument_List
    FileName = argument_list[0]                             #FileName_Argument
    Excel_Filename = argument_list[1]                       #Excel_Argument
    Directory_Name = argument_list[2]                       #Directory_Argument      
    if FileName:
        FileName = Document_to_pdf(FileName)
        Resume_Dataframe = dataframe_for_filepath(FileName)
    if Directory_Name:
        Resume_Dataframe = dataframe_for_Directory(Directory_Name)

    writer = pd.ExcelWriter(Excel_Filename, engine='xlsxwriter')                        #write to excel    
    Resume_Dataframe.to_excel(writer, sheet_name='Sheet1',index=False)
    workbook_object = writer.book
    worksheet_object  = writer.sheets['Sheet1'] 
    format_object1 = workbook_object.add_format({'text_wrap': True,'valign': 'top'})    #added Text Wrap
    worksheet_object.set_column('A:L', 20,format_object1)                               #setting column width
    worksheet_object.set_column('M:U', 33,format_object1)                               #setting column width
    worksheet_object.set_column('V:W', 22,format_object1)
    writer.save()

if __name__ == "__main__":
    main()
    

               





    




    



    
  