import time
import pickle
import os
import glob

import numpy as np
import argparse
import pathlib

parser = argparse.ArgumentParser(description = "arguement parsing:")
parser.add_argument('--nul', type = float, default = 0)

parser.add_argument('--TEMPS', type = float, nargs='*', required = False)
parser.add_argument('--VAS', help ="Voltages on CH1 Tension (see temperature dependant limitations in Razorbill User Guide): ex. [0, 5, 20, 50]", type = float, nargs='*', required = False)
parser.add_argument('--VBS', type = float, nargs='*', required = False)
parser.add_argument('--FIELD', type = float, nargs=3, required = False)
parser.add_argument('--QD_FILES', type=pathlib.Path, required = False)

args = parser.parse_args()

print("This will run Field Sweeps at a list of given Temperatures for each Razorbill Power Setting VAS,VBS supplied:")               

if args.TEMPS is None:
    args.TEMPS = input("Range of temperatures in Kelvin: ex. [50, 10, 2]:  ")
if args.VAS is None:
    args.VAS = input("Voltages on CH1 Tension (see temperature dependant limitations in Razorbill User Guide): ex. [0, 5, 20, 50]:  ")
if args.VBS is None:
    args.VBS = input("Voltages on CH2 Compression(see temperature dependant limitations in Razorbill User Guide): ex. [10, 10, 10, 10]:  ")
if args.FIELD is None:
    args.FIELD = input("max field (Oe), min field (Oe), ramping rate (Oe/sec): ex. 90000, -90000, 50:  ")
if args.QD_FILES is None:
    args.QD_FILES  = input("Folder Path:  ")




print('list inputs:')

print("args.TEMPS:")
for i in args.TEMPS:
    print(i)
print(args.TEMPS)
print("*args.FIELD")
print(*args.FIELD)




























