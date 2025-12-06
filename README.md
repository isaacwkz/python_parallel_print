# python-parallel-print
Yet another (?) printer library

# Pre-requisite
pillow==12.0.0
Tested with Windows 11 for Canon Selphy CP1500 photo printers.

# Intro
This library tries to detect CP1500 printers that are connected, then it distributes the print jobs between available printers.

# Getting started
`python3 -m pipenv install pillow==12.0.0`
`python3 -m pipenv shell`
`python example.py`