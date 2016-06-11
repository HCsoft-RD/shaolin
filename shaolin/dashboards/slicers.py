# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 23:17:20 2016

@author: Guillem Duran Ballester for HCSoft
"""
import numpy as np
import datetime
import pandas as  pd
import math

from seaborn.palettes import diverging_palette
from matplotlib.colors import LinearSegmentedColormap

from IPython.display import Image
from seaborn.rcmod import axes_style 
import matplotlib.pyplot as plt

from shaolin.core.dashboard import Dashboard
from shaolin.dashboards.colormap import MasterPalette

class AxisPlotLight(Dashboard):
    def __init__(self,
                 data,
                 mask,
                 strf='%a\n%d\n%h\n%Y',
                 font_size=20,
                 pct_space=0.1,
                 width="20em",
                 height="3em",
                 cmap=None,
                 orient='horizontal',
                 **kwargs
                ):
        if cmap is None:
            colors = diverging_palette(h_neg=38, h_pos=167, s=99, l=66, sep=39, n=256, center='light')
            cmap = LinearSegmentedColormap.from_list("interactive", colors)
            cmap._init()
            cmap._set_extremes()
            self.cmap = cmap
        else:
            self.cmap = cmap
            
        self._width = width
        self._height = height
        self.data = data
        self.mask = mask
        if self.is_time_array(data):
            start = 'HTML$N=start&val='+pd.to_datetime(self.data[0]).strftime(strf)                   
            end ='HTML$N=end&val='+pd.to_datetime(self.data[-1]).strftime(strf)               
            #self.start = TimeDisplay(datetime=pd.to_datetime(self.data[0]), strf=self.strf.value)
            #self.end = TimeDisplay(datetime=pd.to_datetime(self.data[-1]), strf=self.strf.value)
        else:
            start = 'HTML$N=start&val='+str(self.data[0])
            end = 'HTML$N=end&val='+str(self.data[-1])
        self.strf = strf
        self.font_size = font_size
        self.pct_space = pct_space
        self.orient = orient
            
        plot = 'HTML$N=plot'
        dash = ['c$N=AxisPlot',
                 [
                    ['r$N=plot_box',[start, plot, end]]
                 ]
               ]
        Dashboard.__init__(self, dash, **kwargs)        
        self.plot.value = self.plot_axis(data=self.data,
                                   idx=self.mask,
                                   cmap=self.cmap,
                                   strf=self.strf,
                                   fontsize=self.font_size,
                                   pct_space=self.pct_space
                                  )
        self.observe(self._trigger_update)
        self._trigger_update()
        self.update()
    
    def _trigger_update(self, _=None ):
        try:
            self.update()
        except ValueError:#when there is not a valid strf while typing 
            pass
    def update(self, data=None, mask=None):
        if data is None:
            data = self.data
        if mask is None:
            mask = self.mask
        self.plot.value = self.plot_axis(data,
                                   idx=mask,
                                   cmap=self.cmap,
                                   strf=self.strf,
                                   fontsize=self.font_size,
                                   pct_space=self.pct_space
                                  )
        self.plot.widget.layout.width =self._width
        self.plot.target.layout.width = "100%"
        self.plot.widget.layout.height = self._height
        self.plot.target.layout.height = "100%"
        self.data = data
        self.mask = mask
        if self.is_time_array(data):
            self.start.target.description = pd.to_datetime(self.data[0]).strftime(self.strf)
            self.end.target.description = pd.to_datetime(self.data[-1]).strftime(self.strf)
        else:
            self.start.target.description = str(self.data[0])
            self.end.target.description = str(self.data[-1])
        
        
    @staticmethod
    def is_time(val):
        int_or_float = (int, np.int, np.int16, np.int0, np.int8,
                        np.int32, np.int64, np.float, np.float128,
                        np.float16, np.float32, np.float64, float)
        time_type = (datetime.date, datetime.datetime, np.datetime64)
        
        if isinstance(val,time_type):
            return True
        elif isinstance(val,int_or_float):
            return False
        try:
            _ = pd.to_datetime(val)
            _ = val.strftime('%Y')
            return True
        except ValueError:
            return False 
        except AttributeError:
            return False
    @staticmethod
    def is_time_array(val):
        return np.all([AxisPlotLight.is_time(x) for x in val])
    
    def fig_to_html(self, fig, img_class=''):
        """This is a hack that converts a matplotlib like fig to an HTML image div"""
        from io import BytesIO
        import base64
        import warnings
        warnings.filterwarnings('ignore')
        imgdata = BytesIO()
        fig.savefig(imgdata, format='png',bbox_inches='tight',dpi=160, transparent=True)
        imgdata.seek(0)  # rewind the data
        svg_dta = imgdata.getvalue()
        svg_image = Image(svg_dta)#
        svg_b64 = base64.b64encode(svg_image.data).decode()
        css = '''<style>
                        .cmap-axis {width:'''+self._width+''' !important;
                               height:'''+self._height+'''em !important;
                               margin:15px;
                               align:left;}

                </style>'''
        height = self.plot.target.layout.height
        width = self.plot.target.layout.width
        return '<img class="cmap '+img_class+'" height="'+str(height)+'" width="'\
                +str(width)+'" src="data:image/png;base64,'+svg_b64+'" />'
        
        #return '<img class="cmap-axis" '+img_class+'" src="data:image/png;base64,'+svg_b64+'" />'#+css
    
    
        
    def plot_axis(self,data,idx,cmap,strf='%a\n%d\n%h\n%Y',fontsize=20, pct_space=0.1):
        #display original array as index
        xticks_ix = int(math.ceil(len(data)/100)*1/pct_space)
        xticks_vals = np.arange(len(data))[::xticks_ix]
        xticks_labels = data[::xticks_ix]
        with axes_style("white"):
                f, ax = plt.subplots(figsize=(10, 1))
        if True:#idx.ndim <= 1:
            idx_plot = np.tile(idx, (1, 1))
        else:
            idx_plot = idx
            
        ax.pcolormesh(idx_plot,cmap=cmap)
        if self.is_time_array(data):
            ticks = pd.DatetimeIndex(xticks_labels).to_pydatetime()
            _ = plt.xticks(xticks_vals, [x.strftime(strf) for x in ticks], fontsize = fontsize,
                           rotation=self.orient)
        else:
            _ = plt.xticks(xticks_vals, xticks_labels, fontsize = fontsize,
                           rotation=self.orient)
        ax.axis([0,len(data), 0, 1])
        ax.axes.get_yaxis().set_visible(False)
        #f.tight_layout()

        html =  self.fig_to_html(f,img_class='axisplot')
        plt.close(f)
        return html
        
class AxisPlot(Dashboard):
    def __init__(self,
                 data,
                 mask,
                 strf='%a\n%d\n%h\n%Y',
                 fontsize=20,
                 pct_space=0.1,
                 **kwargs
                ):
        self.data = data
        self.mask = mask
        if self.is_time_array(data):
            start = 'HTML$N=start&val='+pd.to_datetime(self.data[0]).strftime(strf)                   
            end ='HTML$N=end&val='+pd.to_datetime(self.data[-1]).strftime(strf)
            strf = '@text$N=strf&val='+strf                    
            #self.start = TimeDisplay(datetime=pd.to_datetime(self.data[0]), strf=self.strf.value)
            #self.end = TimeDisplay(datetime=pd.to_datetime(self.data[-1]), strf=self.strf.value)
        else:
            start = 'HTML$N=start&val='+str(self.data[0])
            end = 'HTML$N=end&val='+str(self.data[-1])
            strf = strf+'$N=strf&v=0'  
            
        plot = 'HTML$N=plot'
        dash = ['c$N=AxisPlot',
                [
                    ['r$N=plot_box',[start, plot, end]],
                    ['r$N=buttons_row',['@btn$d=Options&N=opt_button_open']],
                    ['c$N=opt_box&v=0',[
                                    ['r$N=opt_row_1',['@(1,25,1,18)$d=Font size',
                                                      '@rad$N=vertical&d=Orient&o=["horizontal","vertical"]',
                                                      strf, '@(0.,1.,0.02,0.1)$N=pct_space&d=Label spacing',
                                                      ['c$N=mini_box',['@(1.,100.,0.05,8.75)$N=img_height&d=Height',
                                                                       '@(1.,100.,0.05,50.)$N=img_width&d=Width']
                                                      ]
                                                    ]
                                    ],
                                    ['r$N=opt_row_2',['@btn$d=Cmap&N=cmap_button_open','@btn$d=Close&N=opt_button_close']
                                    ]
                                   ]
                    ],
                    ['c$N=cmap_box&v=0',[MasterPalette(name='palette', mode='interactive'),
                                         '@btn$d=Close&N=cmap_button_close']
                    ]
                 ]
                ]
        Dashboard.__init__(self, dash, **kwargs)
        for opt in self.palette.buttons.target.options.values():
            setattr(getattr(getattr(self.palette,opt),'as_cmap'),'value',True)
        
        self.plot.value = self.plot_axis(data=self.data,
                                   idx=self.mask,
                                   cmap=self.palette.cmap,
                                   strf=self.strf.value,
                                   fontsize=self.font_size.value,
                                   pct_space=self.pct_space.value
                                  )
        self.opt_button_open.observe(self._on_optopen_click)
        self.opt_button_close.observe(self._on_optclose_click)        
        self.cmap_button_open.observe(self._on_cmopen_click)
        self.cmap_button_close.observe(self._on_cmclose_click)
        self.observe(self._trigger_update)
        self._trigger_update()
        self.update()
    def _on_optopen_click(self, _ ):
        self.opt_box.visible = True
        
    def _on_optclose_click(self, _):
        self.opt_box.visible = False
    def _on_cmopen_click(self, _):
        self.cmap_box.visible = True
    def _on_cmclose_click(self, _):
        self.cmap_box.visible = False
        self.update()
    
    def _trigger_update(self, _=None ):
        try:
            self.update()
        except ValueError:#when there is not a valid strf while typing 
            pass
    def update(self, data=None, mask=None):
        if data is None:
            data = self.data
        if mask is None:
            mask = self.mask
        self.plot.value = self.plot_axis(data,
                                   idx=mask,
                                   cmap=self.palette.cmap,
                                   strf=self.strf.value,
                                   fontsize=self.font_size.value,
                                   pct_space=self.pct_space.value
                                  )
        self.plot.widget.layout.width = str(self.img_width.value)+'em'
        self.plot.target.layout.width = "100%"
        self.plot.widget.layout.height = str(self.img_height.value)+'em'
        self.plot.target.layout.height = "100%"
        self.data = data
        self.mask = mask
        if self.is_time_array(data):
            self.start.target.description = pd.to_datetime(self.data[0]).strftime(self.strf.value)
            self.end.target.description = pd.to_datetime(self.data[-1]).strftime(self.strf.value)
        else:
            self.start.target.description = str(self.data[0])
            self.end.target.description = str(self.data[-1])
        
        
    @staticmethod
    def is_time(val):
        int_or_float = (int, np.int, np.int16, np.int0, np.int8,
                        np.int32, np.int64, np.float, np.float128,
                        np.float16, np.float32, np.float64, float)
        time_type = (datetime.date, datetime.datetime, np.datetime64)
        
        if isinstance(val,time_type):
            return True
        elif isinstance(val,int_or_float):
            return False
        try:
            _ = pd.to_datetime(val)
            _ = val.strftime('%Y')
            return True
        except ValueError:
            return False 
        except AttributeError:
            return False
    @staticmethod
    def is_time_array(val):
        return np.all([AxisPlot.is_time(x) for x in val])
    
    def fig_to_html(self, fig, img_class=''):
        """This is a hack that converts a matplotlib like fig to an HTML image div"""
        from io import BytesIO
        import base64
        import warnings
        warnings.filterwarnings('ignore')
        imgdata = BytesIO()
        fig.savefig(imgdata, format='png',bbox_inches='tight',dpi=160, transparent=True)
        imgdata.seek(0)  # rewind the data
        svg_dta = imgdata.getvalue()
        svg_image = Image(svg_dta)#
        svg_b64 = base64.b64encode(svg_image.data).decode()
        css = '''<style>
                        .cmap-axis {width:'''+str(self.img_width.value)+'''em !important;
                               height:'''+str(self.img_height.value)+'''em !important;
                               margin:15px;
                               align:left;}

                </style>'''
        height = self.plot.target.layout.height
        width = self.plot.target.layout.width
        return '<img class="cmap '+img_class+'" height="'+str(height)+'" width="'\
                +str(width)+'" src="data:image/png;base64,'+svg_b64+'" />'
        
        #return '<img class="cmap-axis" '+img_class+'" src="data:image/png;base64,'+svg_b64+'" />'#+css
    
    
        
    def plot_axis(self,data,idx,cmap,strf='%a\n%d\n%h\n%Y',fontsize=20, pct_space=0.1):
        #display original array as index
        xticks_ix = int(math.ceil(len(data)/100)*1/pct_space)
        xticks_vals = np.arange(len(data))[::xticks_ix]
        xticks_labels = data[::xticks_ix]
        with axes_style("white"):
                f, ax = plt.subplots(figsize=(10, 1))
        if True:#idx.ndim <= 1:
            idx_plot = np.tile(idx, (1, 1))
        else:
            idx_plot = idx
            
        ax.pcolormesh(idx_plot,cmap=cmap)
        if self.is_time_array(data):
            ticks = pd.DatetimeIndex(xticks_labels).to_pydatetime()
            _ = plt.xticks(xticks_vals, [x.strftime(strf) for x in ticks], fontsize = fontsize,
                           rotation=self.vertical.value)
        else:
            _ = plt.xticks(xticks_vals, xticks_labels, fontsize = fontsize,
                           rotation=self.vertical.value)
        ax.axis([0,len(data), 0, 1])
        ax.axes.get_yaxis().set_visible(False)
        #f.tight_layout()

        html =  self.fig_to_html(f,img_class='axisplot')
        plt.close(f)
        return html
        
class ArraySlicer(Dashboard):
    """Array slicer widget. Performs arbitary slicing in a array-like object"""
    def __init__(self,
                 data,
                 start=0,
                 end=-1,
                 step=1,
                 display='sliders',
                 slice_mode='single',
                 description='Slicer',
                 strf='%d\n%h\n%Y\n%T',
                 **kwargs):
        self.strf = strf
        if AxisPlotLight.is_time_array(data):
            st = str(self.strf)
            st = st.replace('\n',' ')
            time_data = [pd.to_datetime(x).strftime(st) for x in data]
            dd_sel = ['@sel$N=dd_selector&o='+str(list(time_data))]
            sel_sli = ['@selslider$N=sel_sli&o='+str(list(time_data))]
            self._data = time_data
            self._ast_vals = False
        
        elif isinstance(data[0],str):
            dd_sel = ['@sel$N=dd_selector&o='+str(list(data))]
            sel_sli = ['@selslider$N=sel_sli&o='+str(list(data))]
            self._data = data
            self._ast_vals = False
        else:
            self._data = [str(x) for x in data]
            dd_sel = ['@sel$N=dd_selector&o=["'+str(list(data)[0])+'"]']
            sel_sli = ['@selslider$N=sel_sli&o=["'+str(list(data)[0])+'"]']
            self._ast_vals = True
        if end==-1:
            end = len(data)
        
        self.idx = np.ones(len(data),dtype=bool)
        plot = AxisPlotLight(data,self.idx, name='plot',strf=strf)
        dash = ['c$N=array_slicer',
                [['###'+description+'$N=title_slicer'],
                 ['r$N=plot_row',[plot]],
                 dd_sel,
                 sel_sli,
                 ['r$N=controls_row',[['r$N=columns_mode_row',['@togs$N=slice_mode&o=["single", "slice"]&val='+str(slice_mode),
                                                               ]],


                                      ['c$N=sliders_col',['@('+str(-len(data)+1)+','+str(end)+',1,'+str(start)+')$N=start_slider&d=Start',
                                                          '@('+str(-len(data)+1)+','+str(end)+',1,'+str(end)+')$N=end_slider&d=End',
                                                          '@(1,'+str(len(data)-1)+',1,'+str(step)+')$N=step_slider&d=Step'
                                                         ]

                                      ],
                                     ]
                 ]
                ]
               ]    
        Dashboard.__init__(self, dash, mode='interactive', **kwargs)
        
        if self._ast_vals:
            self.dd_selector.target.options = [str(x) for x in data]
            self.sel_sli.target.options = [str(x) for x in data]
        self.sel_sli.target.continuous_update=False
        self.start_slider.target.continuous_update=False
        self.dd_selector.target.layout.width = "12em"
        self.dd_selector.observe(self._link_dropdown)
        self.sel_sli.observe(self._link_sel_sli)
        self.start_slider.observe(self._link_start_sli)
        self.observe(self.update)
        self.update()
        self.data = self._data.copy()
    def _link_dropdown(self, _=None):
        try:
            self.sel_sli.value = self.dd_selector.value
            self.start_slider.value = list(self._data).index(self.dd_selector.value)
        except:
            pass
    
    def _link_sel_sli(self, _=None):
        try:
            self.dd_selector.value = self.sel_sli.value  
            self.start_slider.value = list(self._data).index(self.dd_selector.value)
        except:
            pass
        
    def _link_start_sli(self, _=None):
        try:
            if self.start_slider.value >= len(self._data):
                self.dd_selector.value = list(self._data)[-1]
                self.sel_sli.value = list(self._data)[-1]
            else:
                self.dd_selector.value = list(self._data)[self.start_slider.value]
                self.sel_sli.value = list(self._data)[self.start_slider.value]
        except:
            pass
    
    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, val):
        new_end = len(val)
        old_end = len(self._data)
        self._data = val
        if new_end != old_end:

            if AxisPlotLight.is_time_array(val):

                st = str(self.strf) 
                st = st.replace('\n',' ')
                time_data = [pd.to_datetime(x).strftime(st) for x in val]
                self._data = time_data
                if old_end < new_end:
                    self.dd_selector.target.options = list(time_data)
                    self.dd_selector.target.value = list(time_data)[0]
                else:
                    
                    self.dd_selector.target.value = list(time_data)[0]
                    self.dd_selector.target.options = list(time_data)
                    
            elif self._ast_vals:
                self._data = [str(x) for x in val]
                if old_end < new_end:
                    self.dd_selector.target.options = [str(x) for x in self._data]
                    self.dd_selector.target.value = str(list(self._data)[0])
                else:
                    self.dd_selector.target.value = str(list(self._data)[0])
                    self.dd_selector.target.options = [str(x) for x in self._data]
            else:
               
                if old_end < new_end:
                    self.dd_selector.target.options = list(self._data)
                    self.dd_selector.target.value = list(self._data)[0]
                else:
                    self.dd_selector.target.value = list(self._data)[0]
                    self.dd_selector.target.options = list(self._data)
            if old_end < new_end:
                self.start_slider.target.max = new_end
                self.dd_selector.target.options = list(self._data)
                self.dd_selector.target.value = list(self._data)[0]
                #self.start_slider.target.value = new_end
                self.start_slider.target.min = -new_end +1
                self.end_slider.target.max = new_end
                self.end_slider.target.value = new_end
                self.end_slider.target.min = -new_end +1   
            else:
                self.start_slider.target.max = new_end
                self.start_slider.target.min = -new_end +1
                self.dd_selector.target.value = list(self._data)[0]
                self.dd_selector.target.options = list(self._data)
                #self.dd_selector.target.value = list(self._data)[0]
                #self.start_slider.target.value = new_end
                
                self.end_slider.target.value = new_end
                self.end_slider.target.max = new_end
                self.end_slider.target.min = -new_end +1            
            self.step_slider.target.max = new_end-1
        #self.sel_sli.options = list(self._data)
        self._link_dropdown()

    def filter_index(self):
        new_idx = np.zeros(len(self._data), dtype=bool)
        if self.slice_mode.value == 'single':
            if len(self.data) <=10:
                new_idx[list(self._data).index(self.dd_selector.value)] = True
            else:
                if self.start_slider.value < len(self._data):
                    new_idx[self.start_slider.value] = True
                else:
                    new_idx[-1] = True
        else:
            if self.end_slider.value <= len(self._data)-1:
                 new_idx[self.start_slider.value:\
                        self.end_slider.value:\
                        self.step_slider.value] = True
            else:
                new_idx[self.start_slider.value::self.step_slider.value] = True
                #new_idx[-1] = True
        self.idx = new_idx        
    
    
    def update_mode(self):
        if self.slice_mode.value == 'single':
            if len(self.data) <=15:
                self.plot_row.visible = False
                self.dd_selector.visible = True
                self.sel_sli.visible = True
                self.start_slider.visible = False
            else:
                self.start_slider.visible = True
                self.plot_row.visible = True
                self.dd_selector.visible = False
                self.sel_sli.visible = True
            self.end_slider.visible = False
            self.step_slider.visible = False
        else:
            self.plot_row.visible = True
            self.dd_selector.visible = False
            self.sel_sli.visible = True
            self.end_slider.visible = True
            self.step_slider.visible = True
            self.start_slider.visible = True
    

    def update_widgets(self):
        L = len(self._data)
        for w in ['start_slider', 'end_slider', 'step_slider']:
            if w != 'step_slider':
                getattr(self, w).target.min = -L
            getattr(self, w).target.max = L
        self.update_mode()
        self.plot.update(self.data, self.idx)


    def update(self,_=None, data=None):
        if not data is None:
            self._data = data
            self.idx = np.ones(len(data),dtype=bool)
        self.filter_index()
        self.update_widgets()




class DataFrameSlicer(Dashboard):
    
    def __init__(self, df,description='DataFrame', **kwargs):
        self.df = df
        self.output = None
        dash =['r$N=df_slicer',
               [
                '##'+description+'$N=description_text',
                ArraySlicer(df.index.values, name='index_slicer', description='index'),
                ArraySlicer(df.columns.values, name='columns_slicer', description='columns')
               ]
              ]
        Dashboard.__init__(self, dash, mode='interactive', **kwargs)
        self.observe(self.update)
        self.update()
    
    @property
    def description(self):
        return self.df.columns[self.columns_slicer.idx].values[0]
    
    @property
    def data(self):
        return self.df
    @data.setter
    def data(self, val):
        self.df = val
        self.index_slicer.data = val.index.values
        self.columns_slicer.data = val.columns.values
        self.update()
        
    def _init_layout(self):
        self.index_slicer.plot.img_height.value = 3.
        self.index_slicer.plot.img_width.value = 20.
        self.columns_slicer.plot.img_height.value = 3.
        self.columns_slicer.plot.img_width.value = 20.
    
    def update(self, _=None):
        self.output = self.df.ix[self.index_slicer.idx,self.columns_slicer.idx]

class PanelSlicer(Dashboard):
    
    def __init__(self, panel,description='Panel', mode='interactive', **kwargs):
        self.panel = panel
        self.output = None
        if description == '':
            desc_title = '##'+description+'$N=pslicer_text&v=0'
        else:
            desc_title = '##'+description+'$N=pslicer_text'
        dash =['c$N=panel_slicer',
               [
                desc_title,
                ['r$N=panel_slicer_row',
                 [ArraySlicer(panel.items.values, name='items_slicer', description='items'),
                  ArraySlicer(panel.major_axis.values, name='major_axis_slicer', description='major_axis'),
                  ArraySlicer(panel.minor_axis.values, name='minor_axis_slicer', description='minor_axis')
                 ]
                ]
               ]
              ]
        Dashboard.__init__(self, dash, mode=mode, **kwargs)
        self.observe(self.update)
        self.update()
    
    
    @property
    def data(self):
        return self.panel
    @data.setter
    def data(self, val):
        self.panel = val
        self.update()
        
    
    def update(self, _=None):
        self.output = self.panel.ix[self.items_slicer.idx,self.major_axis_slicer.idx, self.minor_axis_slicer.idx]

class Panel4DSlicer(Dashboard):
    
    def __init__(self, panel4D,description='Panel', mode='interactive', **kwargs):
        self.panel4D = panel4D
        self.output = None
        if description == '':
            desc_title = '##'+description+'$N=pslicer_text&v=0'
        else:
            desc_title = '##'+description+'$N=pslicer_text'
            
        labels_slicer = ArraySlicer(panel4D.labels.values, name='labels_slicer', description='labels')
        items_slicer = ArraySlicer(panel4D.items.values, name='items_slicer', description='items')
        dash =['c$N=p4d_slicer',
               [
                desc_title,
                ['r$N=p4d_slicer_row',
                 [labels_slicer,
                  items_slicer,
                  ArraySlicer(panel4D.major_axis.values, name='major_axis_slicer', description='major_axis'),
                  ArraySlicer(panel4D.minor_axis.values, name='minor_axis_slicer', description='minor_axis')
                 ]
                ]
               ]
              ]
        Dashboard.__init__(self, dash, mode=mode, **kwargs)
        self.observe(self.update)
        self.update()
    
    
    @property
    def data(self):
        return self.panel
    @data.setter
    def data(self, val):
        self.panel = val
        self.update()
        
    
    def update(self, _=None):
        self.output = self.panel4D.ix[self.labels_slicer.idx,
                                    self.items_slicer.idx,
                                    self.major_axis_slicer.idx,
                                    self.minor_axis_slicer.idx]