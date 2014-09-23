'''
Uses the 'ecl_summary' command found in the Ensambles ERT software package
created by statoil to convert data from an eclipse summary file to a csv format.
Requires both a *.UNSMRY and *.SMSPEC file to be present.

https://github.com/Ensembles/ert
'''

from matplotlib import pyplot as plt
import subprocess

def list_summary_files():
    summary_files = subprocess.check_output(['find', '.', '-name', '*.UNSMRY'])
    summary_files = summary_files.split('\n')
    if summary_files[-1] == '':
        summary_files.pop()  # Deleting empty element at end
    # Removing ./ and .UNSMRY
    summary_files = [sumfile[2:-7] for sumfile in summary_files]

    print '\n',
    print '|-----------------------------------------------------------------|'
    print '| The following files are available in the active folder:         |'
    print '|-----------------------------------------------------------------|'
    for i in range(len(summary_files)):
        print '| (%i) %s' % (i, summary_files[i])
    print '|-----------------------------------------------------------------|'
    return summary_files

def get_file_name():
    summary_files = list_summary_files()
    input_file = raw_input('\nFilename or number: ')
    try:
        file_number = int(input_file)
        filename = summary_files[file_number]
    except Exception:
        filename = input_file
    return filename

def get_properties(filename):
    proplist = subprocess.check_output(["ecl_summary", filename, "--list"])
    proplist = proplist.replace('\n', ' ')
    proplist = proplist.split(' ')
    while '' in proplist:
        proplist.remove('') # Remove emtystrings from list
    return proplist

def get_valuestring(filename, proplist):
    command = ["ecl_summary", filename]
    for propstring in proplist:
        command.append(propstring)
    return subprocess.check_output(command)

def parse_valuestring(valuestring):
    valuelist = valuestring.split('\n')
    valuelist.pop(1)  # Pop dividing '===' line

    # Constructing header list
    headers = valuelist.pop(0).split(' ')  # Headers is first line
    headers = [header for header in headers if header != ''] # Remove empty elements and leading '--'
    headers.pop(0) # Pop leading '--'
    

    # Constructing value list
    valuelist = [line.split(' ') for line in valuelist]  # Split into value elements by whitespace
    for line in valuelist:  # Remove empty elements
        while '' in line:
            line.remove('')
    return (headers, valuelist)

def save_to_csv(headers, valuelist, filename):
    output_filename = filename.lower() + '.csv' 
    f = open(output_filename, 'w')

    # Write headers
    for header in headers:
        f.write(header + ',')

    # Write values
    for line in valuelist:
        f.write('\n')
        for value in line:
            f.write(value + ',')
    f.close()
    print 'Successfully created csv file ' + output_filename


filename = get_file_name()  # Getting file from user input
proplist = get_properties(filename)  # Generate list of properties in file
valuestring = get_valuestring(filename, proplist)  # Get the ecl_summary output for all properties
(headers, valuelist) = parse_valuestring(valuestring)  # Parse the output to lists
save_to_csv(headers, valuelist, filename)