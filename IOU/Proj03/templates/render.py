#!/usr/bin/python2.7

import os
from optparse import OptionParser
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
import yaml

#Get options
parser = OptionParser()
parser.add_option("-c", "--config", dest="conf",
                  help="Config values file")
parser.add_option("-t", "--template", dest="template",
                  help="Config template file")
(options, args) = parser.parse_args()

#

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
#    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    loader=FileSystemLoader(".."),
    trim_blocks=False)

def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

with open(options.conf, 'r') as stream:
    try:
        y=yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

out=render_template(options.template, y )
print out
