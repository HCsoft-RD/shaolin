=======
Shaolin
=======
***************************************************************************************************************
Framework for interactive widget-based dashboards programming. Feedback is really appreciated
***************************************************************************************************************

Shaolin (Structure Helper for dAshbOard LINking) is an ipywidgets based framework that allows to create interactive dashboards that can be linked with each other to build interactive applications.

Its still in a alpha alpha version, the beta version will be realeased before 17 july.

PLEASE HELP! I have not been able to upload it to pypy correctly, if someone told me whats wrong with my code it would be really appreciated.
Anyway, it can be installed using the setup script included in the code typing "python setup.py install" inside the project folder, or if you have the dependencies installed you can just download the folder and improt it on runtime to the python path. (The first cell in every example notebook does that.)

Dependencies:
- six.
- numpy.
- pandas.
- planarity.
- networkx.
- bokeh.
- seaborn.
- vpython (not yet, but really soon)


=============
Main features
=============

The documentation is located in the `examples <http://www.python.org/>`_ folder.
************
Scatter plot
************

This tool allows to make an interactive scatter plot from an arbitary pandas DataFrame.

****************
Graph Calculator
****************

It is possible to convert arbitrary timeseries into graphs with a few lines of code using its widget GUI.

**********
Graph Plot
**********
This is a widget intended to visualize the data inside a GraphCalculator.


========
Examples
========

Check online the examples on how to use Shaolin. All the widgets have been saved as images so you can take a look at them online. 

*****************
Parameter Widgets
*****************
A set of widgets that can be used as stand-alone classes for selecting function parameters or can be combined to make more complex interfaces. 


=================
Upcoming features
=================

*******
Walkers
*******
It will extend the capabilities of the GraphCalculator for making interactive animated graphs in real time. This is really usefull for visualizing correlation matrix time series. 

***************
VPython support
***************
It will be possible to replicate the capabilities of the GraphPlot using VPython as a plotting engine. This will make very easy visualizing interactive 3D graphs in the notebook. 


*************************
Full pandas compatibility
*************************
All the plots that support an arbitrary DataFrame will support both Panel and Panel4D data structures.

**********************
Custom colormap widget
**********************
It will be possible to create any arbitrary colormap using widgets for interacting with the Seaborn Colormap interface.

*********************
Seaborn compatibility
*********************
Compatibility for displaying seaborn plots will be added shortly. 

*****
MplD3
*****
Compatibility for mapping data to interactive matplotlib plots using MplD3.

