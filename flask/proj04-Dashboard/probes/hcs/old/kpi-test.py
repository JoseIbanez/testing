#!/usr/bin/python

from kpi import Kpi


def main():
  cmd = Kpi("UKX","2016-01-01","ping")
  print(cmd)
  cmd.parseLine("333")


if __name__ == "__main__":
    main()
