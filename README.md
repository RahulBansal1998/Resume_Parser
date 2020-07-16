# pyresparser

```
A simple resume parser used for extracting information from resumes
```

Built with ❤︎ and coffee



# Features

- Extract name
- Extract email
- Extract mobile numbers
- Extract skills
- Extract total experience
- Extract college name
- Extract degree
- Extract designation
- Extract company names

# Installation

- You can install this package using

```bash
pip install pyresparser
```

- For NLP operations we use spacy and nltk. Install them using below commands:

```bash
# spaCy
python -m spacy download en_core_web_sm

# nltk
python -m nltk.downloader words
```

# Supported File Formats

- PDF and DOCx and Doc files are supported on all Operating Systems


# Usage

- Import it in your Python project

```python
from pyresparser import ResumeParser
data = ResumeParser('/path/to/resume/file').get_extracted_data()
For File:
      python resume.py --filepath <filepath of Resume Complete> --excel <Excel Filename>

      E.g - python resume.py --filepath Resume/OmkarResume.docx --excel Omkar.xlsx

For Directory:

      python resume.py --directory <Directory Name> --excel <Excel Filename>

      E.g - python resume.py --directory Resume --excel Resume.xlsx
```

# Notes:

- If you are running the app on windows, then you can only extract .docs and .pdf files

# Result

The module would return a Excel File


# References that helped me get here

- Some of the core concepts behind the algorithm have been taken from [https://github.com/divapriya/Language_Processing](https://github.com/divapriya/Language_Processing) which has been summed up in this blog [https://medium.com/@divalicious.priya/information-extraction-from-cv-acec216c3f48](https://medium.com/@divalicious.priya/information-extraction-from-cv-acec216c3f48). Thanks to Priya for sharing this concept

- [https://www.kaggle.com/nirant/hitchhiker-s-guide-to-nlp-in-spacy](https://www.kaggle.com/nirant/hitchhiker-s-guide-to-nlp-in-spacy)

- [https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/](https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/)


