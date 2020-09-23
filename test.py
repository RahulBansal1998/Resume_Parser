import json
import argparse

def argument_parser():
    '''Taking JSON Argument'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help = "json file") 
    args = parser.parse_args() 
    return args.file

filee = argument_parser()
with open(filee) as json_data:
    data = json.load(json_data)
    print(data["sheets"][0])
    

