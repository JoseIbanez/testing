#!/usr/bin/python

class Kpi:

    def hello(self):
        return "hello"

    def __init__(self,host,date,cmd):
        self.ret=0
        self.host=host
        self.date=date
        self.cmd=cmd
        self.section=""
        self.kpi={}

    def __str__(self):
        return str(self.host)+str(self.kpi)

    def parseLine(self,l):
        print(l)
        return 0
