import time
import pickle
import os
import glob

import numpy as np
import argparse
import pathlib

parser = argparse.ArgumentParser(description = "arguement parsing:")
parser.add_argument('--start', type = string, default = "start")

args = parser.parse_args()
parser.add_argument('--TRANSITION_TEMP', type = float, required = False)          # Warm to this with zero field, zero voltage
if args.TRANSITION_TEMP is None:
    args.TRANSITION_TEMP = input("Transition temperature: ")                        
parser.add_argument('--TEMPS', type = float, nargs='*', required = False)
if args.TEMPS is None:
    args.TEMPS = input("Range of temperatures in Kelvin: ex. [50, 10, 2]:  ")
parser.add_argument('--VAS', help ="Voltages on CH1 Tension (see temperature dependant limitations in Razorbill User Guide): ex. [0, 5, 20, 50]", type = float, nargs='*', required = False)
if args.VAS is None:
    args.VAS = input("Voltages on CH1 Tension (see temperature dependant limitations in Razorbill User Guide): ex. [0, 5, 20, 50]:  ")
parser.add_argument('--VBS', type = float, nargs='*', required = False)
if args.VBS is None:
    args.VBS = input("Voltages on CH2 Compression(see temperature dependant limitations in Razorbill User Guide): ex. [10, 10, 10, 10]:  ")
parser.add_argument('--FIELD', type = float, nargs=3, required = False)
if args.FIELD is None:
    args.FIELD = input("max field (Oe), min field (Oe), ramping rate (Oe/sec): ex. 90000, -90000, 50:  ")
parser.add_argument('--QD_FILES', type=pathlib.Path, required = False)
if args.QD_FILES is None:
    args.QD_FILES  = input("Folder Path:  ")
args = parser.parse_args()



print('list inputs:')
print("args.TRANSITION_TEMP:")
print(args.TRANSITION_TEMP)
print("args.TEMPS:")
print(args.TEMPS)
















