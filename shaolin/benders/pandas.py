# -*- coding: utf-8 -*-
"""Module in charge of linking graphs to plots"""

#from sh.widgets.generic import SelectMultiple, MarkerFreeParams, MarkerMappedParams



#import numpy as np
import ipywidgets as widgets
from IPython.core.display import display

from bokeh.models import HoverTool

import bokeh.models.sources as bks

from bokeh.io import output_notebook, push_notebook

from bokeh.plotting import figure, show
import pandas as pd

from .context import swg#KungFu Widgets
from .context import sww#Kungo Widgets for wranlgers
from .visual import MarkerTranslator
from .shaolinabc import Shaolin

#output_server('scatter')
output_notebook()



class DataFrameScatter(Shaolin):
    """This class enables us to map an arbitary pandas DataFrame to aplot"""
    MARKER_PARAMS = ['x', 'y',
                     'line_color',
                     'fill_color',
                     'fill_alpha',
                     'line_alpha',
                     'size',
                     'line_width'
                    ]
    #This is a semi constant. The values can change but the keys are fixed.
    #This values are ment for the plot default values when a param is not fixed
    FREE_PARAMS = {'fill_color':'blue',
                   'fill_alpha': 0.8,
                   'size':10,
                   'fill_colormap':'copper',
                   'line_colormap':'copper',
                   'marker':'circle',
                   'line_width':1,
                   'line_color':'black',
                   'line_alpha':1
                  }

    def __init__(self, df,
                 marker_params=None,
                 free_params=None,
                 default_map=None,
                ):
        if marker_params is None:
            self.marker_params = self.default_marker_params()
        else:
            self.marker_params = marker_params

        if free_params is None:
            self.free_params = self.default_free_params()
        else:
            self.free_params = free_params

        self.default_map = default_map
                            #Im not sure if wrangling with self.df
        self.df = df.copy() #affects the original df from outside the class
        self.df = self.metadata_to_df(dataframe=self.df)
        self.active_params = dict([(x, False) for x in self.marker_params])
        self.active_params['x'] = True
        self.active_params['y'] = True
        self.x_label = None
        self.y_label = None
        self.scaler = sww.ScaleParams()
        self.scaler.external_observe(self.trigger_update)
        super(DataFrameScatter, self).__init__()
        self.init_widget()
        self.customize_children_widgets()
        self.init_plot()


    @property
    def widget(self):
        """Dispaly full GUI"""
        return display(self.controls, show(self.plot))

    @classmethod
    def default_marker_params(cls):
        """Returns the ingredient list."""
        return cls.MARKER_PARAMS
    @classmethod
    def default_free_params(cls):
        """Returns the ingredient list."""
        return cls.FREE_PARAMS

    @staticmethod
    def metadata_to_df(dataframe):
        """Add names to the index and columns and add the index as a column"""
        if dataframe.index.name is None:
            dataframe.index.name = 'columns'
        if dataframe.index.name is None:
            dataframe.index.name = 'index'
        if not dataframe.index.name in dataframe.columns:
            dataframe[dataframe.index.name] = dataframe.reset_index()[dataframe.index.name].values
        return dataframe

    def init_widget(self):
        """Shaolin widget init. This is mainly for defining the widget
        the user will interact with
        """
        self._plotbox = widgets.VBox(children=[self.marker_free_sel.widget,
                                               self.tooltip.widget,
                                              ]
                                    )
        self.controls = widgets.HBox(children=[self.marker_map_sel.widget,
                                               self._plotbox, self.scaler.widget])

    def init_free_params_sel(self):
        """Handle plot free params selectors init. A free param means a
        plot parameter that is not mapped to data
        """
        self.marker_free_sel = swg.MarkerFreeParams(self.free_params, title=('Select a column'))
        for param in self.free_params:
            getattr(self.marker_free_sel, param).observe(self.trigger_update, names='value')

    def trigger_update(self, _):
        """wrapper for updating from an event"""
        self.update()

    def init_mapped_params_sel(self):
        """Handle plot parameter selectors init"""
        self.marker_map_sel = swg.MarkerMappedParams(df=self.df,
                                                     default_map=self.default_map,
                                                     params=self.marker_params)
        for param in self.marker_params:
            marker_widget = getattr(self.marker_map_sel, param)
            marker_widget.target.observe(self.trigger_update, names='value')
            marker_widget.active.observe(self.update_active, names='value')

    def init_mappers(self):
        """The mapper is a Dataframe use for preprocessing the marker parameters,
         its colums are the mapped parameters and its index its the same as the original data
        """
        self.mapper = pd.DataFrame(index=self.df.index, columns=self.marker_params)


    def init_tooltips(self):
        """This tooltip allows us to map any colum to the """
        self.tooltip = swg.SelectMultiple(list(self.df.columns.values), title='Tooltip data')
        self.tooltip.target.observe(self.trigger_update_tooltip, names='value')

    def trigger_update_tooltip(self, _):
        """This updates just the tooltip info without reselecting all the data"""
        self.update_tooltips()
        self.push_data()

    def init_plot(self):
        """Handle plot init"""
        self.bokeh_source = bks.ColumnDataSource(dict([(x, self.source[x].values)\
                                                 for x in self.source.columns]))
        tooltip = self.create_tooltip()

        self.plot = figure(title="Scatter plot", width=600, height=600, webgl=False,
                           tools="pan,wheel_zoom,box_zoom,reset,resize,crosshair",)
        self.plot.xaxis.axis_label = self.x_label
        self.plot.yaxis.axis_label = self.y_label

        marker = self.marker_free_sel.marker.value

        scatter = self.plot.scatter(source=self.bokeh_source,
                                    x='x', y='y',
                                    line_color='line_color',
                                    fill_color='fill_color',
                                    fill_alpha='fill_alpha',
                                    line_alpha='line_alpha',
                                    size='size',
                                    line_width='line_width',
                                    marker=marker
                                   )
        self.plot.add_tools(HoverTool(tooltips=tooltip, renderers=[scatter]))

    def select_tooltip_data(self):
        """tooltip data selection logic"""
        #dfx = self.df.loc[:,list(self.tooltip.target.value)].copy()
        #cols=dfx.columns
        #dfx.columns = [x+'_tip' for x in dfx.columns]
        self.tooltip_data = self.df.loc[:, list(self.tooltip.target.value)].copy()

    def update_mappers(self):
        """Iterate the widget to know wich parameters are mapped and store its
           values into the corresponding mapper columns. If they are free get the value
           from the free params selector.
        """
        for attr in self.marker_params:
            sel_attr = getattr(self.marker_map_sel, attr)
            values = sel_attr.target.value
            if sel_attr.active.value:
                data = self.df[values]
            #x and y are always used and related to the plot axis labels
            elif attr in ['x', 'y']:
                setattr(self, attr+'_label', values)
                data = self.df[values]
            else:
                data = self.marker_free_sel.params[attr]
            self.mapper.loc[:, attr] = data

    def update_translators(self):
        """translator logic"""
        self.update_mappers()
        self.translator = MarkerTranslator(df=self.mapper,
                                           active=self.active_params,
                                           free_params=self.free_params,
                                           mapped_params=self.marker_params,
                                           scaler_params=self.scaler.params)

    def update_source_dfs(self):
        """Datasources for plots managing"""
        marker_visual_data = self.translator.visual
        self.source = pd.concat([marker_visual_data, self.tooltip_data], axis=1)

    def update_active(self, change):
        """A fuction for updating its active dictionary"""
        self.active_params = dict([(x, getattr(self.marker_map_sel,
                                               x).active.value) for x in self.marker_params])
        self.active_params['x'] = True
        self.active_params['y'] = True
        self.update()


    def customize_children_widgets(self):
        """Adapt children widgets to a combined display"""
        self.marker_map_sel.x.name.visible = True
        pass



    def create_tooltip(self):
        """A function for creating a tooltip suitable for the plot. This means
        that by default all kinds of plots should try to include tooltips
        """
        return [("index", "$index")] + [(x, '@'+x) for x in self.tooltip_data.columns]

    def push_data(self):
        """A function to push the content of the source DataFrame
        to a specific plot source
        """
        self.bokeh_source.data = dict([(x, self.source[x].values) for x in self.source.columns])
        self.plot.xaxis.axis_label = self.x_label
        self.plot.yaxis.axis_label = self.y_label
        push_notebook()

    def update_datasources(self):
        """Make sure all the data needed for the plot is update and ready to push"""
        self.init_mappers()
        self.update_tooltips()
        self.update_translators()
        self.update_source_dfs()

    def update_tooltips(self):
        """Update tooltip data and inject it into the plot tooltips"""
        self.select_tooltip_data()
        self.plot.tools[-1].tooltips = self.create_tooltip()

    def update(self):
        """Set up all the combined elements needed for the plot"""
        self.update_datasources()
        self.push_data()
