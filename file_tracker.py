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

def pdf_documents(arguments):
    ''' tracking pdf documents by using pdf_file.csv'''
    files=pd.read_csv(arguments["file_tracker"][0])
    list_of_files=os.listdir(arguments["Directory"])
    document_list = []
    for i in list_of_files:
        if i.endswith('.pdf'):
            document_list.append(i)


    if len(files.files)!=len(document_list):                                                    #save again the curent list of files 
        pd.DataFrame({'files':document_list}).to_csv(arguments["file_tracker"][0])

    document_init_list = files.files.values.tolist()
    document_lists = [document_list,document_init_list]
    return document_lists

def doc_documents(arguments):
    ''' tracking doc_documents by using doc_file.csv'''
    doc_files=pd.read_csv(arguments["file_tracker"][1])
    list_of_files=os.listdir(arguments["Directory"])
    documents_list = []
    for i in list_of_files:
        if i.endswith('.doc') or i.endswith('.docx'):
            documents_list.append(i)


    if len(doc_files.files)!=len(documents_list):                                   #save again the curent list of files 
        pd.DataFrame({'files':documents_list}).to_csv(arguments["file_tracker"][1])

    documents_init_list = doc_files.files.values.tolist()
    documents_lists = [documents_list,documents_init_list]
    return documents_lists