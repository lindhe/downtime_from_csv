#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# License: MIT
# Author: Andreas Lindhé

""" Main function description.

This is where general documentation should go.
"""

import sys
import time
import argparse

version = "0.0.1"

def main():
  """ Main function description """
  return (0)

if __name__ == '__main__':
  # Bootstrapping
  p = argparse.ArgumentParser(description="Skeleton file for Python!")
  # Add cli arguments
  p.add_argument('-V', '--version', action="version", version=version)
  # Run:
  args = p.parse_args()
  try:
    main()
  except KeyboardInterrupt:
    sys.exit("\nInterrupted by ^C\n")

