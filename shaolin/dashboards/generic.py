# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 10:22:21 2016

@author: Guillem Duran for HCSOFT
"""
#import random
import ipywidgets as wid
#from matplotlib import cm
#import pandas as pd

#MARKER_PARAMS = ['x', 'y', 'fill_color', 'marker',
#                 'line_color', 'size', 'line_width',
#                 'fill_alpha', 'line_alpha']

class Widget(object):
    """This is a wrapper for any selector widget so its description can be tweaked with css
    Parameters. This will also make backwadrs compatible the instantiation with layout properties.
    ----------
    widget : ipydidgets widget
        this is intender for selector widgets, but it can be
        any widget with from the ipywidgets package.
    description : String or None
        Text for the description of the widget. Acs as the description
        parameter of the widget but can be tweaked with css
    desc_css : String or None
        css for the description text.
    custom_id : String or None
        A custom attribute tag for the description div.
    kwargs : **kwargs
        Arguments of the widget we are wrapping.
    """
    def __init__(self,
                 widget,
                 class_=None,
                 id=None,
                 name=None,
                 html=None,
                 js=None,
                 css=None,
                 visible=True,
                 **kwargs):

        if id is None:
            id = ''
        else:
            id = id.lower().replace(' ', '_')
        if html is None:
            html = ''
        if js is None:
            js = ''
        if css is None:
            css = ''
        if name is None:
            name = ''
        else:
            name = name.lower().replace(' ', '_')
        if class_ is None:
            class_ = ''

        self.name = name
        self.id = id
        self.class_ = class_
        self.html = html
        self.js = js
        self.css = css
        """
        #this ensures a unique class name for javascript hacking
        self._hack_id = ''.join(random.choice('0123456789ABCDEFGHIJK') for i in range(16))
        self._hack_widget = wid.HTML(value='<div id="'+self._hack_id+'"></div>'\
                                            +'<style>'+self.css+'</style>'\
                                            +'<script>'+self.js+'</script>'+self.html)
        self._hack_widget.layout.display = 'none'
        self._hack_widget.layout.visibility = 'hidden'
        
        self._label_css = ''
        #if 'description' in kwargs.keys():
        #    self.description = kwargs['description']
        #    kwargs.pop('description')
        
        self._description = description
        self.label = wid.HTML(value='<div id="label-'+self.id+'" style="'+self._label_css+\
                                    '">'+self._description+'</div>')
        if self._description == '':
            self.label.layout.display = 'none'
            self.label.layout.visibility = 'hidden'
        """
        self.target = widget(**kwargs)
        self.widget = wid.HBox(children=[self.target])
        
        #self.widget.layout.width = self.target.layout.width
        #self.add_ids()
        self.visible = visible
        #Attributes for mimicking standard widget interface
        #----------------------------------------------------

    @property
    def hack(self):
        return self._hack_widget
    @hack.setter
    def hack(self, val):
        self._hack_widget = val

    @property
    def value(self):
        """Get the value of the wrapped widget"""
        return self.target.value
    @value.setter
    def value(self, val):
        self.target.value = val

    @property
    def options(self):
        """Same interface as widgets but easier to iterate"""
        try:
            return self.target.options
        except AttributeError:
            return None
    @options.setter
    def options(self, val):
        try:
            self.target.options = val
        except AttributeError:
            pass

    @property
    def visible(self):
        """Easier visibility changing"""
        return self.widget.layout.visibility == '' \
               and self.widget.layout.display == ''
    @visible.setter
    def visible(self, val):
        """Easier visibility changing"""
        if val:
            self.widget.layout.visibility = ''
            self.widget.layout.display = ''
        else:
            self.widget.layout.visibility = 'hidden'
            self.widget.layout.display = 'none'


    @property
    def description(self):
        """Same interface as widgets but easier to iterate"""
        return self._description
        
    @description.setter
    def description(self, val):
        """Same interface as widgets but easier to iterate"""
        self._description = val
        self.label = wid.HTML(value='<div id="label-'+self.id+'" style="'+self._label_css+'">'+self._description+'</div>')
        if val == '':
            self.label.layout.display = 'none'
            self.label.layout.visibility = 'hidden'
        else:
            self.label.layout.display = ''
            self.label.layout.visibility = ''

    @property
    def orientation(self):
        """Same interface as widgets but easier to iterate"""
        try:
            return self.target.orientation
        except AttributeError:
            return None
    @orientation.setter
    def orientation(self, val):
        """Same interface as widgets but easier to iterate"""
        try:
            self.widget.orientation = val
        except AttributeError:
            pass

    def update(self, val):
        self.value = val

    def observe(self, func, names='value'):
        """A quickly way to add observe calls to the widget"""
        if isinstance(self.target,
                      wid.Widget.widget_types['Jupyter.Button']):
            self.target.on_click(func)
        if hasattr(self.target, 'value'):
            self.target.observe(func, names=names)
    #Methods
    #------------------------------
    def add_ids(self):
        hack_id = self._hack_id
        class_tag = str(self.class_)
        if class_tag == '':
            class_tag = ""
        id_tag = str(self.id)
        if id_tag == '':
            child_id = hack_id
        else:
            child_id = id_tag
        javascript = """
        function iterateChildren(c,level) {
            var i;
            level = level+1;
            for (i = 0; i < c.length; i++) {
                if (typeof c[i] != 'undefined') {
                    if (typeof c[i].style != 'undefined') {
                        c[i].id += '"""+child_id+"""'+"-"+level+"-"+i;
                    }
                    children = c[i].childNodes;
                    iterateChildren(children,level)
                }
            }                       
        }

        function markChildren_"""+hack_id+"""(hack_id) {
            var widget =  document.getElementById('"""+hack_id+"""').parentElement.parentElement;
            widget.id += "shao ";
            widget.id += '"""+id_tag+"""';
            widget.classList.add('"""+class_tag+"""') ;
            var c = widget.childNodes;
            //iterateChildren(c,0);
        }
        var hack_id = 'H6D2B1S9C0G';
        markChildren_"""+hack_id+"""(hack_id);
        """
        self.update_hack(js=javascript)
        self.hack.visibility = 'hidden'

    def update_hack(self,
                    hack_id=None,
                    html=None,
                    css=None,
                    js=None):
        """updates css hack"""
        if not html is None:
            self.html = html
        if not js is None:
            self.js = js
        if not css is None:
            self.css = css
        if not hack_id is None:
            self._hack_id = hack_id
        value = '<div id="'+self._hack_id+'"></div>'\
              +'<style>'+self.css+'</style>'\
            +'<script>'+self.js+'</script>'+self.html
        self.hack.value = value



class Title(Widget):
    """Widget used to mimic the markwodn syntax of the notebook"""
    def __init__(self, value='Title', **kwargs):
        self._text = value
        kwargs['value'] = "<h1>"+value+"</h1>"
        Widget.__init__(self, widget=wid.HTML, **kwargs)
    @property
    def text(self):
        return self._text
    @text.setter
    def text(self,value):
        self._text = value
        self.value = "<h1>"+value+"</h1>"

class SubTitle(Widget):
    """Widget used to mimic the markwodn syntax of the notebook"""
    def __init__(self, value='Title', **kwargs):
        self._text = value
        kwargs['value'] = "<h2>"+value+"</h2>"
        Widget.__init__(self, widget=wid.HTML, **kwargs)
    @property
    def text(self):
        return self._text
    @text.setter
    def text(self,value):
        self._text = value
        self.value = "<h2>"+value+"</h2>"

class SubSubTitle(Widget):
    """Widget used to mimic the markwodn syntax of the notebook"""
    def __init__(self, value='Title', **kwargs):
        self._text = value
        kwargs['value'] = "<h4 style='font-weight:bold;'>"+value+"</h4>"
        Widget.__init__(self, widget=wid.HTML, **kwargs)
    @property
    def text(self):
        return self._text
    @text.setter
    def text(self,value):
        self._text = value
        self.value = "<h4 style='font-weight:bold;'>"+value+"</h4>"
"""
class DataFrameMappedParameter(object):
    """"""Generic selector for an arbitrary parameter.
           values: list of values to select from.
           name: String containing the name of the param.
           default: Default value. If not specified the firt element of values
                    will be used
    """"""
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
        """"""Alias for target value""""""
        return self.target.value

class PanelMappedParameter(object):
    """"""Selector for an arbitrary marker param mapped from a panel insted of
       a DataFrame. This is stated as a sepparated in order to be able to add
       custom css and model tweaking in further versions""""""
    def __init__(self, panel, name='Parameter', defaults=(None, None)):
        self.panel = panel
        html = ('<div class="pa_map_param-name-' + name
                + '" style=" font-size:22px; text-align:right;">'
                + name + ':</div>')
        self.name = widgets.HTML(value=html, height=30, width="110px")
        self.active = widgets.Checkbox(value=False,
                                       width="15px",
                                       height="15px",
                                       padding=6
                                      )
        #ax1 = panel_shao.panel.axes[panel_shao.not_ti[0]]
        if defaults is None:
            defaults = (None, None)
        if defaults[0] is None:
            self.ax1 = widgets.Dropdown(options=panel.items.values.tolist(),
                                        padding=6,
                                       )
        else:
            self.ax1 = widgets.Dropdown(options=panel.items.values.tolist(),
                                        padding=6,
                                        value=defaults[0])
        if defaults[1] is None:
            self.ax2 = widgets.Dropdown(options=panel.minor_axis.values.tolist(),
                                        padding=6,
                                       )
        else:
            self.ax2 = widgets.Dropdown(options=panel.minor_axis.values.tolist(),
                                        padding=6,
                                        value=defaults[1])

        self.namebox = widgets.HBox(children=[self.active, self.name],
                                    width='150px', align='center')
        self.widget = widgets.HBox([self.namebox, self.ax1, self.ax2])

class Panel4DMappedParameter(object):
    """"""Selector for an arbitrary marker param mapped from a Panel4D. This is
       stated as a sepparated in order to be able to add custom css and model tweaking""""""

    def __init__(self, panel4d, name='Parameter', defaults=(None, None, None)):
        self.panel4d = panel4d
        html = ('<div class="pa_map_param-name-' + name
                + '" style=" font-size:22px; text-align:right;">'
                + name + ':</div>')
        self.name = widgets.HTML(value=html, height=30, width="110px")
        self.active = widgets.Checkbox(value=False,
                                       width="15px",
                                       height="15px",
                                       padding=6
                                      )
        if defaults is None:
            defaults = (None, None, None)
        if defaults[0] is None:
            self.ax1 = widgets.Dropdown(options=panel4d.labels.values.tolist(),
                                        padding=6,
                                       )
        else:
            self.ax1 = widgets.Dropdown(options=panel4d.labels.values.tolist(),
                                        padding=6,
                                        value=defaults[0])
        if defaults[1] is None:
            self.ax2 = widgets.Dropdown(options=panel4d.major_axis.values.tolist(),
                                        padding=6,
                                       )
        else:
            self.ax2 = widgets.Dropdown(options=panel4d.major_axis.values.tolist(),
                                        padding=6,
                                        value=defaults[1])
        if defaults[2] is None:
            self.ax3 = widgets.Dropdown(options=panel4d.minor_axis.values.tolist(),
                                        padding=6,
                                       )
        else:
            self.ax3 = widgets.Dropdown(options=panel4d.minor_axis.values.tolist(),
                                        padding=6,
                                        value=defaults[2])

        self.namebox = widgets.HBox(children=[self.active, self.name],
                                    width='150px', align='center')
        self.widget = widgets.HBox([self.namebox, self.ax1, self.ax2, self.ax3])

class MarkerFreeParams(object):
    """"""Manages the values of the parameters that have not been mapped to data
    """"""
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
                   'marker':'circle',
                   'line_width':1,
                   'line_color':'black',
                   'line_alpha':1
                  }
    @classmethod
    def default_markers(cls):
        """"""Returns a dict containing the label and name of all the bokeh markers.""""""
        return cls.MARKERS
    @classmethod
    def default_free_params(cls):
        """"""Returns a default parameter dict.""""""
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

        top_line = widgets.HBox([self.marker, self.size, self.line_width])
        top_line.padding = 6
        line_block = widgets.VBox([self.line_alpha,
                                   self.line_color])

        fill_block = widgets.VBox([self.fill_alpha,
                                   self.fill_color])

        self.widget = widgets.VBox(children=[self.title,
                                             top_line,
                                             widgets.HBox([line_block,
                                                           fill_block])])
        self.widget.margin = 6

    @property
    def plot_params(self):
        """"""Prepare the dict for tha actual parameter mapping. This means
        eliminating the keys regaring to metaparameters such as colormaps that
        are not explicitly defined on the plot
        """"""
        param_dict = self.params.copy()
        param_dict.pop('marker')
        return param_dict

    def on_fillcolor_change(self, change):
        """"""This is used to keep trac of the selected values in the params dict""""""
        self.params['fill_color'] = change['new']

    def on_fillalpha_change(self, change):
       """ """This is used to keep trac of the selected values in the params dict""""""
        self.params['fill_alpha'] = change['new']

    def on_linecolor_change(self, change):
     """   """This is used to keep trac of the selected values in the params dict""""""
        self.params['line_color'] = change['new']

    def on_linealpha_change(self, change):
      """  """This is used to keep trac of the selected values in the params dict""""""
        self.params['line_alpha'] = change['new']

    def on_marker_change(self, change):
     """   """This is used to keep trac of the selected values in the params dict""""""
        self.params['marker'] = change['new']

    def on_size_change(self, change):
     """   """This is used to keep trac of the selected values in the params dict""""""
        self.params['size'] = change['new']

    def on_linewidth_change(self, change):
     """   """This is used to keep trac of the selected values in the params dict""""""
        self.params['line_width'] = change['new']

class MarkerMappedParams(object):
    """"""A selector composed of multiple parameters to handle
    the input of arguments for a generic plot marker
    """"""
    def __init__(self,
                 default_map=None,
                 pandas=None,
                 values=None,
                 params=None,
                 name=None,
                 title='Mapper'):
        """"""This widget creates a parameter selector""""""
        self.pandas = pandas
        #if there is no default map use a dataframe,
        #if there is no df then use values as columns and default marker params
        if default_map is None:
            if pandas is None:
                param_type = DataFrameMappedParameter
                self.params = MARKER_PARAMS
                if values is None:
                    return #TODO error handling
                else:
                    self.values = values
            elif isinstance(pandas, pd.DataFrame):
                param_type = DataFrameMappedParameter
                self.values = pandas.columns.values.tolist()
                if params is None:
                    self.params = MARKER_PARAMS
                else:
                    self.params = params
            elif isinstance(pandas, pd.Panel4D):
                param_type = Panel4DMappedParameter
                self.values = pandas
                if params is None:
                    self.params = MARKER_PARAMS
                else:
                    self.params = params
            elif isinstance(pandas, pd.Panel):
                param_type = PanelMappedParameter
                self.values = pandas
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
                if isinstance(pandas, pd.DataFrame):
                    param_type = DataFrameMappedParameter
                    self.values = pandas.columns.values.tolist()
                elif isinstance(pandas, pd.Panel4D):
                    param_type = Panel4DMappedParameter
                    self.values = pandas
                elif isinstance(pandas, pd.Panel):
                    param_type = PanelMappedParameter
                    self.values = pandas

            else:
                self.values = values
        #if default map is a list, the list
        #of values can be either the df columsn or the parameter values
        elif isinstance(default_map, list):
            self.default_map = dict([(x, None) for x in self.params])
            self.params = default_map
            self.values = pandas.columns.values.tolist()
        #try to infer the name from the df
        if name is None:
            self.name = 'Columns'
            if isinstance(pandas, pd.DataFrame):
                if not pandas.columns.name is None:
                    self.name = pandas.columns.name
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
        title_text = '<div style="font-size:22px;font-weight:bold;">'+title+'</div>'
        self.titlebar = [widgets.HTML(value=title_text+css)]
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
        self.targets = self.get_targets()
        for tget in self.targets:
            getattr(self.x, tget).observe(self._on_target_change, names='value')

    @property
    def fixed(self):
        """"""Alias to return a boolean if the selector is fixed""""""
        return self.x.active.value

    def get_targets(self):
        if isinstance(self.pandas, pd.Panel):
            return ['ax1', 'ax2']
        elif isinstance(self.pandas, pd.Panel4D):
            return ['ax1', 'ax2', 'ax3']
        elif isinstance(self.pandas, pd.DataFrame) or self.pandas is None:
            return ['target']

    def fix_targets(self):
        """"""All the parameter values will mimic x.value""""""
        if self.fixed:
            #fix all the targets to x and leave y free
            for tget in self.targets:
                for name in self.params[2:]:#do not change y
                   getattr(getattr(self, name), tget).value = getattr(self.x, tget).value
                setattr(self.x, tget+'.disabled', False)
                setattr(self.y, tget+'.disabled', False)
        #else:
            #self.x.target.disabled = True

    def disable_target(self, disabled=True):
        """"""Set all the disable values of the children to disabled""""""
        for tget in self.targets:
            #Do not disable x and y
            for name in self.params[2:]:
                setattr(getattr(getattr(self, name), tget), 'disabled', disabled)

    def _on_fixed_change(self, _):
        self.fix_targets()
        self.disable_target(self.fixed)

    def _on_target_change(self, _):
        self.fix_targets()

class ButtonController(object):
    """"""Buttons for controlling the walkers. Consists of:
        play: run the simulation at "fps" frames per second for "streak" frames
        fwd: tun 1 step forward
        nwd: run 1 step backwards
        rate: Max frames per second when play is clicked
        streak: Play streak frames when play is clicked
    """"""
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
    """"""Simple Datetime HTML display.
        strf: string representig the dt format of the conversion""""""
    def __init__(self, strf='%a %d-%h-%Y %H:%M'):
        self.strf = strf
        html = '<div>Time</div>'
        self.widget = widgets.HTML(html, font_size=20)
        self.widget.width = '300px'

    def update(self, datetime):
        """"""Updates the display value. datetime: date/datetime object""""""
        html = '<div>Time: <strong>'+datetime.strftime(self.strf)+'</strong></div>'
        self.widget.value = html

class TimeProgressBar(object):
    """"""Custom progressbar adapted for displaying datetimes.
        index: Pandas datetime index object. Used in displaying start
               and end labels and determines the size of the bar.
        strf: string representig the dt format of the conversion
    """"""
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
    """"""A widget for controlling a walker. It has all the time widgets
        combined to provide a animation control panel for Walkers.
        index: Pandas datetime index object. Used in displaying start
               and end labels and determines the size of the bar.
        strf: string representig the dt format of the conversion
    """"""
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
        """"""Alias for its internal TimeDiraplay widget""""""
        return self.tdis.widget

    def update(self, datetime, strf=None):
        """"""Updates Walker bar and its children""""""
        if strf is None:
            strf = self.strf
        self.pbar.pbar.value = self.index.get_loc(datetime)
        self.tdis.update(datetime)
        self.tdis.strf = strf
        self.pbar.strf = strf
"""