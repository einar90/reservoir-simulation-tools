'''
Uses the 'ecl_summary' command found in the Ensambles ERT software package
created by statoil to read and plot data from an eclipse summary file.
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
    print 'The following files are available in the active folder:'
    for i in range(len(summary_files)):
        print '(%i) %s' % (i, summary_files[i])
    return summary_files


def get_file_name():
    summary_files = list_summary_files()
    input_file = raw_input('Filename or number: ')
    try:
        file_number = int(input_file)
        filename = summary_files[file_number]
    except Exception:
        filename = input_file
    return filename


def get_wells(filename):
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
    wells = raw_input('Select wells (space-separated): ').split(' ')
    return wells


def get_properties(filename, wells):
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
        #print proplist[well]
        for prop in range(len(proplist[well])):
            print proplist[well][prop] + '\t',
            if (prop % 8) == 0 and prop != 0 and prop < len(proplist[well]):
                print '\n',
        print '\n'
    props = raw_input('Properties to plot (space-separated): ').split(' ')
    return props


def get_field_props(filename):
    print 'Available properties are:'
    proplist = subprocess.check_output([
                                       "ecl_summary",
                                       filename,
                                       "--list",
                                       "F*"])
    proplist = proplist.replace('\n', "")
    proplist = proplist.split(' ')
    while '' in proplist:
        proplist.remove('')
    for prop in range(len(proplist)):
        print proplist[prop] + '\t',
        if (prop % 8) == 0 and prop != 0 and prop < len(proplist):
            print '\n',
    print '\n'
    props = raw_input('Properties to plot (space-separated): ').split(' ')
    return props


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


def plot_values(propstrings, values, time, props, wells):
    plt.Figure()
    plots = []
    for i in range(len(props)):
        for j in range(len(wells)):
            line, = plt.plot(time, values[i*len(wells)+j])
            plots.append(line)

    plt.legend(plots, propstrings, loc=2)
    plt.show()

    next_action = raw_input('Quit program (q) or write data to csv (w)? ')

    if next_action == 'q':
        plt.close()
    elif next_action == 'w':
        plt.close()
        write_data_to_csv(propstrings, values, time, wells, props)


def write_data_to_csv(propstrings, values, time, wells, props):
    output_filename = raw_input("Name of output file:")
    f = open(output_filename, 'w')

    # Write headers
    f.write('TIME,')
    for header in propstrings:
        f.write(header + ',')

    for value in range(len(values[0])):
        f.write('\n')
        f.write(time[value] + ',')
        for prop in range(len(props)):
            for well in range(len(wells)):
                f.write(values[prop*len(wells)+well][value] + ',')

    f.close()


def get_action():
    if action == 'p':
        plot_values(propstrings, values, time, props, wells)
    elif action == 'w':
        write_data_to_csv(propstrings, values, time, wells, props)


# Getting input from user
filename = get_file_name()  # Getting file from user input

# Asking for well/field data
field_data = (raw_input('Plot field (f) or well (w) data? ') == 'f')

# Getting well and property lists
if field_data:
    props = propstrings = get_field_props(filename)
    wells = ['FIELD']
else:
    wells = get_wells(filename)  # Getting wells from user input
    props = get_properties(filename, wells)  # Getting props from user input
    propstrings = create_propery_selection_string(props, wells)  # Parsing props


# Getting the ecl_summary output and parsing it
output = get_summary_output(filename, propstrings)
(headers, valuelines) = parse_output(output)

# Creating vectors creating vectors from parsed output
time = create_time_vector(valuelines)
values = create_value_vectors(valuelines, props, wells)

action = raw_input('Plot results (p) or write to csv file (w)? ')

get_action()
