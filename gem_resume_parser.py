import json
import argparse
import resumes_parser

def argument_parser():
    '''Taking JSON Argument from user'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help = "json file") 
    args = parser.parse_args() 
    with open(args.file) as json_data:
        data = json.load(json_data)
    
    return data

def main():
    arguments_data = argument_parser()
    for i in arguments_data.keys():
        resumes_parser.main(arguments_data[i])

if __name__ == "__main__":
    main()