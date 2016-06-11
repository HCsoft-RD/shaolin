# -*- coding: utf-8 -*-
"""
Created on Thu May 19 12:02:20 2016

@author: Guillem Duran Ballester
"""
import six
import pickle
from .stateless_dashboard import StatelessDashboard
from .css import LayoutHacker

class Dashboard(StatelessDashboard):
    """Clash for managing arbitrary Dashboards"""
    def __init__(self,dash, state=None, **kwargs):
        StatelessDashboard.__init__(self, dash, **kwargs)
        self._state = self._load_state(state)
    
    
    def _load_state(self, state):
        if isinstance(state, six.string_types):
            try:
                with open(state, "rb") as input_file:
                    state = pickle.load(input_file)
            except:
                return None
        if not state is None:
            self.apply_state(state)
        return state
        
    @property
    def state(self):
        return self._state
    @state.setter
    def state(self, val):
        self._state = val
        self.apply_state()
    def _update_state(self, _=None):
        self._state = self._state_manager.output

    @property
    def state_manager(self):
        self._state_manager = LayoutHacker(self)
        self._state_manager.observe(self._update_state)
        self._update_state()
        return self._state_manager.widget
    
    def apply_state(self, state_dict=None):
        "loads a generated state dict and applies it to the dashboard"
        if state_dict is None:
            state_dict = self._state
        if state_dict is None:
            self.state_manager()
        for attr in self.mode_dict['all']:
            for css_tra, items_dict in state_dict[attr]['css_traits'].items():
                for widget,val in items_dict.items():
                    layout = getattr(getattr(self, attr), widget).layout
                    if val != '':
                        setattr(layout,css_tra,val)
            for tget_attr, val in state_dict[attr]['widget_attrs'].items():
                tget_wid = getattr(self, attr).target
                if val != '':
                    setattr(tget_wid, tget_attr, val)

class ToggleMenu(Dashboard):
    def __init__(self,
                 children,
                 description='',
                 buttons_shao=None,
                 name=None,
                 button_labels=None,
                 button_type='togs',
                 button_pos='bottom',
                 **kwargs):
        self.child_names = self.get_children_names(children)
        if button_labels is None:
            self.button_labels = self.child_names
        else:
            self.button_labels = button_labels
        
        if buttons_shao is None:
            opts = dict(zip(self.button_labels,self.child_names))
            buttons_shao  = ['@'+button_type+'$N=buttons&d='+str(description)+'&o='+str(opts)]
            
        self.children_dash = children
        #children = ['fs$d=fs','fs$d=fs2']
        #buttons = ['r$n=buttons', buttons_shao]
        if button_pos == 'bottom':
            dash = ['V$n=toggleMenu',
                    children+buttons_shao
                   ]
        elif button_pos == 'top':
            dash = ['V$n=toggleMenu',
                    buttons_shao+children
                   ]
        elif button_pos == 'right':
            dash = ['r$n=toggleMenu',
                    children+buttons_shao
                   ]
        elif button_pos == 'left':
            dash = ['r$n=toggleMenu',
                    buttons_shao+children
                   ]
        Dashboard.__init__(self, dash, func=None, name=name, **kwargs)
        self.update_toggle()
        self.buttons.target.observe(self.update_toggle)
    
    def get_children_names(self,children):
        names = []
        for c in children:
            try:
                names += [self.name_from_shaoscript(c)]
            except:
                names += [c.name]
            
        return names
    
    def update_toggle(self,_=None):

        for name in self.child_names:
            child = getattr(self,name)
            if name == self.buttons.value:
                child.visible = True
            else:
                child.visible = False