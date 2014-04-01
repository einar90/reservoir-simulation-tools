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


def create_propery_selection_string(props, wells):
    propstrings = []
    for p in range(len(props)):
        for w in range(len(wells)):
            propstrings.append(props[p] + ':' + wells[w])
    return propstrings


def get_summary_output(filename, propstrings):
    command = ["ecl_summary", filename]
    for propstring in propstrings:
        command.append(propstring)
    return subprocess.check_output(command)


def parse_output(output):
    lines = output.split("\n")
    headers = lines[0].split(" ")
    headers = [x for x in headers if x != ' ' and x != '' and x != '--']
    valuelines = lines[2:]
    valuelines = [line.split(' ') for line in valuelines]
    for line in valuelines:
        while '' in line:
            line.remove('')
    valuelines.pop()  # Removing \n at the end
    return (headers, valuelines)


def create_time_vector(valuelines):
    time = []
    for line in valuelines:
        time.append(line[0])
    return time


def create_value_vectors(valuelines, props, wells):
    values = [[]]
    for i in range(len(props)):
        for j in range(len(wells)):
            for line in valuelines:
                values[i*len(wells)+j].append(line[2+i*len(wells)+j])
            values.append([])
    values.pop()
    return values


def plot_values(values, time, props, wells):
    plt.Figure()
    plots = []
    for i in range(len(props)):
        for j in range(len(wells)):
            line, = plt.plot(time, values[i*len(wells)+j])
            plots.append(line)

    plt.legend(plots, propstrings, loc=2)
    plt.show()


# Get filename
filename = raw_input('Filename: ')

# Well selection
get_well_list()
wells = raw_input('Select wells (space-separated): ').split(' ')

# Property selection
get_property_list()
props = raw_input('Properties to plot (space-separated): ').split(' ')
propstrings = create_propery_selection_string(props, wells)


# Getting the ecl_summary output
output = get_summary_output(filename, propstrings)
(headers, valuelines) = parse_output(output)

# Creating vectors
time = create_time_vector(valuelines)
values = create_value_vectors(valuelines, props, wells)

plot_values(values, time, props, wells)
