# -*- coding: utf-8 -*-
"""Module in charge of Ploting Graphs"""
import numpy as np
import ipywidgets as widgets
from IPython.core.display import display
from IPython.display import clear_output
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
class GraphPlot(Shaolin):
    """This class enables us to map an arbitary pandas DataFrame to aplot"""
    NODE_MARKER_PARAMS = ['line_color',
                          'fill_color',
                          'fill_alpha',
                          'line_alpha',
                          'size',
                          'line_width'
                         ]

    EDGE_MARKER_PARAMS = ['line_color',
                          'fill_color',
                          'fill_alpha',
                          'line_alpha',
                          'size',
                          'line_width'
                         ]
    #This is a semi constant. The values can change but the keys are fixed.
    #This values are ment for the plot default values when a param is not fixed
    NODE_FREE_PARAMS = {'fill_color':'blue',
                        'fill_alpha': 0.8,
                        'size':60,
                        'fill_colormap':'spectral',
                        'line_colormap':'copper',
                        'marker':'circle',
                        'line_width':2,
                        'line_color':'black',
                        'line_alpha':1,}

    EDGE_FREE_PARAMS = {'fill_color':'#107167',
                        'fill_alpha': 0.8,
                        'size':7,
                        'fill_colormap':'copper',
                        'line_colormap':'coolwarm',
                        'marker':'circle',
                        'line_width':3,
                        'line_color':'black',
                        'line_alpha':1,}

    NODE_DEFAULT_MAP = {'fill_color':'label',
                        'fill_alpha': 'degree',
                        'size':'degree',
                        'marker':'label',
                        'line_width':'degree',
                        'line_color':'label',
                        'line_alpha':'degree',}

    EDGE_DEFAULT_MAP = {'fill_color':'weight',
                        'fill_alpha': 'weight',
                        'size':'weight',
                        'marker':'weight',
                        'line_width':'weight',
                        'line_color':'weight',
                        'line_alpha':'corr',}

    def __init__(self, gc,
                 node_marker_params=None,
                 node_free_params=None,
                 node_default_map=None,
                 edge_marker_params=None,
                 edge_free_params=None,
                 edge_default_map=None,
                ):
        if node_marker_params is None:
            self.node_marker_params = self.node_default_marker_params()
        else:
            self.node_marker_params = node_marker_params

        if node_free_params is None:
            self.node_free_params = self.node_default_free_params()
        else:
            self.node_free_params = node_free_params

        if node_default_map is None:
            self.node_default_map = self.get_node_default_map()
        else:
            self.node_default_map = node_default_map

        if edge_marker_params is None:
            self.edge_marker_params = self.edge_default_marker_params()
        else:
            self.edge_marker_params = edge_marker_params

        if edge_free_params is None:
            self.edge_free_params = self.edge_default_free_params()
        else:
            self.edge_free_params = edge_free_params

        if edge_default_map is None:
            self.edge_default_map = self.get_edge_default_map()
        else:
            self.edge_default_map = edge_default_map

        self.gc = gc
        self.nodes = pd.DataFrame(index=['node'], columns=self.gc.G.nodes())
        self.labels = pd.DataFrame(index=['node'], columns=self.gc.G.nodes())

        self.node_active_params = dict([(x, False) for x in self.node_marker_params])
        self.edge_active_params = dict([(x, False) for x in self.edge_marker_params])

        self.node_scaler = sww.ScaleParams()
        self.edge_scaler = sww.ScaleParams()
        self.node_scaler.external_observe(self.trigger_update)
        self.edge_scaler.external_observe(self.trigger_update)
        super(GraphPlot, self).__init__()
        self.init_widget()
        self.init_plot()


    @property
    def widget(self):
        """Dispaly full GUI"""
        return display(self.controls, show(self.plot))

    @classmethod
    def node_default_marker_params(cls):
        """Returns the ingredient list."""
        return cls.NODE_MARKER_PARAMS
    @classmethod
    def node_default_free_params(cls):
        """Returns the ingredient list."""
        return cls.NODE_FREE_PARAMS
    @classmethod
    def get_node_default_map(cls):
        return cls.NODE_DEFAULT_MAP

    @classmethod
    def edge_default_marker_params(cls):
        """Returns the ingredient list."""
        return cls.EDGE_MARKER_PARAMS
    @classmethod
    def edge_default_free_params(cls):
        """Returns the ingredient list."""
        return cls.EDGE_FREE_PARAMS
    @classmethod
    def get_edge_default_map(cls):
        return cls.EDGE_DEFAULT_MAP

    def on_marker_change(self, _):
        a = self.node_marker_map_sel.marker.active.value
        b = self.edge_marker_map_sel.marker.active.value
        if a or b:
            clear_output()
            self.init_plot()
            return show(self.plot)

    def on_tognod_change(self, _):
        self.node_sel_b.visible = self.toggle_nod.value

    def on_togedg_change(self, _):
        self.edge_sel_b.visible = self.toggle_edg.value

    def on_togdef_change(self, _):
        self.node_marker_free_sel.widget.visible = self.toggle_def.value
        self.edge_marker_free_sel.widget.visible = self.toggle_def.value

    def on_toggraph_change(self, _):
        self.gc.widget.visible = self.toggle_graph.value

    def on_calculate_click(self, _):
        self.gc.update()
        self.update()

    def init_widget(self):
        """Shaolin widget init. This is mainly for defining the widget
        the user will interact with
        """
        self.node_marker_free_sel.marker.observe(self.on_marker_change,
                                                 names='value')
        self.edge_marker_free_sel.marker.observe(self.on_marker_change,
                                                 names='value')
        self.node_marker_map_sel.marker.active.observe(self.on_marker_change,
                                                       names='value')
        self.edge_marker_map_sel.marker.active.observe(self.on_marker_change,
                                                       names='value')

        self.toggle_nod = widgets.ToggleButton(description='Node P',
                                               value=True, padding=6)

        self.toggle_nod.observe(self.on_tognod_change, names='value')

        self.toggle_edg = widgets.ToggleButton(description='Edge P',
                                               value=True, padding=6)
        self.toggle_edg.observe(self.on_togedg_change, names='value')

        self.toggle_def = widgets.ToggleButton(description='Defaults',
                                               value=True, padding=6)
        self.toggle_def.observe(self.on_togdef_change, names='value')

        self.toggle_graph = widgets.ToggleButton(description='Graph',
                                                 value=True, padding=6)
        self.toggle_graph.observe(self.on_toggraph_change, names='value')

        self.btn_box = widgets.HBox(children=[self.toggle_nod,
                                              self.toggle_edg,
                                              self.toggle_def,
                                              self.toggle_graph], padding=6)
        title_html = '''<div class="kf-graph-gplot" style=" font-size:22px;
                                                        font-weight: bold; 
                                                        text-align:right;">
                                                        Graph Manager</div>'''
        self.title = widgets.HTML(value=title_html)

        sel_title_html = '''<div class="kf-graph-gplot-sel_title" style=" font-size:22px;
                                                        font-weight: bold; 
                                                        text-align:right;">
                                                        Parameter Selecttor</div>'''
        sel_title = widgets.HTML(value=sel_title_html)
        node_html = '''<div class="kf-graph-gplot-node_sel" style=" font-size:18px;
                                                        font-weight: bold; 
                                                        text-align:right;">
                                                        Node parameters</div>'''
        node_sel_title = widgets.HTML(value=node_html)
        edge_html = '''<div class="kf-graph-glot-edge_sel" style=" font-size:18px;
                                                        font-weight: bold; 
                                                        text-align:right;">
                                                        Edge Parameters</div>'''
        edge_sel_title = widgets.HTML(value=edge_html)

        ns = self.node_marker_map_sel
        es = self.edge_marker_map_sel
        n_box1 = widgets.HBox(children=[ns.x.widget,
                                        ns.fill_color.widget,
                                        ns.fill_alpha.widget])
        n_box2 = widgets.HBox(children=[ns.size.widget,
                                        ns.line_color.widget,
                                        ns.line_alpha.widget])
        n_box3 = widgets.HBox(children=[ns.line_width.widget,
                                        ns.marker.widget])
        e_box1 = widgets.HBox(children=[es.x.widget,
                                        es.fill_color.widget,
                                        es.fill_alpha.widget])
        e_box2 = widgets.HBox(children=[es.size.widget,
                                        es.line_color.widget,
                                        es.line_alpha.widget])
        e_box3 = widgets.HBox(children=[es.line_width.widget, es.marker.widget])
        self.node_sel_b = widgets.VBox(children=[node_sel_title, n_box1,
                                                 n_box2, n_box3])
        self.edge_sel_b = widgets.VBox(children=[edge_sel_title, e_box1,
                                                 e_box2, e_box3])

        sel_params = widgets.HBox(children=[self.node_sel_b, self.edge_sel_b])
        self.sel_box = widgets.VBox(children=[sel_title, sel_params])
        self.def_box = widgets.HBox(children=[self.node_marker_free_sel.widget,
                                              self.node_ttip.widget,
                                              self.edge_marker_free_sel.widget,
                                              self.edge_ttip.widget])

        self.calculate = widgets.Button(description='Update', padding=6, margin=6)
        self.calculate.on_click(self.on_calculate_click)
        gcbody = widgets.HBox(children=[self.gc.gp.widget,
                                           self.gc.mp.widget,
                                           self.gc.layout.widget])
        gcwidget = widgets.VBox(children=[self.gc.title,
                                          gcbody,
                                          self.gc.buttonbox])
        self.controls = widgets.VBox(children=[self.title,
                                               self.def_box,
                                               gcwidget,
                                               self.sel_box,
                                               self.btn_box,
                                               self.calculate])

    def init_free_params_sel(self):
        """Handle plot free params selectors init. A free param means a
        plot parameter that is not mapped to data
        """
        self.node_marker_free_sel = swg.MarkerFreeParams(self.node_free_params,
                                                         title=('Node Mapping'))
        self.edge_marker_free_sel = swg.MarkerFreeParams(self.edge_free_params,
                                                         title=('Edge Mapping'))
        for param in self.node_free_params:
            getattr(self.node_marker_free_sel, param).observe(self.trigger_update,
                                                              names='value')
        for param in self.edge_free_params:
            getattr(self.edge_marker_free_sel, param).observe(self.trigger_update,
                                                              names='value')

    def trigger_update(self, _):
        """wrapper for updating from an event"""
        self.update()

    def init_mapped_params_sel(self):
        """Handle plot parameter selectors init"""
        self.node_marker_map_sel = swg.MarkerMappedParams(df=self.gc.node,
                                                          default_map=self.node_default_map,
                                                          params=self.node_marker_params)

        self.edge_marker_map_sel = swg.MarkerMappedParams(df=self.gc.edge[:, 1],
                                                          default_map=self.edge_default_map,
                                                          params=self.edge_marker_params)
        for name in  ['edge', 'node']:
            marker_map_sel = getattr(self, name+'_marker_map_sel')
            marker_params = getattr(self, name+'_marker_params')
            for param in marker_params:
                marker_widget = getattr(marker_map_sel, param)
                marker_widget.target.observe(self.trigger_update, names='value')
                marker_widget.active.observe(self.update_active, names='value')

    def init_mappers(self):
        """The mapper is a Dataframe use for preprocessing the marker parameters,
         its colums are the mapped parameters and its index its the same as the original data
        """

        self.node_mapper = pd.DataFrame(index=self.gc.G.nodes(), columns=self.node_marker_params)
        rm = self.gc.edge.to_frame().reset_index()
        mi = pd.MultiIndex.from_tuples(self.gc.G.edges())
        self.edge_mapper = pd.DataFrame(index=mi, columns=rm.columns)
        for u, v in self.gc.G.edges_iter():
            ix = np.logical_and.reduce([rm.minor == v, rm.major == u])
            vals = rm[ix].values
            if vals.size == 0:
                vals = np.nan
            self.edge_mapper.loc[u, v] = vals
        self.edge_mapper = self.edge_mapper.fillna(self.edge_mapper.dropna().min(axis=0).T)

    def init_tooltips(self):
        """This tooltip allows us to map any colum to the """
        cols = self.gc.matrix_panel.to_frame().columns
        self.node_ttip = swg.SelectMultiple(list(self.gc.node.columns.values), title='Node Tooltip')
        self.node_ttip.target.observe(self.trigger_update_tooltip, names='value')

        self.edge_ttip = swg.SelectMultiple(list(cols), title='Edge Tooltip')
        self.edge_ttip.target.observe(self.trigger_update_tooltip, names='value')

    def trigger_update_tooltip(self, _):
        """This updates just the tooltip info without reselecting all the data"""
        self.update_tooltips()
        self.push_data()

    def init_plot(self):
        """Handle plot init"""
        self.bk_node_source = bks.ColumnDataSource(dict([(x,
                                                          self.node_source[x].values)\
                                                 for x in self.node_source.columns]))
        self.bk_edge_source = bks.ColumnDataSource(dict([(x,
                                                          self.edge_source[x].values)\
                                                 for x in self.edge_source.columns]))
        self.select_tooltip_data()
        n_ttip = self.create_tooltip()
        e_ttip = self.create_tooltip('edge')

        self.plot = figure(title="Graph plot", width=600, height=600, webgl=False,
                           tools="pan,wheel_zoom,box_zoom,reset,resize,crosshair",)

        node_marker = self.node_marker_free_sel.marker.value
        edge_marker = self.edge_marker_free_sel.marker.value

        self.plot.segment('x0', 'y0',
                          'x1', 'y1',
                          color='line_color',
                          line_width='line_width',
                          alpha='line_alpha',
                          source=self.bk_edge_source)

        edg_center = self.plot.scatter(source=self.bk_edge_source,
                                       x='cx', y='cy',
                                       line_color='line_color',
                                       fill_color='fill_color',
                                       alpha='fill_alpha',
                                       size='size',
                                       line_width='line_width',
                                       marker=edge_marker)

        nod = self.plot.scatter(source=self.bk_node_source,
                                x='x', y='y',
                                line_color='line_color',
                                fill_color='fill_color',
                                fill_alpha='fill_alpha',
                                size='size',
                                line_width='line_width',
                                marker=node_marker)

        self.plot.text(source=self.bk_node_source,
                       x='x', y='y',
                       text='label',
                       text_align='center')

        self.plot.add_tools(HoverTool(tooltips=n_ttip, renderers=[nod]))
        self.plot.add_tools(HoverTool(tooltips=e_ttip, renderers=[edg_center]))

    def select_tooltip_data(self):
        """tooltip data selection logic"""
        self.gc.node_metrics.combine_first(self.gc.node)
        self.node_tooltip_data = self.gc.node_metrics[list(self.node_ttip.target.value)]\
                                                     .fillna('NaN').copy()
        
        self.edge_tooltip_data = self.gc.matrix_panel.to_frame()[list(self.edge_ttip.target.value)]\
                                                                .fillna('NaN').copy()
        self.edge_tooltip_data.index = pd.MultiIndex.from_tuples(self.edge_tooltip_data.index)
        self.edge_tooltip_data.loc[:, 'From'] = self.edge_tooltip_data.reset_index()['level_0'].values
        self.edge_tooltip_data.loc[:, 'To'] = self.edge_tooltip_data.reset_index()['level_1'].values

    def update_node_mapper(self):
        for attr in self.node_marker_params:
            sel_attr = getattr(self.node_marker_map_sel, attr)
            val = sel_attr.target.value

            if sel_attr.active.value:
                sval = self.gc.node[val].copy()
            elif attr == 'x':
                sval = self.gc.node[val]
                #self.x_label = x
            elif attr == 'y':
                sval = self.gc.node[val]
                #self.y_label = x
            else:
                sval = self.node_marker_free_sel.params[attr]
            self.node_mapper.loc[:, attr] = sval

    def update_edge_mapper(self):
        for attr in self.edge_marker_params:
            sel_attr = getattr(self.edge_marker_map_sel, attr)
            val = sel_attr.target.value

            if sel_attr.active.value:
                sval = self.edge_mapper[val].copy()
            elif attr == 'x':
                sval = self.edge_mapper[val]
                #self.x_label = x
            elif attr == 'y':
                sval = self.edge_mapper[val]
                #self.y_label = x
            else:
                sval = self.edge_marker_free_sel.params[attr]
            self.edge_mapper.loc[:, attr] = sval

    def update_mappers(self):
        """Iterate the widget to know wich parameters are mapped and store its
           values into the corresponding mapper columns. If they are free get the value
           from the free params selector.
        """
        self.update_node_mapper()
        self.update_edge_mapper()

    def update_translators(self):
        """translator logic"""
        self.update_mappers()
        self.node_translator = MarkerTranslator(df=self.node_mapper,
                                                active=self.node_active_params,
                                                free_params=self.node_free_params,
                                                mapped_params=self.node_marker_params,
                                                scaler_params=self.node_scaler.params)

        self.edge_translator = MarkerTranslator(df=self.edge_mapper,
                                                active=self.edge_active_params,
                                                free_params=self.edge_free_params,
                                                mapped_params=self.edge_marker_params,
                                                scaler_params=self.edge_scaler.params)

    def update_source_dfs(self):
        """Datasources for plots managing"""
        node_pos = self.gc.layout.node['2d'].dropna(axis=1).copy()
        node_vis = self.node_translator.visual.copy()

        edge_pos = self.gc.layout.edge['2d'].copy()
        edge_vis = self.edge_translator.visual.copy()

        edge_pos.index = pd.MultiIndex.from_tuples(edge_vis.index)
        edge_pos = edge_pos
        self.node_source = pd.concat([node_vis, node_pos,
                                      self.node_tooltip_data], axis=1).fillna('NaN').copy()
        self.node_source['label'] = self.gc.node.index.values
        self.edge_source = pd.concat([edge_vis,
                                      edge_pos],
                                     axis=1).join(self.edge_tooltip_data).fillna('Nan').copy()

    def update_active(self, _):
        """A fuction for updating its active dictionary"""

        self.node_active_params = dict([(x, getattr(self.node_marker_map_sel, x).active.value)\
                                      for x in self.node_marker_params])
        self.edge_active_params = dict([(x, getattr(self.edge_marker_map_sel, x).active.value)\
                                      for x in self.edge_marker_params])
        self.update()


    def customize_children_widgets(self):
        """Adapt children widgets to a combined display"""
        self.gc.calculate.visible=False
        pass



    def create_tooltip(self, s='node'):
        """A function for creating a tooltip suitable for the plot. This means
        that by default all kinds of plots should try to include tooltips
        """
        return  [("index", "$index")] +\
                [(x[:15], '@'+str(x)) for x in getattr(self, s+'_tooltip_data').columns]

    def push_data(self):
        """A function to push the content of the source DataFrame
        to a specific plot source
        """
        self.bk_node_source.data = dict([(x, self.node_source[x].values)\
                                         for x in self.node_source.columns])
        self.bk_edge_source.data = dict([(x, self.edge_source[x].values)\
                                         for x in self.edge_source.columns])
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
        self.plot.tools[-2].tooltips = self.create_tooltip()
        self.plot.tools[-1].tooltips = self.create_tooltip('edge')

    def update(self):
        """Set up all the combined elements needed for the plot"""
        self.update_datasources()
        self.push_data()
