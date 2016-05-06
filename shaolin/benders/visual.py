# -*- coding: utf-8 -*-
"""This is the module in charg of convertion arbitrary data to processed
visual attributes for a plot.
"""
from matplotlib import cm
from matplotlib import colors as clrs
import pandas as pd
import numpy as np
from .context import sww#Shaolin Widgets for Wranglers
class MarkerTranslator(object):
    """This Class is used to map each parameter of an arbitrary
            DataFrame to the values needed for bokeh to format a scatter plot
            Parameters
            ----------
            df: pd.DataFrame
                Pandas DataFrame to plot

            active: dict
                mapping which columns will not hold the default value

            free_params: dict
                A dictionary mapping each attribute to its default values

            cat_cols: list
                Names of the columns containing categorical values

            names: list
                column names of the parameter dataframe used to contain the mapped info
    """
    def __init__(self, df,
                 active,
                 free_params,
                 mapped_params,
                 scaler_params,
                 update=False
                ):

        self.mapped_params = mapped_params

        self.free_params = free_params
        self.active = active
        self.data = df.copy()
        self.visual = self.default_visual_df()
        self.scales = sww.ScaleParams(scaler_params)
        #self.cat_cols = cat_cols#TODO improve categorical filtering
        self.data_to_plot()
        self.widget = self.scales.widget

    @staticmethod
    def is_categorical_series(data):
        """true if data is a categorical series"""
        return  isinstance(data[0], str)
        #return

    def external_update(self, scaler_params):
        """trigger function for calculating values"""
        self.scales.params = scaler_params
        self.data_to_plot()

    def data_to_plot(self):
        """Maps active columns to its non default values"""
        for col in self.mapped_params:
            if self.active[col]:
                if self.is_categorical_series(self.data.loc[:, col]):
                    self.data.loc[:, col] = self.categorical_to_num(self.data.loc[:, col].copy())
                self.visual.loc[:, col] = self.df_data_to_plot(self.data, col)


    def default_visual_df(self):
        """Creates a DataFrame conaining the default values of every parameter to plot"""
        df = pd.DataFrame(index=self.data.index, columns=self.mapped_params)
        for col in self.free_params:
            df[col] = self.free_params[col]
        return df

    def atribute_to_color(self, array, cmap_name='spectral'):
        """This function map any series of data to the selected matplotlib colormap values"""
        if isinstance(array[0], str):
            array = np.array(self.categorical_to_num(data=array))
        Ma = array.max()
        mi = array.min()
        if Ma != mi:
            new = (array-mi)/(Ma-mi)
        else:
            new = array
        norm = [int(x) for x in new*256]
        colormap = getattr(cm, cmap_name)
        rgb_vals = [colormap(x) for x in norm]
        colorarray = [clrs.rgb2hex(rgb).upper() for rgb in rgb_vals]
        return colorarray

    @staticmethod
    def categorical_to_num(data):
        """Converts categorical data into an array of ints"""
        cats = np.unique(data)
        imap = {}
        for i, cat in enumerate(cats):
            imap[cat] = i
        fun = lambda x: imap[x]
        return list(map(fun, data))


    def df_data_to_plot(self, df, target):
        """Custom mapping for each of the plot params"""
        data = df[target]
        Ma = data.max()
        mi = data.min()
        if target == 'line_color':
            return self.atribute_to_color(data.values,
                                          cmap_name=self.free_params['line_colormap'])

        if target == 'fill_color':
            return self.atribute_to_color(data.values,
                                          cmap_name=self.free_params['fill_colormap'])

        if target == 'color':
            return self.atribute_to_color(data.values,
                                          cmap_name=self.free_params['colormap'])

        if target == 'size':
            if Ma == mi:
                return 50
            score = ((data-mi)/(Ma-mi))#*2.0-1
            scale_h = self.scales.params['size_max'] - self.scales.params['size_min']
            scale_l = self.scales.params['size_min']
            return scale_h * score.values + scale_l

        if target in ['fill_alpha', 'alpha']:
            if mi == Ma:
                return 0.7
            #score = ((data-mi)/(Ma-mi))*(1-min_a)+min_a
            score = ((data-mi)/(Ma-mi))#*2.0-1
            scale_h = self.scales.params['fill_alpha_max'] - self.scales.params['fill_alpha_min']
            scale_l = self.scales.params['fill_alpha_min']
            return scale_h * score.values + scale_l

        if target == 'line_alpha':
            if mi == Ma:
                return 0.7
            #score = ((data-mi)/(Ma-mi))*(1-min_a)+min_a
            score = ((data-mi)/(Ma-mi))#*2.0-1
            scale_h = self.scales.params['line_alpha_max'] - self.scales.params['line_alpha_min']
            scale_l = self.scales.params['line_alpha_min']
            return scale_h * score.values + scale_l

        if target == 'line_width':
            if mi == Ma:
                return 5
            score = ((data-mi)/(Ma-mi))
            scale_h = self.scales.params['line_width_max'] - self.scales.params['line_width_min']
            scale_l = self.scales.params['line_width_min']
            return scale_h * score.values + scale_l
        else:
            return data.values
