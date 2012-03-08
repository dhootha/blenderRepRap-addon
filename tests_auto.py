import sys
# we should consider adding pyserial into blender path and make tests !
PYSERIAL_PATH = "/usr/local/lib/python3.2/dist-packages/"
DEBUG_COMMUNICATION = False

def checkpaths():
    """ checks if PySerial already defined in sys.path()

    if already defined in path, prints message in console,
    else adds path to blender path.
    
    """
    if (PYSERIAL_PATH in sys.path):
        print("PySerial path already defined.")
    else:
        sys.path.append(PYSERIAL_PATH)       # print("PySerial added to path.")
        
checkpaths()    # adds PySerial path to blender

from serial import Serial
import glob
import os

def scanserial():
    """scan for available ports. 
    return a list of device names. """
    baselist=[]
    if os.name == "nt" :
        pass
#        import winreg
#        try:
#            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,"HARDWARE\\DEVICEMAP\\SERIALCOMM")
#            i = 0
#            while(1):
#                baselist += [winreg.EnumValue(key,i)[1]]
#                i += 1
#        except:
#            pass
    if os.name == "posix" :
        pass
    
    return baselist+glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*') + glob.glob("/dev/tty.*") + glob.glob("/dev/cu.*") + glob.glob("/dev/rfcomm*")

def testport():        
    """ Test found available port from scanserial() function 
    returns 'port name' or 'none' """
    ok = "none"
    
    port_name = scanserial()
    if DEBUG_COMMUNICATION:
        print(port_name)
        print("Number of ports found: ", len(port_name))
    else:
        pass
        
    num = len(port_name)
    
    try:    
        for port_name[num-1] in port_name:
            printer = Serial(port_name[num-1], 115200, timeout = 10)
         
            answer = printer.readline().strip()
            printer.close()
            print(answer.decode('ascii'))
            if ("start" in answer.decode('ascii')):
                ok = port_name[num-1]
                if DEBUG_COMMUNICATION:
                    print("OK port is: ", ok)
                else:
                    pass
            else:
                pass
    
    except:
        print("Something happend, don't know yet.")
           
    if ok is not "none":            
        return ok
    else:
        return ok
        print("Port not found.")

def check_axis(axis):
    """ Checks input parameters for the movement
    Returns True or False. """
    allowed = ["X","Y","Z","E"]
    
    if DEBUG_COMMUNICATION:
        print(allowed)
        print("Axis is: ")
        print(axis)
    else:
        pass    
     
    if axis in allowed:
        return True
    else:
        return False
        
def move(axis, direction, value, speed):
    """ Moves given 'axis' in '+' or '-' 'direction' with 'value' and 'speed'
    
    
    
    """
    axis_work = "none"
    
    if check_axis(axis):
        axis_work = axis
    else:
        print("Axis definition Error. Please enter \"X\", \"Y\", \"Z\", \"E\". ")
        
    #axis = str(axis)   # X, Y, Z, E
    direction = str(direction)  # '+' or '-'
    value = str(value)  # relative move 
    speed = str(speed)  # set speed of movement from 0 to 3000

    if axis_work is not "none":
        word = "G1 " + axis_work + direction + value + " F" + speed + "\r\n"
        return word.encode('ascii') 
        print( word.strip() )
    else:
        pass

port = testport()
baud = 115200

print(port)
if ("ACM" in port):
    printer = Serial(port, baud, timeout = 5)
    print(printer.readline().strip().decode('ascii'))
    word = 'G91\r\n'
    printer.write(word.encode('ascii'))
    word = move('X', '-', 15, 600)
    try:
        printer.write(word)
    except:
        print("No word to write.")
else: 
    pass

if ("none" not in port):
    if printer.isOpen():
        printer.close()
else: pass
print("That\'s all folks.")