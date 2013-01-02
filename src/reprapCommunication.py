import sys
# we should consider adding pyserial into blender path and make tests !
pyserialPath = "/usr/local/lib/python3.2/dist-packages/"    # path to installed pySerial for python 3.2py
debug = True   # allow print in functions to be printed in console

def checkPathInBlender():
    """ checks if PySerial already defined in sys.path()
    if already defined in path, prints message in console, else adds path to blender path.   
    """
    if (pyserialPath in sys.path):
        print("PySerial path already defined.")
    else:
        sys.path.append(pyserialPath)       # print("PySerial added to path.")
        
checkPathInBlender()    # adds PySerial path to blender

from serial import Serial
import glob
import os

def scanForSerialPorts():
    """scan for available ports. 
    return a list of device names. 
    """
    baselist=[]
    if os.name == "nt" :
        try:
            import winreg #@UnresolvedImport
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,"HARDWARE\\DEVICEMAP\\SERIALCOMM")
            i = 0
            while(1):
                baselist += [winreg.EnumValue(key,i)[1]]
                i += 1
        except:
            pass
    if os.name == "posix" :
        pass
    
    return baselist+glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*') + glob.glob("/dev/tty.*") + glob.glob("/dev/cu.*") + glob.glob("/dev/rfcomm*")

def testPortsForRepRap():
    """ Test found available port from scanserial() function 
    returns 'port name' or 'none' """
    
    portOk = "none" # port that will be used for communication with RepRap
    
    portName = scanForSerialPorts()
    if debug:
        print(portName)
        print("Number of ports found: ", len(portName))
    else:
        pass
        
    num = len(portName)
    
    try:    
        for portName[num-1] in portName:
            printer = Serial(portName[num-1], 115200, timeout = 30)
            
            answer = printer.readline().strip()
            printer.close()
            #print(answer.decode('ascii'))
            if ("start" in answer.decode('ascii')):
                portOk = portName[num-1]
                if debug:
                    print("OK port is: ", portOk)
                else:
                    pass
            else:
                pass
    except:
        print("Something happend, don't know yet.")
           
    if portOk is not "none":            
        return portOk
    else:
        return portOk
        print("Port not found.")

def checkForValidAxis(axis):
    """ Checks input parameters for the movement
    Returns True or False. """
    allowed = ["X","Y","Z","E"]
    
    if debug:
        print(allowed)
        print("Axis is: ")
        print(axis)
    else:
        pass    
     
    if axis in allowed:
        return True
    else:
        return False

def checkForValidDirection(direction):
    """ Checks input parameters for the direction
    Returns True or False. """
    allowed = ["+","-"]
       
    if debug:
        print(allowed)
        print("Direction is: ")
        print(direction)
    else:
        pass    
    
    if direction in allowed:
        return True
    else:
        return False 
        
def move(axis, direction, value, speed):
    """ Moves given 'axis' in '+' or '-' 'direction' with 'value' and 'speed'
       
    """
    word = "none"
    moveAxis = "none"
    moveDirection = "none"
    
    if checkForValidAxis(axis):
        moveAxis = axis
    else:
        print("Axis definition Error. Please enter \"X\", \"Y\", \"Z\", \"E\".")
        
    if checkForValidDirection(direction):
        moveDirection = direction
    else:
        print("Direction definition Error. Please enter \"+\", \"-\".")
        
    #axis = str(axis)   # X, Y, Z, E
    direction = str(direction)  # '+' or '-'
    value = str(value)  # relative move 
    speed = str(speed)  # set speed of movement from 0 to 3000

    if moveAxis is not "none":
        word = "G1 " + moveAxis
    else:
        word = "none"
    
    if moveDirection is not "none":
        word = word + moveDirection
    else:
        word = "none"
    
    if word is not "none":
        word = word + value + " F" + speed + "\r\n"
        if debug:
            print(word)
        else: 
            pass
        
        return word.encode(encoding='ascii', errors='strict')
    else:
        pass

port = testPortsForRepRap()
baud = 115200

print("Found RepRap on port: ")
print(port)

if ("USB" in port):
    printer = Serial(port, baud, timeout = 5)
    print(printer.readline().strip().decode('ascii')) #without these readout nothing moves ??? strange but true
    word = 'G91\r\n'
    printer.write(word.encode('ascii'))
    
    if word is not "none":
        word = move('X', '+', 100, 400)
        print(word)
        try:
            printer.write(word)
        except:
            print("No word to write.")
    else:
        pass
    
else: 
    pass

if ("none" not in port):
    if printer.isOpen():
        printer.close()
        print("Now port is open: ")
        print(printer.isOpen())
else: 
    pass

print("That\'s all folks.")