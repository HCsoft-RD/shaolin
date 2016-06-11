# -*- coding: utf-8 -*-
"""
Created on Wed May 25 12:38:54 2016

@author: Guillem Duran. Property of HCSOFT
"""
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import ListedColormap
from seaborn.palettes import (color_palette, dark_palette, light_palette,
                              diverging_palette, cubehelix_palette)

from IPython.core.display import Image
from matplotlib import cm
import matplotlib as mpl


from shaolin.core.dashboard import Dashboard, ToggleMenu


class ColormapPicker(Dashboard):
    
    def __init__(self,description='Cmap', **kwargs):
        
        dash = ['c$N=cmap_picker',
                [
                    ['r$N=display_col',['btn$N=cmap_btn&d='+description, 'HTML$N=mini_display']],
                    ['c$N=palette_col', [MasterPalette(name='master_palette',mode='interactive'),'btn$d=Close&N=close_btn'] ]
                 
                ]
               ]
        Dashboard.__init__(self, dash, **kwargs)
        self.mini_display.target.layout.width = "20em"
        self.mini_display.target.layout.height = "2em"
        self.palette_col.visible = False
        self.cmap = self.master_palette.cmap
        self.pal = self.master_palette.pal
        self.cmap_btn.observe(self._on_cmap_click)
        self.close_btn.observe(self._on_close_click)
        self._on_close_click()
    
    def map_data(self, data, hex=None):
        if hex is None:
            hex = self.master_palette._hex
        return self.master_palette.map_data(data, hex)    
    
    def _on_cmap_click(self,_=None):
        self.palette_col.visible = True
    
    def _on_close_click(self,_=None):
        self.palette_col.visible = False
        self.mini_display.value = self.master_palette.fig_widget.value
        self.cmap = self.master_palette.cmap
        self.pal = self.master_palette.pal
        
class SeabornColor(Dashboard):
    
    def __init__(self,metaparam_dash,control_dash,title, **kwargs):
        self._metaparam_dash = metaparam_dash
        self._control_dash = control_dash
        dash = ['c$N=color_widget',
                [
                    ['r$N=row_title',['#'+title+'$N=title']],
                    ['r$N=row_controls',[self._metaparam_dash, self._control_dash]],
                    'HTML$n=fig_widget'
                ]
               ]
        
        self.pal = []
        self.cmap = self._init_mutable_colormap()
        Dashboard.__init__(self, dash, **kwargs)
        self.init_fig_widget()
        
    def init_fig_widget(self, size=1):
        f, ax = plt.subplots(1, 1, figsize=(1 * size, size))
        plt.close()
        self.fig_widget.value = self.fig_to_html(f)
    
    def update_fig_widget(self, _=None, height=None, width=None):
        if self.as_cmap.value:
            self.n_colors.widget.visible = False
            fig = self._cmap_figure(self.cmap)
        else:
            self.n_colors.widget.visible = True
            fig = self._palplot_figure(self.pal)
        if height is None:
            self.fig_widget.widget.layout.height= "7em"
        else:
            self.fig_widget.widget.layout.height= height
        if width is None:
            self.fig_widget.widget.layout.width= "100%"
        else:
            self.fig_widget.widget.layout.width= width
        self.fig_widget.target.layout.width= "100%"
        self.fig_widget.target.layout.height= "100%"
        self.fig_widget.value = self.fig_to_html(fig[0])# height=height, width=width)
    
    def get_mini_plot(self,height, width):
        if self.as_cmap.value:
            self.n_colors.widget.visible = False
            fig = self._cmap_figure(self.cmap)
        else:
            self.n_colors.widget.visible = True
            fig = self._palplot_figure(self.pal)
        return self.fig_to_html(fig[0], height=height, width=width)
    
    @staticmethod
    def _init_mutable_colormap():
        """Create a matplotlib colormap that will be updated by the widgets."""
        greys = color_palette("Greys", 256)
        cmap = LinearSegmentedColormap.from_list("interactive", greys)
        cmap._init()
        cmap._set_extremes()
        return cmap
    
    @staticmethod
    def _update_lut(cmap, colors):
        """Change the LUT values in a matplotlib colormap in-place."""
        cmap._lut[:256] = colors
        cmap._set_extremes()
    @staticmethod
    def _show_cmap(cmap):
        """Show a continuous matplotlib colormap."""
        from seaborn.rcmod import axes_style  # Avoid circular import
        with axes_style("white"):
            f, ax = plt.subplots(figsize=(13.25, .75))
        ax.set(xticks=[], yticks=[])
        x = np.linspace(0, 1, 256)[np.newaxis, :]
        ax.pcolormesh(x, cmap=cmap)
    @staticmethod
    def _palplot_figure(pal, size=1):
        """Return the matplotlib figure and axis corresponding to a palplot plot.
        Plot the values in a color palette as a horizontal array.
        Parameters
        ----------
        pal : sequence of matplotlib colors
            colors, i.e. as returned by seaborn.color_palette()
        size :
            scaling factor for size of plot
        """
        n = len(pal)
        f, ax = plt.subplots(1, 1, figsize=(n * size, size))
        ax.imshow(np.arange(n).reshape(1, n),
                  cmap=mpl.colors.ListedColormap(list(pal)),
                  interpolation="nearest", aspect="auto")
        ax.set_xticks(np.arange(n) - .5)
        ax.set_yticks([-.5, .5])
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        plt.close(f)
        return f, ax
    @staticmethod
    def _cmap_figure(cmap):
        """Show a continuous matplotlib colormap."""
        from seaborn.rcmod import axes_style  # Avoid circular import
        with axes_style("white"):
            f, ax = plt.subplots(figsize=(13.25, .75))
        ax.set(xticks=[], yticks=[])
        x = np.linspace(0, 1, 256)[np.newaxis, :]
        ax.pcolormesh(x, cmap=cmap)
        plt.close(f)
        return f, ax

    def fig_to_html(self, fig, img_class='', height=None, width=None):
        """This is a hack that converts a matplotlib like fig to an HTML image div"""
        from io import BytesIO
        import base64
        imgdata = BytesIO()
        fig.savefig(imgdata, format='png', bbox_inches=0, transparent=True)
        imgdata.seek(0)  # rewind the data
        svg_dta = imgdata.getvalue()
        svg_image = Image(svg_dta)#
        svg_b64 = base64.b64encode(svg_image.data).decode()
        if height is None:
            height = self.fig_widget.target.layout.height
        if width is None:
            width = self.fig_widget.target.layout.width
        return '<img class="cmap '+img_class+'" height="'+str(height)+'" width="'\
                +str(width)+'" src="data:image/png;base64,'+svg_b64+'" />'


class MasterPalette(ToggleMenu):

    def __init__(self, hex=False, **kwargs):
        self._hex = hex
        colorbrewer = ColorBrewerPalette(name='colorbrewer')
        diverging = DivergingPalette(name='diverging')
        sequential = SequentialPalette(name='sequential')
        cubehelix = CubeHelixPalette(name='cubehelix')
        sns_palette = SeabornPalette(name='sns_palette')
        button_labels = ['Diverging', 'Colorbrewer', 'Sequential',
                         'Cubehelix', 'Seaborn']
        ToggleMenu.__init__(self,
                            children=[diverging, colorbrewer, sequential,
                                            cubehelix, sns_palette],
                            button_labels=button_labels,
                            **kwargs
                           )
        
        
        self.pal = self.diverging.pal
        self.cmap = self.diverging.cmap
        self.observe(self.update_masterpalette)
        self.update_masterpalette()
        selected = getattr(self, self.buttons.value)
        selected.as_cmap.value = False
        selected.as_cmap.value = True
        #self.buttons.observe(self._display_one)
        #self._display_one()
    def _hide_all(self):
        for child in self.get_children_names(self.children_dash):
            if getattr(self,child).widget.visible:
                setattr(getattr(self,child).widget,'visible',False)
        
    
    def update_toggle(self, _=None):
        """updates toggle visibility"""
        
        """self.cubehelix.update()
        self.cubehelix.update_fig_widget()
        self.sequential.update()
        self.sequential.update_fig_widget()
        self.sns_palette.update()
        self.sns_palette.update_fig_widget()
        self.diverging.update()
        self.diverging.update_fig_widget()
        self.colorbrewer.update()
        self.colorbrewer.update_fig_widget()"""

        for name in self.child_names:
            child = getattr(self, name)
            if name == self.buttons.value:
                child.visible = True
                child.update()
            elif child.visible:
                    child.visible = False
        
    
    @property
    def target(self):
        return self
    @property
    def fig_widget(self):
        return getattr(self, self.buttons.value).fig_widget
        
    def _display_one(self, _=None):
        self._hide_all()
        setattr(getattr(self,self.buttons.value), 'visible', True)
        
    def update_masterpalette(self, _=None):
        val = self.buttons.value
        self.pal = getattr(self,val).pal
        self.cmap = getattr(self,val).cmap

    def map_data(self, data, hex=None):
        "Maps an array of data according to the selected palette/colormap"
        if hex is None:
            hex = self._hex
        selected = getattr(self, self.buttons.value)
        Ma = np.max(data)
        mi = np.min(data)
        norm = ((data-mi)/(Ma-mi))#to 0-1 interval
        if selected.as_cmap.value:
            rgb_colors = self.cmap(norm)
        else:
            self.pal_cmap = ListedColormap(self.pal,
                                      N=selected.n_colors.value)
            rgb_colors = self.pal_cmap(norm)

        if hex:
            return [mpl.colors.rgb2hex(rgb).upper() for rgb in rgb_colors]
        else:
            return rgb_colors

class SeabornPalette(SeabornColor):
    """Select a palette from the seaborn palette function.
    These palettes are built into matplotlib and can be used by name in
    many seaborn functions, or by passing the object returned by this function.
    Parameters
    ----------
    data_type : {'sequential', 'diverging', 'qualitative'}
        This describes the kind of data you want to visualize. See the seaborn
        color palette docs for more information about how to choose this value.
        Note that you can pass substrings (e.g. 'q' for 'qualitative.
    as_cmap : bool
        If True, the return value is a matplotlib colormap rather than a
        list of discrete colors.
    Returns
    -------
    pal or cmap : list of colors or matplotlib colormap
        Object that can be passed to plotting functions.
    See Also
    --------
    dark_palette : Create a sequential palette with dark low values.
    light_palette : Create a sequential palette with bright low values.
    diverging_palette : Create a diverging palette from selected colors.
    cubehelix_palette : Create a sequential palette or colormap using the
                        cubehelix system.
    """
    def __init__(self,
                 type='seaborn',
                 title='Seaborn palette',
                 as_cmap=False,
                 n=10,
                 desat=1,
                 name='sns_palette',
                 **kwargs
                ):
        cmlist = list(cm.cmap_d.keys())
        cmlist.sort()
        sns_pals = ['deep', 'muted', 'bright',
                    'pastel', 'dark', 'colorblind']
        variants = ["regular", "reverse", "dark"]
        types = ['hls', 'husl', 'seaborn', 'matplotlib']
        control_box = ['c$N=seaborn_palette',
                       [
                        ['r$N=varopts_row',['@rad$N=variant&o='+str(variants),
                                            '@select$N=mpl_cmaps&o='+str(cmlist),
                                            '@select$N=sns_palette&o='+str(sns_pals),
                                           ]],
                        ['r$N=desat_row',['@(0, 1, 0.05, 1.00)$d=Desat']]#'@fs$d=desat&min=0&max=1&val=1&step=0.05']]

                       ]
                      ]
        metaparam_box =['c$N=cbw_metaparam_box',
                        ['@True$d=As cmap',
                         '@rad$d=Type&o='+str(types),
                         '@int_slider$d=n_colors&min=2&max=32&val=10&step=1'
                        ]
                       ]
        
        SeabornColor.__init__(self, control_box, metaparam_box, title, mode='interactive', name=name, **kwargs)
        self.observe(self.update)
        self.observe(self.update_fig_widget)
        self.update()
        self.update_fig_widget()
        


    def update(self, _=None):
        #color_palette(palette=None, n_colors=None, desat=None)
        if self.type.value == 'hls':
            self.sns_palette.visible = False
            self.mpl_cmaps.visible = False
            self.variant.visible = False
            self.choose_palette(name=self.type.value,
                                n=self.n_colors.value,
                                desat=self.desat.value,
                                as_cmap=self.as_cmap.value)
        elif self.type.value == 'husl':
            self.sns_palette.visible = False
            self.mpl_cmaps.visible = False
            self.variant.visible = False
            self.choose_palette(name=self.type.value,
                                n=self.n_colors.value,
                                desat=self.desat.value,
                                as_cmap=self.as_cmap.value)
        elif self.type.value == 'seaborn':
            self.sns_palette.visible = True
            self.mpl_cmaps.visible = False
            self.variant.visible = False
            self.choose_palette(name=self.sns_palette.value,
                                n=self.n_colors.value,
                                desat=self.desat.value,
                                as_cmap=self.as_cmap.value)
        elif self.type.value == 'matplotlib':
            self.sns_palette.visible = False
            self.mpl_cmaps.visible = True
            self.variant.visible = True
            self.choose_matplotlib(name=self.mpl_cmaps.value,
                                   n=self.n_colors.value,
                                   desat=self.desat.value,
                                   variant=self.variant.value,
                                   as_cmap=self.as_cmap.value)
        self.update_fig_widget()

    def choose_matplotlib(self, name, n,
                          desat, variant,
                          as_cmap=False):
        is_variant = lambda x: x[-2:] in ['_d', '_r']
        if not is_variant(name):
            if variant == "reverse":
                name += "_r"
            elif variant == "dark":
                name += "_d"

        if as_cmap:
            pal = []
            pal[:] = color_palette(name, 256, desat)
            if variant == "reverse" and is_variant(name):
                self.pal = self.pal[::-1]
                
            self.cmap  = getattr(cm, name)
        else:
            self.pal[:] = color_palette(name, n, desat)
            if variant == "reverse" and is_variant(name):
                self.pal = self.pal[::-1]

    def choose_palette(self, name, n, desat, as_cmap):
        if as_cmap:
            pal = []
            pal[:] = color_palette(name, n, desat)
            self.cmap = ListedColormap(pal,
                                       N=self.n_colors.value)
        else:
            self.pal[:] = color_palette(name, n, desat)


class CubeHelixPalette(SeabornColor):
    """Launch an interactive widget to create a sequential cubehelix palette.
    This corresponds with the :func:`cubehelix_palette` function. This kind
    of palette is widget good for data that range between relatively uninteresting
    low values and interesting high values. The cubehelix system allows the
    palette to have more hue variance across the range, which can be helpful
    for distinguishing a wider range of values.
    Requires IPython 2+ and must be used in the notebook.
    Parameters
    ----------
    as_cmap : bool
        If True, the return value is a matplotlib colormap rather than a
        list of discrete colors.
    Returns
    -------
    pal or cmap : list of colors or matplotlib colormap
        Object that can be passed to plotting functions.
    See Also
    --------
    cubehelix_palette : Create a sequential palette or colormap using the
                        cubehelix system.
    """
    
    def __init__(self,
                 as_cmap=False,
                 reverse=False,
                 n_colors=9,
                 start=0.65,
                 rot=-0.9,
                 gamma=1.,
                 hue=0.8,
                 light=0.85,
                 dark=0.15,
                 title='Cubehelix palette ',
                 name='cubehelix',
                 **kwargs
                ):
        
        control_box = ['r$N=divergint_controls',
                       [
                           ['c$N=row_1_cubehelix',['@(0,3.,0.05,'+str(start)+')$d=start',
                                                   '@(-1.,1.,0.05,'+str(rot)+')$d=rot',
                                                   '@(0.,5.,0.05,'+str(gamma)+')$d=gamma',]]
                           ,
                           ['c$N=row_2_cubehelix',['@(0.,1.,0.05,'+str(hue)+')$d=hue',
                                                   '@(0.,1.,0.05,'+str(light)+')$d=light',
                                                   '@(0.,1.,0.05,'+str(dark)+')$d=dark']]
                       ]
                      ]
                   
        metaparam_box =['c$N=cbw_metaparam_box',
                        [
                         '@True$d=As cmap', '@True$d=reverse',
                         '@(2,32,1,'+str(n_colors)+')$d=n_colors'
                        ]
                       ]
        SeabornColor.__init__(self, control_box, metaparam_box, title, mode='interactive',name=name,**kwargs)
        self.update_fig_widget()
        self.observe(self.update)
        self.observe(self.update_fig_widget)
        self.update()
        self.update_fig_widget()
        
    def update(self, _=None):
        self.choose_cubehelix(n_colors=self.n_colors.value,
                              start=self.start.value,
                              rot=self.rot.value,
                              gamma=self.gamma.value,
                              hue=self.hue.value,
                              light=self.light.value,
                              dark=self.dark.value,
                              reverse=self.reverse.value,
                              as_cmap=self.as_cmap.value)
        if self.as_cmap.value:
            self.n_colors.widget.visible = False
        else:
            self.n_colors.widget.visible = True

    def choose_cubehelix(self, n_colors, start, rot, gamma,
                         hue, light, dark, reverse, as_cmap
                        ):

        if as_cmap:
            colors = cubehelix_palette(256, start, rot, gamma,
                                       hue, light, dark, reverse)
            self._update_lut(self.cmap, np.c_[colors, np.ones(256)])
            cmap_fig = self._cmap_figure(self.cmap)
            self.fig_widget.value = self.fig_to_html(cmap_fig[0])
        else:
            self.pal[:] = self.cubehelix_palette(n_colors, start, rot, gamma,
                                            hue, light, dark, reverse)
            pal_fig = self._palplot_figure(self.pal)
            self.fig_widget.value = self.fig_to_html(pal_fig[0])


class DivergingPalette(SeabornColor):
    
    def __init__(self,
                 as_cmap=False,
                 h_neg=38,
                 h_pos=167,
                 l=66,
                 s=99,
                 sep=39,
                 n=10,
                 center="light",
                 title='Diverging palette',
                 name='diverging',
                 **kwargs
                ):
        
        control_box = ['c$N=divergint_controls',['@(0,359,1,'+str(h_neg)+')$d=h_neg',
                                                 '@(0,359,1,'+str(h_pos)+')$d=h_pos',
                                                 '@(0,99,1,'+str(l)+')$d=l',
                                                 '@(0,99,1,'+str(s)+')$d=s',
                                                 '@(1,50,1,'+str(sep)+')$d=sep'
                                                ]
                      ]
                   
                    
        metaparam_box =['c$N=cbw_metaparam_box',
                        [
                            '@True$d=As cmap', '@rad$d=center&o='+str(["dark", "light"]),
                             '@(2,32,1,'+str(n)+')$d=n_colors'
                        ]
                       ]
        SeabornColor.__init__(self, control_box, metaparam_box, title, mode='interactive', name=name, **kwargs)
        self.update_fig_widget()
        self.observe(self.update)
        self.observe(self.update_fig_widget)
        self.update()
        self.update_fig_widget()
        
    def choose_diverging_palette(self,
                                 h_neg=220,
                                 h_pos=74,
                                 l=50,
                                 sep=10,
                                 n=9,
                                 s=74,
                                 center=["light", "dark"],
                                 as_cmap=False):
        if as_cmap:
            colors = diverging_palette(h_neg, h_pos, s, l, sep, 256, center)
            self._update_lut(self.cmap, colors)
            cmap_fig = self._cmap_figure(self.cmap)
            self.fig_widget.value = self.fig_to_html(cmap_fig[0])
        else:
            self.pal[:] = diverging_palette(h_neg, h_pos, s, l, sep, n, center)
            pal_fig = self._palplot_figure(self.pal)
            self.fig_widget.value = self.fig_to_html(pal_fig[0])

    def update(self, _=None):
        self.choose_diverging_palette(h_neg=self.h_neg.value,
                                      h_pos=self.h_pos.value,
                                      l=self.l.value,
                                      s=self.s.value,
                                      sep=self.sep.value,
                                      n=self.n_colors.value,
                                      center=self.center.value,
                                      as_cmap=self.as_cmap.value)
        if self.as_cmap.value:
            self.n_colors.widget.visible = False
        else:
            self.n_colors.widget.visible = True

    

class SequentialPalette(SeabornColor):
    
    def __init__(self,
                 title='Sequential Palette',
                 input="husl",
                 type='light',
                 n=10,
                 as_cmap=False,
                 r=0.5, g=0.5, b=0.5,
                 h_hls=0.5, s_hls=0.5, l_hls=0.5,
                 h_husl=176, s_husl=50, l_husl=50,
                 name='sequential',
                 **kwargs
                ):
        
        control_box = ['r$N=colorbrewer_palette_controls',
                       [
                        ['c$N=rgb_box',['@(0.,1.,0.05,'+str(r)+')$d=r',
                                        '@(0.,1.,0.05,'+str(g)+')$d=g',
                                        '@(0.,1.,0.05,'+str(b)+')$d=b'
                         
                                           ]],
                        ['c$N=hls_box',['@(0.,1.,0.05,'+str(h_hls)+')$d=h_hls',
                                        '@(0.,1.,0.05,'+str(l_hls)+')$d=l_hls',
                                        '@(0.,1.,0.05,'+str(s_hls)+')$d=s_hls'
                         
                                           ]],
                        ['c$N=husl_box',['@(0,359,1,'+str(h_husl)+')$d=h_husl',
                                        '@(0,99,1,'+str(s_husl)+')$d=s_husl',
                                        '@(0,99,1,'+str(l_husl)+')$d=l_husl'
                         
                                           ]],
                       ]
                      ]
        metaparam_box =['c$N=cbw_metaparam_box',
                        [
                            ['r$N=metbox_row',['@True$d=As cmap', '@rad$d=Type&o='+str(["dark", "light"]),'@togs$d=Input&o='+str(["rgb", "hls", "husl"])]],
                             '@(2,32,1,10)$d=n_colors'
                        ]
                       ]
        SeabornColor.__init__(self, control_box, metaparam_box, 'Sequential palette',mode='interactive', name=name, **kwargs)
        self.update_fig_widget()
        self.observe(self.update)
        self.observe(self.update_fig_widget)
        self.update()
        self.update_fig_widget()
    def update(self, _=None):

        if self.input.value == 'rgb':
            self.choose_palette_rgb(r=self.r.value,
                                    g=self.g.value,
                                    b=self.b.value,
                                    n=self.n_colors.value,
                                    as_cmap=self.as_cmap.value
                                   )
            self.hls_box.visible = False
            self.husl_box.visible = False
            self.rgb_box.visible = True

        elif self.input.value == 'hls':
            self.choose_palette_hls(h=self.h_hls.value,
                                    l=self.l_hls.value,
                                    s=self.s_hls.value,
                                    n=self.n_colors.value,
                                    as_cmap=self.as_cmap.value
                                   )
            self.hls_box.visible = True
            self.husl_box.visible = False
            self.rgb_box.visible = False

        elif self.input.value == 'husl':
            self.choose_palette_husl(h=self.h_husl.value,
                                     l=self.l_husl.value,
                                     s=self.s_husl.value,
                                     n=self.n_colors.value,
                                     as_cmap=self.as_cmap.value
                                    )
            self.hls_box.visible = False
            self.husl_box.visible = True
            self.rgb_box.visible = False
        self.update_fig_widget()

    def choose_palette_rgb(self,
                           r=0.5,
                           g=0.5,
                           b=0.5,
                           n=0.5,
                           as_cmap=False):
        color = r, g, b
        if as_cmap:
            if self.type.value == 'light':
                colors = light_palette(color, 256, input="rgb")
            else:
                colors = dark_palette(color, 256, input="rgb")
            self._update_lut(self.cmap, colors)
        else:
            if self.type.value == 'light':
                self.pal[:] = light_palette(color, n, input="rgb")
            else:
                self.pal[:] = dark_palette(color, n, input="rgb")

    def choose_palette_hls(self,
                           h=0.5,
                           l=0.5,
                           s=0.5,
                           n=10,
                           as_cmap=False):
        color = h, l, s
        if as_cmap:
            if self.type.value == 'light':
                colors = light_palette(color, 256, input="hls")
            else:
                colors = dark_palette(color, 256, input="hls")
            self._update_lut(self.cmap, colors)
        else:
            if self.type.value == 'light':
                self.pal[:] = light_palette(color, n, input="hls")
            else:
                self.pal[:] = dark_palette(color, n, input="hls")

    def choose_palette_husl(self,
                            h=0,
                            s=0,
                            l=0,
                            n=10,
                            as_cmap=False):
        color = h, s, l
        if as_cmap:
            if self.type.value == 'light':
                colors = light_palette(color, 256, input="husl")
            else:
                colors = dark_palette(color, 256, input="husl")
            self._update_lut(self.cmap, colors)
        else:
            if self.type.value == 'light':
                self.pal[:] = light_palette(color, n, input="husl")
            else:
                self.pal[:] = dark_palette(color, n, input="husl")
    

class ColorBrewerPalette(SeabornColor):

    def __init__(self,type='sequential',
                 title='ColorBrewer palette',
                 as_cmap=False,
                 n=10,
                 desat=1.,
                 name='colorbrewer',
                 **kwargs
                ):
        seq_opts = ["Greys", "Reds", "Greens", "Blues", "Oranges", "Purples",
                         "BuGn", "BuPu", "GnBu", "OrRd", "PuBu", "PuRd", "RdPu", "YlGn",
                         "PuBuGn", "YlGnBu", "YlOrBr", "YlOrRd"]
        div_opts = ["RdBu", "RdGy", "PRGn", "PiYG", "BrBG",
                         "RdYlBu", "RdYlGn", "Spectral"]
        qua_opts = ["Set1", "Set2", "Set3", "Paired", "Accent",
                         "Pastel1", "Pastel2", "Dark2"]
        self.seq_var = ["regular", "reverse", "dark"]
        self.div_var = ["regular", "reverse"]
        options = ['sequential', 'diverging', 'qualitative']
        control_box = ['c$N=colorbrewer_palette',
                       [
                        ['r$N=varopts_row',['@rad$N=variant&o='+str(self.seq_var),
                                            '@select$N=seq_opts&o='+str(seq_opts),
                                            '@select$N=div_opts&o='+str(div_opts),
                                            '@select$N=qua_opts&o='+str(qua_opts)
                                           ]],
                        ['r$N=desat_row',['@(0, 1, 0.05, 1.00)$d=Desat']]#'@fs$d=desat&min=0&max=1&val=1&step=0.05']]

                       ]
                      ]
        metaparam_box =['c$N=cbw_metaparam_box',
                        ['@True$d=As cmap',
                         '@rad$d=Type&o='+str(options),
                         '@int_slider$d=n_colors&min=2&max=32&val=10&step=1'
                        ]
                       ]
        SeabornColor.__init__(self, control_box, metaparam_box, title,
                              mode='interactive', name=name, **kwargs)
        
        self.observe(self.update)
        self.observe(self.update_fig_widget)
        self.update()  
        self.update_fig_widget()
        

    def update(self, _=None):
        if self.type.value == 'sequential':
            self.seq_opts.visible = True
            self.div_opts.visible = False
            self.qua_opts.visible = False
            self.variant.visible = True

            self.choose_sequential(name=self.seq_opts.value,
                                   n=self.n_colors.value,
                                   desat=self.desat.value,
                                   variant=self.variant.value,
                                   as_cmap=self.as_cmap.value)
        elif self.type.value == 'diverging':
            self.seq_opts.visible = False
            self.div_opts.visible = True
            self.qua_opts.visible = False
            self.variant.target.options = self.div_var
            self.variant.visible = True
         
            self.choose_sequential(name=self.div_opts.value,
                                   n=self.n_colors.value,
                                   desat=self.desat.value,
                                   variant=self.variant.value,
                                   as_cmap=self.as_cmap.value)
        elif self.type.value == 'qualitative':
            self.seq_opts.visible = False
            self.div_opts.visible = False
            self.qua_opts.visible = True
            self.variant.visible = False

            self.choose_qualitative(name=self.qua_opts.value,
                                    n=self.n_colors.value,
                                    desat=self.desat.value,
                                    as_cmap=self.as_cmap.value
                                   )
        

    def choose_sequential(self, name, n,
                          desat, variant,
                          as_cmap=False):
        if variant == "reverse":
            name += "_r"
        elif variant == "dark":
            name += "_d"

        if as_cmap:
            colors = color_palette(name, 256, desat)
            self.cmap = self._init_mutable_colormap()
            self._update_lut(self.cmap, np.c_[colors, np.ones(256)])
        else:
            self.pal[:] = color_palette(name, n, desat)

    def choose_diverging(self, name, n,
                         desat, variant,
                         as_cmap=False):
        if variant == "reverse":
            name += "_r"
        if as_cmap:
            colors = color_palette(name, 256, desat)
            self.cmap = self._init_mutable_colormap()
            self._update_lut(self.cmap, np.c_[colors, np.ones(256)])
        else:
            self.pal[:] = color_palette(name, n, desat)

    def choose_qualitative(self, name, n, desat, as_cmap):
        if as_cmap:
            pal = []
            pal[:] = color_palette(name, n, desat)
            self.cmap = ListedColormap(pal,
                                       N=self.n_colors.value)
        else:
            self.pal[:] = color_palette(name, n, desat)
