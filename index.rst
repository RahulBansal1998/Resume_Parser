.. Resume Parser documentation master file, created by
   sphinx-quickstart on Mon Aug 10 16:50:51 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Resume Parser's documentation!
=========================================


1.Resume.py - it is the main file which runs our Program argument is passing to this file here we are also importing Resume_parser.py file which are returning all the information as a Dictionary  also all the function are in this file such as:
	-Argument_Parser : Taking Argument and converting doc,docx to pdf

2.Resume_Parser.py - this file consists of all the functions calls to utils.py that helps us to extract information from Resumes.

3.Utils.py - Main file where all the regex and all the logic are written to extract information form Resumes from regex to using spacy pretrained model to extract name


.. toctree::
   :maxdepth: 2
  
   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
