# -*- coding: utf-8 -*-
import argparse
import subprocess
import time
import pandas as pd
import pandas as pd
import os
from pyresparser import ResumeParser                              #call to resume_parser file from pyresparser folder


#Argument Parser
def Argument_Parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath',help='path to resume file')                                  #Taking arguments
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

if FileName:                                                     #If User Enters file
    def Document_to_pdf(FileName):                               #doc and docx converter to pdf
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
        Resume_Data['skills'] = Resume_Data['Top skills']
        del Resume_Data['skills']
        Resume_Dataframe = pd.DataFrame.from_dict(Resume_Data ,orient='index')       #DataFrame from Dict
        Resume_Dataframe = Resume_Dataframe.transpose()                              #Transpose
    except:
        print("Enter Correct Path")


if Directory_Name:                                                                   #If User Enters Directory
    Resume_Dataframe = pd.DataFrame()
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
        a =1
        if(a==1):
            Resume_Data = ResumeParser(FileName).get_extracted_data()                                            #call to resume_parser file in pyresparser   
            Resume_Data['Top skills'] = Resume_Data['skills']
            del Resume_Data['skills']                                                                             #Renaming Skill to top_skill
            Resume_dataframe = pd.DataFrame.from_dict(Resume_Data ,orient='index')
            Resume_dataframe = Resume_dataframe.transpose()
            Resume_Dataframe = Resume_Dataframe.append(Resume_dataframe, ignore_index=True)                        #appending all resumedataframe into main
        else:
            print("Enter Correct Directory")

def main():                                                                                     #main function to write to excel
    writer = pd.ExcelWriter(Excel_Filename, engine='xlsxwriter')                                #write to excel
    Resume_Dataframe.to_excel(writer, sheet_name='Sheet1')
    writer.save()

if __name__ == "__main__":
    main()
    

               





    




    



    
  