import sys, os, glob
# we should consider adding pyserial into blender path and make tests !
# path to installed pySerial for python 3.2py
pyserialPath = "2.62/scripts/addons/blenderRepRap-addon/dist-packages/"
debug = False   # allow print in functions to be printed in console

def checkPathInBlender():
    """ Checks if PySerial already defined in sys.path()
    
        If already defined in path, 
        prints message in console, 
        else adds path to blender path.   
    
    """
    if (pyserialPath in sys.path):
        print("PySerial path already defined.")
    else:
        sys.path.append(pyserialPath)       # print("PySerial added to path.")
        
checkPathInBlender()    # adds PySerial path to blender

from serial import Serial

def scanForSerialPorts():
    """ Scans for available serial ports. 
    
        returns a list of port names 
    
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
    """ Test found available port from scanForSerialPorts() function 
    
        returns: "port name" or "none"
        on exception returns "Exception while trying to open port."    
    
    """
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
            printer = Serial(portName[num-1], 115200, timeout = 10)
         
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
        exception = "Exception while trying to open port."
        return exception
           
    if portOk is not "none":            
        return portOk
    else:
        return portOk
        print("Port not found.")
