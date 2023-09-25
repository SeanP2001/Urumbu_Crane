# Urumbu Crane

## Table of Contents <!-- omit from toc -->

- [Introduction](#introduction)
- [Design](#design)
- [Manufacturing](#manufacturing)
  - [3D Printing](#3d-printing)
  - [CNC Routing](#cnc-routing)
  - [Laser Cutting](#laser-cutting)
  - [Assembling](#assembling)
- [Demonstration](#demonstration)
- [Conclusion](#conclusion)

## Introduction

## Design

|  <img src="./Images/CAD/Crane_Drive_Section_V1.1.png"> | <img src="./Images/CAD/Crane_Carriage_V1.1.png"> |
| --- | --- |

<img src="./Images/CAD/Crane_V1.1.png" width=100%>

|  <img src="./Images/CAD/Crane_Brace_V1.1.PNG"> | <img src="./Images/CAD/Crane_Hook_V1.1.PNG"> |
| --- | --- |

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

## Demonstration

## Conclusion