import time
import pickle
import os
import glob

import numpy as np
import argparse
import pathlib

parser = argparse.ArgumentParser(description = "arguement parsing:")

parser.add_argument("TRANSITION_TEMP", help ="Transition temperature", type = float)          # Warm to this with zero field, zero voltage
parser.add_argument("TEMPS", help ="Range of temperatures in Kelvin: ex. [50, 10, 2]", type = float, nargs='*')
parser.add_argument("VAS", help ="Voltages on CH1 Tension (see temperature dependant limitations in Razorbill User Guide): ex. [0, 5, 20, 50]", type = float, nargs='*')
parser.add_argument("VBS", help ="Voltages on CH2 Compression(see temperature dependant limitations in Razorbill User Guide): ex. [10, 10, 10, 10]", type = float, nargs='*')
parser.add_argument("FIELD", help ="max field (Oe), min field (Oe), ramping rate (Oe/sec): ex. 90000, -90000, 50", type = float, nargs=3)
parser.add_argument("QD_FILES", help ="Folder Path:  ", type=pathlib.Path)
args = parser.parse_args()

if args.TRANSITION_TEMP is None:
    args.TRANSITION_TEMP = input(args.TRANSITION_TEMP.help())
if args.TEMPS is None:
    args.TEMPS = input(args.TEMPS.help())
if args.VAS is None:
    args.VAS = input(args.VAS.help())
if args.VBS is None:
    args.VBS = input(args.VBS.help())
if args.FIELD is None:
    args.FIELD = input(args.FIELD.help())
if args.QD_FILES is None:
    args.QD_FILES  = input(args.QD_FILES.help())


print('list inputs:')
print("args.TRANSITION_TEMP:")
print(args.TRANSITION_TEMP)
print("args.TEMPS:")
print(args.TEMPS)






