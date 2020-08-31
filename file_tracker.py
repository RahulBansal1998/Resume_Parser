import os
import pandas as pd
# list_of_files=os.listdir('./drive_cli/Resumes')
# document_list = []
# for i in list_of_files:
#     if i.endswith('.pdf'):
#         document_list.append(i)

# pd.DataFrame({'files':document_list}).to_csv('pdf_file.csv')

# list_of_files=os.listdir('./drive_cli/Resumes')
# documents_list = []
# for i in list_of_files:
#     if i.endswith('.doc') or i.endswith('.docx'):
#         documents_list.append(i)

# pd.DataFrame({'files':documents_list}).to_csv('doc_file.csv')

def pdf_documents():
    files=pd.read_csv('pdf_file.csv')
    list_of_files=os.listdir('./drive_cli/Resumes')
    document_list = []
    for i in list_of_files:
        if i.endswith('.pdf'):
            document_list.append(i)


    if len(files.files)!=len(document_list):
            #save again the curent list of files 
        pd.DataFrame({'files':document_list}).to_csv('pdf_file.csv')

    document_init_list = files.files.values.tolist()
    document_lists = [document_list,document_init_list]
    return document_lists

def doc_documents():
    doc_files=pd.read_csv('doc_file.csv')
    list_of_files=os.listdir('./drive_cli/Resumes')
    documents_list = []
    for i in list_of_files:
        if i.endswith('.pdf'):
            documents_list.append(i)


    if len(doc_files.files)!=len(documents_list):
            #save again the curent list of files 
        pd.DataFrame({'files':documents_list}).to_csv('doc_file.csv')

    documents_init_list = doc_files.files.values.tolist()
    documents_lists = [documents_list,documents_init_list]
    return documents_lists