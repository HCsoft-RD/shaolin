# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 23:31:50 2016

@author: Guillem Duran Ballester for HCSoft
"""
import numpy as np
import pandas as pd
from shaolin.core.dashboard import Dashboard
class DataFrameScaler(Dashboard):
    
    def __init__(self,
                 data,
                 funcs=None,
                 min=0,
                 max=100,
                 step=None,
                 low=None,
                 high=None,
                 **kwargs):
        if funcs is None:
            self.funcs = {'raw':lambda x: x,
                          'zscore': lambda x: (x-np.mean(x))/np.std(x),
                          'log': np.log,
                          'rank':lambda x: pd.DataFrame(x).rank().values.flatten()
                         }
        else:
            self.funcs  = funcs
        self._df = data.apply(self.categorical_to_num)
        if min is None:
            min = self._df.min().values[0]
        if max is None:
            max = self._df.max().values[0]
        if step is None:
            step = (max-min)/100.
        if low is None:
            low = min
        if high is None:
            high = max
        
        self.output = None
        
        dash = ['c$N=df_scaler',
                ['@('+str(min)+', '+str(max)+', '+str(step)+', ('+str(low)+', '+str(high)+'))$N=scale_slider&d=Scale',
                 ['r$N=main_row',['@dd$d=Apply&N=dd_sel&val=raw&o='+str(list(self.funcs.keys())),'@True$N=scale_chk&d=Scale']]
                ]
               ]
        Dashboard.__init__(self, dash, mode='interactive', **kwargs)
        self.dd_sel.target.layout.width = "100%"
        self.scale_chk.widget.layout.padding = "0.25em"
        self.observe(self.update)
        self.update()
    
    @property
    def data(self):
        return self._df

    @data.setter
    def data(self, val):
        self._df = val.apply(self.categorical_to_num)
        self.update()
    
    def scale_func(self, data):
        Ma = np.max(data)
        mi = np.min(data)
        score = ((data-mi)/(Ma-mi))#to 0-1 interval
        if mi == Ma:
               return np.ones(len(score)) *0.5
        scale_h = self.scale_slider.value[1]
        scale_l = self.scale_slider.value[0]
        return score*(scale_h-scale_l)+scale_l 
    
    def update(self, _=None):
        self.output = self.data.apply(self.funcs[self.dd_sel.value])
        if self.scale_chk.value:
            self.scale_slider.visible = True
            self.output = self.output.apply(self.scale_func)
        else:
            self.scale_slider.visible = False
    @staticmethod
    def categorical_to_num(data):
        """Converts categorical data into an array of ints"""
        if isinstance(data.values[0], str):
            cats = np.unique(data)
            imap = {}
            for i, cat in enumerate(cats):
                imap[cat] = i
            fun = lambda x: imap[x]
            return list(map(fun, data))
        else:
            return data
    
    @staticmethod
    def is_categorical_series(data):
        """true if data is a categorical series"""
        return  isinstance(data.values[0], str)
