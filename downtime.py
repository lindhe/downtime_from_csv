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
import argparse
# }}}

##############################     VARIABLES     ##############################
version = "0.0.1"

################################     INPUT     ################################
def input_data(csv_file, delimiter, status_col, time_col, begin):# {{{
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
  # }}}
  return changes

################################     OUTPUT     ################################
def output_data(changes, output_file=None, csv_format=False, delimiter=',', indicator='TRUE'):# {{{
  """ Prints or writes the list of changes, depending on program arguments. """
  downtime = []
  if changes[0]['status'] != indicator:
    changes = changes[1:]
  if len(changes) % 2 != 0:
    changes = changes[:-1]
  n = 0
  while n < len(changes):
    downtime.append({'from': changes[n]['time'], 'to': changes[n+1]['time']})
    n += 2
  if csv_format:
    if output_file:
      with output_file as f:
        for c in changes:
          csv_line = c['time'] + delimiter + c['status'] + '\n'
          f.write(csv_line)
    for c in changes:
      csv_line = c['time'] + delimiter + c['status']
      print(csv_line)
  else:
    if output_file:
      with output_file as f:
        for span in downtime:
          human_readable = "Downtime from [" + span['from'] + "] to [" + span['to'] + "]\n"
          f.write(human_readable)
    for span in downtime:
      human_readable = "Downtime from [" + span['from'] + "] to [" + span['to'] + "]"
      print(human_readable)
# }}}

#################################     MAIN     #################################
def main(csv_file, delimiter, indicator, status_col, time_col, begin, csv_format, output):# {{{
  """ Reads the file and prints all gaps. """
  changes = input_data(csv_file, delimiter, status_col, time_col, begin)
  output_data(changes, csv_format=csv_format, delimiter=delimiter, indicator=indicator, output_file=output)
# }}}

############################     BOOTSTRAPPING     ############################
if __name__ == '__main__':# {{{
  desc = "Downtime extractor 5000!!"
  # Arguments
  p = argparse.ArgumentParser(description=desc)
  # p.add_argument('-e', '--end', type=int, default=0, metavar='E', help="number of lines to skip at the bottom (default: 0)")
  # p.add_argument('-u', '--uptime', action='store_true', help="get uptime instead of downtime")
  p.add_argument('-b', '--begin', type=int, default=2, metavar='B', help="number of lines to skip at the beginning (default: 2)")
  p.add_argument('-c', '--csv', action='store_true', help="output CSV format")
  p.add_argument('-d', '--delimiter', default=',', metavar='D', help="delimiter (default: ,)")
  p.add_argument('-i', '--indicator', default='TRUE', metavar='I', help="the string indicating downtime (default: \"TRUE\")")
  p.add_argument('-o', '--output', type=argparse.FileType('a'), help="output file")
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
        begin = args.begin,
        csv_format = args.csv,
        output = args.output
        )
  except KeyboardInterrupt:
    sys.exit("\nInterrupted by ^C\n")
# }}}
