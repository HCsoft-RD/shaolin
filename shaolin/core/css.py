# -*- coding: utf-8 -*-
"""
Created on Tue May 24 08:44:17 2016

@author: Guillem Duran Ballester for HCSoft.
"""

import pickle
import ipywidgets as wid

from .stateless_dashboard import StatelessDashboard
        
class CssKeyword(StatelessDashboard):
    """class for managing a css numeric attribute"""
    def __init__(self, numeric=False, default_val=50, default_unit='%', default=True, mode='interactive', **kwargs):
        if numeric:
            attr_type = 'Numeric'
        else:
            attr_type = 'Text'
        dashboard = ['r$N=css_keyword_sel',
                        ['###'+str(attr_type)+'$N=name_label',
                         '@text$N=text_val&v=0&val='+str(default_val)+default_unit,
                         '@(0.,100,0.25,'+str(default_val)+')$N=num_value',
                         '@togs$N=units&o=["%","px","em","cm"]&val='+default_unit,
                         'Default$N=def_label','[[True]]$N=def_display','@('+str(default)+')$n=default',
                         'Apply to$N=css_label','@togs$N=css_target&o=["widget", "target"]&val=target',
                         'Text$N=kw_mode_label', '@('+str(not numeric)+')$n=kw_mode_val',
                        ]
                    ]
        StatelessDashboard.__init__(self,dashboard,func=self.update, mode=mode, **kwargs)
        self._numeric = numeric
        if not self._numeric:
            self._text_mode_dashboard()
        
        self._manual_css_settings()
        self.observe(self._custom_linking)
        self.observe(self._kw_mode_update)
        self.observe(self.update)
        self.output = {}
        self.update()
        self._kw_mode_update()
                
    @property
    def numeric(self):
        return self._numeric
    @numeric.setter
    def numeric(self, value):
        
        if value and not self.numeric and self.kw_mode_val.value:
                self.num_board_dashboard()
        elif not value and self.numeric and not self.kw_mode_val.value:
                self.text_mode_dashboard()
        self._numeric = value
        self.update()
    
    def _manual_css_settings(self):
        """Styling set using the underlying ipywidgets interface"""
        self.def_display.target.readout = 'Invalid syntax'
        self.def_label.target.layout.padding = "6px"
        self.def_label.target.layout.width = "4em"
        self.kw_mode_label.target.layout.padding = "6px"
        self.css_target.target.layout.wodth = "3em"
        self.name_label.target.layout.width = "110%"
        self.text_val.target.layout.width="100%"
        self.default.widget.layout.width = "3em"
        self.kw_mode_val.widget.width='8em'
        self.widget.layout.height = '3em'
    
    def text_mode_dashboard(self):
        """Dispalys only the text widget"""
        self.kw_mode_val.value = True
        self.kw_mode_val.visible = False
        self.kw_mode_label.visible = False
        self.kw_mode_val.value = True
        self.name_label.text = 'Text'
        
        
    def num_board_dashboard(self):
        """Can switch between text and num"""
        self.kw_mode_val.value = False
        self.kw_mode_val.visible = True
        self.kw_mode_label.visible = True
        self.kw_mode_val.value = False
        self.name_label.text = 'Numeric'
       
    
    
    def _kw_mode_update(self, _=None):
        
        if self.kw_mode_val.value:
            self.text_val.visible = True
            self.num_value.visible = False
            self.units.visible = False
        else:
            self.text_val.visible = False
            self.num_value.visible = True
            self.units.visible = True
        
    def _custom_linking(self, _=None):
        """custom display linking"""
        if self.default.value:
            self.def_display.visible = True
            self.def_display.value = True
        else:
            self.def_display.visible = False
        try:    
            if self.numeric:  
                if self.kw_mode_val.value:
                    if self.text_val.value[-1] == '%':
                        self.num_value.value = float(self.text_val.value[:-1])
                        self.units.value = self.text_val.value[-1]
                    elif self.text_val.value[-2:] in self.units.options:
                        self.num_value.value = float(self.text_val.value[:-2])
                        self.units.value = self.text_val.value[-2:]
                    else:
                        self.def_display.visible = True
                        self.def_display.value = False

                elif not self.kw_mode_val.value and not self.default.value:
                    self.text_val.value = str(self.kwargs['num_value'])+self.kwargs['units']

                elif not self.def_display.value and self.default.value:
                        self.def_display.value = True
                elif not self.def_display.value and not self.default.value:
                    self.def_display.visible = False
        except Exception:
            self.def_display.visible = True
            self.def_display.value = False


           
    def update(self, _=None, **kwargs):
        """interactive output generation"""
        if self.default.value:
            self.output = {'value':'',
                           'target': self.css_target.value
                          }
        elif self.kw_mode_val.value:
            self.output = {'value':str(self.kwargs['text_val']),
                           'target': self.css_target.value
                          }
        else:
            self.output = {'value':str(self.kwargs['num_value'])+self.kwargs['units'],
                           'target': self.css_target.value
                          }


class GridCssKeyword(StatelessDashboard):
    """class for managing a css numeric attribute"""
    def __init__(self,
                 default_val='center',
                 default=True,
                 mode='interactive',
                 **kwargs):
        
        justify_content_options = ["flex-start", "flex-end", "center",
                         "space-between", "space-around"]
        align_items_options = ["flex-start", "flex-end", "center",
                               "baseline", "auto"]
        align_self_options = ["flex-start", "flex-end", "center",
                              "baseline", "auto", "stretch"]
        
        if not default:
            attr_type = 'Grid Dropdowns'
        else:
            attr_type = 'Grid Text'
        #TODO add margin ad padding
        dashboard = ['c$N=css_keyword_sel',
                     [
                        ['r$N=title_row_grid',['##Grid setting$N=title_text_grid']],
                        ['r$N=discrete_vals',
                            ['###'+str(attr_type)+'$N=name_label',
                             #align self
                             '@text$d=Self&N=aself_text&v=0&val='+str(default_val),
                             '@dd$d=Self&N=align_self&o='+str(align_self_options),
                             'Default$N=def_self_label', '[[True]]$N=def_self_display', '@('+str(default)+')$n=def_self_value',
                             #align items
                             '@text$d=Items&N=aitems_text&v=0&val='+str(default_val),
                             '@dd$d=Items&N=align_items&o='+str(align_items_options),
                             'Default$N=def_items_label', '[[True]]$N=def_items_display', '@('+str(default)+')$n=def_items_value',
                             #justify content
                             '@text$d=Justify&N=justcont_text&v=0&val='+str(default_val),                            
                             '@dd$d=Justify&N=justify_content&o='+str(justify_content_options),
                             'Default$N=def_just_label', '[[True]]$N=def_just_display', '@('+str(default)+')$n=def_just_value',
                             #Common to css keyword widget
                             
                             'Apply to$N=grid_target_label&v=0', '@togs$v=0&N=grid_target&o=["widget", "target"]',
                             'Text$N=grid_mode_label', '@('+str(not default)+')$n=grid_mode_val',
                            ]
                        ],
                        ['r$N=numeric_vals',[CssKeyword(numeric=True,name='margin_val'),
                                             CssKeyword(numeric=True,name='padding_val'),
                                             '@rad$N=pad_or_mar&o=["padding","margin"]']]
                      ]
                    ]
        StatelessDashboard.__init__(self,dashboard,func=self.update, mode=mode, **kwargs)
        self._manual_css_settings()
        self.observe(self._grid_mode_update)
        self.pad_or_mar.observe(self._pad_mar_update)
        self.observe(self.update)
        self.output = {}
        self.update()
        self._grid_mode_update()
        self._pad_mar_update()
        self.padding_val._kw_mode_update()
        self.pad_or_mar.observe(self.padding_val._kw_mode_update)
        self.pad_or_mar.observe(self.margin_val._kw_mode_update)

    def _manual_css_settings(self):
        """Styling set using the underlying ipywidgets interface"""
        self.def_items_display.target.readout = 'Error'
        self.def_self_display.target.readout = 'Error'
        self.def_just_display.target.readout = 'Error'
        
        
        self.def_items_value.target.layout.width = "100%"
        self.def_self_value.target.layout.width = "100%"
        self.def_just_value.target.layout.width = "100%"
        self.def_items_value.widget.layout.width = "100%"
        self.def_self_value.widget.layout.width = "100%"
        self.def_just_value.widget.layout.width = "100%"
        
        
        
       
    def _pad_mar_update(self, _=None):
        if self.pad_or_mar.value == 'padding':
            self.padding_val.visible = True
            self.margin_val.visible = False
        else:
            self.padding_val.visible = False
            self.margin_val.visible = True
    def _grid_mode_update(self, _=None):
        
        if self.def_self_value.value:
            self.def_self_display.visible = True
            self.def_self_display.value = True
        else:
            self.def_self_display.visible = False
        
        if self.def_just_value.value:
            self.def_just_display.visible = True
            self.def_just_display.value = True
        else:
            self.def_just_display.visible = False
            
        if self.def_items_value.value:
            self.def_items_display.visible = True
            self.def_items_display.value = True
        else:
            self.def_items_display.visible = False
            
        if self.grid_mode_val.value:
            self.aself_text.visible = True
            self.aitems_text.visible = True
            self.justcont_text.visible = True
            self.align_self.visible = False
            self.align_items.visible = False
            self.justify_content.visible = False
            self.name_label.text = 'Align text'
        else:
            self.aself_text.visible = False
            self.aitems_text.visible = False
            self.justcont_text.visible = False
            self.align_self.visible = True
            self.align_items.visible = True
            self.justify_content.visible = True
            self.name_label.text = 'Align dropdown'
            
    def update(self, _=None, **kwargs):
        """interactive output generation"""
        if self.def_self_value.value:
            align_self = ('', 'widget')
        else:
            if self.grid_mode_val.value:
                align_self = (str(self.kwargs['aself_text']), 'widget')
            else:
                align_self = (str(self.kwargs['align_self']), 'widget')
                
        if self.def_items_value.value:
            align_items = ('', 'target')
        else:
            if self.grid_mode_val.value:
                align_items = (str(self.kwargs['aitems_text']), 'target')
            else:
                align_items = (str(self.kwargs['align_items']), 'target')
        
        if self.def_just_value.value:
            justify_content = ('', 'target')
        else:
            if self.grid_mode_val.value:
                justify_content = (str(self.kwargs['justcont_text']), 'target')
            else:
                justify_content = (str(self.kwargs['justify_content']), 'target')
                
        
        if self.margin_val.default.value:
            margin = ('', self.kwargs['grid_target'] )
        else:
            margin = (str(self.margin_val.output['value']), self.kwargs['grid_target'] )
            
            
        if not self.padding_val.default.value:
            padding = (str(self.padding_val.output['value']), self.kwargs['grid_target'])
        else:
            padding = ('', self.kwargs['grid_target'] )
            
        self.output = {'align_self':align_self,
                       'align_items':align_items,
                       'justify_content':justify_content,
                       'padding':padding,
                       'margin':margin
                      }
       
       
class WidthAndHeight(StatelessDashboard):
    
    def __init__(self,mode='interactive',**kwargs):
        dash = ['c$N=widht_and_height',
                 
                 [
                    ['r$N=title_row_wh',['##Width and height$N=title_text_wh']],
                    ['c$N=keyword_row',[
                         CssKeyword(numeric=True,name='height_val'),
                         CssKeyword(numeric=True,name='width_val')]
                    ],
                    ['r$N=toggle_row',[
                     '@togs$N=toggle_val&o=["val","max","min"]']
                    ]
                 ]
                ]
        self.output = {'width':('','target'),
                       'max_width':('','target'),
                       'min_width':('','target'),
                       'height':('','target'),
                       'min_height':('','target'),
                       'max_height':('','target'),
                      }
        StatelessDashboard.__init__(self,dash,mode=mode, **kwargs)
        self.observe(self.update)
        self.height_val.name_label.text = 'Height'
        self.width_val.name_label.text = 'Width'
        
    def update(self, _=None):

        if self.toggle_val.value == 'val':
            self.output['width'] = (self.width_val.output['value'],
                                    self.kwargs['width_val']['css_target'])
            self.output['height'] = (self.height_val.output['value'],
                                     self.kwargs['height_val']['css_target'])
            
        elif self.toggle_val.value == 'max':
            self.output['max_width'] = (self.width_val.output['value'],
                                        self.kwargs['width_val']['css_target'])
            self.output['max_height'] = (self.height_val.output['value'],
                                        self.kwargs['height_val']['css_target'])
            
        elif self.toggle_val.value == 'min':
            self.output['min_width'] = (self.width_val.output['value'],
                                        self.kwargs['width_val']['css_target'])
            self.output['min_height'] = (self.height_val.output['value'],
                                       self.kwargs['height_val']['css_target'])

class WidgetAttributes(StatelessDashboard):
    
    def __init__(self, widget=None, **kwargs):
        styles = ['default','primary', 'success', 'info', 'warning', 'danger']

        dash = ['r$N=widget_s',
                 [
                   ['c$N=widget_optionsSel',
                      [  
                         ['r$N=row_title',['##Widget selector$N=title']],
                          ['r$N=row_btn',
                            ["@dd$N=dd_style&d=Style&o="+str(styles),
                             '@text$d=Icon',
                             '@text$d=Tooltip',
                             'Visible$N=mode_label', '@('+str(True)+')$n=visible_chk'
                            ]
                          ],
                         ['r$N=row_slider',
                          [
                           '@rad$d=orientation&o=["horizontal", "vertical"]',
                           '@(True)$d=Readout',
                           'Format$N=rof_label','@text$N=ro_format',
                           '@cpicker$d=Color','@cpicker$d=Slider color'
                          ]
                         ],

                       ]
                    ]
                  ]
                ]
        self._data_widget = widget
        StatelessDashboard.__init__(self,dash , **kwargs)
        self.ro_format.target.width="5em"
        self.observe(self._update_layout)
        self.observe(self.update)
        self.update()
        self._update_layout()
    
    def _hide_widgets(self):
        self.dd_style.visible = False
        self.icon.visible = False
        self.tooltip.visible = False
        self.orientation.visible = False
        self.readout.visible = False
        self.ro_format.visible = False
        self.rof_label.visible = False
        self.color.visible = False
        self.slider_color.visible = False
    @property
    def data_widget(self):
        return self._data_widget
    @data_widget.setter
    def data_widget(self,val):
        self._data_widget = val
        self._update_layout()
        self.update()
        
    
    def _update_layout(self, _=None):
        sliders = (wid.FloatRangeSlider, wid.FloatSlider, wid.IntRangeSlider, wid.IntSlider)
        num_text = (wid.FloatText, wid.BoundedFloatText, wid.IntText, wid.BoundedIntText)
        
        self._hide_widgets()
        if isinstance(self._data_widget.target,(wid.Button, wid.ToggleButton, wid.ToggleButtons)):
            self.dd_style.visible = True
            if isinstance(self._data_widget, wid.Button):
                self.icon.visible = True
                
        elif isinstance(self._data_widget.target, sliders):
            self.orientation.visible = True
            self.readout.visible = True
            self.ro_format.visible = True
            self.rof_label.visible = True
            self.color.visible = True
            self.slider_color.visible = True
            
        elif isinstance(self._data_widget.target, wid.Valid):
            self.ro_format.visible = True
            self.ro_label.visible = True
            
        elif isinstance(self._data_widget.target, num_text):
            self.color.visible = True

        elif isinstance(self._data_widget.target, (wid.IntProgress, wid.FloatProgress)):
            self.orientation.visible = True
            self.dd_style.visible = True
        
    
    def update(self, _=None):
        sliders = (wid.FloatRangeSlider, wid.FloatSlider, wid.IntRangeSlider, wid.IntSlider)
        num_text = (wid.FloatText, wid.BoundedFloatText, wid.IntText, wid.BoundedIntText)
        if isinstance(self._data_widget.target,(wid.Button, wid.ToggleButton, wid.ToggleButtons)):
            if isinstance(self._data_widget,wid.Button):
                self.output = {'button_style':self.dd_style.value,
                          'icon': self.icon.value,
                          'visible':self.visible_chk.value,
                         }
            else:
                self.output = {'button_style':self.dd_style.value,
                         'visible':self.visible_chk.value}
            
        elif isinstance(self._data_widget.target, sliders):
            #BUG FIX FROM IPYWIEDGETS not allowing to set the readout format of a range slider
            if isinstance(self._data_widget.target, (wid.FloatRangeSlider,wid.IntRangeSlider)):
                self.output = {'orientation':self.orientation.value,
                               'readout':self.readout.visible,
                               'color':self.color.value,
                               'slider_color':self.slider_color.value,
                               'visible':self.visible_chk.value,
                              }
            else:
                self.output = {'orientation':self.orientation.value,
                               'readout':self.readout.visible,
                               'readout_format': self.ro_format.value,
                               'color':self.color.value,
                               'slider_color':self.slider_color.value,
                               'visible':self.visible_chk.value,
                              }

        elif isinstance(self._data_widget.target, wid.Valid):
            self.output = {'readout_format': self.ro_format.value,
                           'visible':self.visible_chk.value,
                          }
            
        elif isinstance(self._data_widget.target, num_text):
            self.output = {'color':self.color.value,
                           'visible':self.visible_chk.value,
                          }

        elif isinstance(self._data_widget.target, (wid.IntProgress, wid.FloatProgress)):
            self.output = {'orientation':self.orientation.value,
                           'button_style':self.dd_style.value,
                           'visible':self.visible_chk.value,
                          }
        else:
            self.output = {'visible':self.visible_chk.value}


class LayoutHacker(StatelessDashboard):
    KEYWORD_TYPES = {'align_content': 'layout',
                     'align_items': 'layout',
                     'align_self': 'layout',
                     'border': 'str',
                     'bottom': 'num',
                     'display': 'str',
                     'flex': 'str',
                     'flex_flow':'str',
                     'height': 'num',
                     'justify_content': 'layout',
                     'left': 'num',
                     'margin': 'num',
                     'max_height': 'num',
                     'max_width': 'num',
                     'min_height': 'num',
                     'min_width': 'num',
                     'overflow': 'str',
                     'padding': 'num',
                     'right': 'num',
                     'top': 'num',
                     'visibility': 'str',
                     'width': 'num'}
    
    DDOWN_OPTS = ['border', 'overflow', 'flex', 'flex_flow', 'top',
                     'bottom', 'right', 'left','visibility', 'display']
                     
    
    def __init__(self, dashboard, **kwargs):
        
        self.kwtypes,self.ddown_options = self.get_default_kwtypes()
        
        
        self._target_dashboard = dashboard
        self._target_dashboard.mode='passive'
        self._dash_attrs = []
        self.get_attribute_list()
        first_widget = getattr(dashboard,self._dash_attrs[0])
        #get trait names
        self.traits = list(self.kwtypes.keys())
        dash = ['c$N=css_dash',
                   [  
                      ['r$N=row_title',['#Css Manager$N=title']],
                      ['r$N=row_kwrd',
                           ['@ddown$N=keyword&d=Css keyword&o='+str(tuple(self.ddown_options)),
                            CssKeyword(numeric=True, name='keyword_sel')
                           ]
                      ],
                      ['r$N=row_grid',
                           [
                            GridCssKeyword(name='grid_sel')
                           ]
                      ],
                      ['r$N=row_wh',
                           [
                            WidthAndHeight(name='wh_sel')
                           ]
                      ],
                      ['r$N=row_widget',
                           [
                            WidgetAttributes(widget=first_widget,name='widget_sel')
                           ]
                      ],
                      ['r$N=row_sel',
                            ['##Widget$N=widget_label',
                             '@sel$N=dash_attr&o='+str(sorted(list(self._dash_attrs))),
                             '@togs$N=main_buttons&o=["Grid","WH","Other","Widget"]',
                             '###Default value$N=css_value_display',
                             'text$d=File Name&val='+self._target_dashboard.name+'.pkl',
                             'button$d=Save&N=save_button'
                            ]
                      ],
                      ['r$N=row_dash',
                           [
                            self._target_dashboard
                           ]
                      ],
                      
                   ]
               ]
                              
        
        StatelessDashboard.__init__(self,dash,**kwargs)
        self.main_buttons.target.options = ["Grid","W&H","Other","Widget"]
        self.keyword.target.width = "100%"
        self.dash_attr.target.width = "100%"
        self.row_kwrd.widget.layout.height = "13em"
        self.row_grid.widget.layout.height = "13em"
        self.row_wh.widget.layout.height = "13em"
        #self.css_value_display.widget.layout.padding = "1em"
        self.dash_attr.target.button_style = 'primary'
        self.output = dict({})
        self.init_output_dict()
        self.observe(self.update)
        self.widget_sel.observe(self.update)
        self.grid_sel.observe(self.update)
        self.wh_sel.observe(self.update)
        self.keyword_sel.observe(self.update)
        self.save_button.observe(self.save_layout)
        self.file_name.target.layout.width="80%"
        self.update()
    
    
    def save_layout(self, _=None):
        output = open(self.file_name.value, 'wb')
        # Pickle dictionary using protocol 0.
        pickle.dump(self.output, output)
        output.close()
        print("Layout saved")
        
        
    def update_output_dict(self):
        widget_name = self.dash_attr.value
        if self.main_buttons.value == 'Other':
            for tra in sorted(self.traits):
                self.output[widget_name]['css_traits'][tra][self.keyword_sel.output['target']] = self.keyword_sel.output['value']

        elif self.main_buttons.value == 'W&H':
            for tra in self.wh_sel.output.keys():
                self.output[widget_name]['css_traits'][tra][self.wh_sel.output[tra][1]] = self.wh_sel.output[tra][0]
        elif self.main_buttons.value == 'Grid':
            for tra in self.grid_sel.output.keys():
                self.output[widget_name]['css_traits'][tra][self.grid_sel.output[tra][1]] = self.grid_sel.output[tra][0]
                
        elif self.main_buttons.value == 'Widget': 

            for attr_key in self.widget_sel.output.keys():
                    if attr_key == 'visible':
                        val = getattr(getattr(self._target_dashboard,widget_name),attr_key)
                    else:
                        val = getattr(getattr(getattr(self._target_dashboard,widget_name),'target'), attr_key)
                    self.output[widget_name]['widget_attrs'][attr_key] = val
                
    def update_dashboard(self):
        if self.kwtypes[self.keyword.value] == 'num':
            self.keyword_sel.numeric = True
        else:
            self.keyword_sel.numeric = False
        
        if self.main_buttons.value == 'Grid':
            self.row_kwrd.visible = False
            self.row_grid.visible = True
            self.row_wh.visible = False
            self.row_widget.visible = False
            self.row_widget.visible = False
        elif self.main_buttons.value == 'W&H':
            self.row_kwrd.visible = False
            self.row_grid.visible = False
            self.row_wh.visible = True
            self.row_widget.visible = False
        elif self.main_buttons.value == 'Other':
            self.row_kwrd.visible = True
            self.row_grid.visible = False
            self.row_wh.visible = False
            self.row_widget.visible = False
        elif self.main_buttons.value == 'Widget':
            self.widget_sel.data_widget = getattr(self._target_dashboard,self.dash_attr.value)
            self.row_kwrd.visible = False
            self.row_grid.visible = False
            self.row_wh.visible = False
            self.row_widget.visible = True
            
    def update(self, _=None):
        self.update_dashboard()
        self.update_output_dict()
        self.apply_css()
    
    def apply_css(self):
        attr = self.dash_attr.value
        if self.main_buttons.value == 'Other':
            trait = self.keyword.value
            tget = self.keyword_sel.output['target']
            val = self.keyword_sel.output['value']
            layout = getattr(getattr(self._target_dashboard,attr), tget).layout
            setattr(layout,trait,val)
            self.css_value_display.text = "{} {} ---> {}:{}".format(attr, tget, trait, val)
            
        elif self.main_buttons.value == 'Grid':
            for trait, tup in self.grid_sel.output.items():
                val, target = tup
                layout = getattr(getattr(self._target_dashboard,attr), target).layout
                setattr(layout,trait,val)
            self.css_value_display.text = "{} {} ---> {}:{}".format(attr, target, trait, val)
        elif self.main_buttons.value == 'W&H':
            for trait, tup in self.wh_sel.output.items():
                val, target = tup
                layout = getattr(getattr(self._target_dashboard,attr), target).layout
                setattr(layout,trait,val)
            self.css_value_display.text = "{} {} ---> {}:{}".format(attr, target, trait, val)
            
        elif self.main_buttons.value == 'Widget':
            widg = getattr(self._target_dashboard,self.dash_attr.value)
            for attr, val in self.widget_sel.output.items():
                if attr == 'visible':
                    setattr(widg,attr,val)
                else:
                    setattr(getattr(widg,'target'), attr, val)
            self.css_value_display.text = "{} ---> {}".format(attr, val)
        
        
                
    
    def get_attribute_list(self):
        for name in self._target_dashboard.mode_dict['all']:
            if not isinstance(getattr(self._target_dashboard,name), StatelessDashboard):
                self._dash_attrs += [name]
    
    def init_output_dict(self):
        for attr in self._dash_attrs:
            self.output[attr] = {'css_traits':{},
                                 'widget_attrs':{}
                                }
            for tra in sorted(self.traits):
                self.output[attr]['css_traits'][tra] = {'widget':'',
                                    #'label':'',
                                    'target':''
                                   }
        #widget target attrs logic
        for widget_name in self._dash_attrs:
            for attr_key in self.widget_sel.output.keys():
                if attr_key == 'visible':
                    val = getattr(getattr(self._target_dashboard,widget_name),attr_key)
                else:
                    val = getattr(getattr(getattr(self._target_dashboard,widget_name),'target'), attr_key)
                self.output[widget_name]['widget_attrs'][attr_key] = val

    @classmethod
    def get_default_kwtypes(cls):
        return cls.KEYWORD_TYPES, cls.DDOWN_OPTS
