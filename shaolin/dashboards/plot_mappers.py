# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 23:23:59 2016

@author: Guillem Duran Ballester for HCSoft
"""
import pandas as pd
import numpy as np
from shaolin.core.dashboard import Dashboard, ToggleMenu
from shaolin.dashboards.slicers import PanelSlicer, Panel4DSlicer, DataFrameSlicer
from shaolin.dashboards.data_transforms import DataFrameScaler
from shaolin.dashboards.colormap import ColormapPicker
class PanelToPlot(Dashboard):
    
    def __init__(self, panel, description='Panel', mode='interactive',output_mode=None, **kwargs):
        self.panel = panel
        dash = ['c$N=df_slicer',
               [
                '##'+description+'$N=pts_description_text',
                ['r$N=mode_column',['@togs$N=index_tog&d=index&o=["items","major_axis","minor_axis"]&val=major_axis',
                                    '@rad$N=output_mode&d=Output&val=series&o=["series","matrix"]']
                ],
                PanelSlicer(panel, name='panel_slicer', description='')
               ]
              ]
        Dashboard.__init__(self, dash, mode=mode, **kwargs )
        if output_mode == 'series':
            self.output_mode.value = 'series'
            self.output_mode.visible = False
        elif output_mode == 'matrix':
            self.output_mode.value = 'matrix'
            self.output_mode.visible = False
            
        self.observe(self.update)
        self.update()

    @property
    def data(self):
        return self.panel

    @data.setter
    def data(self, val):
        self.panel = val
        self.panel_slicer.data = val
        self.update()

    def apply_output_mode(self):
        if self.output_mode.value == 'series':
            if self.index_tog.value == 'items':
                self.panel_slicer.items_slicer.slice_mode.value = 'slice'
                self.panel_slicer.major_axis_slicer.slice_mode.value = 'single'
                self.panel_slicer.minor_axis_slicer.slice_mode.value = 'single'
                self.description = str(self.panel.major_axis[self.panel_slicer.major_axis_slicer.idx].values[0])+'_'+\
                                    str(self.panel.minor_axis[self.panel_slicer.minor_axis_slicer.idx].values[0])
            elif self.index_tog.value == 'major_axis':
                self.panel_slicer.items_slicer.slice_mode.value = 'single'
                self.panel_slicer.major_axis_slicer.slice_mode.value = 'slice'
                self.panel_slicer.minor_axis_slicer.slice_mode.value = 'single'
                self.description = str(self.panel.items[self.panel_slicer.items_slicer.idx].values[0])+'_'+\
                                    str(self.panel.minor_axis[self.panel_slicer.minor_axis_slicer.idx].values[0])
            elif self.index_tog.value == 'minor_axis':
                self.panel_slicer.items_slicer.slice_mode.value = 'single'
                self.panel_slicer.major_axis_slicer.slice_mode.value = 'single'
                self.panel_slicer.minor_axis_slicer.slice_mode.value = 'slice'
                self.description = str(self.panel.items[self.panel_slicer.items_slicer.idx].values[0])+'_'+\
                                    str(self.panel.major_axis[self.panel_slicer.major_axis_slicer.idx].values[0])
                
        elif self.output_mode.value == 'matrix':
            if self.index_tog.value == 'items':
                self.panel_slicer.items_slicer.slice_mode.value = 'single'
                self.panel_slicer.major_axis_slicer.slice_mode.value = 'slice'
                self.panel_slicer.minor_axis_slicer.slice_mode.value = 'slice'
                self.description = str(self.panel.items[self.panel_slicer.items_slicer.idx].values[0])
            elif self.index_tog.value == 'major_axis':
                self.panel_slicer.items_slicer.slice_mode.value = 'slice'
                self.panel_slicer.major_axis_slicer.slice_mode.value = 'single'
                self.panel_slicer.minor_axis_slicer.slice_mode.value = 'slice'
                self.description = str(self.panel.major_axis[self.panel_slicer.major_axis_slicer.idx].values[0])
            elif self.index_tog.value == 'minor_axis':
                self.panel_slicer.items_slicer.slice_mode.value = 'slice'
                self.panel_slicer.major_axis_slicer.slice_mode.value = 'slice'
                self.panel_slicer.minor_axis_slicer.slice_mode.value = 'single'
                self.description = str(self.panel.minor_axis[self.panel_slicer.minor_axis_slicer.idx].values[0])
    
    def update(self, _=None):
        self.apply_output_mode()
        if self.panel_slicer.items_slicer.slice_mode.value == 'single':
            items_idx = list(self.panel_slicer.items_slicer.idx).index(True)
        else:
            items_idx = self.panel_slicer.items_slicer.idx
            
        if self.panel_slicer.major_axis_slicer.slice_mode.value == 'single':
            major_axis_idx = list(self.panel_slicer.major_axis_slicer.idx).index(True)
        else:
            major_axis_idx = self.panel_slicer.major_axis_slicer.idx

        if self.panel_slicer.minor_axis_slicer.slice_mode.value == 'single':
            minor_axis_idx = list(self.panel_slicer.minor_axis_slicer.idx).index(True)
        else:
            minor_axis_idx = self.panel_slicer.minor_axis_slicer.idx
        
        self.output = self.panel.ix[items_idx,major_axis_idx,minor_axis_idx]
        if self.output_mode.value == 'series':
            self.output = pd.DataFrame(self.output)

class Panel4DToPlot(Dashboard):
    
    def __init__(self, panel, description='Panel', mode='interactive', output_mode=None, **kwargs):
        self.panel = panel
        dash = ['c$N=df_slicer',
               [
                '##'+description+'$N=pts_description_text',
                ['r$N=mode_column',['@togs$N=index_tog&d=index&o=["labels","items","major_axis","minor_axis"]&val=items',
                                    '@togs$N=columns_tog&d=index&o=["labels","items","major_axis","minor_axis"]&val=minor_axis&v=0',
                                    '@rad$N=output_mode&d=Output&val=series&o=["series","matrix"]']
                ],
                Panel4DSlicer(panel, name='panel_slicer', description='')
               ]
              ]
        Dashboard.__init__(self, dash, mode=mode, **kwargs )
        if output_mode == 'series':
            self.output_mode.value = 'series'
            self.output_mode.visible = False
        elif output_mode == 'matrix':
            self.output_mode.value = 'matrix'
            self.output_mode.visible = False
        self.observe(self.update)
        self.update()

    @property
    def data(self):
        return self.panel

    @data.setter
    def data(self, val):
        self.panel = val
        self.panel_slicer.data = val
        self.update()

    def apply_output_mode(self):
        if self.output_mode.value == 'series':
            self.columns_tog.visible = False
            self.index_tog.target.description = 'index'
            if self.index_tog.value == 'labels':
                self.panel_slicer.labels_slicer.slice_mode.value = 'slice'
                self.panel_slicer.items_slicer.slice_mode.value = 'single'
                self.panel_slicer.major_axis_slicer.slice_mode.value = 'single'
                self.panel_slicer.minor_axis_slicer.slice_mode.value = 'single'
                self.description = str(self.panel.items[self.panel_slicer.items_slicer.idx].values[0])+'_'+\
                                    str(self.panel.major_axis[self.panel_slicer.major_axis_slicer.idx].values[0])+'_'+\
                                    str(self.panel.minor_axis[self.panel_slicer.minor_axis_slicer.idx].values[0])
            elif self.index_tog.value == 'items':
                self.panel_slicer.labels_slicer.slice_mode.value = 'single'
                self.panel_slicer.items_slicer.slice_mode.value = 'slice'
                self.panel_slicer.major_axis_slicer.slice_mode.value = 'single'
                self.panel_slicer.minor_axis_slicer.slice_mode.value = 'single'
                self.description = str(self.panel.labels[self.panel_slicer.labels_slicer.idx].values[0])+'_'\
                                    +str(self.panel.major_axis[self.panel_slicer.major_axis_slicer.idx].values[0])+'_'\
                                    +str(self.panel.minor_axis[self.panel_slicer.minor_axis_slicer.idx].values[0])
            elif self.index_tog.value == 'major_axis':
                self.panel_slicer.labels_slicer.slice_mode.value = 'single'
                self.panel_slicer.items_slicer.slice_mode.value = 'single'
                self.panel_slicer.major_axis_slicer.slice_mode.value = 'slice'
                self.panel_slicer.minor_axis_slicer.slice_mode.value = 'single'
                self.description = str(self.panel.labels[self.panel_slicer.labels_slicer.idx].values[0])+'_'\
                                   +str(self.panel.items[self.panel_slicer.items_slicer.idx].values[0])+'_'\
                                   +str(self.panel.minor_axis[self.panel_slicer.minor_axis_slicer.idx].values[0])
            elif self.index_tog.value == 'minor_axis':
                self.panel_slicer.labels_slicer.slice_mode.value = 'single'
                self.panel_slicer.items_slicer.slice_mode.value = 'single'
                self.panel_slicer.major_axis_slicer.slice_mode.value = 'single'
                self.panel_slicer.minor_axis_slicer.slice_mode.value = 'slice'
                self.description = str(self.panel.labels[self.panel_slicer.labels_slicer.idx].values[0])+'_'\
                                   +str(self.panel.items[self.panel_slicer.items_slicer.idx].values[0])+'_'\
                                   +str(self.panel.major_axis[self.panel_slicer.major_axis_slicer.idx].values[0])
                
        elif self.output_mode.value == 'matrix':
            self.columns_tog.visible = True
            self.index_tog.target.description = 'rows'
            opts = set(['labels', 'items', 'major_axis', 'minor_axis'])
            slices = set([self.index_tog.value, self.columns_tog.value])
            singles = opts-slices
            for sli in slices:
                getattr(self.panel_slicer,sli+'_slicer').slice_mode.value = 'slice'
            for sli in singles:
                getattr(self.panel_slicer,sli+'_slicer').slice_mode.value = 'single'
    
    def update(self, _=None):
        self.apply_output_mode()
        if self.panel_slicer.labels_slicer.slice_mode.value == 'single':
            labels_idx = list(self.panel_slicer.labels_slicer.idx).index(True)
        else:
            items_idx = self.panel_slicer.items_slicer.idx
            
        if self.panel_slicer.items_slicer.slice_mode.value == 'single':
            items_idx = list(self.panel_slicer.items_slicer.idx).index(True)
        else:
            items_idx = self.panel_slicer.items_slicer.idx
            
        if self.panel_slicer.major_axis_slicer.slice_mode.value == 'single':
            major_axis_idx = list(self.panel_slicer.major_axis_slicer.idx).index(True)
        else:
            major_axis_idx = self.panel_slicer.major_axis_slicer.idx

        if self.panel_slicer.minor_axis_slicer.slice_mode.value == 'single':
            minor_axis_idx = list(self.panel_slicer.minor_axis_slicer.idx).index(True)
        else:
            minor_axis_idx = self.panel_slicer.minor_axis_slicer.idx
        
        self.output = self.panel.ix[labels_idx,items_idx,major_axis_idx,minor_axis_idx]
        if self.output_mode.value == 'series':
            self.output = pd.DataFrame(self.output)

class PlotDataFilter(Dashboard):
    
    def __init__(self,
                 data,
                 max=None,
                 min=None,
                 step=None,
                 low=None,
                 high=None,
                 description='plot data',
                 map_data = True,
                 default=None,
                 fixed_active=False,
                 **kwargs
                ):
        self._description = description
        self._data = data
        slicer = self._get_data_slicer(description=description)
        scaler = DataFrameScaler(slicer.output, max=max, min=min, step=step, low=low, high=high, name='data_scaler')
        self.output = pd.DataFrame(index=scaler.output.index, columns=[description])
        if max is None:
            max = 100
        if min is None:
            min = 0
        if high is None:
            high = 100
        if low is None:
            low = 0
        if step is None:
            step = 1
        if default is None:
            default = (high+low)*0.5
        if np.isnan(default):
            def_widget='HTML$N=default_w&v=0'
            self.default_value = np.nan
        else:
            def_widget = '@('+str(min)+','+str(max)+','+str(step)+','+str(default)+')$d=Default value'
        dash = ['r$N=main_row',
                [
                 slicer,
                 ['c$N=aply_col',[scaler,
                                  ['r$N=apply_row',['Map Data$N=map_text','@'+str(map_data)+'$N=map_chk','[['+str(map_data)+']]$N=map_valid']]
                                 ]],
                def_widget
                
                ]
                ]
        Dashboard.__init__(self, dash, **kwargs)
        
        if fixed_active:
            self.map_chk.visible = False
            self.map_valid.visible = False
            self.map_chk.target.disabled = True
            
        self.link('map_chk','map_valid')
        self.map_chk.target.layout.width = "100%"
        self.map_valid.target.readout = 'Mapping disabled'
        self.observe(self.update)
        self.update()

    @property
    def data(self):
        return self._data
        
    @data.setter
    def data(self, val):
        self._data = val
        self.update()
        
    def _get_data_slicer(self, description):
        #leave room for other pandas structures
        if isinstance(self._data, pd.DataFrame):
            slicer = DataFrameSlicer(self._data, name='data_slicer', description=description)
            slicer.index_slicer.slice_mode.value = 'slice'
            return slicer
        
        elif isinstance(self._data, pd.Panel4D):
            slicer = Panel4DToPlot(self._data, name='data_slicer', description=description, output_mode='series')
            return slicer
        elif isinstance(self._data, pd.Panel):
            slicer = PanelToPlot(self._data, name='data_slicer', description=description)
            return slicer
        
    def update(self, _=None):
        self.data_slicer.data = self._data
        self.data_scaler.data = self.data_slicer.output
        active_data = self.data_scaler.output
        if isinstance(active_data,pd.Series):
            columns = self.data_scaler.dd_sel.value
        else:
            columns = active_data.columns
        if isinstance(self._data, pd.DataFrame):
            empty_df = pd.DataFrame(index=self._data.index, columns=columns)
        else:
            empty_df = pd.DataFrame(index=self.data_scaler.output.index, columns=columns)
        if self.map_chk.value:
            if hasattr(self.default_value,'value'):
                self.output = empty_df.combine_first(active_data).fillna(self.default_value.value)
            else:
                self.output = empty_df.combine_first(active_data).fillna(self.default_value)
        else:
            if hasattr(self.default_value,'value'):
                self.output = empty_df.fillna(self.default_value.value)
            else:
                self.output = empty_df.fillna(self.default_value)
        self.output.columns = [self._description]

class PlotCmapFilter(Dashboard):
    
    def __init__(self,
                 data,
                 max=None,
                 min=None,
                 step=None,
                 low=None,
                 high=None,
                 description='plot_data',
                 map_data = True,
                 default_color='blue',
                 **kwargs
                ):
        self._data = data
        self._description = description
        slicer = self._get_data_slicer(description=description)
        scaler = DataFrameScaler(slicer.output, max=max, min=min, step=step, low=low, high=high, name='data_scaler')
        self.output = pd.DataFrame(index=scaler.output.index, columns=[description])
        cmap = ColormapPicker(name='cm_picker', mode='interactive')
        dash = ['r$N=main_row',
                [
                 slicer,
                 ['c$N=aply_col',[scaler,
                                  ['r$N=apply_row',['Map Data$N=map_text','@'+str(map_data)+'$N=map_chk','[['+str(map_data)+']]$N=map_valid']]
                                 ]],
                ['c$N=color_col',[ cmap,
                 '@cpicker$N=default_color&d=Default color&val='+default_color]]
                ]
                ]
        Dashboard.__init__(self, dash, **kwargs)
        self.link('map_chk','map_valid')
        self.map_chk.target.layout.width = "100%"
        self.map_valid.target.readout = 'Mapping disabled'
        self.observe(self.update)
        self.update()
        
    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, val):
        self._data = val
        self.update()
    def _get_data_slicer(self, description):
        #leave room for other pandas structures
        if isinstance(self._data, pd.DataFrame):
            slicer = DataFrameSlicer(self._data, name='data_slicer', description=description)
            slicer.index_slicer.slice_mode.value = 'slice'
            return slicer
        
        elif isinstance(self._data, pd.Panel4D):
            slicer = Panel4DToPlot(self._data, name='data_slicer', description=description, output_mode='series')
            return slicer
        elif isinstance(self._data, pd.Panel):
            slicer = PanelToPlot(self._data, name='data_slicer', description=description)
            return slicer
    
    def update(self, _=None):
        self.data_slicer.data = self._data
        self.data_scaler.data = self.data_slicer.output
        active_data = self.data_scaler.output.apply(lambda x: self.cm_picker.master_palette.map_data(x,hex=True))
        if isinstance(active_data,pd.Series):
            columns = self.data_scaler.dd_sel.value
        else:
            columns = active_data.columns
        
        if isinstance(self._data, pd.DataFrame):
            empty_df = pd.DataFrame(index=self._data.index, columns=columns)
        else:
            empty_df = pd.DataFrame(index=self.data_scaler.output.index, columns=columns)
        if self.map_chk.value:
            self.output = empty_df.combine_first(active_data).fillna(self.default_color.value)
        else:
            self.output = empty_df.fillna(self.default_color.value)
        self.output.columns = [self._description]

class PlotMapper(ToggleMenu):
    mapper_dict = {'x':{'max':100.0,
                    'min':0.0,
                    'step':0.1,
                    'high':1.,
                    'low':0.,
                    'default':np.nan,
                    'map_data':True,
                    'fixed_active':True,
                   },
               'y':{'max':100.0,
                    'min':0.0,
                    'step':0.1,
                    'high':1.,
                    'low':0.,
                    'default':np.nan,
                    'map_data':True,
                    'fixed_active':True,
                   },
               'size':{'max':100,
                    'min':1,
                    'step':0.5,
                    'high':20,
                    'low':10,
                    'default':12,
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
               'fill_color':{'default_color':'blue','map_data':False,'step':0.05,'min':0.0,'low':0.0}
              }
    
    def __init__(self, data, mapper_dict=None, marker_opts=None, **kwargs):
        if marker_opts is None:
            self._marker_opts = ['circle', 'square', 'asterisk', 'circle_cross',
                                 'circle_x', 'square_cross', 'square_x', 'triangle',
                                 'diamond', 'cross', 'x', 'inverted_triangle',
                                 ]
        else:
            self._marker_opts = marker_opts
        self._data = data
        if isinstance(self._data, pd.DataFrame):
            if isinstance(self._data.index.values[0], (list,tuple,str)):
                old = self._data.index
                ix = [str(x) for x in self._data.index.values]
                self._data.index = ix
                self._data = self._data.reset_index()
                self._data.index = old
            else:
                ix = self._data.index
                self._data = self._data.reset_index()
                self._data.index = ix
        if mapper_dict is None:
            self.mapper_dict = self.get_default_mapper_dict()
        else:
            self.mapper_dict = mapper_dict
        children = self.init_filters()
        ToggleMenu.__init__(self, children=children, **kwargs)
        self.observe(self.update)
        self.update()

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, val):
        self._data = val
        for param in self.params:
            getattr(self, param).data = self._data
        self.update()

    @classmethod
    def get_default_mapper_dict(cls):
        return cls.mapper_dict
    
    def init_filters(self):
        self.params = list(sorted(self.mapper_dict.keys()))
        filters = []
        for param in self.params:
            kwargs = self.mapper_dict[param]
            if 'default_color' in kwargs.keys():
                filters += [PlotCmapFilter(self._data, name=param,description=param, mode='interactive', **kwargs)]
            else:
                filters += [PlotDataFilter(self._data, name=param, description=param, mode='interactive', **kwargs)]
        marker = [Dashboard(['dd$d=Marker type&val=circle&o='+str(self._marker_opts)], name='marker' )]
        filters += marker        
        return filters
    
    def update(self, _=None):
        out = getattr(self,self.params[0]).output.copy()
        for p in self.params[1:]:
            out = pd.concat([out,getattr(self,p).output],axis=1)
        self.output = out.dropna()