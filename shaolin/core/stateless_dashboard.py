# -*- coding: utf-8 -*-
"""
Created on Wed May 25 15:26:23 2016

@author: sergio
"""
import traitlets
import shaolin.core as sc
from shaolin.core import shaoscript as scpt
class StatelessDashboard(object):
    """Clash for managing arbitrary Dashboards"""
    def __init__(self, dashboard, func=None, mode='active', name=None):
        
        self.func = func
        self.dashboard = dashboard
        self.mode = mode
        if not name is None:
            self.name = name
        elif hasattr(dashboard, 'name'):
            self.name = dashboard.name
        else:
            self.name = self.name_from_shaoscript(dashboard[0])
        self.mode_dict = {'active' : [],
                          'passive': [],
                          'interactive' : [],
                          'all':[]
                         }
        self._init_dash(self.dashboard)
        self._link_children(self.dashboard)
        if not self.func is None:
            self.observe(self.interact)
        #self.output = self.kwargs

    def _init_dashboard(self, dashboard):
        """Integrates a child Dashboard as an attribute of the current Dashboard"""
        setattr(self, dashboard.name, dashboard)
        if dashboard.mode == 'interactive':
            self.mode_dict['interactive'] += [dashboard.name]
        elif dashboard.mode == 'passive':
            self.mode_dict['passive'] += [dashboard.name]
        else:
            self.mode_dict['active'] += [dashboard.name]

    def _init_toggle_menu(self, children, kwargs):
        """Integrates a child ToggleMenu as an attribute of the current Dashboard"""
        dashboard = sc.dashboard.ToggleMenu(children)
        if 'name' in kwargs.keys():
            dashboard.name = kwargs['name']
        setattr(self, dashboard.name, dashboard)
        if dashboard.mode == 'interactive':
            self.mode_dict['interactive'] += [dashboard.name]
        elif dashboard.mode == 'passive':
            self.mode_dict['passive'] += [dashboard.name]
        else:
            self.mode_dict['active'] += [dashboard.name]

    def _init_widget(self, shao, kwargs):
        """Integrates a child Widget as an attribute of the current Dashboard"""
        widget = scpt.shaoscript(shao, kwargs)
        try:
            setattr(self, widget.name, widget)
        except Exception as e:
            e.args += (('Dont use widget attributes as shaoscript names,'
                        'they are reserved words! (You can use dashboard'
                        'as a generic name if you want)'),)
            raise e

        if 'mode' in kwargs.keys():
            if kwargs['mode'] == 'interactive':
                self.mode_dict['interactive'] += [widget.name]
            elif kwargs['mode'] == 'passive':
                self.mode_dict['passive'] += [widget.name]
            else:
                self.mode_dict['active'] += [widget.name]
        else:
            self.mode_dict['active'] += [widget.name]
        self.mode_dict['all'] += [widget.name]

    def interact(self, _):
        """Apply the dashboard kwargs to the dashboard function"""
        self.func(self.output)

    def link(self, name_1, name_2):
        """Same as trailets but applied to Dashboard attribute names"""
        widget_1 = getattr(self, name_1).target
        widget_2 = getattr(self, name_2).target
        setattr(self, 'link_'+name_1+'_'+name_2, traitlets.link((widget_1, 'value'),
                                                                (widget_2, 'value')))

    def dlink(self, name_1, name_2):
        """Same as trailets but applied to Dashboard attribute names"""
        widget_1 = getattr(self, name_1).target
        widget_2 = getattr(self, name_2).target
        setattr(self, 'link_'+name_1+'_'+name_2, traitlets.dlink((widget_1, 'value'),
                                                                 (widget_2, 'value')))

    def unlink(self, name_1, name_2):
        """Same as trailets but applied to Dashboard attribute names"""
        link = getattr(self, 'link_'+name_1+'_'+name_2)
        link.unlink()

    @property
    def visible(self):
        """Easy visibility management"""
        visible = False
        for name in self.mode_dict['all']:
            visible = visible or getattr(self, name).visible
        return visible
    @visible.setter
    def visible(self, val):
        """Easy visibility management"""
        for name in self.mode_dict['all']:
            getattr(self, name).visible = val

    @property
    def value(self):
        """alias for better modularity"""
        return self.kwargs

    @property
    def kwargs(self):
        """Children values as a kwargs dict for easier interactivity"""
        kwargs = {}
        for name in self.mode_dict['active']:
            kwargs[name] = getattr(self, name).value
        for name in self.mode_dict['interactive']:
            kwargs[name] = getattr(self, name).value
        return kwargs
    @property
    def interactive_kwargs(self):
        """Interactive children values as a kwargs dict for easier interactivity"""
        kw = {}
        for name in self.mode_dict['interactive']:
            kw[name] = getattr(self, name).value
        return kw
    @property
    def widget(self):
        """Alias for easy access to the Dashboard main widget"""
        return getattr(self, self.name_from_shaoscript(self.dashboard[0])).widget

    @staticmethod
    def name_from_shaoscript(string):
        """Get a name from a shaoscript string"""
        params = string.split('$')[1].split('&')
        desc = None
        name = None
        for p in params:
            pname = p.split('=')[0]
            if pname in ['d', 'desc', 'description', 'D']:
                desc = p.split('=')[1]
            elif pname in ['n', 'name', 'N']:
                name = p.split('=')[1]
        if name is None and desc is None:
            return False
        elif name is None:
            return desc.lower().replace(' ', '_')
        else:
            return name.lower().replace(' ', '_')

    @staticmethod
    def read_shaolist(shaolist):
        """Convert a shaolist block to a corresponding shaoscrpt, kwargs,
        children mapping"""
        try:
            len(shaolist)
        except TypeError:
            shaoscrpt = None
            kwargs = {}
            children = None
            return shaoscrpt, kwargs, children

        if shaolist[0] is sc.dashboard.ToggleMenu:
            shaoscrpt = sc.dashboard.ToggleMenu
            kwargs = {}
            children = shaolist[1]
        elif isinstance(shaolist, str):
            shaoscrpt = shaolist
            kwargs = {}
            children = None
        elif len(shaolist) == 1:
            #[(shaoscript,kwargs)]
            if isinstance(shaolist[0], tuple):
                kwargs = shaolist[0][1]
                shaoscrpt = shaolist[0][0]
                children = None
            #[shaoscript]
            else:
                shaoscrpt = shaolist[0]
                kwargs = {}
                children = None
        elif len(shaolist) == 2:
            #[(shaoscript, kwargs), children]
            if isinstance(shaolist[0], tuple):
                if shaolist[0][0] is sc.dashboard.ToggleMenu:
                    shaoscrpt = sc.dashboard.ToggleMenu
                    kwargs = shaolist[0][1]
                    children = shaolist[1]
                    return shaoscrpt, kwargs, children
                else:
                    kwargs = shaolist[0][1]
                    shaoscrpt = shaolist[0][0]
                    children = shaolist[1]
            #[shaoscript,children]
            else:
                kwargs = {}
                shaoscrpt = shaolist[0]
                children = shaolist[1]
        else:
            pass
        return shaoscrpt, kwargs, children

    def observe(self, func, names='value'):
        """Same as ipywidgets. Applies to all interactive children widgets"""
        for name in self.mode_dict['interactive']:
            getattr(self, name).observe(func, names=names)

    def _link_children(self, shaolist):
        """Creates the dashboard structure linking each children with its parent"""
        shaoscrpt, kwargs, children = self.read_shaolist(shaolist)
        if children is None:
            return
        else:
            name = self.name_from_shaoscript(shaoscrpt)
            for child in children:
                shao_c, kwargs_c, c_children = self.read_shaolist(child)
                if shao_c is None:
                    cname = child.name
                else:
                    cname = self.name_from_shaoscript(shao_c)
                getattr(self, name).target.children += (getattr(self, cname).widget,)
                self._link_children(child)

    def _init_dash(self, value):
        """Creates all the children Widgets and dashboards the current Dashboard will have"""
        shaoscrpt, kwargs, children = self.read_shaolist(value)
        if shaoscrpt is None:
            self._init_dashboard(value)
        elif shaoscrpt is sc.dashboard.ToggleMenu:
            self._init_toggle_menu(children, kwargs)
        else:
            self._init_widget(shaoscrpt, kwargs)
        if children is None:
            return
        for child in children:
            self._init_dash(child)

