=======
Shaolin
=======
***************************************************************************************************************
Widget-based Interactive visualization sotware for the ipython jupyter notebook. Feedback is really appreciated
***************************************************************************************************************

Shaolin allows for making complex plot just with a few clicks. It is possible to configure every parameter of diffrerent kinds of plots using ipython widgets and bokeh.

Its still in a really alpha version (not even uploaded to pypy). Can be installed using the setup script included in the code typing "python setup.py install" inside the project folder.

It aims to be a usefull library in the

=============
Main features
=============

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

