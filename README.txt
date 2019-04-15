---------------------------------------
------ A 3D Editor --------------------
------------- by ----------------------
----------- Oktay Comu ----------------
---------------------------------------

---------------------------------------
--- Project Description
---------------------------------------
	This project is a python program designed to serve as a simplistic 3D editing tool for .obj files. It only uses
one of the built-in Python module, Tkinter. The 3D rendering is accomplished through the usage of three dimensional vector
operations. Arbitrary vertices that are defined as 3D vectors within the .obj file are converted into two dimensional x,y
coordinates using the dot product property of 3D vectors and then scaled according to their distance form the camera in order
to create the illusion of perpective and depth. Following that, polygons are drawn in between these vertices according to the 
face definitions inside the .obj file. 
	The editor comes with a customizable viewport. The user has the option to view the given .obj file in X-ray mode which 
allows the user to see behind faces that would normally block the view of faces behind. There is also a togglable grid option.
This option displays a 20x20 grid on y=0 which serves as a reference point for any editing the user might do. Every cell on
the grid corresponds to one unit inside the .obj file.
	Editing .obj is very simple and easy to grasp. The user can open any .obj file, anywhere on his drive, and start editing
immediately. Hovering over any vertex displays a small red square as an indicator to show that the vertex is selectable and
clicking on the vertex turns the square into yellow indicating that it has been selected. The user can click on the yellow 
square any time in order to unselect the vertex. There are two ways of editing a vertex. You can set the exact values for the 
coordinates of the vertex using the entry boxes in the GUI bar below the window or you can use the scrollwheel of your mouse
while hovering over the entry boxes to make faster but more crude adjustments.