# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 10:22:21 2016

@author: Guillem Duran for HCSOFT
"""

import ipywidgets as widgets
from matplotlib import cm

MARKER_PARAMS = ['x', 'y', 'fill_color', 'marker',
                 'line_color', 'size', 'line_width',
                 'fill_alpha', 'line_alpha']

class SelectMultiple(object):
    """This is a customized SelectMultiple widget
        with custom HTML description
    """
    def __init__(self, options, title='Tooltip Data', value=None,
                 description='Select <br> columns:',):
        """This is a customized SelectMultiple widget
        with custom HTML description"""
        if value is None:
            value = options
        self.target = widgets.SelectMultiple(options=options,
                                             value=value,
                                             width='100%',
                                             height='100%'
                                            )
        self._desc_text = description
        self._desc_css = """font-size:14px;font-weight:bold;"""
        self.desc_w = widgets.HTML()

        self.update_description()
        self._title_text = title
        self._title_css = """font-size:22px;font-weight:bold;"""

        self.title_w = widgets.HTML()
        self.update_title()
        self.title_w.margin = "1.5%"
        self._target_b = widgets.HBox(children=[self.desc_w, self.target])

        self.widget = widgets.VBox(children=[self.title_w, self._target_b])
        self.widget.margin = 4

    @property
    def title(self):
        """Alias for title text"""
        return self.title_w.value
    @title.setter
    def title(self, value):
        self.title_w.value = value

    @property
    def options(self):
        """Alias for widget options"""
        return self.target.options
    @options.setter
    def options(self, value):
        self.target.options = value

    @property
    def value(self):
        """Alias for widget value"""
        return self.target.value
    @value.setter
    def value(self, value):
        self.target.value = value

    @property
    def description(self):
        """Alias for widget description"""
        return self._desc_text
    @description.setter
    def description(self, value):
        self._desc_text = value

    #Triggered updates doesnd work as intended (mabe trailets)
    def update_title(self):
        """Creates title HTML"""
        self.title_html = '<div class="kf-pms-mulsel" id="title" style="'+\
                                  self._title_css+'">'+\
                                  self._title_text+'</div>'
        self.title_w.value = self.title_html
    def update_description(self):
        """Creates description HTML"""
        self._desc_html = '<div class="kf-pms-mulsel" id="description" style="'+\
                                  self._desc_css+'">'+\
                                  self._desc_text+'</div></br>'
        self.desc_w.value = self._desc_html

class DataFrameMappedParameter(object):
    """Generic selector for an arbitrary parameter.
           values: list of values to select from.
           name: String containing the name of the param.
           default: Default value. If not specified the firt element of values
                    will be used
    """
    def __init__(self, values, name='Parameter', default=None):
        html = ('<div class="scparam scparam-'+name+
                '" style=" font-size:22px; text-align:right;">'+
                name+':</div>')
        self.name = widgets.HTML(value=html, height=30, width="110px")
        self.active = widgets.Checkbox(value=False)
        self.active.width = "15px"
        self.active.height = "15px"
        self.active.padding = 6
        if default is None:
            self.target = widgets.Dropdown(options=values)
        else:
            self.target = widgets.Dropdown(options=values, value=default)
        self.target.padding = 6
        self.namebox = widgets.HBox(children=[self.active, self.name],
                                    width='150px', align='center')
        self.widget = widgets.HBox([self.namebox, self.target])
    @property
    def value(self):
        """Alias for target value"""
        return self.target.value

class PanelMappedParameter(object):
    """Selector for an arbitrary marker param mapped from a panel insted of a DataFrame"""
    def __init__(self, panel_shao, name='Parameter', default=None):
        self.panel_shao = panel_shao
        html = ('<div class="pa_map_param-name-' + name
                + '" style=" font-size:22px; text-align:right;">'
                + name + ':</div>')
        self.name = widgets.HTML(value=html, height=30, width="110px")
        self.active = widgets.Checkbox(value=False,
                                       width="15px",
                                       height="15px",
                                       padding=6
                                      )
        ax1 = panel_shao.panel.axes[panel_shao.not_ti[0]]
        self.ax1 = widgets.Dropdown(options=ax1.values.tolist(), padding=6)
        ax2 = panel_shao.panel.axes[panel_shao.not_ti[1]]
        self.ax2 = widgets.Dropdown(options=ax2.values.tolist(), padding=6)
        self.namebox = widgets.HBox(children=[self.active, self.name],
                                    width='150px', align='center')
        self.widget = widgets.HBox([self.namebox, self.ax1, self.ax2])

class MarkerFreeParams(object):
    """Manages the values of the parameters that have not been mapped to data
    """
    MARKERS = {'Square X':'square_x',
               'X':'x', 'Circle':'circle',
               'Diamond Cross':'diamond_cross',
               'Circle X':'circle_x', 'Asterisk':'asterisk',
               'Diamond':'diamond', 'Cross':'cross',
               'Square Cross':'square_cross', 'Circle Cross':'circle_cross',
               'Inverted Triangle':'inverted_triangle',
               'Triangle':'triangle', 'Square':'square'
              }
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
    @classmethod
    def default_markers(cls):
        """Returns a dict containing the label and name of all the bokeh markers."""
        return cls.MARKERS
    @classmethod
    def default_free_params(cls):
        """Returns a default parameter dict."""
        return cls.FREE_PARAMS

    def __init__(self,
                 default_params=None,
                 markers=None,
                 title='Select parameter mapping'):

        if default_params is None:
            self.params = self.default_free_params()
        else:
            self.params = default_params
        if markers is None:
            self.markers = self.default_markers()
        else:
            self.markers = markers

        self.title = widgets.HTML(value=('<b style="font-size:22px;">'+title+'</b></br>'))

        if 'marker' in self.params.keys():
            self.marker = widgets.Dropdown(options=self.MARKERS,
                                           value=self.params['marker'],
                                           description='Marker:')
            self.marker.observe(self.on_marker_change, names='value')
        else:
            self.marker = widgets.HBox()

        if 'fill_color' in self.params.keys():
            self.fill_color = widgets.ColorPicker(value=self.params['fill_color'],
                                                  description='Fill color:')
            self.fill_color.observe(self.on_fillcolor_change, names='value')
            self.fill_color.width = "50px"
        else:
            self.fill_color = widgets.HBox()

        if 'line_color' in self.params.keys():
            self.line_color = widgets.ColorPicker(value=self.params['line_color'],
                                                  description='Line color:')
            self.line_color.observe(self.on_linecolor_change, names='value')
            self.line_color.width = "50px"
        else:
            self.line_color = widgets.HBox()

        if 'fill_alpha' in self.params.keys():
            self.fill_alpha = widgets.BoundedFloatText(
                value=self.params['fill_alpha'],
                min=0,
                max=1,
                description='Fill alpha:')
            self.fill_alpha.observe(self.on_fillalpha_change, names='value')
            self.fill_alpha.width = "50px"
            #self.fill_alpha.padding=6
        else:
            self.fill_alpha = widgets.HBox()

        if 'line_alpha' in self.params.keys():
            self.line_alpha = widgets.BoundedFloatText(
                value=self.params['line_alpha'],
                min=0,
                max=1,
                description='Line alpha:')
            self.line_alpha.observe(self.on_linealpha_change, names='value')
            self.line_alpha.width = "50px"
            #self.line_alpha.padding=6
        else:
            self.line_alpha = widgets.HBox(
            )
        if 'size' in self.params.keys():
            self.size = widgets.BoundedFloatText(
                value=self.params['size'],
                min=0,
                max=40,
                description='Size:')
            self.size.observe(self.on_size_change, names='value')
            self.size.width = "50px"
        else:
            self.size = widgets.HBox()
        if 'line_width' in self.params.keys():
            self.line_width = widgets.BoundedFloatText(
                value=self.params['line_width'],
                min=0.1,
                max=40,
                description='Line width:')
            self.line_width.observe(self.on_linewidth_change, names='value')
            self.line_width.width = "50px"
        else:
            self.line_width = widgets.HBox()
        #self.line_width.padding=5
        cmlist = list(cm.cmap_d.keys())
        cmlist.sort()
        if 'line_colormap' in self.params.keys():
            self.line_colormap = widgets.Select(
                options=cmlist,
                value=self.params['line_colormap'],
                description='Line colormap:',
                width='100%'
            )
            self.line_colormap.observe(self.on_linecolormap_change, names='value')
            self.line_colormap.padding = 6
            self.line_colormap.width = '130px'
        else:
            self.line_colormap = widgets.HBox()

        if 'fill_colormap' in self.params.keys():
            self.fill_colormap = widgets.Select(
                options=cmlist,
                value=self.params['fill_colormap'],
                description='Fill colormap:',
                width='100%'
            )
            self.fill_colormap.observe(self.on_fillcolormap_change, names='value')
            self.fill_colormap.padding = 6
            self.fill_colormap.width = '130px'
        else:
            self.fill_colormap = widgets.HBox()

        top_line = widgets.HBox([self.marker, self.size, self.line_width])
        top_line.padding = 6
        line_block = widgets.VBox([self.line_alpha,
                                   self.line_color,
                                   self.line_colormap])

        fill_block = widgets.VBox([self.fill_alpha,
                                   self.fill_color,
                                   self.fill_colormap])

        self.widget = widgets.VBox(children=[self.title,
                                             top_line,
                                             widgets.HBox([line_block,
                                                           fill_block])])
        self.widget.margin = 6

    @property
    def plot_params(self):
        """Prepare the dict for tha actual parameter mapping. This means
        eliminating the keys regaring to metaparameters such as colormaps that
        are not explicitly defined on the plot
        """
        param_dict = self.params.copy()
        param_dict.pop('fill_colormap')
        param_dict.pop('line_colormap')
        param_dict.pop('marker')
        return param_dict

    def on_fillcolor_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['fill_color'] = change['new']

    def on_fillalpha_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['fill_alpha'] = change['new']

    def on_fillcolormap_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['fill_colormap'] = change['new']

    def on_linecolor_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['line_color'] = change['new']

    def on_linealpha_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['line_alpha'] = change['new']

    def on_linecolormap_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['line_colormap'] = change['new']

    def on_marker_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['marker'] = change['new']

    def on_size_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['size'] = change['new']

    def on_linewidth_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['line_width'] = change['new']

class MarkerMappedParams(object):
    """A selector composed of multiple parameters to handle
    the input of arguments for a generic plot marker
    """
    def __init__(self,
                 default_map=None,
                 df=None,
                 values=None,
                 params=None,
                 name=None,
                 param_type=DataFrameMappedParameter):
        """This widget creates a parameter selector"""

        #if there is no default map use a dataframe,
        #if there is no df then use values as columns and default marker params
        if default_map is None:
            if df is None:
                self.params = MARKER_PARAMS
                if values is None:
                    return #TODO error handling
                else:
                    self.values = values
            else:
                self.values = df.columns.values.tolist()
                if params is None:
                    self.params = MARKER_PARAMS
                else:
                    self.params = params
            self.default_map = dict([(x, None) for x in self.params])
        #if default map is a dict, its keys will
        #be used to infer the params and defaults
        #and values os a df will be used for the columns
        elif isinstance(default_map, dict):
            self.default_map = default_map
            self.params = list(default_map.keys())
            if values is None:
                self.values = df.columns.values.tolist()
            else:
                self.values = values
        #if default map is a list, the list
        #of values can be either the df columsn or the parameter values
        elif isinstance(default_map, list):
            self.default_map = dict([(x, None) for x in self.params])
            self.params = default_map
            self.values = df.columns.values.tolist()
        #try to infer teh name from the df
        if name is None:
            self.name = 'Columns'
            if not df is None:
                if not df.columns.name is None:
                    self.name = df.columns.name
        else:
            self.name = name
        self.x = param_type(self.values, 'x')
        self.x.active.description = 'Fix '+self.name
        self.x.name.width = '25px'
        if not 'x' in self.params:
            self.params = ['x']+self.params
            self.x.name.visible = False

        self.y = param_type(self.values, 'y')
        if not 'y' in self.params:
            self.y.target.visible = False
            self.y.name.visible = False
            self.y.active.visible = False
        if 'marker' in self.params:
            self.marker = param_type(self.values,
                                     'marker',
                                     self.default_map['marker'])
        else:
            self.marker = widgets.HBox()
        if 'line_color' in self.params:
            self.line_color = param_type(self.values,
                                         'line_color',
                                         self.default_map['line_color'])
        else:
            self.line_color = widgets.HBox()
        if 'fill_color' in self.params:
            self.fill_color = param_type(self.values,
                                         'fill_color',
                                         self.default_map['fill_color'])
        else:
            self.fill_color = widgets.HBox()
        if 'fill_alpha' in self.params:
            self.fill_alpha = param_type(self.values,
                                         'fill_alpha',
                                         self.default_map['fill_alpha'])
        else:
            self.fill_alpha = widgets.HBox()

        if 'line_alpha' in self.params:
            self.line_alpha = param_type(self.values,
                                         'line_alpha',
                                         self.default_map['line_alpha'])
        else:
            self.line_alpha = widgets.HBox()

        if 'size' in self.params:
            self.size = param_type(self.values,
                                   'size',
                                   self.default_map['size'])
        else:
            self.size = widgets.HBox()
        if 'line_width' in self.params:
            self.line_width = param_type(self.values,
                                         'line_width',
                                         self.default_map['line_width'])
        else:
            self.line_width = widgets.HBox()

        css = '''<style>
                    .scpsel-tbar { 
                        text-align:center;
                        font-weight: bold;
                    }
                    .scparam{margin-top:5% !important;}
                    
                </style>'''

        self.titlebar = [widgets.HTML(value=css)]
        self.titlebar += [widgets.HTML(value='<h3 class="scpsel-tbar">Property<h3>',
                                       width="150px")]
        self.titlebar += [widgets.HTML(value='<h3 class="scpsel-tbar">'+
                                       self.name+'<h3>',
                                       width="150px")]

        atrwidgets = [getattr(self, name).widget for name in self.params]
        self.widget = widgets.VBox(children=
                                   [widgets.HBox(self.titlebar)]
                                   +atrwidgets)

        self.x.active.observe(self._on_fixed_change, names='value')
        self.x.target.observe(self._on_target_change, names='value')

    @property
    def fixed(self):
        """Alias to return a boolean if the selector is fixed"""
        return self.x.active.value

    def fix_target(self, value):
        """All the parameter values will mimic x.value"""
        if self.fixed:
            #fix all the targets to x and leave y free
            for name in self.params[1:]:
                getattr(self, name).target.value = value
            self.x.target.disabled = False
        #else:
            #self.x.target.disabled = True

    def disable_target(self, disabled=True):
        """Set all the disable values of the children to disabled"""
        #Do not disable x and y
        for name in self.params[1:]:
            getattr(self, name).target.disabled = disabled

    def _on_fixed_change(self, _):
        self.fix_target(self.x.target.value)
        self.disable_target(self.fixed)

    def _on_target_change(self, _):
        self.fix_target(self.x.target.value)

class ButtonController(object):
    """Buttons for controlling the walkers. Consists of:
        play: run the simulation at "fps" frames per second for "streak" frames
        fwd: tun 1 step forward
        nwd: run 1 step backwards
        rate: Max frames per second when play is clicked
        streak: Play streak frames when play is clicked
    """
    def __init__(self):
        self.play = widgets.Button(description='Play')
        #self.stop = widgets.Button(description='Stop')
        self.fwd = widgets.Button(description='+1')
        self.bwd = widgets.Button(description='-1')
        self.rate = widgets.BoundedIntText(min=1, max=60,
                                           description='Fps: ', value=2)
        self.rate.width = '40px'
        self.streak = widgets.BoundedIntText(min=1, max=60,
                                             description='Streak: ',
                                             value=15)
        self.streak.width = '40px'
        self.streak.margin = '-2px'
        self.widget = widgets.HBox(children=[self.bwd, self.play,
                                             self.fwd, self.streak, self.rate])
        self.widget.align = 'center'

class TimeDisplay(object):
    """Simple Datetime HTML display.
        strf: string representig the dt format of the conversion"""
    def __init__(self, strf='%a %d-%h-%Y %H:%M'):
        self.strf = strf
        html = '<div>Time</div>'
        self.widget = widgets.HTML(html, font_size=20)
        self.widget.width = '300px'

    def update(self, datetime):
        """Updates the display value. datetime: date/datetime object"""
        html = '<div>Time: <strong>'+datetime.strftime(self.strf)+'</strong></div>'
        self.widget.value = html

class TimeProgressBar(object):
    """Custom progressbar adapted for displaying datetimes.
        index: Pandas datetime index object. Used in displaying start
               and end labels and determines the size of the bar.
        strf: string representig the dt format of the conversion
    """
    def __init__(self, index, strf='%d-%m-%y %H:%M'):
        self.strf = strf
        self.index = index
        self.pbar = widgets.FloatProgress(value=0,
                                          min=0,
                                          max=len(index.values),
                                          step=1,
                                          description='',
                                         )
        self.pbar.border_radius = 8
        self.pbar.margin = '10px'
        self.pbar.padding = '10px'
        self.pbar.border_size = '1px'
        self.pbar.width = '100em'
        self.pbar.font_size = 18

        self.start = widgets.HTML('<div>'+self.index[0].strftime(self.strf)+
                                  '</div>', font_size=16)
        self.end = widgets.HTML('<div>'+self.index[-1].strftime(self.strf)+
                                '</div>', font_size=16)
        self.widget = widgets.HBox(children=[self.start, self.pbar, self.end])
        self.widget.align = 'center'

class WalkerBar(object):
    """A widget for controlling a walker. It has all the time widgets
        combined to provide a animation control panel for Walkers.
        index: Pandas datetime index object. Used in displaying start
               and end labels and determines the size of the bar.
        strf: string representig the dt format of the conversion
    """
    def __init__(self, index, strf='%d-%m-%y %H:%M'):
        self.strf = strf
        self.index = index
        self.value = index[0]

        self.tdis = TimeDisplay(self.strf)
        self.tdis.update(self.value)

        self.pbar = TimeProgressBar(self.index, self.strf)
        self.widget = widgets.VBox(children=[self.pbar.widget, self.tdisplay])
        self.widget.align = 'center'

        self.widget.padding = '10px'

    @property
    def tdisplay(self):
        """Alias for its internal TimeDiraplay widget"""
        return self.tdis.widget

    def update(self, datetime, strf=None):
        """Updates Walker bar and its children"""
        if strf is None:
            strf = self.strf
        self.pbar.pbar.value = self.index.get_loc(datetime)
        self.tdis.update(datetime)
        self.tdis.strf = strf
        self.pbar.strf = strf
