import pyvisa
import time
rm = pyvisa.ResourceManager()
SPARKY = rm.open_resource('ASRL08::INSTR')

print('set ch1 volt to 0')
time.sleep(0.1)
SPARKY.write('sour1:volt 0')

print('turn off chn 1')
time.sleep(0.1)
SPARKY.write('outp1 0')

print('set ch2 volt to 0')
time.sleep(0.1)
SPARKY.write('sour2:volt 0')

print('turn off chn 2')
time.sleep(0.1)
SPARKY.write('outp2 0')

print('query both channels check that it did turn off')
time.sleep(0.1)
print(SPARKY.query('outp1?'))
print(SPARKY.query('outp2?'))

print('determine voltages')
time.sleep(0.1)
print(SPARKY.query('sour1:volt?'))
print(SPARKY.query('sour2:volt?'))




