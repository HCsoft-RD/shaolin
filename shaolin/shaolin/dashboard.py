# -*- coding: utf-8 -*-
"""
Created on Thu May 19 12:02:20 2016

@author: Guillem Duran Ballester
"""
import traitlets

#from .context import shaoscript
#from .context import ToggleMenu
from .shaoscript import shaoscript
class Dashboard(object):
    """Clash for managing arbitrary Dashboards"""
    def __init__(self, dash, func=None, mode='active', name=None):
        self.func = func
        self.dash = dash
        self.mode = mode
        if not name is None:
            self.name = name
        elif hasattr(dash, 'name'):
            self.name = dash.name
        else:
            self.name = self.name_from_shaoscript(dash[0])
        self.mode_dict = {'active' : [],
                          'passive': [],
                          'interactive' : [],
                          'all':[]
                         }
        self.init_dash(self.dash)
        self.link_children(self.dash)
        if not self.func is None:
            self.observe(self.interact)

    def init_dashboard(self, dashboard):
        """Integrates a child Dashboard as an attribute of the current Dashboard"""
        setattr(self, dashboard.name, dashboard)
        if dashboard.mode == 'interactive':
            self.mode_dict['interactive'] += [dashboard.name]
        elif dashboard.mode == 'passive':
            self.mode_dict['passive'] += [dashboard.name]
        else:
            self.mode_dict['active'] += [dashboard.name]

    def init_toggle_menu(self, children, kwargs):
        """Integrates a child ToggleMenu as an attribute of the current Dashboard"""
        dashboard = ToggleMenu(children)
        if 'name' in kwargs.keys():
            dashboard.name = kwargs['name']
        setattr(self, dashboard.name, dashboard)
        if dashboard.mode == 'interactive':
            self.mode_dict['interactive'] += [dashboard.name]
        elif dashboard.mode == 'passive':
            self.mode_dict['passive'] += [dashboard.name]
        else:
            self.mode_dict['active'] += [dashboard.name]

    def init_widget(self, shao, kwargs):
        """Integrates a child Widget as an attribute of the current Dashboard"""
        widget = shaoscript(shao, kwargs)
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
        self.func(**self.kwargs)

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
        return getattr(self, self.name).widget

    @staticmethod
    def name_from_shaoscript(string):
        """Get a name from a shaoscript string"""
        params = string.split('$')[1].split('&')
        desc = None
        name = None
        for p in params:
            pname = p.split('=')[0]
            if pname in ['d', 'desc', 'description']:
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

        if shaolist[0] is ToggleMenu:
            shaoscrpt = ToggleMenu
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
                if shaolist[0][0] is ToggleMenu:
                    shaoscrpt = ToggleMenu
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

    def link_children(self, shaolist):
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
                self.link_children(child)

    def init_dash(self, dash):
        """Creates all the children Widgets and dashboards the current Dashboard will have"""
        shaoscrpt, kwargs, children = self.read_shaolist(dash)
        if shaoscrpt is None:
            self.init_dashboard(dash)
        elif shaoscrpt is ToggleMenu:
            self.init_toggle_menu(children, kwargs)
        else:
            self.init_widget(shaoscrpt, kwargs)
        if children is None:
            return
        for child in children:
            self.init_dash(child)

class ToggleMenu(Dashboard):
    """Dashboard in charge of managing the display of non overlaping interfaces"""
    def __init__(self, children,
                 description='',
                 buttons_shao=None,
                 name=None,
                 button_labels=None):
        self.child_names = self.get_children_names(children)
        if button_labels is None:
            self.button_labels = self.child_names
        else:
            self.button_labels = button_labels

        if buttons_shao is None:
            opts = dict(zip(self.button_labels, self.child_names))
            buttons_shao = ['@togs$N=buttons&d='+str(description)+'&o='+str(opts)]

        self.children_dash = children
        #children = ['fs$d=fs','fs$d=fs2']
        #buttons = ['r$n=buttons', buttons_shao]
        dash = ['V$n=toggleMenu',
                children +buttons_shao
               ]
        Dashboard.__init__(self, dash, func=None, name=name)
        self.update_toggle()
        self.buttons.target.observe(self.update_toggle)

    def get_children_names(self, children):
        """Return the names fo all the children of the ToggleMenu"""
        names = []
        for child in children:
            #If child is a Dashboart it will trigger multiple exceptions,
            #works better than isinstance. Isinstance was buggy i dont know why
            try:
                names += [self.name_from_shaoscript(child)]
            except:
                names += [child.name]
        return names

    def update_toggle(self, _=None):
        """updates toggle visibility"""
        for name in self.child_names:
            child = getattr(self, name)
            if name == self.buttons.value:
                child.visible = True
            else:
                child.visible = False
