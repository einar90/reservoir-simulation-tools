'''
Uses the 'ecl_summary' command found in the Ensambles ERT software package
created by statoil to read eclipse summary file and save it in the csv format.
Requires both a *.UNSMRY and *.SMSPEC file to be present.

The ERT software may be downloaded at https://github.com/Ensembles/ert
'''

import subprocess

filename = raw_input('Filename (excluding .UNSMRY): ')
print "The following properties are available:"
subprocess.call(["ecl_summary", filename, "--list", "W*"])
wells = raw_input('Select wells (space-separated): ').split(' ')
print "The following properties are available for the selected wells:"
for well in wells:
    subprocess.call(["ecl_summary", filename, "--list", '*:' + well])
props = raw_input('Properties to plot (space-separated): ').split(' ')

propstrings = []
for p in range(len(props)):
    for w in range(len(wells)):
        propstrings.append(props[p] + ':' + wells[w])

# Getting the ecl_summary output
command = ["ecl_summary", filename]
for propstring in propstrings:
    command.append(propstring)
output = subprocess.check_output(command)

# Splitting output by lines
lines = output.split("\n")

# Getting headers and stripping empty elements and splaces
headers = lines[0].split(" ")
headers = [x for x in headers if x != ' ' and x != '' and x != '--']

# Getting values
valuelines = lines[2:]
valuelines = [line.split(' ') for line in valuelines]

# Removing empty elements
for line in valuelines:
    while '' in line:
        line.remove('')

# Removing last element (usually empty)
valuelines.pop()


# Creating time and value vectors
time = []
for line in valuelines:
    time.append(line[0])

values = [[]]
for i in range(len(props)):
    for j in range(len(wells)):
        for line in valuelines:
            values[i*len(wells)+j].append(line[2+i*len(wells)+j])
        values.append([])
values.pop()

output_filename = raw_input("Name of output file:")
f = open(output_filename, 'w')

# Write headers
for header in propstrings:
    f.write(header + ',')

for value in range(len(values[0])):
    f.write('\n')
    for prop in range(len(props)):
        for well in range(len(wells)):
            f.write(values[prop*len(wells)+well][value] + ',')


f.close()
