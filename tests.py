from serial import Serial
import glob
#import os
#if os.name=="nt":
#    try:
#        import winreg
#    except:
#        pass

def scanserial():
        """scan for available ports. return a list of device names."""
        baselist=[]
#        if os.name=="nt":
#            try:
#                key=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,"HARDWARE\\DEVICEMAP\\SERIALCOMM")
#                i=0
#                while(1):
#                    baselist+=[winreg.EnumValue(key,i)[1]]
#                    i+=1
#            except:
#                pass

        return baselist+glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*') +glob.glob("/dev/tty.*")+glob.glob("/dev/cu.*")+glob.glob("/dev/rfcomm*")
    
def move(axis, direction, value, speed):
    axis = str(axis)    # X, Y, Z, E
    direction = str(direction)  # '+' or '-'
    value = str(value)  # relative move 
    speed = str(speed)  # set speed of movement from 0 to 3000

    word = 'G1 ' + axis + direction + value + ' F' + speed + '\r\n' 
    print( word.strip() )
    
    return word.encode('ascii')    


#START PROGRAM
port = scanserial()
print(port)
port_num = int(input())
try:
    printer = Serial(port[port_num - 1], 115200)

    
#try:
#printer.close()
#printer.open()
    print( printer.readline().strip().decode('ascii') )



    
    data = 'G91' + '\r\n'
    print( data.strip() )
    printer.write( data.encode('ascii') )
    print(printer.readline().strip().decode('ascii'))
    printer.write( move('Y', '+', 10, 500) )
    print(printer.readline().strip().decode('ascii'))

    printer.close()


except:
    print('ERROR!!!')
    
finally:
    print('Thats all folks.')