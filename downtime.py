#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

""" Downtime extractor 5000.# {{{

Takes a CSV file with registered up/downtimes and returns the gaps.
"""# }}}

###############################     IMPORTS     ###############################{{{
import csv
import sys
import time
import argparse
# }}}

##############################     VARIABLES     ##############################
version = "0.0.1"

################################     OUTPUT     ################################
def output(changes, output_file=None):# {{{
  """ Prints or writes the list of changes, depending on program arguments. """
  if output_file:
    pass
  for c in changes:
    print(c['time'] + "," + c['status'])
# }}}

#################################     MAIN     #################################
def main(csv_file, delimiter, indicator, status_col, time_col, begin):# {{{
  """ Reads the file and prints all gaps. """
  with csv_file as f:
    csv_lines = csv.reader(f, delimiter=delimiter)
    for s in range(begin):
      next(csv_lines)
    prev = ""
    changes = []
    for line in csv_lines:
      t = line[time_col]
      s = line[status_col]
      if s != prev:
        changes.append({'time': t, 'status': s})
        prev = s
  output(changes)# }}}


############################     BOOTSTRAPPING     ############################
if __name__ == '__main__':# {{{
  desc = "Downtime extractor 5000!!"
  # Arguments
  p = argparse.ArgumentParser(description=desc)
  # p.add_argument('-e', '--end', type=int, default=0, metavar='E', help="number of lines to skip at the bottom (default: 0)")
  # p.add_argument('-f', '--date-format', help="not implemented")
  # p.add_argument('-o', '--out-file', type=argparse.FileType('w'), help="not implemented")
  # p.add_argument('-u', '--uptime', action='store_true', help="get uptime instead of downtime")
  p.add_argument('-b', '--begin', type=int, default=2, metavar='B', help="number of lines to skip at the beginning (default: 2)")
  p.add_argument('-d', '--delimiter', default=',', metavar='D', help="delimiter (default: ,)")
  p.add_argument('-i', '--indicator', default='TRUE', metavar='I', help="the string indicating downtime (default: \"TRUE\")")
  p.add_argument('-s', '--status-column', type=int, default=3, metavar='S', help="index of status column (defualt: 2)")
  p.add_argument('-t', '--time-column', type=int, default=2, metavar='T', help="index of timestamps (defualt: 3)")
  p.add_argument('-V', '--version', action='version', version=version)
  p.add_argument('file', type=argparse.FileType('r'), help="CSV file")
  # Parsing
  args = p.parse_args()
  # Run:
  try:
    main(
        csv_file = args.file,
        delimiter = args.delimiter,
        indicator = args.indicator,
        status_col = args.status_column,
        time_col = args.time_column,
        begin = args.begin
        )
  except KeyboardInterrupt:
    sys.exit("\nInterrupted by ^C\n")
# }}}
