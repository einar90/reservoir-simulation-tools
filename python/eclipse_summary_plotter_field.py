'''
Uses the 'ecl_summary' command found in the Ensambles ERT software package
created by statoil to read and plot data from an eclipse summary file.
Requires both a *.UNSMRY and *.SMSPEC file to be present.

https://github.com/Ensembles/ert
'''

from matplotlib import pyplot as plt
import subprocess

filename = raw_input('Filename (excluding .UNSMRY): ')
print "The following properties are available:"
subprocess.call(["ecl_summary", filename, "--list", "F*"])
props = raw_input('Properties to plot (space-separated): ').split(' ')

# Getting the ecl_summary output
command = ["ecl_summary", filename]
for prop in props:
    command.append(prop)
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
    for line in valuelines:
        values[i].append(line[2+i])
    values.append([])
values.pop()

plt.Figure()
plots = []
for i in range(len(props)):
    line, = plt.plot(time, values[i])
    plots.append(line)

plt.legend(plots, props, loc=2)
plt.show()
