# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 23:37:47 2016

@author: Guillem Duran Ballester for HCSoft
"""
import pandas as pd
from IPython.core.display import display, clear_output
from bokeh.models import HoverTool
import bokeh.models.sources as bks
from bokeh.plotting import figure, show
from bokeh.io import  push_notebook, output_notebook
from bokeh.embed import notebook_div
from shaolin.core.dashboard import Dashboard, ToggleMenu
from shaolin.dashboards.plot_mappers import PlotMapper
from shaolin.core.shaoscript import shaoscript

class BokehDataFrameTooltip(Dashboard):
    
    def __init__(self, data, mode='interactive', **kwargs):
        self._data = data
        dash = ['c$N=tooltip',
                ['###Tolltip$N=title',
                 '@selmul$n=tooltip_cols&d=Tooltip info&o='+str(tuple(data.columns.values))
                
                ]
               ]
        self.output = data.copy()
        Dashboard.__init__(self, dash, mode=mode, **kwargs)
        self.tooltip_cols.value = tuple(data.columns.values)
        self.observe(self.update)
        self.update()
    
    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, val):
        self._data = val
        self.update()
    def update(self, _=None):
        self.output = self._data[list(self.tooltip_cols.value)]
    
    def create_tooltip(self):
        """A function for creating a tooltip suitable for the plot. This means
        that by default all kinds of plots should try to include tooltips
        """
        return [("index", "$index")] + [(x, '@'+x) for x in self.output.columns]

class ScatterPlot(ToggleMenu):
    
    def __init__(self, data,name='scatter_plot', **kwargs):
        output_notebook(hide_banner=True)
        self._data = data
        mapper = PlotMapper(data, button_type='ddown',button_pos='top', name='mapper', mode='interactive')
        if isinstance(data, pd.DataFrame):
            tooltip = BokehDataFrameTooltip(data, name='tooltip', mode='interactive')
            ToggleMenu.__init__(self, children=[mapper,tooltip], name=name,**kwargs)
        else:
            ToggleMenu.__init__(self, children=[mapper], name=name,**kwargs)
        self.buttons.value = 'mapper'
        self.mapper.buttons.value = 'y'
        if isinstance(self._data,pd.DataFrame):
            self.mapper.y.data_slicer.columns_slicer.dd_selector.value =\
                self.mapper.y.data_slicer.columns_slicer.dd_selector.target.options[1]
        self.observe(self.update)
        self.mapper.marker.marker_type.observe(self._on_marker_change)
        
        self.update_source_df()
        self.init_plot()
        self.update()
    
    def _on_marker_change(self, _=None):
        clear_output()
        self.init_plot()
        self.update()
        return display(show(self.plot))
        
    @property
    def data(self):
        return self._data    
    
    def update_source_df(self):
        """Datasources for plots managing"""
        if isinstance(self._data, pd.DataFrame):
            self.output= self.mapper.output.join(self.tooltip.output) 
        else:
            self.output= self.mapper.output
    
    def update_tooltips(self):
        """Update tooltip data and inject it into the plot tooltips"""
        if isinstance(self._data, pd.DataFrame):
            self.plot.tools[-1].tooltips = self.tooltip.create_tooltip()

    def update(self, _=None):
        """Set up all the combined elements needed for the plot"""
        self.update_source_df()
        if isinstance(self._data, pd.DataFrame):
            self.update_tooltips()
        self.push_data()
        
    def push_data(self):
        """A function to push the content of the source DataFrame
        to a specific plot source
        """
        self.bokeh_source.data = dict([(x, self.output[x].values) for x in self.output.columns])
        self.plot.xaxis.axis_label = self.mapper.x.data_slicer.description
        self.plot.yaxis.axis_label = self.mapper.y.data_slicer.description

        push_notebook()
        
    def init_plot(self):
        """Handle plot init"""
        self.bokeh_source = bks.ColumnDataSource(dict([(x, self.output[x].values)\
                                                 for x in self.output.columns]))
        if isinstance(self._data, pd.DataFrame):
            tooltip = self.tooltip.create_tooltip()

        self.plot = figure(title="Scatter plot", width=600, height=600, webgl=False,
                           tools="pan,wheel_zoom,box_zoom,reset,resize,crosshair",)
        self.plot.xaxis.axis_label = self.mapper.x.data_slicer.description
        self.plot.yaxis.axis_label = self.mapper.y.data_slicer.description

        #marker = self.marker_free_sel.marker.value

        _scatter = self.plot.scatter(source=self.bokeh_source,
                                     x='x', y='y',
                                     line_color='line_color',
                                     fill_color='fill_color',
                                     fill_alpha='fill_alpha',
                                     line_alpha='line_alpha',
                                     size='size',
                                     line_width='line_width',
                                     marker=self.mapper.marker.marker_type.value
                                       
                                    )
        if isinstance(self._data, pd.DataFrame):
            self.plot.add_tools(HoverTool(tooltips=tooltip, renderers=[_scatter]))
    
    def show(self):
        return display(self.widget, show(self.plot))
    
    @property
    def snapshot(self, name='bokeh_scatter'):
      html =  notebook_div(self.plot)
      widget = shaoscript('html$N='+name)
      widget.value = html
      return widget

class GraphPlotBokeh(ToggleMenu):
    
    def __init__(self, gc, name='scatter_plot', **kwargs):
        node_mapper_dict = {'size':{'max':100,
                            'min':5,
                            'step':0.5,
                            'high':75,
                            'low':25,
                            'default':60,
                            'map_data':False,
                            'fixed_active':False,
                           },
                       'line_width':{'max':50,
                            'min':0,
                            'step':0.5,
                            'high':5,
                            'low':1,
                            'default':2,
                            'map_data':False,
                            'fixed_active':False,
                           },
                       'fill_alpha':{'max':1.0,
                            'min':0.,
                            'step':0.05,
                            'high':0.95,
                            'low':0.3,
                            'default':1.,
                            'map_data':False,
                            'fixed_active':False,
                           },
                       'line_alpha':{'max':1.0,
                            'min':0.,
                            'step':0.05,
                            'high':0.95,
                            'low':0.3,
                            'default':1.,
                            'map_data':False,
                            'fixed_active':False,
                           },
                       'line_color':{'default_color':'black','map_data':False,'step':0.05,'min':0.0,'low':0.0},
                       'fill_color':{'default_color':'#11D4CA','map_data':False,'step':0.05,'min':0.0,'low':0.0}
                      }
        edge_mapper_dict = {'size':{'max':100,
                            'min':5,
                            'step':0.5,
                            'high':20,
                            'low':7,
                            'default':7,
                            'map_data':False,
                            'fixed_active':False,
                           },
                       'line_width':{'max':50,
                            'min':0,
                            'step':0.5,
                            'high':5,
                            'low':1,
                            'default':2,
                            'map_data':False,
                            'fixed_active':False,
                           },
                       'fill_alpha':{'max':1.0,
                            'min':0.,
                            'step':0.05,
                            'high':0.95,
                            'low':0.3,
                            'default':1.,
                            'map_data':False,
                            'fixed_active':False,
                           },
                       'line_alpha':{'max':1.0,
                            'min':0.,
                            'step':0.05,
                            'high':0.95,
                            'low':0.3,
                            'default':1.,
                            'map_data':False,
                            'fixed_active':False,
                           },
                       'line_color':{'default_color':'black','map_data':False,'step':0.05,'min':0.0,'low':0.0},
                       'fill_color':{'default_color':'#EDB021','map_data':False,'step':0.05,'min':0.0,'low':0.0}
                      }
        gc.name = 'gc'
        output_notebook(hide_banner=True)
        edge_mapper_data = self.prepare_edge_mapper_data(gc)
        node_mapper = PlotMapper(gc.node, mapper_dict=node_mapper_dict, button_type='ddown',button_pos='top', name='node_mapper', mode='interactive')
        edge_mapper = PlotMapper(edge_mapper_data, mapper_dict=edge_mapper_dict, button_type='ddown',button_pos='top', name='edge_mapper', mode='interactive')
        node_tooltip_data = gc.node.combine_first(gc.node_metrics.T)
        node_tooltip = BokehDataFrameTooltip(node_tooltip_data, name='node_tooltip')
        edge_tooltip = BokehDataFrameTooltip(edge_mapper_data, name='edge_tooltip')
        ToggleMenu.__init__(self,
                            children=[gc,node_mapper,
                                            edge_mapper,
                                            node_tooltip,
                                            edge_tooltip],
                            name=name,**kwargs)
        
        self.observe(self.update)
        self.gc.calculate.observe(self.update)
        self.node_mapper.marker.marker_type.observe(self._on_marker_change)
        self.edge_mapper.marker.marker_type.observe(self._on_marker_change)
        self.update_source_df()
        self.init_plot()
        self.update()
        self._init_layout()
    
    def prepare_edge_mapper_data(self,gc):
        dft = gc.edge.to_frame().reset_index()
        ti = list(zip(dft.minor.values,dft.major.values))
        dft.index = ti
        dft = dft.drop(['major','minor'],axis=1)
        return dft.ix[gc.G.edges()].copy()
        
    def _init_layout(self):
        params = ['size', 'line_width', 'fill_alpha', 'line_alpha', 'line_color', 'fill_color']
        for target in ['node','edge']:
            mapper = getattr(self,target+'_mapper')
            for p in params:
                getattr(mapper,p).data_slicer.index_slicer.visible = False
        
    def update_source_df(self):
        """Datasources for plots managing"""
        def index_to_columns(df):
            old_index = df.index
            new_index = pd.MultiIndex.from_tuples(df.index)
            df.index = new_index
            df = df.reset_index()
            df.index = old_index
            columns = df.columns.values
            columns[:2] = ['major','minor']
            df.columns = columns
            return df
        def fix_pos_index(edge_pos,edge_source):
            changed = set(edge_source.index) - set(edge_pos.index)
            edge_source.index = pd.MultiIndex.from_tuples(edge_source.index)
            edge_pos.index = pd.MultiIndex.from_tuples(edge_pos.index)
            for e in changed:
                inv = (e[1],e[0])
                edge_pos.loc[inv,'minor'] = e[1]
                edge_pos.loc[inv,'major'] = e[0]
            return edge_pos
        self.node_source= self.node_mapper.output.join(self.node_tooltip.output)
        #self.edge_tooltip.output.index = pd.MultiIndex.from_tuples(self.edge_tooltip.output.index.values)
        #self.edge_mapper.output.index = pd.MultiIndex.from_tuples(self.edge_mapper.output.index.values)
        self.edge_source= self.edge_mapper.output.join(self.edge_tooltip.output) 
        
        node_pos = self.gc.layout.node['2d'].dropna(axis=1).copy()
        edge_pos = self.gc.layout.edge['2d'].copy()
        edge_pos = index_to_columns(edge_pos)
        edge_source = index_to_columns(self.edge_source)
        edge_pos = fix_pos_index(edge_pos,edge_source) 
        self.output_node = pd.concat([self.node_source, node_pos], axis=1).fillna('NaN').copy()
        self.output_edge = edge_source.merge(edge_pos,on=['major','minor'], left_index=True).fillna('NaN').copy()#edge_pos.merge(self.edge_source,on=['major','minor'],left_index=True)
        
       
    def update_mappers(self):
        dft = self.gc.edge.to_frame().reset_index()
        ti = list(zip(dft.minor.values,dft.major.values))
        dft.index = ti
        dft = dft.drop(['major','minor'],axis=1)
        edge_mapper_data = dft.ix[self.gc.G.edges()].copy()
        self.edge_mapper.data = edge_mapper_data
        self.node_mapper.data = self.gc.node
        self.node_tooltip.data = self.gc.node_metrics.combine_first(self.gc.node.T).T
        self.edge_tooltip.data = edge_mapper_data
    
    def update_tooltips(self):
        """Update tooltip data and inject it into the plot tooltips"""
        self.plot.tools[-1].tooltips = self.edge_tooltip.create_tooltip()
        self.plot.tools[-2].tooltips = self.node_tooltip.create_tooltip()

    def update(self, _=None):
        """Set up all the combined elements needed for the plot"""
        self.update_mappers()
        self.update_source_df()
        self.update_tooltips()
        self.push_data()
        
    def push_data(self):
        """A function to push the content of the source DataFrame
        to a specific plot source
        """
        self.node_bokeh_source.data = dict([(x, self.output_node[x].values) for x in self.output_node.columns])
        self.edge_bokeh_source.data = dict([(x, self.output_edge[x].values) for x in self.output_edge.columns])
        

        push_notebook()
    
    def _on_marker_change(self, _=None):
        clear_output()
        self.init_plot()
        self.update()
        return display(show(self.plot))
    
    def init_plot(self):
        """Handle plot init"""
        self.node_bokeh_source = bks.ColumnDataSource(dict([(x,
                                                          self.output_node[x].values)\
                                                 for x in self.output_node.columns]))
        self.edge_bokeh_source = bks.ColumnDataSource(dict([(x,
                                                          self.output_edge[x].values)\
                                                 for x in self.output_edge.columns]))
        n_ttip = self.node_tooltip.create_tooltip()
        e_ttip = self.edge_tooltip.create_tooltip()

        self.plot = figure(title="Graph plot", width=600, height=600, webgl=False,
                           tools="pan,wheel_zoom,box_zoom,reset,resize,crosshair",)

        #node_marker = 'circle'#self.node_marker_free_sel.marker.value
        #edge_marker = self.edge_marker_free_sel.marker.value

        self.plot.segment('x0', 'y0',
                          'x1', 'y1',
                          color='line_color',
                          line_width='line_width',
                          alpha='line_alpha',
                          source=self.edge_bokeh_source)

        edg_center = self.plot.scatter(source=self.edge_bokeh_source,
                                       x='cx', y='cy',
                                       line_color='line_color',
                                       fill_color='fill_color',
                                       alpha='fill_alpha',
                                       size='size',
                                       line_width='line_width',
                                       marker=self.edge_mapper.marker.marker_type.value
                                       )#,
                                       #marker=edge_marker)
        
        nod = self.plot.scatter(source=self.node_bokeh_source,
                                x='x', y='y',
                                line_color='line_color',
                                fill_color='fill_color',
                                fill_alpha='fill_alpha',
                                size='size',
                                line_width='line_width',#,
                                marker=self.node_mapper.marker.marker_type.value)

        self.plot.text(source=self.node_bokeh_source,
                       x='x', y='y',
                       text='label',
                       text_align='center')

        self.plot.add_tools(HoverTool(tooltips=n_ttip, renderers=[nod]))
        self.plot.add_tools(HoverTool(tooltips=e_ttip, renderers=[edg_center]))
    @property
    def snapshot(self, name='bokeh_scatter'):
      html =  notebook_div(self.plot)
      widget = shaoscript('html$N='+name)
      widget.value = html
      return widget
    
    def show(self):
        return display(self.widget, show(self.plot))