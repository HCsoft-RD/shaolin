# -*- coding: utf-8 -*-
"""
Created on Thu May 19 12:03:50 2016

@author: sergio
"""

import ast
import six
import ipywidgets as wid
from .object_notation import object_notation
from .context import Widget, Title, SubTitle, SubSubTitle

def shaoscript(word, kwargs=None):
    """Return a shaolin widget from a ShaoScript value"""
    if kwargs is None:
        kwargs = {}

    if isinstance(word, six.string_types):
        word, kwargs = handle_shaoscript_syntax(word, kwargs)
    #word and kwargs from shaoscript syntax
    #If its a shao reserved word for the layout
    if isinstance(word, six.string_types):
        return string_to_wiget(word, kwargs)
    #If word is already a ipywidget class
    elif isinstance(word, tuple(wid.Widget.widget_types.values())):
        return  Widget(word, **kwargs)
    try:
        return object_notation(word, kwargs)
    except:
        raise ValueError('Bad shaoscript syntax.')

def handle_shaoscript_syntax(string, kwargs):
    main_key = string[0]

    #simplified mode for just setting interactivity
    if main_key == '@':
        kwargs['mode'] = 'interactive'
        sliced = string[1:]
    elif main_key == '/':
        kwargs['mode'] = 'active'
        sliced = string[1:]
    else:
        sliced = string
    word = sliced
    #separating widget descriptor from atributes
    split = word.split('$')
    if len(split) == 2:
        if splited_is_ON(split[0]):
            word = ast.literal_eval(split[0])
        else:
            word = split[0]
        params = split[1]
        kwargs = shaoscript_to_kwargs(params, kwargs)
    elif len(split) == 1:
        if splited_is_ON(split[0]):
            word = ast.literal_eval(split[0])
        else:
            word = split[0]
    return word, kwargs

def splited_is_ON(string):
    try:
        onw = ast.literal_eval(string)
        _ = object_notation(onw, {})
        return True
    except:
        return False

def manage_shao_defaults(kwargs):
    if 'description' in kwargs.keys()\
        and 'name' not in kwargs.keys():
        kwargs['name'] = kwargs['description'].lower().replace(' ', '_')

    if 'name' in kwargs.keys()\
        and not 'id' in kwargs.keys():
        kwargs['id'] = kwargs['name'].lower().replace('_', '-')
    return kwargs

def shaoscript_to_kwargs(string, kwargs):
    params = string.split('&')
    for par in params:
        key, val = decode_param(par)
        kwargs[key] = val
    kwargs = manage_shao_defaults(kwargs)
    return kwargs

def decode_param(string):
    """params = {'d':'description',
               'id': 'id',
               'c' : 'class_',
              'val':'value',
               'v':'visible',
               'ori' : 'orientation',
               'o':'options',
               'n' : 'name',
               'm':'mode';
              }"""
    key, val = string.split('=')
    if key in  ['o', 'opt', 'options']:
        name = 'options'
        val = ast.literal_eval(val)
    elif key in  ['d', 'description', 'D']:
        name = 'description'
        val = str(val)
    elif key == 'id':
        name = 'id'
        val = str(val)
    elif key in ['class_', 'c']:
        name = 'class_'
        val = str(val)
    elif key in ['v', 'visible', 'vis']:
        name = 'visible'
        if val in ['0', 'False']:
            val = False
        else:
            val = True
    elif key in ['ori', 'orientation']:
        name = 'orientation'
        if str(val) in ['v', 'vertical']:
            val = 'vertical'
        if str(val) in ['h', 'horizontal']:
            val = 'horizontal'
    elif key in ['n', 'name', 'N']:
        name = 'name'
        val = val
    elif key in ['val', 'value']:
        name = 'value'
        #val = ast.literal_eval(val)
        val = val
    elif key in ['mode', 'm']:
        name = 'mode'
        val = str(val)
    else:
        name = key
    return name, val

def string_to_wiget(word, kwargs):
    assert isinstance(word, six.string_types)
    #Layout
    #---------------------------------
    if word in ['c', 'col', 'column', 'VBox', 'V']:
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        return Widget(wid.VBox, **kwargs)
    elif word in ['r', 'row', 'HBox', 'R', 'Box', 'H']:
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        return Widget(wid.HBox, **kwargs)
    #Markdown
    #--------------------------------
    elif word in ['subsubtitle', 'h3', '###', 'subsub', 'ss']:
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        return SubSubTitle(**kwargs)

    elif word[:3] == '###':
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        if not 'name' in kwargs.keys():
            kwargs['name'] = word[3:].lower().replace(' ', '_')
        if not 'id' in kwargs.keys():
            kwargs['id'] = kwargs['name'].lower().replace('_', '-')
        return SubSubTitle(value=word[3:], **kwargs)

    elif word in ['subtitle', 'h2', '##', 'sub', 's']:
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        return SubTitle(**kwargs)

    elif word[:2] == '##':
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        if not 'name' in kwargs.keys():
            kwargs['name'] = word[2:].lower().replace(' ', '_')
        if not 'id' in kwargs.keys():
            kwargs['id'] = kwargs['name'].lower().replace('_', '-')
        return SubTitle(value=word[2:], **kwargs)

    elif word in ['title', 'h1', '#', 't']:
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        return Title(**kwargs)

    elif word[:1] == '#':
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        if not 'name' in kwargs.keys():
            kwargs['name'] = word[1:].lower().replace(' ', '_')
        if not 'id' in kwargs.keys():
            kwargs['id'] = kwargs['name'].lower().replace('_', '-')
        return Title(value=word[1:], **kwargs)

    #Int and float
    #--------------------------------
    elif word in ['float_slider', 'floatslider', 'fsld', 'fs']:
        return Widget(wid.FloatSlider, **kwargs)
    elif word in ['float_text', 'floattext', 'ftxt', 'ft']:
        return Widget(wid.FloatText, **kwargs)
    elif word in ['int_slider', 'intslider', 'isld', 'is']:
        return Widget(wid.IntSlider, **kwargs)
    elif word in ['int_text', 'inttext', 'itxt', 'it']:
        return Widget(wid.IntText, **kwargs)
    #Range
    #--------------------------------
    elif word in ['float_range', 'floatprogress', 'fprog', 'fp']:
        return Widget(wid.FloatRangeSlider, **kwargs)
    elif word in ['int_range', 'intrange', 'irng', 'ir']:
        return Widget(wid.IntRangeSlider, **kwargs)
    #Progress
    #--------------------------------
    elif word in ['float_progress', 'floatprogress', 'fprog', 'fp']:
        return Widget(wid.FloatProgress, **kwargs)
    elif word in ['int_progress', 'intprogress', 'iprog', 'ip']:
        return Widget(wid.IntProgress, **kwargs)
    #Button
    #--------------------------------
    elif word in ['button', 'btn', 'b']:
        return Widget(wid.Button, **kwargs)
    #string and color
    #---------------
    elif word in ['text', 'txt','str','string']:
        return Widget(wid.Text, **kwargs)
    elif word in ['color', 'colorpicker','cp','cpicker']:
        return Widget(wid.ColorPicker, **kwargs)
        
    #Options for pseudo tabs creation
    #--------------------------------
    #"""
    #elif word in ['radio_display_selection','r_ds','radio_ds']:
    #    return RadioDisplaySelection(**kwargs)
    #elif word in ['toggle_display_selection','t_ds','toggle_ds']:
    #    return ToggleDisplaySelection(**kwargs)
    #elif word in ['display_selection','ds','dsel']:
    #    return DisplaySelection(**kwargs)
    #TODO Include tab options
    #"""
    #Selectors
    #--------------------------
    elif word in ['select_multiple', 'selmul', 'sm']:
        return Widget(wid.SelectMultiple, **kwargs)
    elif word in ['select', 'sel']:
        return Widget(wid.Select, **kwargs)
    elif word in ['dropdown', 'dd', 'ddown']:
        return Widget(wid.Dropdown, **kwargs)
    elif word in ['selection_slider', 'selslider', 'ss']:
        return Widget(wid.SelectionSlider, **kwargs)
    elif word in ['toggle_button', 'toggle', 'tog']:
        return Widget(wid.ToggleButton, **kwargs)
    elif word in ['toggle_buttons', 'toggles', 'togs']:
        return Widget(wid.ToggleButtons, **kwargs)
    elif word in ['radio_buttons', 'radio', 'rad','rs']:
        return Widget(wid.RadioButtons, **kwargs)
    elif word in ['html', 'HTML']:
        return Widget(wid.HTML, **kwargs)
    elif word in ['TextArea', 'texta', 'textarea', 'text_area']:
        return Widget(wid.Textarea, **kwargs)
    
    else:
        if not 'value' in kwargs.keys():
            kwargs['value'] = word
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
            return Widget(wid.Label, **kwargs)
        else:
            return Widget(wid.Label, **kwargs)
