from validSerialPorts import testPortsForRepRap, Serial

debug = False   # print all messages in console 

class RepRap(): # not working yet should find out how classes are defined
    """ This is the main class, where all the action performs
    
        connect()     -    connect port to reprap printer
        disconnect()  -    disconnect port from reprap printer
        move('AXIS','DIRECTION','MOVE WITH GIVEN VALUE','SPEED') - make movement in reprap
        not implemented yet     --    checkExtruderTemp() - returns extruder temperature in degrees
        not implemented yet     --    checkTableTemp()    - returns table temperature in degrees
        not implemented yet     --    sendGCodeFile()     - reads GCode file and sends the commands to the printer.
    
    """
    def checkForValidAxis(self, axis):
        """ Checks input parameters for the movement
            
            Returns: True or False. 
            
            """
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

    def checkForValidDirection(self, direction):
        """ Checks input parameters for the direction
        
        Returns: True or False. 
        
        """
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

    def connect(self, baud, timeout):
        """ Connects to RepRap printer
        
            returns: pyserial object with connected printer
        
        """
        port = testPortsForRepRap()
        if port is not "Exception while trying to open port.":
            if port is not "none":
                printer = Serial( port, baud, timeout)
                return printer
            else:
                return "none"
        else:
            return "none" 
    
    def disconnect(self, reprap):
        try:
            reprap.disconnect()
        except:
            return "Exception while trying to disconnect the printer."
        
    def move(self, axis, direction, value, speed):
        """ Moves given 'axis' in '+' or '-' 'direction' with 'value' and 'speed'
       
        """
        word = "none"
        moveAxis = "none"
        moveDirection = "none"
    
        if self.checkForValidAxis(axis):
            moveAxis = axis
        else:
            print("Axis definition Error. Please enter \"X\", \"Y\", \"Z\", \"E\".")
        
        if self.checkForValidDirection(direction):
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
    
test = RepRap
test.connect(test, 115200, 15)
test.move(test, "X", "+", 5, 600)
test.disconnect(test, test)