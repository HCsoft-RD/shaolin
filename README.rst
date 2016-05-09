*******
Shaolin
*******
================================================================================
Widget-based Interactive visualization sotware for the ipython jupyter notebook.
================================================================================

Shaolin allows for making complex plot just with a few clicks. It is possible to configure every parameter of diffrerent kinds of plots using ipython widgets and bokeh.

Its still in a really alpha version (not even uploaded to pypy). Can be installed using the setup script included in the code typing "python setup.py install" inside the project folder.

*************
Main features
*************

============
Scatter plot
============

This tool allows to make an interactive scatter plot from an arbitary pandas DataFrame.

================
Graph Calculator
================

It is possible to convert arbitrary timeseries into graphs with a few lines of code using its widget GUI.

==========
Graph Plot
==========

This is a widget intended to visualize the data inside a GraphCalculator.


*****************
Upcoming features
*****************

=======
Walkers
=======

It will be possible to extend the capabilities of the GraphCalculator for making interactive animated graphs in real time. This is really usefull for visualizing correlation matrix time series. 

===============
VPython support
===============
It will be possible to replicate the capabilities of the GraphPlot using VPython as a plotting engine. This will make very easy visualizing interactive 3D graphs in the notebook. 
