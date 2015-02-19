#!/usr/bin/python

# Load modules
import jinja2
from optparse import OptionParser


#Get options
parser = OptionParser()
parser.add_option("-n", "--name", dest="hostname",
                  help="Name of host")
parser.add_option("-d", "--desc", dest="description",
                  help="Description of service")
parser.add_option("-p", "--port", dest="port",
                  help="Puerto a monitorizar")
(options, args) = parser.parse_args()


#Load template
templateLoader = jinja2.FileSystemLoader( searchpath="." )
templateEnv = jinja2.Environment( loader=templateLoader )

template = templateEnv.get_template( "service_mrtg.tpl" )



# Specify any input variables to the template as a dictionary.
templateVars = { "port"        : options.port,
                 "hostname"    : options.hostname,
                 "description" : options.description }

# Finally, process the template to produce our final text.
outputText = template.render( templateVars )

print outputText


