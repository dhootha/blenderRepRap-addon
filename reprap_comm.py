# import sys
from serial import Serial

port = '/dev/ttyACM0'   # default serial port for communication with reprap
baud = 115200 

def mx(value):   # moves X axis with given value
    value = 'G1 X' + str(value) + ' F200' + '\r\n'
    value = value.encode('ascii')
    print(value.strip())
    
    return value

def my(value):   # moves Y axis with given value
    value = 'G1 Y' + str(value) + ' F200' + '\r\n'
    value = value.encode('ascii')
    print(value.strip())
    
    return value

def mz(value):   # moves Z axis with given value
    value = 'G1 Z' + str(value) + ' F40' + '\r\n'
    value = value.encode('ascii')
    print(value.strip())
    
    return value

printer = Serial(port, baud)
print(printer.isOpen())
printer.close()
print(printer.isOpen())
printer.open()

printer.write('G91\r\n'.encode(encoding='ascii', errors='strict'))
print(printer.readline().strip())
printer.write(mx(+10))
print(printer.readline().strip())
printer.write(my(-10))
print(printer.readline().strip())
#printer.write('G1 X5 F10\r\n'.encode(encoding='ascii', errors='strict'))
printer.write('G1 F10\r\n'.encode(encoding='ascii', errors='strict'))
printer.write(mz(5))         #        runs too fast, need speed control :)
print(printer.readline().strip())

printer.close()
print('That\'s all folks')
