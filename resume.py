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
    return Argument_list     #returning argument list


argument_list = Argument_Parser()              #Argument_List
FileName = argument_list[0]                    #FileName_Argument
Excel_Filename = argument_list[1]              #Excel_Argument
Directory_Name = argument_list[2]              #Directory_Argument

if FileName:     #If User Enters file
    def Document_to_pdf(FileName):
        ''' converting to pdf when user entered doc and docx'''
        if FileName.endswith('.doc') or FileName.endswith('.docx'): 
            subprocess.call(['soffice', '--headless', '--convert-to', 'pdf','--outdir', 'PDF', FileName]) #calling subprocess
            time.sleep(3)
            FileName = FileName.split('/')[-1]
            FileName = FileName.split('.')[-2]
            FileName = "PDF/" + FileName + ".pdf"  
        return FileName

    FileName = Document_to_pdf(FileName)  
 
    try:
        '''creating dataframe  and calling get_extrcated_data() function from resume_parser.py file inside in pyresparser folder '''
        Resume_Data = ResumeParser(FileName).get_extracted_data()            
        Resume_Dataframe = pd.DataFrame.from_dict(Resume_Data ,orient='index')                #DataFrame from Dict
        Resume_Dataframe = Resume_Dataframe.transpose()                                       #Transpose of dataframe
    except:
        print("Enter Correct Path")


if Directory_Name:            #If User Enters Directory in command line 
    Resume_Dataframe = pd.DataFrame()
    files = os.listdir(Directory_Name)
    for i in files:
        i = Directory_Name + "/" + i
        def Document_to_pdf(FileName):
            if FileName.endswith('.doc') or FileName.endswith('.docx'):
                subprocess.call(['soffice', '--headless', '--convert-to', 'pdf','--outdir', 'PDF', FileName])
                time.sleep(5)
                FileName = FileName.split('/')[-1]
                FileName = FileName.split('.')[-2]
                FileName = "PDF/" + FileName + ".pdf"  
            return FileName 
        FileName = Document_to_pdf(i)

        # print(FileName)
        try:
            Resume_Data = ResumeParser(FileName).get_extracted_data()                                            #call to resume_parser file in pyresparser  
                                                                            #Renaming Skill to top_skill
            Resume_dataframe = pd.DataFrame.from_dict(Resume_Data ,orient='index')
            Resume_dataframe = Resume_dataframe.transpose()
            Resume_Dataframe = Resume_Dataframe.append(Resume_dataframe, ignore_index=True)                      #appending all resumedataframe into main
    
        except:
            print("Enter Correct Directory")

def main():             #main function to write to excel
    '''writing to excel '''
    writer = pd.ExcelWriter(Excel_Filename, engine='xlsxwriter')    #write to excel    
    Resume_Dataframe.to_excel(writer, sheet_name='Sheet1')
    workbook_object = writer.book
    worksheet_object  = writer.sheets['Sheet1'] 
    format_object1 = workbook_object.add_format({'text_wrap': True,'valign': 'top'})  #added Text Wrap
    worksheet_object.set_column('B:D', 25)           #setting column width
    worksheet_object.set_column('E:E', 33),format_object1           #setting column width
    worksheet_object.set_column('F:L', 33,format_object1)
    writer.save()

if __name__ == "__main__":
    main()
    

               





    




    



    
  