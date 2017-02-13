# -*- coding: utf-8 -*-
"""
Created on Thu May 19 12:03:50 2016

@author: sergio
"""

import ast
import six
import ipywidgets as wid
from shaolin.core.object_notation import object_notation
from shaolin.core import widgets

#from .widgets import widgets.Widget, widgets.Title, widgets.SubTitle, widgets.SubSubTitle

def shaoscript(word, kwargs=None):
    """Return a shaolin widgets.Widget from a ShaoScript value.
    Parameters
    ----------
    word : string, object
        String can be the name of a widgets.Widget in shaoscript syntax, or a string 
        conaining the full definition of a widgets.Widget using the shaoscript syntax to
        also define its kwargs.
    kwargs: dict, default: None
        Contains the kwargs values for the widgets.Widget that will be returned. The
        key value parameters contained in the dict will be overriden by those 
        defined in word.
    Returns
    -------
    widgets.Widget: shaolin widgets.Widget.
        
    """
    
    kwargs = kwargs or {}
    #create a widgets.Widget from a string. get its widgets.Widget type and kwargs
    if isinstance(word, six.string_types):
        word, kwargs = _handle_shaoscript_syntax(word, kwargs)
    #word and kwargs from shaoscript syntax
    #if the word corresponds to a widgets.Widget definition
    if isinstance(word, six.string_types):
        return _string_to_wiget(word, kwargs)
    #If word is already an ipywidgets.Widget class
    elif isinstance(word, tuple(wid.Widget.widget_types.values())):
        return  widgets.Widget(word, **kwargs)
    #word has to be a python object representing object notation
    try:
        return object_notation(word, kwargs)
    except:
        raise ValueError('''Bad shaoscript syntax. \n
                         Failed to convert word: {} with kwargs:{}.'''\
                         .format(word, kwargs))

def _handle_shaoscript_syntax(string, kwargs=None):
    """Return a string defining a shaolin widgets.Widget and a dictionary containinng
    its kwargs.
    Parameters
    ----------
    string : string
        String can be the name of a widgets.Widget in shaoscript syntax, or a string 
        conaining the full definition of a widgets.Widget using the shaoscript syntax to
        also define its kwargs.
    kwargs: dict, default: None
        Contains the kwargs values for the widgets.Widget that will be returned. The
        key value parameters contained in the dict will be overriden by those 
        defined in word.
    Returns
    -------
    word: string
        Contains only the type of the widgets.Widget in shaoscript notation.
    kwargs: dict
        Dictionary containing the kwargs for creating a shaolin widgets.Widget.
        
    Shaoscript custom parameters available
    --------------------------------------
        paramters(aliases): value parsing 
        
        'options'('o', 'opt','opts'): ast.literal_eval
        'description'('d','desc'): str
        'id': str
        'class_'('c','cls'): str
        'visible'('vis'): boolean
        'orientation'('ori','orient'): 'vertical','horizontal' 
        'name'('n'): str
        'value'('val','v'): str
            val being a string means that non string values cannot be set this way.
            Use object notation in the definition of the widgets.Widget.
        
    """
    kwargs = kwargs or {}
    #take into account interactivity
    main_key = string[0]
    if main_key == '@':
        kwargs['mode'] = 'interactive'
        sliced = string[1:]
    elif main_key == '/':
        kwargs['mode'] = 'active'
        sliced = string[1:]
    else:
        sliced = string
    word = sliced
    #separating widgets.Widget descriptor from atributes
    split = word.split('$')
    if _is_object_notation(split[0]):
        word = ast.literal_eval(split[0])
    else:
        word = split[0]
    #string defines kwargs
    
    kwargs = shaoscript_to_kwargs(split[1], kwargs) if len(split) == 2 else kwargs
    return word, kwargs

def _is_object_notation(string):
    """Checks if a string can be converted to object notation"""
    try:
        onw = ast.literal_eval(string)
        __ =object_notation(onw, {})
        return True
    except:
        return False


def shaoscript_to_kwargs(string, kwargs):
    params = string.split('&')
    for par in params:
        key, val = decode_param(par)
        kwargs[key] = val
    #name infered from description         
    if 'description' in kwargs.keys()\
        and 'name' not in kwargs.keys():
        kwargs['name'] = kwargs['description'].lower().replace(' ', '_')
    #id infered from name
    if 'name' in kwargs.keys()\
        and not 'id' in kwargs.keys():
        kwargs['id'] = kwargs['name'].lower().replace('_', '-')
    return kwargs

def decode_param(string):
    """
    Converts a string representing a parameter in shaoscript syntax to a pair of key, value
     a valid parameter in shaoscript will have the following form:
         
         param --> 'name=val'
    There are some parameters that have custom parsing and are allowed aliases.
    The aliases are not case sensitive.

    Paramters(aliases): value parsing 
    ---------------------------------
    'options'('o', 'opt','opts'): ast.literal_eval
    'description'('d','desc'): str
    'id': str
    'class_'('c','cls'): str
    'visible'('vis'): boolean
    'orientation'('ori','orient'): 'vertical','horizontal' 
    'name'('n'): str
    'value'('val','v'): str
        val being a string means that non string values cannot be set this way.
        Use object notation in the definition of the widgets.Widget.
    'placeholder'('ph','pholder'): str
    '_widgets.Titles'('widgets.Titles','t','widgets.Title','tit'): dict
        the val attribute will be the names of each widgets.Title separated by commas.
        no need to specify string simbols "" or '', as conversion will be taken
        care of internally.
            
               
    """
    key, val = string.split('=')
    key = key.lower()
    if key in  ['o','opt','opts','options']:
        name = 'options'
        val = ast.literal_eval(val)
    elif key in  ['d','desc', 'description']:
        name = 'description'
    elif key == 'id':
        name = 'id'
    elif key in ['continuous_update', 'cu','cont','cupdate']:
        name = 'continuous_update'
        val = True if val in ['1','True'] else False
    elif key in ['class_','cls']:
        name = 'class_'
    elif key in ['visible', 'vis']:
        name = 'visible'
        val = 'visible' if val in ['0', 'False','None'] else 'hidden'
    elif key in ['ori', 'orientation','orient']:
        name = 'orientation'
        if val in ['v','vert', 'vertical']:
            val = 'vertical'
        elif val in ['h','hori', 'horizontal']:
            val = 'horizontal'
    elif key in ['n', 'name']:
        name = 'name'
    elif key in ['v','val', 'value']:
        name = 'value'
        #val = ast.literal_eval(val)
    elif key in ['mode', 'm']:
        name = 'mode'
    elif key in ['placeholder','ph','pholder']:
        name='placeholder'
    elif key in ['_titles','title','t','widget_titles','tit']:
        name = '_titles'
        widgets.Titles_names = val.split(',')
        val = dict(zip(range(len(widgets.Titles_names)),widgets.Titles_names))
    else:
        name = key
        val = ast.literal_eval(val)
    return name, val

def _string_to_wiget(word, kwargs):
    def create_colormap(kwargs):
        from shaolin.dashboards import colormap as cmap
        if 'id' in kwargs.keys():
            del kwargs['id']
        return cmap.ColormapPicker(**kwargs)
    """Creates a shaolin widgets.Widget from a string and a dictionary of kwargs"""
    assert isinstance(word, six.string_types)
    word = word.lower()
    #Layout
    #---------------------------------
    if word in ['c', 'col', 'column', 'vbox', 'v']:
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        return widgets.Widget(wid.VBox, **kwargs)
    elif word in ['r', 'row', 'HBox', 'box', 'h']:
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        return widgets.Widget(wid.HBox, **kwargs)
    #Markdown
    #--------------------------------
    elif word in ['widgets.SubSubTitle', 'h3', '###', 'subsub', 'ss']:
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        return widgets.SubSubTitle(**kwargs)

    elif word[:3] == '###':
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        if not 'name' in kwargs.keys():
            kwargs['name'] = word[3:].lower().replace(' ', '_')
        if not 'id' in kwargs.keys():
            kwargs['id'] = kwargs['name'].lower().replace('_', '-')
        return widgets.SubSubTitle(value=word[3:], **kwargs)

    elif word in ['widgets.SubTitle', 'h2', '##', 'sub', 's']:
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        return widgets.SubTitle(**kwargs)

    elif word[:2] == '##':
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        if not 'name' in kwargs.keys():
            kwargs['name'] = word[2:].lower().replace(' ', '_')
        if not 'id' in kwargs.keys():
            kwargs['id'] = kwargs['name'].lower().replace('_', '-')
        return widgets.SubTitle(value=word[2:], **kwargs)

    elif word in ['widgets.Title', 'h1', '#']:
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        return widgets.Title(**kwargs)

    elif word[:1] == '#':
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
        if not 'name' in kwargs.keys():
            kwargs['name'] = word[1:].lower().replace(' ', '_')
        if not 'id' in kwargs.keys():
            kwargs['id'] = kwargs['name'].lower().replace('_', '-')
        return widgets.Title(value=word[1:], **kwargs)

    #Int and float
    #--------------------------------
    elif word in ['float_slider', 'floatslider', 'fsld', 'fs']:
        return widgets.Widget(wid.FloatSlider, **kwargs)
    elif word in ['float_text', 'floattext', 'ftxt', 'ft']:
        return widgets.Widget(wid.FloatText, **kwargs)
    elif word in ['int_slider', 'intslider', 'isld', 'is']:
        return widgets.Widget(wid.IntSlider, **kwargs)
    elif word in ['int_text', 'inttext', 'itxt', 'it']:
        return widgets.Widget(wid.IntText, **kwargs)
    #Range
    #--------------------------------
    elif word in ['float_range', 'floatprogress', 'fprog', 'fp']:
        return widgets.Widget(wid.FloatRangeSlider, **kwargs)
    elif word in ['int_range', 'intrange', 'irng', 'ir']:
        return widgets.Widget(wid.IntRangeSlider, **kwargs)
    #Progress
    #--------------------------------
    elif word in ['float_progress', 'floatprogress', 'fprog', 'fp']:
        return widgets.Widget(wid.FloatProgress, **kwargs)
    elif word in ['int_progress', 'intprogress', 'iprog', 'ip']:
        return widgets.Widget(wid.IntProgress, **kwargs)
    #Button
    #--------------------------------
    elif word in ['button', 'btn', 'b']:
        return widgets.Widget(wid.Button, **kwargs)
    #string and color
    #---------------
    elif word in ['text', 'txt','str','string']:
        return widgets.Widget(wid.Text, **kwargs)
    elif word in ['color', 'colorpicker','cp','cpicker']:
        return widgets.Widget(wid.ColorPicker, **kwargs)
    #colormap
    
        
    elif word in ['cm', 'cmap','colormap','cmappicker']:
        return create_colormap(kwargs)
        
    #Options for pseudo tabs creation
    #--------------------------------
    #"""
    #elif word in ['radio_display_selection','r_ds','radio_ds']:
    #    return RadioDisplaySelection(**kwargs)
    #elif word in ['toggle_display_selection','t_ds','toggle_ds']:
    #    return ToggleDisplaySelection(**kwargs)
    #elif word in ['display_selection','ds','dsel']:
    #    return DisplaySelection(**kwargs)
    
    #"""
    #Selectors
    #--------------------------
    elif word in ['select_multiple', 'selmul', 'sm']:
        return widgets.Widget(wid.SelectMultiple, **kwargs)
    elif word in ['select', 'sel']:
        return widgets.Widget(wid.Select, **kwargs)
    elif word in ['dropdown', 'dd', 'ddown']:
        return widgets.Widget(wid.Dropdown, **kwargs)
    elif word in ['selection_slider', 'selslider', 'ss']:
        return widgets.Widget(wid.SelectionSlider, **kwargs)
    elif word in ['toggle_button', 'toggle', 'tog']:
        return widgets.Widget(wid.ToggleButton, **kwargs)
    elif word in ['toggle_buttons', 'toggles', 'togs']:
        return widgets.Widget(wid.ToggleButtons, **kwargs)
    elif word in ['radio_buttons', 'radio', 'rad','rs']:
        return widgets.Widget(wid.RadioButtons, **kwargs)
    elif word in ['html', 'HTML']:
        return widgets.Widget(wid.HTML, **kwargs)
    elif word in ['TextArea', 'texta', 'textarea', 'text_area']:
        return widgets.Widget(wid.Textarea, **kwargs)
    
    elif word in ['tex','latex']:
        kwargs['value'] = '$$'+str(kwargs['value'])+'$$'
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
            return widgets.Widget(wid.Label, **kwargs)
    elif word in ['tab','t','tabs']:
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
            return widgets.Widget(wid.Tab, **kwargs)
    elif word in ['accordion','accord','tabs','ac','a']:
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
            return widgets.Widget(wid.Accordion, **kwargs)
    
    else:
        if not 'value' in kwargs.keys():
            kwargs['value'] = word
        if not 'mode' in kwargs.keys():
            kwargs['mode'] = 'passive'
            return widgets.Widget(wid.Label, **kwargs)
        else:
            return widgets.Widget(wid.Label, **kwargs)
