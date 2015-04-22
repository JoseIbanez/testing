#!/usr/bin/python

# Load modules
import jinja2
from optparse import OptionParser


#Get options
parser = OptionParser()
parser.add_option("-H", "--host", dest="hostname",
                  help="Name of host")
parser.add_option("-i", "--ip", dest="ip",
                  help="IP address of host")
parser.add_option("-g", "--groups", dest="hostgroups",
                  help="groups of this host")
parser.add_option("-t", "--template", dest="template",
                  help="groups of this host")
                  

(options, args) = parser.parse_args()


#Load template
templateLoader = jinja2.FileSystemLoader( searchpath="." )
templateEnv =    jinja2.Environment( loader=templateLoader )

template = templateEnv.get_template( options.template )



# Specify any input variables to the template as a dictionary.
templateVars = { "ip"         : options.ip,
                 "hostname"   : options.hostname,
                 "hostgroups" : options.hostgroups }

# Finally, process the template to produce our final text.
outputText = template.render( templateVars )


print outputText
f = open( options.hostname + ".cfg", 'w')
f.write(outputText)
f.close;


