# Urumbu Crane

## Table of Contents <!-- omit from toc -->

- [Introduction](#introduction)
- [Design](#design)
  - [Y-Axis Drum](#y-axis-drum)
  - [X-Axis Drive Section](#x-axis-drive-section)
  - [X-Axis Carriage](#x-axis-carriage)
  - [Tail Pulley](#tail-pulley)
  - [Hook](#hook)
  - [End Plates](#end-plates)
  - [Frame](#frame)
- [Manufacturing](#manufacturing)
  - [3D Printing](#3d-printing)
  - [CNC Routing](#cnc-routing)
  - [Laser Cutting](#laser-cutting)
  - [Assembling](#assembling)
- [Software](#software)
- [Build Video and Demonstration](#build-video-and-demonstration)
- [Conclusion](#conclusion)

## Introduction

I designed a set of Urumbu USB stepper motor modules for students in the FabLAB to use for rapidly prototype motion systems. The files to create these modules can be found in my ["Urumbu_USB_Stepper_Motor" repostiory](https://github.com/SeanP2001/Urumbu_USB_Stepper_Motor). 

I designed and built this crane to test and demonstrate the use of the modules. This repository serves as documentation of a project which students can reference when learning how to use the modules.

## Design

<p align="center">
  <img src="./Images/CAD/Crane_V1.1.png">
</p>

### Y-Axis Drum

<p align="center">
  <img src="./Images/CAD/Y-Axis_Drum.png" width=50%> 
</p>

Design Features:
- Two holes to tie the fishing line to.
- Reels in the fishing line.
- Friction fits onto NEMA 14 motor D-shaft.

### X-Axis Drive Section

|  <img src="./Images/CAD/Crane_Drive_Section_V1.1.png"> | <img src="./Images/CAD/Pulley_Grooves.png"> |
| --- | --- |

Design Features:
- Mounts the NEMA 14 motor to the aluminium extrusion.
- Secured to the aluminium extrusion using two M5 tee-nuts.
- Tensioner pulley increases friction between the motor pulley and fishing line, preventing it from slipping.
- Tensioner pulley has two bearings to help the fishing line move smoothly.

### X-Axis Carriage

<p align="center">
  <img src="./Images/CAD/Crane_Carriage_V1.1.png" width=50%> 
</p>

Design Features:
- Three M5 bolts secure spacers and Delrin V-wheels 
- The V-wheels slot into the V-slot linear rail, allowing the carriage to glide smoothly along the axis.
- Two holes for tying the x-axis fishing line to.
- A central pulley, to allow the fishing line to run over it and down to the hook.
- Two holes for the y-axis fishing line to be tied to after going through the hook. (There are two symmetrical holes to allow for the fishing line to come from the left or right side of the crane)

### Tail Pulley

|  <img src="./Images/CAD/Crane_Idler_Pulley.png"> | <img src="./Images/CAD/Tail_Pulley_Angle.png"> |
| --- | --- |

Design Features:
- 3D printed bracket to secure the pulley to the aluminium extrusion at an angle. The angle matches the angle of the fishing line, allowing it to travel in a straight line from the motor pulley.
- Mounted to the extrusion with two M5 tee-nuts.

### Hook

<p align="center">
  <img src="./Images/CAD/Crane_Hook_V1.1.PNG" width=50%> 
</p>

Design Features:
- Made from 5 layers of laser cut 3mm plywood glued together.
- Includes a pulley for the fishing line to go through and back up to the carriage. The doubled-up line prevents the hook from easily spinning.

### End Plates

<p align="center">
  <img src="./Images/CAD/Crane_End_Plate_V1.1.png" width=50%> 
</p>

Design Features:
- Two central holes to secure the plates to the tapped holes in the aluminium extrusion using M5 bolts.
- Four corner holes to secure the plates to the MDF frame with self-tapping wood screws.  

### Frame

<p align="center">
  <img src="./Images/CAD/Crane_Brace_V1.1.PNG" width=50%> 
</p>

Design Features:
- Slot together with mortise and temon joints (dogboned to take into account the radius of the end mill)
- Symmetrical to allow the Y-axis motor to be mounted on either the left or right side.

## Manufacturing

### 3D Printing

I created a new Fusion360 file and imported the 3D printed bodies from the main Fusion360 file. I then laid out all of the parts flat on the XZ plane before exporting the STL file.

I opened the STL file in Cura and sliced the file for my 3D printer. I saved the Gcode to the microSD card to transfer the file to the printer.

<p align="center">
  <img src="./Images/CAM/3D_Printing/Cura.png" width = 70%>
</p>

I printed the parts using black PLA filament.

<p align="center">
  <img src="./Images/CAM/3D_Printing/3D_Printed_Parts.jpg" width = 70%>
</p>

### CNC Routing

The MDF parts were imported into two new Fusion 360 designs, laid flat on the XZ plane and arranged to fit 8’x4’ sheets of MDF. Using the "Manufacturing" workspace, a new "Setup" was created, defining the type of CNC operation and the material properties. The "2D Pocket" and "2D Contour" operations were used to create the toolpaths.

|  <img src="./Images/CAM/CNC/CNC_Toolpath_1.png"> | <img src="./Images/CAM/CNC/CNC_Toolpath_2.png"> |
| --- | --- |

The toolpaths were exported as `.nc` files and saved to a USB stick. The USB stick was plugged into the large format CNC machine controller. The MDF was placed on the CNC, the vacuum table and extraction were turned on, the origins were set and the files were selected to cut.

|  <img src="./Images/CAM/CNC/Finished_Sides.jpg"> | <img src="./Images/CAM/CNC/Finished_Base.jpg"> |
| --- | --- |

### Laser Cutting

Using the Fusion 360 app "Shaper", I created SVG images for all the profiles that needed laser cutting.

<p align="center">
  <img src="./Images/CAM/Laser_Cutting/Using_Shaper.png" width = 70%>
</p>

This created SVG images of the end plate, carriage, outer hook, inner hook and motor mount profiles.

These profiles were imported into Inkscape and altered to have a red outline with no fill. The profiles were arranged to best use the space.

<p align="center">
  <img src="./Images/CAM/Laser_Cutting/Laser_Cut_Parts_Layout.png" width = 70%>
</p>


In CorelDRAW, all lines were set to hairline thickness, and the file was sent to "print" on the Trotec Speedy400 laser-cutter. This opened Trotec JobControl. 

The 3mm Plywood was placed on the bed of the laser cutter, the laser height and position were set, and the lid was closed. In JobControl, the file was dragged to the position of the laser and set to cut.

<p align="center">
  <img src="./Images/CAM/Laser_Cutting/Laser_Cut_Parts.jpg" width = 70%>
</p>

### Assembling

- Slotted the frame together.
- Tapped M5 threads into 80x20x1000mm aluminium extrusion ends.
- Bolted the end plates to the ends of the aluminium extrusion.
- Screwed the end plates to the frame.

|  <img src="./Images/Build/Crane_Side_Brace.jpg"> | <img src="./Images/Build/End_Plate.jpg"> |
| --- | --- |
  
- Glued the hook profiles together.
  
<p align="center">
  <img src="./Images/Build/Crane_Hook_Glueing.jpg" width = 70%>
</p>

- Fixed both motors in place using M3 bolts.
- Covered the backs of both motors with electrical tape to prevent short circuits.
- Bolted Urumbu modules to the back of the motors using M3 bolts and several nylon washers.
- Plugged the stepper motor cables into the headers on the Urumbu boards.

|  <img src="./Images/Build/X_Motor.jpg"> | <img src="./Images/Build/Y_Motor.jpg"> |
| --- | --- |

- Press fitted the X-axis motor pulley and Y-axis drums onto the motor shafts.
- Secured the X-axis motor mount, tail pulley bracket and other parts to the aluminium extrusion using M5 bolts and tee-nuts.

|  <img src="./Images/Build/X_Drive_Section.jpg"> | <img src="./Images/Build/Tail_Pulley.jpg"> |
| --- | --- |

- Secured the carriage pulley to the carriage using a spacer with an M5 nut and bolt.
- Bolted the top two Delrin V-wheels to the carriage with spacers along with M5 nuts and bolts.
- Placed the carriage on the extrusion with the top V-wheels slotted into the top V-slot.
- Held the third V-wheel in place underneath the extrusion and secured it to the carriage.

|  <img src="./Images/Build/Carriage_Front.jpg"> | <img src="./Images/Build/Carriage_Back.jpg"> |
| --- | --- |

- Tied the fishing line to one side of the carriage.
- Wrapped the line around the X-axis motor pulley and tensioner pulley in a figure-eight.
- Looped the line around the tail pulley.
- Tied the line to the other side of the carriage.

<p align="center">
  <img src="./Images/Build/Drive_Section_Top.jpg" width = 70%>
</p>


- Tied a second piece of fishing line to the bottom of the carriage.
- Threaded the line through the hook pulley, over the carriage pulley and the second pulley.
- Tied the line to the Y-axis drum with enough slack for the hook to touch the floor at the far end of the X-axis travel.
- Wound the line up on the Y-axis drum.

<p align="center">
  <img src="./Images/Build/Y_Drum.jpg" width = 70%>
</p>

The complete crane was assembled in less than three hours.

<p align="center">
  <img src="./Images/Build/Crane_V1.1_Assembled.jpg">
</p>

## Software

I programmed a graphical controller program in Python using the PySimpleGUI library. The graphical interface allows users to select the USB port for each motor and connect to them. They can set upper and lower limits for each axis, change the movement speed and control the crane.

<p align="center">
  <img src="./Images/CraneControllerGUI.png">
</p>

## Build Video and Demonstration

[<img src="./Images/Youtube_Video_Screenshot.png" />](https://www.youtube.com/watch?v=1Sd0MmUDr9s&ab_channel=SeanPrice)

## Conclusion

The modules were quick and easy to use to prototype a working motion system. They were reliable, which made troubleshooting my code much easier. One area of improvement is that inefficiencies in the code caused the crane to move slowly at times. Using multiple CPU cores would allow multiple sections of code to run simultaneously, allowing the crane to run at full speed.