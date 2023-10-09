#!/usr/bin/env python3

'''
Converts data from input csv file and creates testbed yaml file
using Jinja2 templates

'''
import argparse
import csv
from jinja2 import Environment, FileSystemLoader
import sys


def CreateTestbedFile(input_file, output_file):

    data={}

    #Import CSV
    csv.register_dialect('excel', delimiter=';')

    with open(input_file, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf, dialect='excel')
        for rows in csvReader:
            key = rows['HOSTNAME']
            data[key] = rows

    # Generate testbed from template
    file_loader = FileSystemLoader('./templates')
    env = Environment(loader= file_loader)

    template = env.get_template('testbed_header.j2')
    
    batch= template.render()
    try:
        outputfile = open(output_file, "w")
    except:
        print('Unable to create file ', output_file)
        sys.exit(1)

    outputfile.write(batch)

    try:
        outputfile.close()
    except:
        print('Unable to close file ', output_file)
        sys.exit(1)

    template = env.get_template('testbed_device.j2')

    for key in data:
        batch= template.render(hostname= data[key]['HOSTNAME'], ip=data[key]['IP'])

        try:
            outputfile = open(output_file, "a")
        except:
            print('Unable to create file ', output_file)
            sys.exit(1)

        outputfile.write(batch)

        try:
            outputfile.close()
        except:
            print('Unable to close file ', output_file)
            sys.exit(1)

    print(f'Testbed file {output_file} was successfully generated.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Creates testbed yaml file from given csv file')
    parser.add_argument(
        '-i', '--input_file', help='Input CSV file with list of provisioned devices', required=True, type=str)
    parser.add_argument(
        '-o', '--output_file', help='Output YAML testbed file', required=True, type=str)
    args = parser.parse_args()

    CreateTestbedFile(args.input_file, args.output_file)
