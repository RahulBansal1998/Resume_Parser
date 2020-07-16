# -*- coding: utf-8 -*-
from pyresparser import ResumeParser
import argparse
import subprocess
import pdfplumber
import docx2txt
import nltk
import time
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize 
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer 
import heapq
import pandas as pd
import os

#Argument and doc and docx converter
def Argument_Parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath',help='path to resume file')
    parser.add_argument('--directory',help="directory containing all the resumes to be extracted")
    parser.add_argument('--excel',required=True,help='Excel Filename')
    args = parser.parse_args()
    filename = args.filepath
    Excel_Filename = args.excel 
    Directory_Name = args.directory
    Argument_list = [filename,Excel_Filename,Directory_Name]
    return Argument_list


argument_list = Argument_Parser()
filename = argument_list[0]
Excel_Filename = argument_list[1]
Directory_Name = argument_list[2]

if filename:
    #Convert to pdf
    def document_to_pdf(filename):
        if filename.endswith('.doc') or filename.endswith('.docx'):
            output_dir = os.getcwd()
            print(output_dir)
            output_dir = output_dir + "/Resume_Pdf"
            print(output_dir)
            subprocess.call(['soffice', '--headless', '--convert-to', 'pdf', filename])
            time.sleep(3)
            filename = filename.split('/')[-1]
            filename = filename.split('.')[-2]
            filename = filename + ".pdf"  
        return filename

    filename = document_to_pdf(filename)  

    # Text Extractor from pdf
    def Text_Extractor(filename):
        text = ""
        if filename.endswith('.pdf'):
            with pdfplumber.open(filename) as pdf:
                Total_pages = pdf.pages
                Total_pages = len(Total_pages)
                pdf_text = []
                for i in range(Total_pages):
                    page = pdf.pages[i]
                    pdf_text.append(page.extract_text())
                    listToStr = ' '.join([str(elem) for elem in pdf_text])
                    text = listToStr       
        return text    

    Parsed_text = Text_Extractor(filename)

    # cleaned Text 
    def Extracted_Text(Parsed_text):
        punctuations = '''!()-[]–;:'"\,<>./?+@#$%^&*_~0123456789'''
        for x in Parsed_text.lower(): 
            if x in punctuations: 
                Parsed_text = Parsed_text.replace(x, "")
        stopwords = nltk.corpus.stopwords.words('english')
        word_tokens = word_tokenize(Parsed_text)         
        Parsed_sentence = []         
        for w in word_tokens: 
            if w not in stopwords: 
                Parsed_sentence.append(w)
        return Parsed_sentence

    Cleaned_Text = Extracted_Text(Parsed_text)

    def Sentenced_extractor(parsed_text):
        Sentence_text = nltk.sent_tokenize(parsed_text) 
        return Sentence_text

    Sentenced_Extractor = Sentenced_extractor(Parsed_text)

    # Sentiment Analyzer 
    def SentimentAnalyzer(Sen_text):
        Analyser = SentimentIntensityAnalyzer()
        df = pd.DataFrame([Analyser.polarity_scores(item) for item in Sen_text])
        Sentenced_Extractor_Mean = df.mean(axis = 0)
        return Sentenced_Extractor_Mean

    SentimentAnalyzerMean = SentimentAnalyzer(Sentenced_Extractor).to_dict()

    # rounding to 4 digit
    def Round_Values_OfDict(SentimentAnalyzerMean):
        for k,v in SentimentAnalyzerMean.items():
            SentimentAnalyzerMean[k] = round(v,4)
        return SentimentAnalyzerMean

    SentimentAnalyzerMean = Round_Values_OfDict(SentimentAnalyzerMean)
    SentimentAnalyzerMean = sorted(SentimentAnalyzerMean.items(), key = lambda d:(d[1], d[0]),reverse=True)
    sentiment = {"SentimentAnalyzer" : str(SentimentAnalyzerMean) }

    #Skill Term Frequency

    def skill_term_frequency():
        Resume_data = ResumeParser(filename).get_extracted_data() 
        Dict = Resume_data['skills']
        Parsed_sentence = Extracted_Text(Parsed_text)
        for k,v in Dict.items():
            Dict[k] = Dict[k]/len(Parsed_sentence)
        Dict = Round_Values_OfDict(Dict)
        Dict = sorted(Dict.items(), key = lambda d:(d[1], d[0]),reverse=True)

        Dict = {"Skill Term Frequemcy":str(Dict)}
        return Dict

    Skills = skill_term_frequency() 


    try:
        Resume_Data = ResumeParser(filename).get_extracted_data()
        keys_to_remove = ["skills"]      #removing skills
        for key in keys_to_remove:
            del Resume_Data[key]

        #write to excel
        a = pd.DataFrame.from_dict(Resume_Data ,orient='index')
        b = pd.DataFrame.from_dict(sentiment ,orient='index')
        c = pd.DataFrame.from_dict(Skills ,orient='index')
        # d = pd.DataFrame.from_dict(Experience_Keywords ,orient='index')

        e = a.append(b)
        g = e.append(c)
        g = g.transpose()
        writer = pd.ExcelWriter(Excel_Filename, engine='xlsxwriter')
        g.to_excel(writer, sheet_name='Sheet1')
        writer.save()
    except:
        print("Enter Correct Path")

#directory

if Directory_Name:
    df = pd.DataFrame()
    files = os.listdir(Directory_Name)
    for i in files:
        i = Directory_Name + "/" + i
        def document_to_pdf(filename):
            if filename.endswith('.doc') or filename.endswith('.docx'):
                subprocess.call(['soffice', '--headless', '--convert-to', 'pdf', filename])
                time.sleep(5)
                filename = filename.split('/')[-1]
                filename = filename.split('.')[-2]
                filename = filename + ".pdf"  
            return filename

        filename = document_to_pdf(i)


        #Text Extractor from pdf
        def Text_Extractor(filename):
            text = ""
            if filename.endswith('.pdf'):
                with pdfplumber.open(filename) as pdf:
                    Total_pages = pdf.pages
                    Total_pages = len(Total_pages)
                    pdf_text = []
                    for i in range(Total_pages):
                        page = pdf.pages[i]
                        pdf_text.append(page.extract_text())
                        listToStr = ' '.join([str(elem) for elem in pdf_text])
                        text = listToStr       
            return text    

        Parsed_text = Text_Extractor(filename)

        # cleaned Text 
        def Extracted_Text(Parsed_text):
            punctuations = '''!()-[]–;:'"\,<>./?+@#$%^&*_~0123456789'''
            for x in Parsed_text.lower(): 
                if x in punctuations: 
                    Parsed_text = Parsed_text.replace(x, "")
            stopwords = nltk.corpus.stopwords.words('english')
            word_tokens = word_tokenize(Parsed_text)         
            Parsed_sentence = []         
            for w in word_tokens: 
                if w not in stopwords: 
                    Parsed_sentence.append(w)
            return Parsed_sentence

        Cleaned_Text = Extracted_Text(Parsed_text)

        def Sentenced_extractor(parsed_text):
            Sentence_text = nltk.sent_tokenize(parsed_text) 
            return Sentence_text

        Sentenced_Extractor = Sentenced_extractor(Parsed_text)

        # Sentiment Analyzer 
        def SentimentAnalyzer(Sen_text):
            Analyser = SentimentIntensityAnalyzer()
            df = pd.DataFrame([Analyser.polarity_scores(item) for item in Sen_text])
            Sentenced_Extractor_Mean = df.mean(axis = 0)
            return Sentenced_Extractor_Mean

        SentimentAnalyzerMean = SentimentAnalyzer(Sentenced_Extractor).to_dict()
        # rounding to 4 digit
        def Round_Values_OfDict(SentimentAnalyzerMean):
            for k,v in SentimentAnalyzerMean.items():
                SentimentAnalyzerMean[k] = round(v,4)
            return SentimentAnalyzerMean

        SentimentAnalyzerMean = Round_Values_OfDict(SentimentAnalyzerMean)
        SentimentAnalyzerMean = sorted(SentimentAnalyzerMean.items(), key = lambda d:(d[1], d[0]),reverse=True)
        sentiment = {"SentimentAnalyzer" : str(SentimentAnalyzerMean) }

        #Skill Term Frequency
        def skill_term_frequency():
            Resume_data = ResumeParser(filename).get_extracted_data() 
            Dict = Resume_data['skills']
            Parsed_sentence = Extracted_Text(Parsed_text)
            for k,v in Dict.items():
                Dict[k] = Dict[k]/len(Parsed_sentence)
            Dict = Round_Values_OfDict(Dict)
            Dict = sorted(Dict.items(), key = lambda d:(d[1], d[0]),reverse=True)

            Dict = {"Skill Term Frequemcy":str(Dict)}
            return Dict

        Skills = skill_term_frequency() 

        try:
            Resume_Data = ResumeParser(filename).get_extracted_data()
            keys_to_remove = ["skills"]      #removing skills
            for key in keys_to_remove:
                del Resume_Data[key]

            #write to excel
            a = pd.DataFrame.from_dict(Resume_Data ,orient='index')
            b = pd.DataFrame.from_dict(sentiment ,orient='index')
            c = pd.DataFrame.from_dict(Skills ,orient='index')
            e = a.append(b)
            g = e.append(c)
            g = g.transpose()
            df = df.append(g)
        except:
            print("Enter Correct Directory")
    writer = pd.ExcelWriter(Excel_Filename, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    

               





    




    



    
  