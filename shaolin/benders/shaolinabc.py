# -*- coding: utf-8 -*-
"""Shaolin Abstract Class definition"""
import abc
class Shaolin(object):
    """Shaolin stands for Structured Helper for Animations and Object LINking"""
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.init_free_params_sel()
        self.init_mapped_params_sel()
        self.init_mappers()
        self.init_tooltips()
        self.select_tooltip_data()
        self.update_translators()
        self.update_source_dfs()
        return

    @abc.abstractmethod
    def init_free_params_sel(self):
        """Handle plot free params selectors init. A free param means a
        plot parameter that is not mapped to data
        """
        pass
    @abc.abstractmethod
    def init_mapped_params_sel(self):
        """Handle plot parameter selectors init"""
        pass
    @abc.abstractmethod
    def init_mappers(self):
        """Handle mappers init"""
        pass
    @abc.abstractmethod
    def init_tooltips(self):
        """Handle tooltips init"""
        pass
    @abc.abstractmethod
    def init_plot(self):
        """Handle plot init"""
        pass
    @abc.abstractmethod
    def select_tooltip_data(self):
        """tooltip data selection logic"""
        pass
    @abc.abstractmethod
    def update_translators(self):
        """translator logic"""
        pass
    @abc.abstractmethod
    def update_source_dfs(self):
        """Datasources for plots managing"""
        pass
    @abc.abstractmethod
    def update_active(self, change):
        """A fuction for updating its active dictionary"""
        pass
    @abc.abstractmethod
    def customize_children_widgets(self):
        """Adapt children widgets to a combined display"""
        pass
    @abc.abstractmethod
    def init_widget(self):
        """Shaolin widget init. This is mainly for defining the widget
        the user will interact with
        """
        pass
    @abc.abstractmethod
    def create_tooltip(self):
        """A function for creating a tooltip suitable for the plot. This means
        that by default all kinds of plots should try to include tooltips
        """
        pass
    @abc.abstractmethod
    def push_data(self):
        """A function to push the content of the source DataFrame
        to a speciffic plot sourceç
        """
        pass
    @abc.abstractmethod
    def update(self):
        """Set up all the combined elements needed for the plot"""
        pass
