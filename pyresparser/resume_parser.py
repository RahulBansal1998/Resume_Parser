
import os
import multiprocessing as mp
import io
import spacy
import pprint
from spacy.matcher import Matcher
from . import utils


class ResumeParser(object):
    ''' Main class to define all entity global variable resume.py is calling this class  '''             

    def __init__(
        self,
        resume,
        skills_file=None,
        custom_regex=None
    ):
        nlp = spacy.load('en_core_web_sm')
        custom_nlp = spacy.load(os.path.dirname(os.path.abspath(__file__)))
        self.__skills_file = skills_file
        self.__custom_regex = custom_regex
        self.__matcher = Matcher(nlp.vocab)
        self.__details = {       
            #entities 
            'name': None,
            'Email': None,
            'mobile_number': None,
            'skills': None,
            'Institute_name': None,
            'degree': None,
            'Current Location':None,
            'total_experience': None,
            'Remarks':None,
            


            
        }
        self.__resume = resume
        if not isinstance(self.__resume, io.BytesIO):
            ext = os.path.splitext(self.__resume)[1].split('.')[1]
        else:
            ext = self.__resume.name.split('.')[1]
        self.__text_raw = utils.extract_text(self.__resume, '.' + ext)  #raw text extracting from utils.py file by calling utils
        self.__text = ' '.join(self.__text_raw.split())
        self.__nlp = nlp(self.__text)
        self.__custom_nlp = custom_nlp(self.__text_raw)
        self.__noun_chunks = list(self.__nlp.noun_chunks)
        self.__get_basic_details()

    def get_extracted_data(self):   #function calling from resume.py file
        return self.__details
    
    def get_extracted_text(self):
        ext1 = self.__resume.name.split('.')[1]
        text_raw = utils.extract_text(self.__resume, '.' + ext1)
        return text_raw


    def __get_basic_details(self):
        '''function to collect all basic details'''
        cust_ent = utils.extract_entities_wih_custom_model(
                            self.__custom_nlp
                        )
        name = utils.extract_name(self.__nlp, matcher=self.__matcher)
        email = utils.extract_email(self.__text)
        mobile = utils.extract_mobile_number(self.__text, self.__custom_regex)
        experiences = utils.extracts_experience(self.__text)
        Degree = utils.extract_degree(self.__nlp,self.__noun_chunks)
        skills = utils.extract_skills(
                    self.__nlp,
                    self.__noun_chunks,
                    self.__skills_file
                )
        college = utils.extract_college(
                    self.__nlp,
                    self.__noun_chunks
                )
        
        Location = utils.extract_location(
                    self.__nlp,
                    self.__noun_chunks
                )

        entities = utils.extract_entity_sections_grad(self.__text_raw)

        # extract name
        try:
            self.__details['name'] = cust_ent['Name']
        except (IndexError, KeyError):
            self.__details['name'] = name

        # extract Email
        self.__details['Email'] = email

        # extract mobile number
        self.__details['mobile_number'] = mobile

        # extract skills
        self.__details['skills'] = skills

        #extract_colllege_name
        try:
            self.__details['Institute_name'] = cust_ent['College Name']
        except (IndexError, KeyError):
            self.__details['Institute_name'] = college

        #extract location
        try:
            self.__details['Current Location'] = Location
        except (IndexError, KeyError):
            location = cust_ent['Location']
            if location:
                location = location.split(",")[0]
            self.__details['Current Location'] = location
        

     

        # extract education Degree
        try:
            self.__details['degree'] = cust_ent['Degree']
        except KeyError:
            self.__details['degree'] = Degree
        #extract Total Experience
        try:
            self.__details['total_experience'] = cust_ent['years of experience']                  
        except KeyError:
            self.__details['total_experience'] = experiences
            # pass
            # exp = round(utils.get_total_experience(entities['experience']) / 12,2)
            # self.__details['total_experience'] = exp


 
        return


def resume_result_wrapper(resume):
    parser = ResumeParser(resume)
    return parser.get_extracted_data()


if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())

    resumes = []
    data = []
    for root, directories, filenames in os.walk('resumes/'):
        for filename in filenames:
            file = os.path.join(root, filename)
            resumes.append(file)

    results = [
        pool.apply_async(
            resume_result_wrapper,
            args=(x,)
        ) for x in resumes
    ]

    results = [p.get() for p in results]
    pprint.pprint(results)
