# -*- coding: utf-8 -*-
"""
Created on Thu May 19 12:37:11 2016

@author: sergio
"""

# -*- coding: utf-8 -*-
import ipywidgets as wid
import numpy as np
from .context import Widget
"""Object notation library. This is used to easily instantiate widgets"""
def object_notation(word, kwargs):
    """
    Object Syntax
    -------------
    Widget creation rules according to object notation syntax. It its based on the syntax
    used in interact functions in ipywidgets.

    Sliders:
    --------
             Data types:
             -----------
             Set by the element of the tuple containint the value parameter.
             Compatible types are:

             float --> FloatSlider widget.
             int --> IntSlider widget.
             tuple of int --> IntRangeSlider widet.
             tuple of float --> FloatRangeSlider widet.

             Syntax
             -------
             Extended object notation: (min,max,step,value):
             Compact notation: (value)

    Boolean:
    --------
             Data types:
             -----------
             Value must be a bool.

             True,False --> Checkbox widget.
             tuple --> Checkbox widget.
             list--> ToggleButton widet.
             [(bool,)] --> Valid Widget

             CheckBox
             --------
             Extended object notation:
               (value,description)
               (value)
             Compact notation: value

             ToggleButton
             ------------
             Extended object notation:
               [value, description]
             Compact notation: [value]

             Valid
             ------------
             Compact notation:
               [[value]]
               [(value,)]

    Options:
    --------
             Data types:
             -----------
             tuple --> Dropdown widget.
             list --> SelectMultiple widget.
             [()] --> ToggleButtons widget.
             ([]) --> RadioButtons widget.
             Dropdown
             --------
             Extended object notation:
               (options,value)
             Compact notation: (options)

            SelectMultiple
            --------------
             Extended object notation:
               [options,value]
             Compact notation: [options]

             RadioButtons
             ------------
             Extended object notation:
               ([options,value])
             Compact notation: ([options],)

            ToggleButtons
            -------------
             Extended object notation:
               [(options,value)]
             Compact notation: [(options,)]

    Numeric text box:
    -----------------
             Data types:
             -----------
             Set by the element of the list containing the value parameter.
             Compatible types are:

             float --> FloatText widget.
             int --> IntText widget.

             Syntax
             -------
             Extended object notation: [min,max,value]:
             Compact notation: [value]
    """
    if word_is_boolean(word):
        return word_to_boolean_widget(word, kwargs)

    elif word_is_numeric(word):
        if is_range_word(word):
            try:
                assert valid_range_word(word)
            except AssertionError as e:
                e.args += ('Your typed in an invalid range widget')
                raise
            kwargs = update_range_kwargs(word, kwargs)
            return word_to_range_widget(word, kwargs)
        else:
            try:
                assert valid_num_word(word)
            except AssertionError as e:
                e.args += ('Your typed in an invalid num widget')
                raise
            kwargs = update_num_kwargs(word, kwargs)
            return word_to_num_widget(word, kwargs)
    else:
        return word_to_options_widget(word, kwargs)
#BOOLEAN OBJECT NOTATION EVALUATION
def word_is_boolean(word):
    """Determines if a word corresponds to a boolean widget in ON
    """
    bool_ = (bool, np.bool)
    #ChecBox CON
    if isinstance(word, bool_):
        return True
    elif isinstance(word, (tuple, list)):
        #CheckBox or ToggleButton FON
        if isinstance(word[0], bool_):
            return True
        #Valid widget
        elif isinstance(word, list)\
             and isinstance(word[0], (tuple, list)):
                 return isinstance(word[0][0], bool_)
        else:
            return False
    else:
        return False

def word_to_boolean_widget(word, kwargs):
    """Check syntax for boolean widgets
    """
    bool_ = (bool, np.bool)
    #ChecBox CON
    if isinstance(word, bool_):
        return Widget(wid.Checkbox, value=word, **kwargs)
    try:
        assert len(word) <= 2
    except AssertionError as e:
        e.args += ('Your typed in an invalid bool word')
        raise e
    if isinstance(word, tuple):
        #valid FON/CON
        if isinstance(word[0], (list, tuple)) and len(word) == 1:
            try:
                assert isinstance(word[0][0], bool_)
            except AssertionError as e:
                e.args += ('Your typed in an invalid Valid widget word')
                raise e
            if not 'mode' in kwargs.keys():
                kwargs['mode'] = 'passive'
            return Widget(wid.Valid, value=word[0][0], **kwargs)
        #checkbox CON
        if len(word) == 1:
            return Widget(wid.Checkbox, value=word[0], **kwargs)
        #checkbox FON
        else:
            return Widget(wid.Checkbox,
                          value=word[0],
                          description=word[1],
                          **kwargs)

    #ToggleButton
    elif isinstance(word, list):
        if len(word) == 1:
            if isinstance(word[0], (list, tuple)):
                if not 'mode' in kwargs.keys():
                    kwargs['mode'] = 'passive'
                return Widget(wid.Valid, value=word[0][0], **kwargs)
            else:
                return Widget(wid.ToggleButton, value=word[0], **kwargs)
        else:
            return Widget(wid.ToggleButton, value=word[0],
                          description=word[1],
                          **kwargs)

def test_bool_words(kwargs={}):
    def compare(word, widget, kwargs):
        return  isinstance(word_to_boolean_widget(word, kwargs).target, widget)
    #CheckBox
    words = [True, (True), (True, 'G1D6B2')]
    for word in words:
        try:
            assert compare(word, wid.Checkbox, kwargs)
        except:
            print('Failed ad word',
                  word,
                  word_to_boolean_widget(word,
                                         kwargs).target
                 )

    words = [[True], [True, 'G1D6B2']]
    for word in words:
        try:
            assert compare(word, wid.ToggleButton, kwargs)
        except:
            print('Failed ad word',
                  word,
                  word_to_boolean_widget(word,
                                         kwargs).target
                 )

    words = [[[True]], [(True,)]]
    for word in words:
        try:
            assert compare(word, wid.Valid, kwargs)
        except:
            print('Failed ad word',
                  word,
                  word_to_boolean_widget(word,
                                         kwargs).target
                 )
    return True

#RANGE WIDGETS
def valid_range_word(word):
    """Check if a confirmed range slider is valid.
    """
    try:
        N = len(word)
        #Slider with value at first item
        if isinstance(word[0], tuple):
            #Slider with value at first item
            valid_value = word[0][0] < word[0][1]
            if N == 1:
            #min must be less than max
                return valid_value
            valid_min = word[0][0] >= word[1]
            if N == 2:
            #Range must have a valid min
                return valid_min
            valid_max = word[0][1] <= word[2]
            if N == 3:
                return valid_min and valid_max
            if N == 4:
                #range greater than step
                slider_range = word[2]-word[1]
                valid_step = slider_range >= word[3]
                return valid_min and valid_max\
                    and valid_step and valid_value
        #Slider with value at first item
        elif isinstance(word[3], tuple):
                valid_value = word[3][0] <= word[3][1]
                valid_min = word[3][0] >= word[0]
                valid_max = word[3][1] <= word[1]
                slider_range = word[1]-word[0]
                valid_step = slider_range > word[2]
                return valid_min and valid_max\
                        and valid_step and valid_value
        else:
             return False
    except:
        return False

def is_range_word(word):
    """Check if a valid numeric word corresponds to a Range widget. If its not then its a
    standard numeric widget.
    """
    try:
        #First item can be a tuple of starting values
        if isinstance(word[0], tuple):
            return True
        elif len(word) == 4:
            #Or it can be stated as the las item of the full tuple
            return isinstance(word[3], tuple) or isinstance(word[0], tuple)
        else:
            return False
    except:
        return False


def word_to_range_widget(word, kwargs):
    """Returns a range widget from a valid range object word"""
    int_types = (int, np.int, np.int16, np.int0, np.int8,
                 np.int32, np.int64)
    #slider CON ((1,2),)
    if isinstance(word[0], tuple):
        if isinstance(word[0][0], int_types):
            return Widget(wid.IntRangeSlider, **kwargs)
        else:
            return Widget(wid.FloatRangeSlider, **kwargs)
    #slider FON (start,end,step,value)
    else:
        if isinstance(word[3][0], int_types):
            return Widget(wid.IntRangeSlider, **kwargs)
        else:
            return Widget(wid.FloatRangeSlider, **kwargs)


def update_range_kwargs(word, kwargs):
    assert is_range_word(word)\
                        and valid_range_word(word)
    N = len(word)
    #Slider with value at first item
    if isinstance(word[0], tuple):
        kwargs['value'] = word[0]
        if N >= 2:
            kwargs['min'] = word[1]
        if N >= 3:
            kwargs['max'] = word[2]
        if N >= 4:
            kwargs['step'] = word[3]
    #Slider with value at first item
    elif isinstance(word[3], tuple):
        kwargs['value'] = word[3]
        kwargs['min'] = word[0]
        kwargs['max'] = word[1]
        kwargs['step'] = word[2]
    else:
        raise ValueError('ONW typo,range word has more than 4 items')
    return kwargs

def test_range_words(kwargs={}):
    def compare(word, widget, kwargs):
        return  isinstance(object_notation(word, kwargs).target, widget)
    #int range CON
    words = [((1, 2), ), ((1, 2), 1), ((1, 5), 1, 10, 1), (1, 5, 1, (1, 2))]
    for word in words:
        #print (kwargs)
        assert compare(word, wid.IntRangeSlider, kwargs)

    words = [((1., 2),), ((1., 2), 1), ((1., 5), 1, 10, 1), (1, 5, 1, (1., 2))]
    for word in words:
        #print (word)
        assert compare(word, wid.FloatRangeSlider, kwargs)

#NUM WIDGETS
#NUMERIC OBJECT NOTATION
def word_is_numeric(word):
    """Determines if an object notation word (ONW) corresponds to a numeric widget
       acording to the ON rules. They have the following properties:
       type: int, float, tuple or list
       If len(word) <= 4 first element must be a value tuple for a range slider or numeric,
       and if the word its specified in full object notation that applies for its last element.
    """
    int_types = (int, np.int, np.int16, np.int0, np.int8,
                 np.int32, np.int64)
    float_types = (np.float, np.float128, np.float16,
                   np.float32, np.float64, float)
    #slider CON
    if isinstance(word, (int_types, float_types)):
        return True
    elif isinstance(word, (tuple, list)):
        #range CON or FON with value as word[0]
        if isinstance(word[0], tuple):
            #weird case when you can define by mistake a ToggleButton
            #filled with numeric data ex:[(1,2,3)]
            if isinstance(word, list)\
                and isinstance(word[0], tuple)\
                and isinstance(word[0][0], (int_types, float_types)):
                    return False
            else:
                return isinstance(word[0][0], (int_types, float_types))
        #check value in FON with value as word[3]
        elif len(word) == 4:
            slider_or_num_text = isinstance(word[3], (int_types, float_types))
            #range FON
            if not slider_or_num_text and isinstance(word[3], tuple):
                return isinstance(word[3][0], (int_types, float_types))
            else:
                return slider_or_num_text

        elif len(word) > 4:
            return False
        #if not first  element must be a number
        else:
            return isinstance(word[0], (int_types, float_types))
    else:
        return False

def valid_num_word(word):
    """Check if a numeric ONW that is not a IntRangeSlider or a FloatRangeSlider
    has valid parameters
    """
    int_types = (int, np.int, np.int16, np.int0, np.int8,
                 np.int32, np.int64)
    float_types = (np.float, np.float128, np.float16,
                   np.float32, np.float64, float)
    try:
        #float or int input
        if isinstance(word, (int_types, float_types)):
            return True
        #Check all possible cases
        N = len(word)
        if N == 1:
            return isinstance(word[0], (int_types, float_types))
        num_range = word[1]-word[0]
        valid_range = num_range > 0
        if N == 2:
            return valid_range
        valid_step = word[2] <= num_range
        if N == 3:
            return valid_range and valid_step
        valid_value = word[0] <= word[3] <= word[1]
        if N == 4:
            return valid_range and valid_step and valid_value
        else:
            return False
    except:
        return False

def update_num_kwargs(word, kwargs):
    assert word_is_numeric(word)\
                        and valid_num_word(word)
    int_types = (int, np.int, np.int16, np.int0, np.int8,
                 np.int32, np.int64)
    float_types = (np.float, np.float128, np.float16,
                   np.float32, np.float64, float)
    if isinstance(word, (int_types, float_types)):
        return kwargs
    if len(word) == 1:
        kwargs['value'] = word[0]
    if len(word) >= 2:
        kwargs['max'] = word[1]
        kwargs['min'] = word[0]
    if len(word) >= 3:
        kwargs['step'] = word[2]
    if len(word) == 4:
            kwargs['value'] = word[3]
    if len(word) > 4:
        raise ValueError('ONW typo,numeric word has more than 4 items')
    return kwargs

def word_to_num_widget(word, kwargs):
    int_types = (int, np.int, np.int16, np.int0, np.int8,
                 np.int32, np.int64)
    float_types = (np.float, np.float128, np.float16,
                   np.float32, np.float64, float)
    if isinstance(word, int_types):
        return Widget(wid.IntSlider, **kwargs)
    elif isinstance(word, float_types):
        return Widget(wid.FloatSlider, **kwargs)

    elif isinstance(word, tuple):
        is_int = np.all([isinstance(w, int_types) for w in word])
        if is_int:
            return Widget(wid.IntSlider, **kwargs)
        else:
             return Widget(wid.FloatSlider, **kwargs)
    else:
        is_int = np.all([isinstance(w, int_types) for w in word])
        if is_int:
            return Widget(wid.IntText, **kwargs)
        else:
             return Widget(wid.FloatText, **kwargs)

def test_num_words(kwargs={}):
    def compare(word, widget, kwargs):
        return  isinstance(object_notation(word, kwargs).target, widget)
    #int range CON
    words = [(1, 5, 1), (1, 100, 10, 20), (1, 5, 1, 2)]
    for word in words:
        assert compare(word, wid.IntSlider, kwargs)

    words = [(1., 1.5, 0.01), (1., 100., 10., 20.), (1., 5., 1., 2.)]
    for word in words:
        print(word)
        assert compare(word, wid.FloatSlider, kwargs)

def word_to_options_widget(word, kwargs):
    #Dropdown
    if isinstance(word, list):
        if len(word) == 1:
            return Widget(wid.SelectMultiple,
                          options=word[0],
                          **kwargs
                         )
        else:
            return Widget(wid.SelectMultiple,
                          options=word[0],
                          value=word[1],
                          **kwargs
                         )
    if isinstance(word, tuple):
        if len(word) == 1:
            return Widget(wid.Dropdown,
                          options=word[0],
                          **kwargs
                         )
        else:
            return Widget(wid.Dropdown,
                          options=word[0],
                          value=word[1],
                          **kwargs
                         )
