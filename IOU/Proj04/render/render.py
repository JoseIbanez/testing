#!/usr/bin/python

import csv
from optparse import OptionParser

def render_template(template, id, names, values):

    templateFile = open(template, "rb")
    outputFile = open(id+".cmd", "w")

    for inLine in templateFile:

        outLine = inLine
        for n in range(0, len(names)):
            outLine = outLine.replace("{{"+names[n]+"}}", values[n])


        outputFile.write(outLine)

    templateFile.close()
    outputFile.close()



#Get options
parser = OptionParser()
parser.add_option("-v", "--values", dest="values",
                  help="Config values file")
parser.add_option("-t", "--template", dest="template",
                  help="Config template file")
parser.add_option("-i", "--id", dest="id",
                  help="Entry id to generate")

(options, args) = parser.parse_args()

#
valuesFile = open(options.values, 'rb')
reader = csv.reader(valuesFile)

line = 0
for i in reader:
    line += 1

    if line == 1:
        names = i
        print names
        continue

    if (i[0] == options.id) or not options.id:
        values = i
        render_template(options.template, i[0], names, values)
        print values


valuesFile.close()



    