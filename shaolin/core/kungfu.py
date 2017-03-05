# -*- coding: utf-8 -*-
import string
import random

import six
import numpy as np
import ipywidgets as wid
from shaolin.core.shaoscript import shaoscript
from shaolin.core.dashboard import Dashboard
from shaolin.core.widgets import Title, SubTitle, SubSubTitle
from shaolin.dashboards.colormap import ColormapPicker


class KungFu(Dashboard):
    def __init__(self,
                 name='dash',
                 box='5c',
                 interact=None,
                 mode=None,
                 func=None,
                 dash=None,
                 group_n=3,
                 **kwargs):
        self._group_n = group_n
        self.__dic_mode = mode
        self.__interact = interact
        if self.__interact and mode is None:
            self.__dic_mode = 'interactive'
        children = self.get_children_widgets(kwargs)
        self.name = name
        dash = dash or self.process_children_layout(box,children)#dash or [box+'$n='+name,children]
        #print(dash)
        Dashboard.__init__(self,dash,name=name,mode=mode)
        self._func = func
        self.observe(self.fun)
    
    #shorthands for widget and value
    @staticmethod
    def is_text_widget(w):
        shao_titles = Title, SubTitle, SubSubTitle
        return isinstance(w,shao_titles) or isinstance(w[0],wid.Label)
    @staticmethod
    def compare_widgets(a,b):
        pass
    
    @staticmethod
    def _get_first_child(children):
        title = []
        buttons = []
        subtitle = []
        subsubtitle = []
        progress = []
        for c in children:
            if isinstance(c,Title):
                title.append(c)
            elif isinstance(c,SubTitle):
                subtitle.append(c)
            elif isinstance(c,SubSubTitle):
                subsubtitle.append(c)
            elif isinstance(c.widget,(wid.FloatProgress,wid.IntProgress)):
                progress.append(c)
            elif isinstance(c.widget,wid.Button):
                buttons.append(c)
        first = title + subtitle +subsubtitle + progress +buttons
        #print(first)
        return first
    
    @staticmethod
    def _get_sliders_child(children):
        slid = []
        slid_types = (wid.FloatSlider,wid.IntSlider,wid.IntText,wid.FloatText)
        for c in children:
            if isinstance(c.widget,slid_types):
                slid.append(c)
        return slid
    @staticmethod
    def _get_colors_child(children):
        
        colors = []
        
        for c in children:
            if isinstance(c.widget,wid.ColorPicker) or isinstance(c,ColormapPicker):
                colors.append(c)
        return colors
    
    @staticmethod
    def _get_text_child(children):
        text = []
        text_types = (wid.Text,wid.Textarea)
        for c in children:
            if isinstance(c.widget,text_types):
                text.append(c)
        return text
    
    @staticmethod
    def _get_selection_child(children):
        select = []
        select_types = (wid.Select,wid.SelectionSlider,
                        wid.Dropdown,wid.ToggleButtons,
                        wid.SelectMultiple,wid.RadioButtons)
        for c in children:
            if isinstance(c.widget,select_types):
                select.append(c)
        return select
    
    @staticmethod
    def _get_bool_child(children):
        bools = []
        bool_types = (wid.Checkbox,wid.ToggleButton,wid.Valid)
        for c in children:
            if isinstance(c.widget,bool_types):
                bools.append(c)
        return bools
    
    @staticmethod
    def _get_range_child(children):
        ranges = []
        range_types = (wid.FloatRangeSlider,wid.IntRangeSlider)
        for c in children:
            if isinstance(c.widget,range_types):
                ranges.append(c)
        return ranges
    
    def create_boxes(self,children,is_col=True,num=5,name=None,child_names=None):
        def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))
        
        
        name = name or id_generator()
        child_names = child_names or [id_generator() for _ in range(len(children))]
        if isinstance(is_col,bool):
            b = 'c$n='+name if is_col else 'r$n='+name
            if len(children)<=num:
                return [b,children]
    
        pases = int(np.floor(len(children)/num))
        j = 0
        sub_children = []
        for p in range(pases):
            sub = []
            for j in range(p*num,p*num+num):
                sub.append(children[j])
            sub_b = 'c$n='+id_generator() if not is_col else 'r$n='+id_generator()
            sub_children.append([sub_b,sub])
        last_sub = []
        for i in range(j+1,len(children)):
            last_sub.append(children[i])
        sub_b = 'c$n='+id_generator() if not is_col else 'r$n='+id_generator()
        sub_children.append([sub_b,last_sub])
        if isinstance(is_col,str):
            b = is_col+'$n='+name+'&t='+str(tuple(child_names)).replace('(',\
                                       '').replace(')','').replace("'",'').replace('"','')
            return [b,children]
        return [b,sub_children]
        
    def group_children(self,children,is_col,num=5):
        #title and buttons
        #is_col = not is_col
        first_child = self._get_first_child(children)
        first_child_b = self.create_boxes(first_child,is_col,num,name='main') if len(first_child)>=1 else []
        #print("first child:",first_child)
        #Sliders int and floar
        sliders = self._get_sliders_child(children)
        sliders_b = self.create_boxes(sliders,is_col,num,name='numeric') if len(sliders)>=1 else []
        #print("sliders:",sliders)
        #text widget
        text = self._get_text_child(children)
        text_b = self.create_boxes(text,is_col,num,name='text') if len(text)>=1 else []
        #print("text:",text)
        #selection widgets
        select = self._get_selection_child(children)
        select_b = self.create_boxes(select,is_col,num,name='selection') if len(select)>=1 else []
        #print("select:",select)
        #boolean widgets
        bools = self._get_bool_child(children)
        bools_b = self.create_boxes(bools,is_col,num,name='booleans') if len(bools)>=1 else []
        #color widgets
        colors = self._get_colors_child(children)
        colors_b = self.create_boxes(colors,is_col,num,name='colors') if len(colors)>=1 else []
        #other widgets 
        others = []
        for c in children:
            if c not in first_child\
                 and c not in sliders and c not in text\
                 and c not in select and c not in bools and c not in colors:
                    others.append(c)
        others_b = self.create_boxes(others,is_col,num,name='others') if len(others)>=1 else []
        #print("bools:",bools)
        new_children = []
        child_names = []
        if first_child != []:
            new_children.append(first_child_b)
            child_names.append(self.name)
        if sliders != []:
            new_children.append(sliders_b)
            child_names.append('Numeric')
        if select != []:
            new_children.append(select_b)
            child_names.append('Options')
        if bools != []:
            new_children.append(bools_b)
            child_names.append('Boolean')
        if text != []:
            new_children.append(text_b)
            child_names.append('String')
        if colors != []:
            new_children.append(colors_b)
            child_names.append('Colors')
        if others != []:
            new_children.append(others_b)
            child_names.append('Other')
        return new_children,child_names
        
    def process_children_layout(self,box='5c',children=None):
        def filter_box_type(box):
            col_words = [ 'column','cols', 'col','c', 'vbox', 'v']
            row_words = ['rows', 'row','r', 'HBox', 'box', 'h']
            tabs_or_accord = ['accordion','accord','ac','a'] +['tabs','tab','t']
                             
            if '|' in box:
                box = box.replace('|','')
                group_ch = True
            else:
                group_ch = False
            is_col = True
            for w in row_words:
                if w in box.lower():
                    box = box.lower().replace(w,'')
                    is_col = False
            for w in col_words:
                if w in box.lower():
                    box = box.lower().replace(w,'')
            
            for w in tabs_or_accord:
                if w in box.lower():
                    box = box.lower().replace(w,'')
                    
                    is_col = w
            if box !='':
                num = int(box)
            else:
                num=5
            return is_col,num,group_ch
                
        assert(isinstance(children,list))
        #group the childfren
        is_col,num,group_ch = filter_box_type(box)
        if group_ch:
            rev = not is_col
            children, child_names = self.group_children(children,rev,num=num)
            #children like [form fi,sli,sel,bools,text]
            if isinstance(is_col,str):
            #two rows/cols with all the blockslen     (child_names)
                return self.create_boxes(children,is_col,num=2,child_names=child_names)
            else:
                return self.create_boxes(children,is_col,num=num,child_names=child_names)
        return self.create_boxes(children,is_col,num)
            
    def fun(self,_=None):
        if not self._func is None and not self.__interact is None :
            return self._func(**self.kwargs)
    
    def kwargs_from_key(self,key):
        kws = {}
        if not self.__dic_mode is None and not 'mode' in kws.keys():
            kws['mode'] = self.__dic_mode  
        if key.startswith('@'):
            k = key[1:]
            kws['mode'] = 'interactive'
        elif key.startswith('I_'):
            k = key[2:]
            kws['mode'] = 'interactive'
        elif key.startswith('/'):
            k = key[1:]
            kws['mode'] = 'passive'
        elif key.startswith('P_'):
            k = key[2:]
            kws['mode'] = 'passive'
        else:
            k = key
        kws['name']=k
        kws['description']=k.capitalize().replace('_',' ')
        
        return kws
    
    def get_children_widgets(self,kwargs):
        def is_shaoscript(x):
            return "$" in x if isinstance(x,six.string_types) else False
        children = []
        for k, v in kwargs.items(): 
            kws = self.kwargs_from_key(k)
            if is_shaoscript(v):
                children.append(shaoscript(v,kws))
            else:
                if isinstance(v,str):
                    children.append(shaoscript('text$v='+v,kws))
                else:
                    children.append(shaoscript(v,kws))
        return children
    
    @staticmethod
    def dict_to_children(self,kwargs):
        def is_shaoscript(x):
            return "$" in x if isinstance(x,six.string_types) else False
        children = []
        for k, v in kwargs.items(): 
            if is_shaoscript(v):
                children.append(shaoscript(v))
            else:
                kws = dict(name=k,description=k.capitalize().replace('_',' '))
                if not self.__dic_mode is None:
                    kws['mode'] = self.__dic_mode
                if isinstance(v,str):
                    children.append(shaoscript('text$v='+v,kws))
                else:
                    children.append(shaoscript(v,kws))
        return children