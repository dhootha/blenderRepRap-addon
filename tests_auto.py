import sys
# we should consider adding pyserial into blender path and make tests !
PYSERIAL_PATH = '/usr/local/lib/python3.2/dist-packages/'

def checkpaths():
    """checks if PySerial already defined in sys.path()"""
    """if defined do nothing, else add path to blender"""
    if (PYSERIAL_PATH in sys.path):
        print('PySerial path already defined.')
    else:
        sys.path.append(PYSERIAL_PATH)
        print('PySerial added to path.')
        
checkpaths()    # adds PySerial path to blender

from serial import Serial
import glob

def scanserial():
    """scan for available ports. return a list of device names."""
    baselist=[]
#       if os.name=="nt":
#       try:
#           key=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,"HARDWARE\\DEVICEMAP\\SERIALCOMM")
#               i=0
#               while(1):
#                   baselist+=[_winreg.EnumValue(key,i)[1]]
#                   i+=1
#       except:
#           pass

    return baselist+glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*') + glob.glob("/dev/tty.*") + glob.glob("/dev/cu.*") + glob.glob("/dev/rfcomm*")

def testport():        
    """Test found available port from scanserial() function and returns 'port name' or 'none' '"""
    ok = 'none'
    
    port_name = scanserial()
    print(port_name)
    print('Number of ports found: ', len(port_name))
    
    num = len(port_name)
    print('Found port numbers: ', num)
    
    for port_name[num-1] in port_name:
        
        printer = Serial(port_name[num-1], 115200, timeout = 5)
        answer = printer.readline().strip()
        printer.close()
        print(answer.decode('ascii'))
        if ('start' in answer.decode('ascii')):
            ok = port_name[num-1]
            print('OK port is: ', ok)
        else:
            pass
    
    if ok is not 'none':            
        return ok
    else:
        return ok
        print( 'Port not found.' )
        
#    Traceback (most recent call last):
#    File "/usr/local/lib/python3.2/dist-packages/serial/serialposix.py", line 275, in open
#    self.fd = os.open(self.portstr, os.O_RDWR|os.O_NOCTTY|os.O_NONBLOCK)
#    OSError: [Errno 16] Device or resource busy: '/dev/ttyACM0'
#
#    During handling of the above exception, another exception occurred:
#
#    Traceback (most recent call last):
#    File "/Text", line 76, in <module>
#    File "/Text", line 47, in testport
#    File "/usr/local/lib/python3.2/dist-packages/serial/serialutil.py", line 261, in __init__
#    self.open()
#    File "/usr/local/lib/python3.2/dist-packages/serial/serialposix.py", line 278, in open
#    raise SerialException("could not open port %s: %s" % (self._port, msg))
#    serial.serialutil.SerialException: could not open port /dev/ttyACM0: [Errno 16] Device or resource busy: '/dev/ttyACM0'

        
    
def move(axis, direction, value, speed):
    """Moves given 'axis' in '+' or '-' 'direction' with 'value' and 'speed'"""
    axis = str(axis)    # X, Y, Z, E
    direction = str(direction)  # '+' or '-'
    value = str(value)  # relative move 
    speed = str(speed)  # set speed of movement from 0 to 3000

    word = 'G1 ' + axis + direction + value + ' F' + speed + '\r\n' 
    print( word.strip() )
    
    return word.encode('ascii')    

port = testport()
baud = 115200

print(port)
if ('ACM' in port):
    printer = Serial(port, baud, timeout = 5)
    print(printer.readline().strip().decode('ascii'))
    word = 'G91\r\n'
    printer.write(word.encode('ascii'))
    word = move('X', '-', 15, 600)
    printer.write(word)
else: pass

if ('none' not in port):
    if printer.isOpen():
        printer.close()
else: pass
print('That\'s all folks.')