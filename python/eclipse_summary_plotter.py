'''
Uses the 'ecl_summary' command found in the Ensambles ERT software package
created by statoil to read and plot data from an eclipse summary file.
Requires both a *.UNSMRY and *.SMSPEC file to be present.

https://github.com/Ensembles/ert
'''

from matplotlib import pyplot as plt
import subprocess


def get_well_list():
    print "The following wells are available:"
    wellist = subprocess.check_output([
                                      "ecl_summary",
                                      filename,
                                      "--list", "WBHP:*"
                                      ])
    wellist = wellist.split(' ')
    while '' in wellist:
        wellist.remove('')
    wellist.pop()  # Last element is \n
    wellist = [well.strip().split(':') for well in wellist]
    wellist = [well[1] for well in wellist]
    for well in wellist:
        print well + ', '


def get_property_list():
    print "The following properties are available for the selected wells:"
    proplist = []
    for well in wells:
        proplist.append(subprocess.check_output([
                                                "ecl_summary",
                                                filename, "--list",
                                                '*:' + well]))
    for well in range(len(proplist)):
        proplist[well] = proplist[well].split(' ')
        proplist[well].pop()
        while '' in proplist[well]:
            proplist[well].remove('')
        proplist[well] = [prop.strip().split(':') for prop in proplist[well]]
        proplist[well] = [prop[0] for prop in proplist[well]]

    for well in range(len(proplist)):
        print 'Properties for well ' + wells[well]
        print proplist[well]



# Get filename
filename = raw_input('Filename: ')

# Well selection
get_well_list()
wells = raw_input('Select wells (space-separated): ').split(' ')

# Property selection
get_property_list()
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

plt.Figure()
plots = []
for i in range(len(props)):
    for j in range(len(wells)):
        line, = plt.plot(time, values[i*len(wells)+j])
        plots.append(line)

plt.legend(plots, propstrings, loc=2)
plt.show()
