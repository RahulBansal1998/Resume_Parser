import json
import argparse
import resumes_parser
from drive_cli import actions
import resumes_parser
import os

def argument_parser():
    '''
    Taking JSON Argument and Key from user
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",required=False,help = "json file",default='gem_resume_parser.json') 
    parser.add_argument("-k", "--key",required=True,help = "Key") 
    args = parser.parse_args()
    args = [args.file,args.key]
    return args

def load_json(argument_data):
    with open(argument_data) as json_data:
        data = json.load(json_data)
    return data

def drive_pull(arguments_data):
    '''
    :param : json argument_data for mapping
     function for pulling data from drive 
    '''
    os.chdir(arguments_data["Directory"])
    # os.system("drive login")
    # os.system("drive add_remote")
    actions.pulls(arguments_data)
    os.chdir(arguments_data["root"])

def main():
    arguments_data = argument_parser()
    arguments_key = arguments_data[1]
    arguments_data_json = load_json(arguments_data[0])
    drive_pull(arguments_data_json[arguments_key])
    resumes_parser.main(arguments_data_json[arguments_key])

if __name__ == "__main__":
    main()