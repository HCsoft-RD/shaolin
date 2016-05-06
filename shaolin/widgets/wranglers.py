# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 10:22:21 2016

@author: Guillem Duran for HCSOFT
This module contains all the widgets used to configure the wranglers
"""

import ipywidgets as widgets
import numpy as np

from .generic import SelectMultiple

LAYOUT_PARAMS = {'dim':'both',
                 'scale':1,
                 'center':None,
                 'weigth':'weight',
                 'fixed':None,
                 'iterations':5000,
                 'prog':'neato',
                 'layout':'dh_spring_layout',
                 'k':'exchange'}
LAYOUTS = {'Circular layout': 'circular_layout',
           'Random layout': 'random_layout',
           'Shell layout':'shell_layout',
           'Spectral layout':'spectral_layout',
           'Spring layout':'spring_layout',
           'Graphviz layout':'draw_graphviz',
           'HCsoft layout':'dh_spring_layout'}

TARGET_OPTIONS = {'Raw':'raw', #Do nothing
                  'Clip':'clip', #limit the matrix values betwen (min,max)
                  'Scale':'scale', #scale the matrix values between (min,max)
                  'Zscore':'zscore', #zscore the matrix elements
                  'Distance':'compute_distance', #Convert corr into a distance
                 }

MATRIX_PARAMS = {'norm_min':0,
                 'norm_max':1,
                 'clip_min':1e-5,
                 'clip_max':1e10,
                 'target':[('clip', (1e-5, 1e10))],#f[(fun,(kwargs))]
                }

GRAPH_PARAMS = {'graph_type':'full',
                'inverted' :  False,
                'threshold': 0.00,
                'target_attr':'exchange'
               }

NODE_METRICS = ['betweenness_centrality',
                'betweenness',
                'degree',
                'degree_weighted',
                'eigenvector_weighted',
                'eigenvector',
                'closeness_weighted',
                'closeness',
                'eccentricity_weighted',
                'eccentricity',
                'X', 'Y', 'XmY', 'XpY']

NODE_TARGET_ATTRS = {'Simetric max':'M',
                     'Correlation':'corr',
                     'Covariance':'cov',
                     'Market custom':'exchange',
                     'k spring':'k_price',
                     'L0':'l0',
                     'Simetric min':'m'}

class ScaleParams(object):
    """This class is used to control the transformation of data into visual attributes"""
    PARAMS = {'size_max':40,
              'size_min':20,
              'size_transform':'raw',
              'fill_alpha_max':1,
              'fill_alpha_min':0.2,
              'fill_alpha_transform':'raw',
              'line_alpha_max':1,
              'line_alpha_min':0.2,
              'line_alpha_transform':'raw',
              'line_width_max':4,
              'line_width_min':1,
              'line_width_transform':'raw',}

    @classmethod
    def get_default_params(cls):
        """Return defaults"""
        return cls.PARAMS

    def __init__(self, default_params=None):
        if default_params is None:
            self.params = self.get_default_params()
        else:
            self.params = default_params

        self.transforms = ['raw', 'zscore', 'log', 'rank']

        #SIZE TRANSFORMS
        self.size_max = widgets.BoundedFloatText(min=0,
                                                 max=150,
                                                 description='Max',
                                                 value=self.params['size_max'],
                                                 width="50px",
                                                 padding=6)
        self.size_max.observe(self.on_sizemax_change, names='value')

        self.size_min = widgets.BoundedFloatText(min=0,
                                                 max=150,
                                                 description='Min',
                                                 value=self.params['size_min'],
                                                 width="50px",
                                                 padding=6)
        self.size_min.observe(self.on_sizemin_change, names='value')

        self.size_transform = SelectMultiple(options=self.transforms,
                                             value=[self.params['size_transform']],
                                             title='',
                                             description='Transform:',
                                            )
        self.size_transform.widget.observe(self.on_sizetrans_change, names='value')


        #FILL ALPHA TRANSFORMS
        self.fill_alpha_max = widgets.FloatSlider(min=0,
                                                  max=1,
                                                  step=0.01,
                                                  description='Max',
                                                  value=self.params['fill_alpha_max'],
                                                  width="130px",
                                                  padding=6)
        self.fill_alpha_max.observe(self.on_maxfilla_change, names='value')

        self.fill_alpha_min = widgets.FloatSlider(min=0,
                                                  max=1,
                                                  step=0.01,
                                                  description='Min',
                                                  value=self.params['fill_alpha_min'],
                                                  width="130px",
                                                  padding=6)
        self.fill_alpha_min.observe(self.on_minfilla_change, names='value')

        self.fill_alpha_transform = SelectMultiple(options=self.transforms,
                                                   value=[self.params['fill_alpha_transform']],
                                                   title='',
                                                   description='Transform:',
                                                  )
        self.fill_alpha_transform.widget.observe(self.on_fillatrans_change, names='value')

        #LINE ALPHA TRANSFROMS
        self.line_alpha_max = widgets.FloatSlider(min=0,
                                                  max=1,
                                                  step=0.01,
                                                  description='Max',
                                                  value=self.params['line_alpha_max'],
                                                  width="130px",
                                                  padding=6)
        self.line_alpha_max.observe(self.on_maxlinea_change, names='value')

        self.line_alpha_min = widgets.FloatSlider(min=0,
                                                  max=1,
                                                  step=0.01,
                                                  description='Min',
                                                  value=self.params['line_alpha_min'],
                                                  width="130px",
                                                  padding=6)
        self.line_alpha_min.observe(self.on_minlinea_change, names='value')

        self.line_alpha_transform = SelectMultiple(options=self.transforms,
                                                   value=[self.params['line_alpha_transform']],
                                                   title='',
                                                   description='Transform:',
                                                  )
        self.line_alpha_transform.widget.observe(self.on_lineatrans_change, names='value')
        #LINE WIDTH
        self.line_width_max = widgets.FloatSlider(min=0,
                                                  max=40,
                                                  step=0.01,
                                                  description='Max',
                                                  value=self.params['line_width_max'],
                                                  width="130px",
                                                  padding=6)
        self.line_width_max.observe(self.on_maxlwidth_change, names='value')

        self.line_width_min = widgets.FloatSlider(min=0,
                                                  max=40,
                                                  step=0.01,
                                                  description='Min',
                                                  value=self.params['line_width_min'],
                                                  width="130px",
                                                  padding=6)
        self.line_width_min.observe(self.on_minlwidth_change, names='value')
        self.line_width_transform = SelectMultiple(options=self.transforms,
                                                   value=[self.params['line_width_transform']],
                                                   title='',
                                                   description='Transform:',
                                                  )
        self.line_width_transform.widget.observe(self.on_lwidthtrans_change, names='value')

        #LAYOUT
        title_text = """Scale parameters"""
        title_css = """font-size:22px;font-weight:bold;"""
        self.title_w = widgets.HTML(value=self.html_text(title_text, title_css), padding=6)

        la_text = """Line alpha"""
        la_css = """font-size:18px;font-weight:bold;"""
        self.la_w = widgets.HTML(value=self.html_text(la_text, la_css))

        fa_text = """Fill alpha"""
        fa_css = """font-size:18px;font-weight:bold;"""
        self.fa_w = widgets.HTML(value=self.html_text(fa_text, fa_css))

        lw_text = """Line width"""
        lw_css = """font-size:18px;font-weight:bold;"""
        self.lw_w = widgets.HTML(value=self.html_text(lw_text, lw_css))

        s_text = """Size"""
        s_css = """font-size:18px;font-weight:bold;"""
        self.s_w = widgets.HTML(value=self.html_text(s_text, s_css))

        self.size_b = widgets.VBox(children=[self.s_w,
                                             self.size_max,
                                             self.size_min,
                                             self.size_transform.widget
                                            ])

        self.lw_b = widgets.VBox(children=[self.lw_w,
                                           self.line_width_max,
                                           self.line_width_min,
                                           self.line_width_transform.widget
                                          ],
                                 padding=6,
                                 width="230px")

        self.la_b = widgets.VBox(children=[self.la_w,
                                           self.line_alpha_max,
                                           self.line_alpha_min,
                                           self.line_alpha_transform.widget],
                                 padding=6,
                                 width="230px")

        self.fa_b = widgets.VBox(children=[self.fa_w,
                                           self.fill_alpha_max,
                                           self.fill_alpha_min,
                                           self.fill_alpha_transform.widget],
                                 padding=6,
                                 width="230px")

        main_row = widgets.HBox(children=[self.size_b, self.lw_b, self.la_b, self.fa_b], padding=6)
        self.widget = widgets.VBox(children=[self.title_w,
                                             main_row])

    def external_observe(self, func):
        """Bind an external function to every widget"""
        for key in self.params.keys():
            if key[-10:] != '_transform':
                getattr(self, key).observe(func, names='value')
            else:
                getattr(self, key).widget.observe(func, names='value')

    @staticmethod
    def html_text(text, css):
        """Creates a div container with the given text and css"""
        html = '<div class="kf-pms-mulsel" id="title" style="'+\
                                      css+'">'+\
                                      text+'</div>'
        return html

    def on_sizetrans_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['size_transform'] = change['new']

    def on_lineatrans_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['line_alpha_transform'] = change['new']

    def on_fillatrans_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['fill_alpha_transform'] = change['new']

    def on_lwidthtrans_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['line_width_transform'] = change['new']

    def on_sizemax_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['size_max'] = change['new']

    def on_sizemin_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['size_min'] = change['new']

    def on_siztrans_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['size_transform'] = change['new']

    def on_maxfilla_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['fill_alpha_max'] = change['new']

    def on_minfilla_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['fill_alpha_min'] = change['new']

    def on_maxlinea_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['line_alpha_max'] = change['new']

    def on_minlinea_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['line_alpha_min'] = change['new']

    def on_maxlwidth_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['line_width_max'] = change['new']

    def on_minlwidth_change(self, change):
        """This is used to keep trac of the selected values in the params dict"""
        self.params['line_width_min'] = change['new']

class LayoutParams(object):
    """Widget for managing the parameters necessary for the layout calculator.
       It's able to manage all the default basic parameters that networkx takes as input
       LAYOUT_PARAMS = {'dim':'both',
                 'scale':1,
                 'center':None,
                 'weigth':'weight',
                 'fixed':None,
                 'iterations':5000,
                 'prog':'neato',
                 'layout':'custom_spring',
                 'k':'exchange'}

       LAYOUTS = {'Circular layout': 'circular_layout',
                           'Random layout': 'random_layout',
                           'Shell layout':'shell_layout',
                           'Spectral layout':'spectral_layout',
                           'Spring layout':'spring_layout',
                           'Graphviz layout':'draw_graphviz',
                           'HCsoft layout':'dh_spring_layout'}
    """
    def __init__(self, G, default_params=LAYOUT_PARAMS):
        self.params = default_params #TODO check user customs is ok
        self.G = G.copy()
        self.dim = widgets.ToggleButtons(description='Dimension:',
                                         options={'2D':'2d',
                                                  '3D':'3d',
                                                  'Both':'both'},
                                         value=self.params['dim'],
                                        )
        self.dim.observe(self.on_value_change, names='value')

        self.scale = widgets.BoundedFloatText(value=self.params['scale'],
                                            min=1e-4,
                                            max=10e4,
                                            description='Scale:',
                                            width="100%",
                                            padding=6
                                           )
        self.scale.observe(self.on_value_change, names='value')

        self.center_display = widgets.Text(description='Center:',
                                           value=str(self.params['center']),
                                           width="80px",
                                           padding=6
                                          )
        self.center_display.observe(self.on_value_change,
                                    names='value')

        self.fixed_display = widgets.SelectMultiple(description='Root Node',
                                                    options=list(G.nodes())+['None'],
                                                    value=[str(self.params['fixed'])],
                                                    width="100%",
                                                    padding=6
                                                   )
        self.fixed_display.observe(self.on_value_change, names='value')

        self.iterations = widgets.BoundedIntText(value=self.params['iterations'],
                                                 min=1,
                                                 max=10e4,
                                                 description='Iterations:',
                                                 width="100%",
                                                 padding=6
                                                )
        self.iterations.observe(self.on_value_change, names='value')

        self.prog = widgets.ToggleButtons(description='Prog:',
                                          options=['neato', 'twopi',
                                                   'fdp', 'dot', 'circo'],
                                          value=self.params['prog']
                                         )
        self.prog.observe(self.on_value_change, names='value')

        edges = G.edges()[0]
        self.ls_weights = list(G.edge[edges[0]][edges[1]].keys())
        self.weight = widgets.Dropdown(description='Weight',
                                       options=self.ls_weights+['None'],
                                       value=str(self.params['weigth']),
                                       width="150px",
                                       padding=6
                                      )
        self.weight.observe(self.on_value_change, names='value')

        self.kmet = widgets.Dropdown(description='k',
                                     options=self.ls_weights,
                                     value=str(self.params['k']),
                                     width="150px",
                                     padding=6
                                    )
        self.kmet.observe(self.on_value_change, names='value')

        self.kfloat = widgets.BoundedIntText(value=0,
                                             min=0,
                                             max=10e4,
                                             description='k:',
                                             width="100%",
                                             padding=6
                                            )
        self.kfloat.observe(self.on_value_change, names='value')

        self.ls_layouts = LAYOUTS
        self.layout = widgets.Select(description='Layout',
                                     options=self.ls_layouts,
                                     value=self.params['layout'],
                                     width="100%",
                                     padding=6
                                    )
        self.layout.observe(self.on_layout_change, names='value')

        self.title = widgets.HTML(value="""<b class="gc-layout"
                                  style="font-size:18px;">Graph Layout</b></br>""")

        self.k_box = widgets.HBox(children=[self.iterations,
                                            self.kmet,
                                            self.kfloat])
        self.top_box = widgets.HBox(children=[self.dim,
                                              self.scale,
                                              self.center_display])
        self.wi_box = widgets.VBox(children=[self.weight,
                                             self.k_box,
                                             self.prog])
        self.bot_box = widgets.HBox(children=[self.fixed_display,
                                              self.wi_box])
        self.r_box = widgets.VBox(children=[self.top_box,
                                            self.bot_box])
        self.body = widgets.HBox(children=[self.layout,
                                           self.r_box])
        self.widget = widgets.VBox(children=[self.title,
                                             self.body])
        self.update_display()
        #Can inherit a target when not used as a widget
        self.update_value()

    def update_display(self):
        """Updates the visual attributes of the widget"""
        simple = ['circular_layout', 'random_layout', 'shell_layout']
        if self.layout.value in simple:
            disable = ['prog', 'iterations', 'fixed_display',
                       'weight', 'kmet', 'kfloat']
            for item in disable:
                getattr(self, item).visible = False

        if self.layout.value == 'spectral_layout':
            disable = ['prog', 'iterations',
                       'fixed_display', 'kmet', 'kfloat']
            for item in disable:
                getattr(self, item).visible = False
            self.weight.visible = True

        if self.layout.value == 'spring_layout':
            disable = ['prog', 'kmet']
            for item in disable:
                getattr(self, item).visible = False
            self.weight.visible = True
            self.iterations.visible = True
            self.fixed_display.visible = True
            self.kfloat.visible = True

        if self.layout.value == 'draw_graphviz':
            disable = ['kmet', 'kfloat']
            for item in disable:
                getattr(self, item).visible = False
            self.weight.visible = True
            self.iterations.visible = True
            self.fixed_display.visible = True
            self.prog.visible = True

        if self.layout.value == 'dh_spring_layout':
            disable = ['prog', 'kfloat']
            for item in disable:
                getattr(self, item).visible = False
            self.fixed_display.visible = True
            self.weight.visible = True
            self.iterations.visible = True
            self.fixed_display.visible = True
            self.kmet.visible = True

    def single_val(self, dim=2):
        """Calculates the layout dict for a given dimension of the layout.
            dim: dimension of the layout we want to calculate its parameters.
            return: an attribute dictionary keyed with the name of the function
                    containing its kwargs
        """
        layout = {}
        simple = ['circular_layout', 'random_layout', 'shell_layout']
        if self.layout.value in simple:
            kwargs = {'dim':dim,
                      'scale':self.scale.value,
                      'center':self.get_center()}

        if self.layout.value == 'spectral_layout':
            kwargs = {'dim':dim,
                      'scale':self.scale.value,
                      'center':self.get_center(),
                      'weight':self.get_weight()}

        if self.layout.value == 'spring_layout':
            kwargs = {'dim':dim,
                      'scale':self.scale.value,
                      'center':self.get_center(),
                      'weight':self.get_weight(),
                      'iterations':self.iterations.value,
                      'fixed':self.get_fixed(),
                      'k':self.get_k()}

        if self.layout.value == 'draw_graphviz':
            kwargs = {'prog':self.prog.value,
                      'root':self.get_fixed()}

        if self.layout.value == 'dh_spring_layout':
            kwargs = {'dim':dim,
                      'scale':self.scale.value,
                      'center':self.get_center(),
                      'weight':self.get_weight(),
                      'iterations':self.iterations.value,
                      'fixed':self.get_fixed(),
                      'k':self.kmet.value}
        layout[self.layout.value] = kwargs
        return layout

    def get_fixed(self):
        """Gets the fixed value from the text input. it's a way to handle the None"""
        values = self.fixed_display.value
        if values[0] == 'None':
            return None
        else:
            return values

    def get_weight(self):
        """Gets the fixed value from the text input. it's a way to handle the None"""
        value = self.weight.value
        if value == 'None':
            return None
        else:
            return value

    def get_k(self):
        """Gets the k value from the text input. it's a way to handle the None"""
        if self.kfloat.value == 0:
            return None
        else:
            return self.kfloat.value

    def get_center(self):
        """Gets the center value from the text input"""
        import ast
        if self.center_display.value == 'None':
            return None
        else:
            data = ast.literal_eval(self.center_display.value)
            np.array(data)

    def update_value(self):
        """Updates the target parameter dict for the selected dimensions"""
        dims = {}
        if self.dim.value == '2d':
            dims['2d'] = self.single_val(dim=2)
            dims['3d'] = None
        elif self.dim.value == '3d':
            dims['3d'] = self.single_val(dim=3)
            dims['2d'] = None
        elif self.dim.value == 'both':
            dims['2d'] = self.single_val(dim=2)
            dims['3d'] = self.single_val(dim=3)
        self.target = dims

    def on_value_change(self, _):
        """Trigger for value updater"""
        self.update_value()
    def on_layout_change(self, _):
        """Trigger for value and layout updater"""
        self.update_display()
        self.update_value()

class MatrixParams(object):
    """Thi widget handles the parameter for creating the matrix we
    will transform into a graph:
    MATRIX_PARAMS = {'norm_min': 0,
                     'norm_max': 1,
                     'clip_min':1e-5,
                     'clip_max':1e10,
                     'target':[('clip', (1e-5,1e10))],#f[(fun,(kwargs))]

    TARGET_OPTIONS = {'Raw':'raw', #Do nothing
                      'Clip':'clip', #limit the matrix values betwen (min,max)
                      'Scale':'scale', #scale the matrix values between (min,max)
                      'Zscore':'zscore', #zscore the matrix elements
                      'Distance':'compute_distance', #Convert corr into a distance
                      }
    """
    def __init__(self, default_params=MATRIX_PARAMS):
        self.params = default_params

        self.norm_min = widgets.BoundedFloatText(value=self.params['norm_min'],
                                                 min=-50,
                                                 max=50,
                                                 description='Rescale min:',
                                                 width='100%',
                                                 padding=6
                                                )
        self.norm_min.observe(self.update_num, names='value')

        self.norm_max = widgets.BoundedFloatText(value=self.params['norm_max'],
                                                 min=-50,
                                                 max=50,
                                                 description='Rescale Max:',
                                                 width='100%',
                                                 padding=6
                                                )
        self.norm_max.observe(self.update_num, names='value')

        self.clip_min = widgets.BoundedFloatText(value=self.params['clip_min'],
                                                 min=-50,
                                                 max=50,
                                                 description='Clip min:',
                                                 width='100%',
                                                 padding=6
                                                )
        self.clip_min.observe(self.update_num, names='value')

        self.clip_max = widgets.BoundedFloatText(value=self.params['clip_max'],
                                                 min=-50,
                                                 max=50,
                                                 description='Clip Max:',
                                                 width='100%',
                                                 padding=6
                                                )
        self.clip_max.observe(self.update_num, names='value')

        self.options = TARGET_OPTIONS
        self.target_selector = widgets.Select(options=self.options,
                                              value=self.params['target'][0][0],
                                              description='Transform matrix:',
                                              width='100%',
                                             )
        self.mapping = {'raw':None,
                        'clip':(self.clip_min.value,
                                self.clip_max.value),
                        'scale':(self.norm_min.value,
                                 self.norm_max.value),
                        'zscore':None,
                        'compute_distance':None,
                       }

        self.add = widgets.Button(description="add")
        self.add.on_click(self.on_add_clicked)

        self.delete = widgets.Button(description="delete")
        self.delete.on_click(self.on_del_clicked)
        self.buttonbox = widgets.HBox(children=[self.add,
                                                self.delete],
                                      align='center'
                                     )
        self.value = self.params['target']
        self.numbox = widgets.VBox(children=[self.norm_min,
                                             self.norm_max,
                                             self.clip_min,
                                             self.clip_max],
                                   margin=10,
                                   align='center'
                                  )

        self.target_display = widgets.Textarea(value=str(self.value),
                                               width='215px',
                                               height='100px'
                                              )
        self.targetbox = widgets.VBox(children=[self.target_selector,
                                                self.buttonbox,
                                                self.target_display],
                                      margin=10,
                                      padding=6
                                     )
        title_html = '''<div class="graph-mtrans" style="font-size:18px;
                                                        font-weight: bold; 
                                                        text-align:right;">
                                                        Matrix transformations</div>'''
        self.title = widgets.HTML(value=title_html)
        self.widget = widgets.VBox(children=[self.title,
                                             widgets.HBox(children=[self.numbox,
                                                                    self.targetbox])
                                            ],
                                   padding=6
                                  )

    def update_num(self, _):
        """Updates the numeric MATRIX_ATTRIBUTES: max and min values for clip and scale"""
        self.mapping = {'raw':None,
                        'clip':(self.clip_min.value,
                                self.clip_max.value),
                        'scale':(self.norm_min.value,
                                 self.norm_max.value),
                        'zscore':None,
                        'distance':None,
                       }

    def on_del_clicked(self, _):
        """Trigger for updating the center widget.from del button."""
        self.value.pop()
        self.target_display.value = str(self.value)
    def on_add_clicked(self, _):
        """Trigger for updating the center widget.from del button."""
        key = self.target_selector.value
        new = (key, self.mapping[key])
        self.value.append(new)
        self.target_display.value = str(self.value)

class GraphParams(object):
    """Widget for managing the parameters needed to convert a matrix into a graph
        Params:
        ---------------------------------------------------------------------
        GRAPH_PARAMS = {'graph_type':'full',
                       'inverted' :  False,
                       'threshold': 0.00,
                       'target_attr':'exchange'}

        NODE_METRICS = ['betweenness_centrality', 'betweenness', 'degree', 'degree_weighted',
                   'X', 'eigenvector_weighted', 'eigenvector', 'closeness_weighted',
                   'closeness', 'eccentricity_weighted', 'eccentricity', 'Y', 'XmY', 'XpY']

        NODE_TARGET_ATTRS = {'Simetric max':'M',
                             'Correlation':'corr',
                             'Covariance': 'cov',
                             'Market custom': 'exchange',
                             'k spring': 'k_price',
                             'L0': 'l0',
                             'Simetric min' : 'm'}
    """
    def __init__(self, default_params=GRAPH_PARAMS,
                 metrics=NODE_METRICS,
                 target=NODE_TARGET_ATTRS):
        self.params = default_params
        self._lmetrics = metrics
        self.dict_target_attrs = target

        self.graph_type = widgets.ToggleButtons(description='Graph type:',
                                                options={'Mst':'mst',
                                                         'Pmfg':'pmfg',
                                                         'Full Matrix':'full'},
                                                value=self.params['graph_type'],
                                                margin=10
                                               )

        self.threshold = widgets.BoundedFloatText(value=self.params['threshold'],
                                                  min=0,
                                                  max=50e10,
                                                  description='Abs val Treshold:',
                                                  width='100%',
                                                  padding=6
                                                 )

        self.inverted = widgets.Checkbox(description='Invert distance',
                                         value=False,
                                        )

        self.metrics = widgets.SelectMultiple(description="Metrics",
                                              options=self._lmetrics,
                                              value=self._lmetrics,
                                              width="100%"
                                             )

        self.row = widgets.HBox(children=[self.threshold, self.inverted],
                                padding=6
                               )

        self.target_attr = widgets.Dropdown(options=self.dict_target_attrs,
                                            value=self.params['target_attr'],
                                            description='Target attribute',
                                            padding=6
                                           )
        title_html = '''<div class="graph-mtrans" style=" font-size:18px;
                                                        font-weight: bold; 
                                                        text-align:right;">
                                                        Graph creation parameters</div>'''
        self.title = widgets.HTML(value=title_html)
        self.widget = widgets.VBox(children=[self.title,
                                             self.graph_type,
                                             self.row,
                                             self.metrics,
                                             self.target_attr],
                                   padding=6
                                  )
