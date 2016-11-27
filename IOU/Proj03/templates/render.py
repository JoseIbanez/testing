import os
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = "/vagrant/"
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)

def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

class BDict(dict):
     def __init__(self,**kw):
         dict.__init__(self,kw)
         self.__dict__.update(kw)


aux=BDict()
aux.id=1

vrf=BDict()
vlan=BDict()

vlan.cucm=aux
vlan.interdc=aux

import yaml
with open("./Cust16.aa.yaml", 'r') as stream:
    try:
        y=yaml.load(stream)
        print(yaml.load(stream))
    except yaml.YAMLError as exc:
        print(exc)


render_template('./cust_vlans.nj2', { vlan:vlan, vrf:vrf })
