from serial import Serial

port = '/dev/ttyUSB0'
baud = 115200

printer = Serial(port, baud, timeout = 10)

if printer.isOpen():
    print('port already open.')
else:
    printer.open()
    
print(printer.readline().decode('ascii').strip())

printer.write('G91\r\n'.encode(encoding='ascii', errors='strict'))
print(printer.readline().decode('ascii').strip())

printer.write('G1 X5 F500\r\n'.encode(encoding='ascii', errors='strict'))
print(printer.readline().decode('ascii').strip())


if printer.isOpen():
    printer.close()
    print('port is closed now.')
else:
    print('port already closed.')