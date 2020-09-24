import json
import argparse
import resume

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
    resume.main(arguments_data)

if __name__ == "__main__":
    main()