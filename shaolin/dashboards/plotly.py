from shaolin.core.dashboard import Dashboard, ToggleMenu
import pandas as pd
import numpy as np
import cufflinks as cf
from shaolin.dashboards.colormap import MasterPalette, ColormapPicker
from IPython.core.display import clear_output
from plotly.offline import init_notebook_mode
from IPython.core.display import display
import matplotlib.font_manager



class RangeSlider(Dashboard):
    
    def __init__(self,
                 bordercolor='#444',
                 visible=False,
                 thickness=0.15,
                 bgcolor='#fff',
                 borderwidth=0,
                 **kwargs):
        
        
        
        dash = ['c$N=range_slider_plotly',['###Slider$N=title_slider',['r$N=row_1',['@cp$n=bgcolor&d=Color&val='+bgcolor,'@cp$d=Border&n=bordercolor&val='+bordercolor]],
                                           ['r$N=row_2',['@(0,50,1,'+str(borderwidth)+')$d=Border width&N=borderwidth',
                                                         '@(0.,1.,0.05,'+str(thickness)+')$d=Thickness&N=thickness']],
                                           ['@'+str([visible])+'$d=Visible&n=slider_visible']
                                          ]
               ]
        Dashboard.__init__(self,dash,**kwargs)
        
    @property
    def output(self):
        """visible is a shaolin reserved word so it can be used directly to create a kwargs dict.
        This allows to override the kwargs attribute so visible can be a key.
        """
        kwargs = self.kwargs.copy()
        del(kwargs['slider_visible'])
        kwargs['visible'] = self.slider_visible.value
        return kwargs
    
            

class FontManager(Dashboard):
    
    def __init__(self,title='Font',family='Verdana',
                 size=12, color='black',
                 mode='interactive',
                 **kwargs):
        fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        #print(fonts)
        font_names = [matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in fonts]
        dash = ['c$n=font_manager',['###'+title+'$n=title',
                                    '@select$d=Family&o='+str(font_names)+'&val='+family,
                                    '@(1,50,1,'+str(size)+')$d=Size',
                                    '@cpicker$d=Color&val='+color
                                   ]
               ]
        Dashboard.__init__(self, dash, **kwargs)
        self.family.widget.layout.width = "20em"
        self.color.widget.layout.width = "20em"
        self.family.target.layout.width = "100%"
        self.color.target.layout.width = "100%"

class Ticks(Dashboard):
    
    def __init__(self,
                 showticklabels=True,
                 nticks=6,
                 ticksuffix="",
                 showticksuffix='none',
                 tickprefix='',
                 showtickprefix='none',
                 tickformat='',
                 tickmode='auto',
                 ticks='outside',
                 ticklen=5,
                 tickvals=[],
                 ticktext=[],
                 tickfont={'family':'Verdana'},
                 tickwidth=1,
                 tick0=0,
                 tickangle=-1,
                 dtick=1,
                 tickcolor='#444',
                 title='Ticks',
                 **kwargs):
        show_mode = ['all','first','all','none']
        show_row = ['r$n=row_show',[
                    ['c$N=subcol_1',['@'+str(showticklabels)+'$d=Showticklabels']],
                    ['c$N=subcol_2',['@dd$d=Show suffix&n=showticksuffix&o='+str(show_mode)+'&val='+str(showticksuffix),
                                     '@text$d=suffix&n=ticksuffix&val='+str(showticksuffix)]],
                    ['c$N=subcol_3',['@dd$d=Show prefix&n=showtickprefix&o='+str(show_mode)+'&val='+str(showtickprefix),
                                     '@text$d=prefix&n=tickprefix&val='+str(showtickprefix)]]
               ]]
       
        tickmode_opts = ['auto','linear','array']
        mode_row = ['r$N=mode_row',[['c$N=mscol_1',['@float_text$d=tick0&val='+str(tick0),
                                                    '@(0,500,1,'+str(nticks)+')$d=nticks']],
                                    ['c$N=mscol_2',['@dd$d=tickmode&o='+str(tickmode_opts)+'&val='+str(tickmode),
                                                    '(0.,500.,0.25,'+str(dtick)+')$d=dtick']],
                                   ]
                   ]
        font_m = FontManager(name='tickfont',title='tickfont',mode='interactive')
        format_row = ['r$N=format_row',[font_m,
                                        ['c$N=fcol_1',['@dd$d=ticks&o=["outside","inside",""]',
                                                       '@cp$d=tickcolor',
                                                       '@(0,25,1,'+str(ticklen)+')$d=ticklen',
                                                       '@(0,25,1,'+str(tickwidth)+')$d=tickwidth',
                                                       '@(-1,360,1,'+str(tickangle)+')$d=tickangle',
                                                       '@text$d=tickformat&val=""',
                                                      ]]
                                       ]
                     ]
        toggle_row = ['r$N=toggle_rowb',['[True]$d=show&n=show_togb&mode=passive','[True]$d=mode&n=mode_tog&mode=passive','[True]$d=format&n=format_togb&mode=passive']]
        dash = ['c$n=ticks_col_b',[['##'+title+'$N=ticks_title'],
                             ['r$N=in_row',[['c$N=widget_row_a',[show_row, mode_row]],format_row]],
                             toggle_row
                             
                            ]
               ]
        Dashboard.__init__(self, dash, **kwargs)
        for slider in ['dtick','ticklen','tickwidth','tickangle']:
            getattr(self,slider).target.continuous_update = False
   
    @property
    def output(self):
        kwargs = self.kwargs.copy()
        if kwargs['tickangle'] == -1:
            kwargs['tickangle'] = 'auto'
        return kwargs

class AxisNonTick(Dashboard):
    
    def __init__(self,
                 titlefont={'family':'Verdana'},
                 title='',
                 hoverformat='',
                 zeroline=True,
                 fixedrange=True,
                 showline=True,
                 showgrid=True,
                 showexponent='all',
                 mirror=False,
                 categoryorder='trace',
                 side='bottom',
                 exponentformat='none',
                 autorange=True,
                 rangemode='normal',
                 color='#444',
                 zerolinecolor='#444',
                 linecolor='#444',
                 linewidth=1,
                 zerolinewidth=1,
                 position=0,
                 gridwidth=1,
                 mode='interactive',
                 **kwargs
                ):
    
        col_font = ['c$N=col_font',[FontManager(name='titlefont',title='titlefont',mode='interactive')]]
        
        colors = ['c$n=colors_col',['@cp$d=Color&val='+color,
                                  '@cp$d=Linecolor&val='+linecolor,
                                  '@cp$n=zerolinecolor&d=Zeroline color&val='+zerolinecolor]]
        
        bools = ['c$n=bool_block',['@text$d=Title',
                                   #'@text$d=Title format&n=titleformat',
                                   ['r$n=brow_1',['@'+str([zeroline])+'$d=Zeroline','@'+str([fixedrange])+'$d=Fixedrange']],
                                   ['r$n=brow_2',['@'+str([showline])+'$d=Showline','@'+str([showgrid])+'$d=Showgrid']],
                                   
                                  ]
                      ]
        
        sliders = ['c$n=slider_row_axis',['@(0,50,1,'+str(linewidth)+')$d=linewidth',
                                  '@(0,50,1,'+str(zerolinewidth)+')$d=zerolinewidth',
                                  '@(0.,1.,0.05,'+str(position)+')$d=position',
                                  '@(0,50,1,'+str(gridwidth)+')$d=gridwidth'
                                 ]
          ]
        
        showexponent_opts = ["all","first","last","none" ]
        mirror_opts = {'True': True, "ticks":"ticks",'False': False , "all":"all" , "allticks":"allticks"}
        categoryorder_opts = ["trace" , "category ascending" , "category descending" , "array" ]
        side_opts = ["top" , "bottom" , "left" , "right" ]
        exponentformat_opts = [ "none" , "e" , "E" , "power" , "SI" , "B" ]
        autorange_opts = {'True': True , 'False': False , "reversed":"reversed" } 
        rangemode_opts = ["normal" , "tozero" , "nonnegative"]
        
        enum_opts = ['r$n=enum_row',[['c$n=eo_c1',['@dd$d=showexponent&o='+str(showexponent_opts)+'&val='+str(showexponent),
                                                '@dd$d=exponentformat&o='+str(exponentformat_opts)+'&val='+str(exponentformat),
                                                '@dd$d=categoryorder&o='+str(categoryorder_opts)+'&val='+str(categoryorder),
                                                '@dd$d=side&o='+str(side_opts)+'&val='+str(side)]],
                                    ['c$n=eo_c2',['@dd$d=mirror&o='+str(mirror_opts),
                                                '@dd$d=autorange&o='+str(autorange_opts),
                                                '@dd$d=rangemode&o='+str(rangemode_opts)+'&val='+str(rangemode)]]
                                   ]
                     ]
        
        dash = ['c$N=non_tick_axis',['###Generic parameters$N=non_ticks_title',
                                     ['r$n=non_tick_axis_params',[bools,col_font,enum_opts, sliders, colors]]
                                    ]
                ]
        Dashboard.__init__(self, dash,mode=mode, **kwargs)
        self.autorange.value = autorange
        self.rangemode.value = rangemode
        
    @property
    def output(self):
        return self.kwargs

class Layout(ToggleMenu):
    
    def __init__(self,
                 title='',
                 html_title='Layout',
                 paper_bgcolor='#fff',
                 aspectmode='auto',
                 plot_bgcolor="#fff",
                 height=680,
                 width=1450,
                 mode='interactive',
                 **kwargs):
        aspectmode_opts = ["auto", "cube", "data", "manual"]
        titlefont = FontManager(name='titlefont', mode='interactive', title='Title font')
        layout_dash = ['r$n=main_row',[['c$N=layout_params',['##'+html_title+'$N=layout_title',
                                            '@text$d=Title&val='+title,
                                            '@cp$d=Paper bgcolor&val='+paper_bgcolor,
                                            '@(0,3840,1,'+str(height)+')$d=height','@(0,2160,1,'+str(width)+')$d=width',
                                            '@cp$n=plot_bgcolor&d=Plot bgcolor&val='+plot_bgcolor,
                                            #'dd$d=Aspectmode&val='+aspectmode+'&o='+str(aspectmode_opts)
                                           ]],titlefont
                      ]]
        layout_params = Dashboard(dash=layout_dash,name='layout_params',mode=mode)
        for slider in ['width','height']:
            getattr(layout_params,slider).target.continuous_update = False
        xaxis = Axis(name='xaxis',mode='interactive')
        yaxis = Axis(name='yaxis',mode='interactive')
        margin = Margin(name='margin', mode='interactive')
        ToggleMenu.__init__(self, children=[xaxis,yaxis,margin,layout_params], **kwargs)
        self.observe(self.update)
    
    
    @property
    def output(self):
        kwargs = self.layout_params.kwargs.copy()
        kwargs['xaxis'] = self.xaxis.output
        kwargs['yaxis'] = self.yaxis.output
        kwargs['margin'] = self.margin.kwargs
        kwargs['legend'] = {}
        return kwargs
    
    def update(self, _=None):
        pass
        #clear_output()
        #percent.iplot(kind='bar',layout=self.kwargs)

class Margin(Dashboard):
    
    def __init__(self,
                 l=80,
                 r=80,
                 b=80,
                 t=100,
                 pad=0,
                 autoexpand=True,    
                 title='Margin',
                 **kwargs):
      
        dash = ['c$n=margin_dash',['###'+title+'$N=margin_title',
                                 ['r$N=margin_row1',['@(0,250,1,'+str(l)+')$d=l','@(0,250,1,'+str(r)+')$d=r','@(0,250,1,'+str(b)+')$d=b']],
                                 ['r$N=margin_row2',['@(0,350,1,'+str(t)+')$d=t','@(0,250,1,'+str(pad)+')$d=pad','@'+str([autoexpand])+'$d=autoexpand']]
                                ]
               ]
        Dashboard.__init__(self, dash, **kwargs)
        for slider in ['l','r','b','t','pad']:
            getattr(self,slider).target.continuous_update = False

class Axis(Dashboard):
    
    def __init__(self,title='Axis',mode='interactive', **kwargs):
        
        ticks = Ticks(name='ticks',mode='interactive')
        non_ticks = AxisNonTick(name='non_ticks',mode='interactive')
        slider = RangeSlider(name='rangeslider',mode='interactive')
        dash = ['c$N=axis_parameters',['##'+title+'$n=axis_title',
                                       ticks,
                                       non_ticks,
                                       slider,
                                       'togs$n=buttons&o=["Ticks","Generic","Slider"]&val=Generic&mode=passive'
                                      ]
               ]
        Dashboard.__init__(self, dash, mode=mode, **kwargs)
        self.buttons.observe(self.buttons_logic)
        self.buttons_logic()
        
    def buttons_logic(self, _=None):
        if self.buttons.value == 'Ticks':
            self.ticks.visible = True
            self.non_ticks.visible = False
            self.rangeslider.visible = False
        elif self.buttons.value == 'Slider':
            self.ticks.visible = False
            self.non_ticks.visible = False
            self.rangeslider.visible = True
        else:
            self.ticks.visible = False
            self.non_ticks.visible = True
            self.rangeslider.visible = False
    
    
    @property
    def output(self):
        axis = self.ticks.output.copy()
        axis.update(self.non_ticks.output)
        axis['rangeslider'] = self.rangeslider.output
        return axis
    
import warnings
warnings.filterwarnings("ignore")

class Cufflinks(Dashboard):
    
    def __init__(self, df, plot_kwargs=None,mode='interactive',theme='space', **kwargs):
        
        if plot_kwargs is None:
            self.plot_kwargs = {'title':'Bar'}
        else:
            self.plot_kwargs = plot_kwargs
        
        self._df = df
        col_opts = [''] + list(df.columns.values)
        col_opts_2 = col_opts.copy()
        col_opts_2[0] = "None"
        self._col_opts = dict(zip(col_opts_2,col_opts))
        cmap = ColormapPicker(name='cmap', mode='interactive')
        layout = Layout(name='layout_d', mode='interactive')
        kind_opts = ["scatter","bar","box",
                     "spread","ratio","heatmap",
                     "surface","histogram", "bubble",
                     "bubble3d","scatter3d","scattergeo","choroplet"]
        color_scales = list(cf.colors.get_scales().keys())+[None]
        dash = ['c$N=cufflinks',
                [
                 ['r$n=general_params',['@sm$d=columns&o='+str(col_opts[1:]),['c$n=aux_col_1',['@dd$d=Kind&o='+str(kind_opts),'@[False]$d=subplots',
                                                                                               '@[False]$d=Shared xaxes','@[False]$d=Shared yaxes']],
                                        ['c$N=titles_col',["@text$d=Title","@text$d=xTitle","@text$d=yTitle","@text$d=zTitle"]],
                                        '@select$d=Theme&o='+str(cf.getThemes())+'&val='+theme,
                                        ['c$n=colorp_row',['@dd$d=categories&o='+str(self._col_opts),'@sm$d=secondary_y&o='+str(self._col_opts),'@dd$d=Color scale',cmap]]
                                       ]
                 ],
                 ['r$n=scatter_params',[['c$n=axis_col_xyz',['@dd$d=x&o='+str(self._col_opts),'@dd$d=y&o='+str(self._col_opts),'@dd$d=z&o='+str(self._col_opts)]],
                                        ['c$n=marker_prop_col',['@dd$d=text&o='+str(self._col_opts),'@(1,500,1,12)$d=Size',
                                      '@dd$d=Marker mode&o=["lines","markers","text","lines+markers","markers+text","lines+text","lines+markers+text"]']],
                                        '@False$d=fill','@dd$d=symbol&o=["dot","cross","square","triangle-down","triangle-right","triangle-left","triangle-up","x"]',
                                        '@dd$d=dash&o=["solid","dash","dashdot","dot"]'
                                     ]],
                 ['r$N=barmode_row',['@ddown$d=barmode&o=["stack", "group", "overlay"]',
                                     ['c$N=mini_bar_col',['@togs$d=Orientation&n=ori&o=["v","h"]&val=v',
                                                          "@(0.,1.,0.05,1.)$d=Bargap",
                                                          "@(0.,1.,0.05,1.)$d=Bargroupgap"]],
                                     ['c$N=hist_col',["@(0,500,1,0)$d=Bins",
                                     '@dd$d=Histnorm&o=["frequency","percent","probaility","density","probability density"]',
                                     '@dd$d=Histfunc&o=["count","sum","avg","min","max"]']],
                                     
                                    ]],
                 layout,
                 ['r$n=btn_rows',['[False]$d=Layout&n=btn_layout','@False$d=Apply layout',
                                         '@btn$d=Update&n=update_btn']
                 ]
                ]
               ]
        
        Dashboard.__init__(self, dash, mode=mode, **kwargs)
        self.theme.target.layout.width = "100%"
        self.theme.widget.layout.width = "100%"
        
        self.url = ''#not used, but prepared for working online.
        self._init_widget_values()
        self.observe(self.update)
        self.btn_layout.observe(self._layout_toggle)
        
    
    def _init_widget_values(self,_=None):
        self.categories.value = ''
        color_scales = list(cf.colors.get_scales().keys())+[None]
        self.color_scale.options = dict(zip([str(x) for x in color_scales],color_scales))
        self.color_scale.value = None
        self.columns.value = tuple(self._df.columns.values[:])
        self.x.value = self._col_opts["None"]
        self.y.value = self._col_opts["None"]
        self.z.value = self._col_opts["None"]
    
    @property
    def df(self):
        return self._df
    
    @df.setter
    def df(self, value):
        """This allows for on the fly data updating so you only need
        to create one BarPlot Dashboard and instantiate the widgets once"""
        self._update_columns(list(value.columns.values))
        self._df = value
        self.update()
        clear_output()
    
    def _update_columns(self, cols):
        """This is for avoiding trailet errors due to invalid selections
        when updating the widgets options values """
        current = set(self.columns.target.options)
        s_cols = set(cols)
        inter = current.intersection(cols)
        if inter == set(()):
            oldopt = self.columns.target.options + ['dummy']
            self.columns.target.options = oldopt
            self.columns.value = ('dummy',)
            newopt = ['dummy'] + cols
            self.columns.target.options = newopt
            self.columns.value = (cols[0],)
            self.columns.target.options = cols
        else:
            self.columns.value = tuple(current.intersection(cols))
            self.columns.target.options = cols
    
    def _layout_toggle(self, _=None):
        if self.btn_layout.value:
            self.layout_d.visible = True
        else:
            self.layout_d.visible = False
        self.update()
    
    
    def update_layout(self,_=None):
        if self.kind.value in ['scatter','scatter3d','bubble', 'bubble3d', 'heatmap']:
            self.scatter_params.visible = True
        else:
            self.scatter_params.visible = False
        if self.kind.value in ['bar', 'histogram']:
            self.barmode_row.visible = True
            if self.kind.value == 'histogram':
                self.hist_col.visible = True
            else:
                self.hist_col.visible = False
        else:
            self.barmode_row.visible = False
    def update(self, _=None):
            """Map the widgets values to cufflinks parameters and creates a plot"""
            clear_output(wait=True)#Is there any way to avoid the clipping?
            self.update_layout()
            if self.bargap.value == 1.0:
                bgap = None
            else:
                bgap = self.bargap.value
            if self.bargroupgap.value == 1.0:
                bgroupgap = None
            else:
                bgroupgap = self.bargroupgap.value
            if self.bins.value == 0:
                bins = None
            else:
                bins = self.bins.value
        #try:
            if self.apply_layout.value:
                self.layout_d.visible = True
                layout = self.layout_d.output.copy()
                layout['barmode'] = self.barmode.value #barmode must be in layout dict to take effect if you are using layout param
                self._df[list(self.columns.value)].iplot(barmode=self.barmode.value,
                                                         colors=self.cmap.map_data(range(len(self.columns.value)), hex=True),
                                                         theme=self.theme.value,
                                                         x=self.x.value,
                                                         y=self.y.value,
                                                         z=self.z.value,
                                                         mode=self.marker_mode.value,
                                                         title=self.title.value,
                                                         xTitle=self.xtitle.value,
                                                         yTitle=self.ytitle.value,
                                                         zTitle=self.ztitle.value,
                                                         colorscale=self.color_scale.value,
                                                         text=self.text.value,
                                                         size=self.size.value,
                                                         layout_update=layout) #weird bug where kind and colors sometimes doesnt apply propperly
            else:
                self.layout_d.visible = False
                self._df[list(self.columns.value)].iplot(kind=self.kind.value,
                                                         barmode=self.barmode.value,
                                                         colors=self.cmap.map_data(range(len(self.columns.value)), hex=True),
                                                         theme=self.theme.value,
                                                         x=self.x.value,
                                                         y=self.y.value,
                                                         z=self.z.value,
                                                         mode=self.marker_mode.value,
                                                         title=self.title.value,
                                                         xTitle=self.xtitle.value,
                                                         yTitle=self.ytitle.value,
                                                         zTitle=self.ztitle.value,
                                                         colorscale=self.color_scale.value,
                                                         text=self.text.value,
                                                         size=self.size.value,
                                                         fill=self.fill.value,
                                                         subplots=self.subplots.value,
                                                         shared_xaxes=self.shared_xaxes.value,
                                                         shared_yaxes=self.shared_yaxes.value,
                                                         symbol=self.symbol.value,
                                                         bins=bins,
                                                         bargap=bgap,
                                                         bargroupgap=bgroupgap,
                                                         orientation=self.ori.value,
                                                         dash=self.dash.value,
                                                         histnorm=self.histnorm.value,
                                                         histfunc=self.histfunc.value,
                                                         categories=self.categories.value,
                                                         secondary_y=list(self.secondary_y.value)


                                                        )
        #except:
            #This is really poorly done, but at least avoid temporal errors caused due to possible javascript desync.
            #happens rarely when having tons of open tabs in your browser.
        #   print('Error')