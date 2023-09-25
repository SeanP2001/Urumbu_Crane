
import serial,sys,time,signal,keyboard
import PySimpleGUI as sg
import serial.tools.list_ports
import math
import random

forward = b'f'                                                # send 'f' to drive the motor forward/clockwise
reverse = b'r'                                                # send 'r' to drive the motor reverse/anti-clockwise

#------------------------------------------------------------------------------- A X I S -------------------------------------------------------------------------------  
class Axis:
    def __init__(self, pulleyDiameter, degreesPerStep, microsteps, position, lowerLimit, upperLimit, mmPerSec, doubled=False):
        self.pulleyDiameter = pulleyDiameter
        self.degreesPerStep = degreesPerStep
        self.microsteps = microsteps
        self.position = position
        self.lowerLimit = lowerLimit
        self.upperLimit = upperLimit
        self.mmPerSec = mmPerSec
        self.doubled = doubled
        
        self.calcStepsPerRev()
        self.calcMmPerStep()
        self.calcStepDelay()

    def calcStepsPerRev(self):
        degPerMicrostep = self.degreesPerStep / self.microsteps        
        self.stepsPerRevolution = 360 / degPerMicrostep
        
    def calcMmPerStep(self):
        pulleyCircumference = math.pi * self.pulleyDiameter
        self.mmPerStep = pulleyCircumference / self.stepsPerRevolution
        
        if self.doubled == True:
            self.mmPerStep = self.mmPerStep / 2
        
    def calcStepDelay(self):
        stepsPerSec = self.mmPerSec / self.mmPerStep
        self.stepDelay = 1 / stepsPerSec
        
    def connectMotor(self, port, baud):
        self.motor = serial.Serial(port, baud, timeout=0)     # connect to the specified serial port at the specified baud rate
        
    def setLimits(self, lowerLimit, upperLimit):
        self.lowerLimit = lowerLimit
        self.upperLimit = upperLimit
    
    def setPulleyDiameter(self, mmDiameter):
        self.pulleyDiameter = mmDiameter
        self.calcMmPerStep()
        self.calcStepDelay()
        
    def setSpeed(self, mmPerSec):
        self.mmPerSec = mmPerSec
        self.calcStepDelay()
    
    def setOrigin(self):
        self.position = 0                                     # Set the current axis position to 0
    
    def stepClockwise(self):
        self.motor.write(forward)                             # send an 'f' to the motor to rotate 1 step clockwise  
        self.position = self.position - self.mmPerStep        # decrease the position by 1 step (in mm)
    
    def stepAntiClockwise(self):
        self.motor.write(reverse)                             # send an 'r' to the motor to rotate 1 step anti-clockwise
        self.position = self.position + self.mmPerStep        # increase the position by 1 step (in mm)
    
    def adjustClockwise(self):
        self.motor.write(forward)                             # send an 'f' to the motor to rotate 1 step clockwise  
    
    def adjustAntiClockwise(self):
        self.motor.write(reverse)                             # send an 'r' to the motor to rotate 1 step anti-clockwise
        
    def isWithinLimit(self, end):
        if end == "lower":
            return self.position > self.lowerLimit
        elif end == "upper":
            return self.position < self.upperLimit 

x = Axis(23.05, 1.8, 8, 0, 0, 610, 200)                                # Axis (pulleyDiameter, degreesPerStep, microsteps, position, lowerLimit, upperLimit, mmPerSec, doubled=False)
y = Axis(40.85, 1.8, 8, 0, -698, 0, 200, doubled=True)


#---------------------------------------------------------------- Y   A X I S   C O M P E N S A T I O N ---------------------------------------------------------------- 
def calcYCompStepsPerXStep(x, y, yMovesBy, overXDist):
    yAxisMovement = yMovesBy / overXDist
    xStepsPerMm = 1 / x.mmPerStep
    yStepsPerMm = 1 / y.mmPerStep
    return ( yStepsPerMm * yAxisMovement ) / xStepsPerMm
        
overXDist = 625                                                        # When moving the crane this far (mm) in the x axis (without Y comp enabled)
yMovesBy = 309.5                                                       # The y axis moves by this distance (mm) 

yCompStepsPerXStep = calcYCompStepsPerXStep(x, y, yMovesBy, overXDist) # calculate how many steps the Y axis has to move for each X axis step to compensate and stay at the same height

yCompEnabled = True                                                    # enable Y axis compensation by default


#---------------------------------------------------------------------- W I N D O W   L A Y O U T ---------------------------------------------------------------------- 
minSpeed = 50                                                 # Minimum movement speed in mm/s
maxSpeed = 500                                                # Maximum movement speed in mm/s

ports = serial.tools.list_ports.comports()                    # get a list of all of the COM ports

sg.theme('Black')                                             # Set the colour theme for the application

connectMotors = [
    sg.Frame("Connect Motors",
    [
        [
            sg.Text("Axis  Port                           Baud")
        ],
        [
            sg.Text("  X "), 
            sg.Combo([port for port in sorted(ports)], s=(15,30), enable_events=True, readonly=True, key='-X_PORT-'),
            sg.Input(key='-X_BAUD-', s=(10,1)),
            sg.Button('Connect', key="-CONNECT_X-")
        ],
        [
            sg.Text("  Y "), 
            sg.Combo([port for port in sorted(ports)], s=(15,30), enable_events=True, readonly=True, key='-Y_PORT-'),
            sg.Input(key='-Y_BAUD-', s=(10,1)),
            sg.Button('Connect', key="-CONNECT_Y-")
        ]
    ], size=(350,140))
]

setLimits = [
    sg.Frame("Set Limits",
    [
        [
            sg.Text("Axis  Lower Limit(mm)    Upper Limit(mm)")
        ],
        [
            sg.Text("  X "), 
            sg.Input(key='-X_LOW_LIM-', s=(15,1), do_not_clear=False),
            sg.Input(key='-X_UP_LIM-', s=(15,1), do_not_clear=False),
            sg.Button('Set', key="-SET_X_LIM-")
        ],
        [
            sg.Text("  Y "), 
            sg.Input(key='-Y_LOW_LIM-', s=(15,1), do_not_clear=False),
            sg.Input(key='-Y_UP_LIM-', s=(15,1), do_not_clear=False),
            sg.Button('Set', key="-SET_Y_LIM-")
        ]
    ], size=(350,140))
]

dPad = [
    sg.Frame("Control",
    [
        [
            sg.RealtimeButton(sg.SYMBOL_UP, key='-UP-', size=(1,1))
        ],
        [
            sg.RealtimeButton(sg.SYMBOL_LEFT, key='-LEFT-', size=(1,1)),
            sg.Text(size=(3,1), justification='c', pad=(0,0)),
            sg.RealtimeButton(sg.SYMBOL_RIGHT, key='-RIGHT-', size=(1,1))
        ],
        [
            sg.RealtimeButton(sg.SYMBOL_DOWN, key='-DOWN-', size=(1,1))
        ]
    ], element_justification="c", size=(350,155))       
]

positions = [
    sg.Frame("Axis Positions", 
    [
        [
            sg.Text("X: "), sg.Text(x.position, s=(8,1), key="-X-"), sg.Text("mm"),
            sg.Button("Set X Origin", key='-SET_X_ORIG-', size=(10,1)),
            sg.Button("To X Origin", key='-TO_X_ORIG-', size=(10,1))
        ],
        [
            sg.Text("Y: "), sg.Text(y.position, s=(8,1), key="-Y-"), sg.Text("mm"),
            sg.Button("Set Y Origin", key='-SET_Y_ORIG-', size=(10,1)),
            sg.Button("To Y Origin", key='-TO_Y_ORIG-', size=(10,1))
        ]
    ], size=(350,125))
]

otherParameters = [
    sg.Frame("Other Parameters", 
    [
        [
            sg.Text("Movement Speed (mm/s)"),
            sg.Slider((minSpeed,maxSpeed), orientation='h', s=(18,15), key="-SPEED-", default_value=200, enable_events=True), 
            sg.Text("     "), 
            sg.Checkbox(' Y-Axis Compensation', key="-Y_COMP-", default=True, enable_events=True),
        ]
    ], size=(710,90))
]

layout = [
    [sg.T('Crane Controller', font='_ 14', justification='c', expand_x=True)],
    [
        sg.Col(
        [
            connectMotors,
            setLimits
        ], p=0, element_justification="c"),
     
        sg.Col(
        [
            dPad, 
            positions
        ], p=0, element_justification="c"),
    ],
    [otherParameters]
]

window = sg.Window('Crane Controller', layout, element_justification="c", icon=r"./icons/CraneIcon.png", use_default_focus=False)  # Build the Application Window


#-------------------------------------------------------------------- M A I N   E V E N T   L O O P --------------------------------------------------------------------
while True:
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED:              # if the user closes the program                                     
        break                                  # break the loop

#--------------------------------------------------------------------- C O N N E C T   M O T O R S ---------------------------------------------------------------------   
    if event == "-CONNECT_X-":                                 # If the user presses the button to connect the x motor
        xPort = str(values['-X_PORT-'])                        # Convert input to a string
        xPort = xPort[0:(xPort.index("-")-1)]                  # Get the directory of the port selected (remove the device name)
        
        xBaudrate = str(values['-X_BAUD-'])                    # Convert the baudrate to a string
        
        x.connectMotor(xPort, xBaudrate)                       # Connect to the specified serial port at the specified baud rate
        
        window['-CONNECT_X-'].update(button_color='green')     # and change the connect button colour to green
        
    if event == "-CONNECT_Y-":                                 # If the user presses the button to connect the x motor
        yPort = str(values['-Y_PORT-'])                        # Convert input to a string
        yPort = yPort[0:(yPort.index("-")-1)]                  # Get the directory of the port selected (remove the device name)
        
        yBaudrate = str(values['-Y_BAUD-'])                    # Convert the baudrate to a string
        
        y.connectMotor(yPort, yBaudrate)                       # Connect to the specified serial port at the specified baud rate
        
        window['-CONNECT_Y-'].update(button_color='green')     # and change the connect button colour to green
    
    
#------------------------------------------------------------------------- S E T   L I M I T S ------------------------------------------------------------------------- 
    if event == "-SET_X_LIM-":                                                  # If the user presses the set X limit button
        x.setLimits(float(values['-X_LOW_LIM-']), float(values['-X_UP_LIM-']))  # set the X axis lower and upper limits to the specified values
     
   
    if event == "-SET_Y_LIM-":                                                  # If the user presses the set Y limit button
        x.setLimits(float(values['-Y_LOW_LIM-']), float(values['-Y_UP_LIM-']))  # set the Y axis lower and upper limits to the specified values

        
         
#-------------------------------------------------------------------------- S E T   S P E E D -------------------------------------------------------------------------- 
    if event == '-SPEED-':            # If the speed slider is updated
        mmPerSec = values['-SPEED-']  # Read the mm/s value from the slider

        x.setSpeed(mmPerSec)          # Set the speed of the X axis               
        y.setSpeed(mmPerSec)          # Set the speed of the Y axis   
    

#---------------------------------------------------------------- Y   A X I S   C O M P E N S A T I O N ---------------------------------------------------------------- 
    if event == "-Y_COMP-":                   # If the Y-Axis Compensation tickbox is updated
        yCompEnabled = values["-Y_COMP-"]     # Enable or disable the Y-Axis Compensation according to the tickbox 
    

#--------------------------------------------------------------------- B U T T O N   C O N T R O L ---------------------------------------------------------------------   
    if event == "-UP-" and y.isWithinLimit("upper"):       # If the up button in the UI is pressed and the axis is within its limits
        y.stepAntiClockwise()                              # move the Y axis up 
        time.sleep(y.stepDelay)                            # delay to control the speed of the motor
        
        
    if event == "-DOWN-" and y.isWithinLimit("lower"):     # If the down button in the UI is pressed and the axis is within its limits
        y.stepClockwise()                                  # move the Y axis down
        time.sleep(y.stepDelay)                            # delay to control the speed of the motor
        
        
    if event == "-RIGHT-" and x.isWithinLimit("upper"):    # If the right button in the UI is pressed and the axis is within its limits
        x.stepAntiClockwise()                              # move the X axis right
        
        if yCompEnabled:                                   # if Y axis compensation is enabled
            if random.random() < yCompStepsPerXStep:       # for every (~0.55) X steps 
                y.adjustClockwise()                        # Move the Y axis 1 step down (to keep the hook at the same level)                               
        
        time.sleep(x.stepDelay)                            # delay to control the speed of the motor
        
        
    if event == "-LEFT-" and x.isWithinLimit("lower"):     # If the left button in the UI is pressed and the axis is within its limits
        x.stepClockwise()                                  # move the X axis left
        
        if yCompEnabled:                                   # if Y axis compensation is enabled
            if random.random() < yCompStepsPerXStep:       # for every (~0.55) X steps 
                y.adjustAntiClockwise()                    # Move the Y axis 1 step up (to keep the hook at the same level)  
                
        time.sleep(x.stepDelay)                            # delay to control the speed of the motor
    
    
    window['-X-'].update(round(x.position, 2))             # Update the X position value displayed in the UI
    window['-Y-'].update(round(y.position, 2))             # Update the Y position value displayed in the UI

    '''
#------------------------------------------------------------------- K E Y B O A R D   C O N T R O L -------------------------------------------------------------------   
    if keyboard.is_pressed('up') and y.isWithinLimits():    # If the up arrow key on the keyboard is pressed and the axis is within its limits
        y.stepAntiClockwise()                               # move the Y axis up 
        time.sleep(y.stepDelay)                             # delay to control the speed of the motor
  
        
    if keyboard.is_pressed('down') and y.isWithinLimits():  # If the down arrow key on the keyboard is pressed and the axis is within its limits
        y.stepClockwise()                                   # move the Y axis down
        time.sleep(y.stepDelay)                             # delay to control the speed of the motor
 
        
    if keyboard.is_pressed('right') and x.isWithinLimits(): # If the right arrow key on the keyboard is pressed and the axis is within its limits
        x.stepAntiClockwise()                               # move the X axis right
        
        if yCompEnabled:                                    # if Y axis compensation is enabled
            if random.random() < yCompStepsPerXStep:        # for every (~0.55) X steps 
                y.adjustClockwise()                         # Move the Y axis 1 step down (to keep the hook at the same level)                               
        
        time.sleep(x.stepDelay)                             # delay to control the speed of the motor
  
        
    if keyboard.is_pressed('left') and x.isWithinLimits():  # If the left arrow key on the keyboard is pressed and the axis is within its limits
        x.stepClockwise()                                   # move the X axis left
        
        if yCompEnabled:                                    # if Y axis compensation is enabled
            if random.random() < 0.550717266:               # for every (~0.55) X steps 
                y.adjustAntiClockwise()                     # Move the Y axis 1 step up (to keep the hook at the same level)  
                
        time.sleep(x.stepDelay)                             # delay to control the speed of the motor
  
    
    window['-X-'].update(round(x.position, 2))              # Update the X position value displayed in the UI
    window['-Y-'].update(round(y.position, 2))              # Update the Y position value displayed in the UI

    '''
#------------------------------------------------------------------------ S E T   O R I G I N S ------------------------------------------------------------------------      
    if event == "-SET_X_ORIG-":                             # If the user presses the set X origin button
        x.setOrigin()                                       # Set the X axis origin to 0
        window['-X-'].update(round(x.position, 2))          # and update the X position value displayed in the UI               
              
    if event == "-SET_Y_ORIG-":                             # If the user presses the set Y origin button
        y.setOrigin()                                       # Set the Y axis origin to 0
        window['-Y-'].update(round(y.position, 2))          # and update the Y position value displayed in the UI  
        
       
#-------------------------------------------------------------------- M O V E   T O   O R I G I N S --------------------------------------------------------------------       
    if event == "-TO_X_ORIG-":                              # If the user presses the 'To X Origin' button
        while x.isWithinLimit("lower"):                     # continue until the crane has reached the left side
            x.stepClockwise()                               # move the X axis left
        
            if yCompEnabled:                                # if Y axis compensation is enabled
                if random.random() < yCompStepsPerXStep:    # for every (~0.55) X steps 
                    y.adjustAntiClockwise()                 # Move the Y axis 1 step up (to keep the hook at the same level) 
                    
            window['-X-'].update(round(x.position, 2))      # and update the X position value displayed in the UI
                    
            time.sleep(x.stepDelay)                         # delay to control the speed of the motor

         
          
    if event == "-TO_Y_ORIG-":                              # If the user presses the 'To Y Origin' button
        while y.isWithinLimit("upper"):                     # continue until the crane has reached the top
            y.stepAntiClockwise()                           # move the Y axis up 
            
            window['-Y-'].update(round(y.position, 2))      # and update the Y position value displayed in the UI
            
            time.sleep(y.stepDelay)                         # delay to control the speed of the motor
                       
   
# If the user has quit the program, the main loop breaks and this code will execute    
    
window.close()         # close the window

