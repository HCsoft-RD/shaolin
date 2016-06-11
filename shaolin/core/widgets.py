
"""
Created on Wed Apr 20 10:22:21 2016

@author: Guillem Duran for HCSOFT
"""

import ipywidgets as wid

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
        if hasattr(self.target, 'value'):
            return self.target.value
    @value.setter
    def value(self, val):
        if hasattr(self.target, 'value'):
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
            self.target.orientation = val
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