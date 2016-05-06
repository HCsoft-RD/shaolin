# -*- coding: utf-8 -*-
"""Created on Wed Apr 20 10:22:21 2016

@author: Guillem Duran for HCSOFT
This module contains the classes for managing and calculating graphs
"""
import numpy as np
import ipywidgets as widgets
import pandas as pd
from networkx.drawing.nx_agraph import graphviz_layout
import networkx as nx
import planarity
#kfw stands for KungFu Widgets
from .context import sww
#from sh.widgets.wranglers import LayoutParams, GraphParams, MatrixParams


LAYOUT_PARAMS = {'dim':'both',
                 'scale':1,
                 'center':None,
                 'weigth':'weight',
                 'fixed':None,
                 'iterations':5000,
                 'prog':'neato',
                 'layout':'dh_spring_layout',
                 'k':'exchange'}
LAYOUTS = {'Circular layout': 'circular_layout',
           'Random layout': 'random_layout',
           'Shell layout':'shell_layout',
           'Spectral layout':'spectral_layout',
           'Spring layout':'spring_layout',
           'Graphviz layout':'draw_graphviz',
           'HCsoft layout':'dh_spring_layout'}

TARGET_OPTIONS = {'Raw':'raw', #Do nothing
                  'Clip':'clip', #limit the matrix values betwen (min,max)
                  'Scale':'scale', #scale the matrix values between (min,max)
                  'Zscore':'zscore', #zscore the matrix elements
                  'Distance':'compute_distance', #Convert corr into a distance
                 }

MATRIX_PARAMS = {'norm_min':0,
                 'norm_max':1,
                 'clip_min':1e-5,
                 'clip_max':1e10,
                 'target':[('clip', (1e-5, 1e10))],#f[(fun,(kwargs))]
                }

GRAPH_PARAMS = {'graph_type':'full',
                'inverted' :  False,
                'threshold': 0.00,
                'target_attr':'exchange'
               }

NODE_METRICS = ['betweenness_centrality',
                'betweenness',
                'degree',
                'degree_weighted',
                'eigenvector_weighted',
                'eigenvector',
                'closeness_weighted',
                'closeness',
                'eccentricity_weighted',
                'eccentricity',
                'X', 'Y', 'XmY', 'XpY']

NODE_TARGET_ATTRS = {'Simetric max':'M',
                     'Correlation':'corr',
                     'Covariance':'cov',
                     'Market custom':'exchange',
                     'k spring':'k_price',
                     'L0':'l0',
                     'Simetric min':'m'}

class LayoutCalculator(object):
    """Calculates an arbitrary layout for a netxorkx Graph.
        Parameters:
        -----------
        G: networkx Graph.
        LAYOUT_PARAMS = {'dim':'both',
                         'scale':1,
                         'center':None,
                         'weigth':'weight',
                         'fixed':None,
                         'iterations':5000,
                         'prog':'neato',
                         'layout':'dh_spring_layout',
                         'k':'exchange'}
        LAYOUTS = {'Circular layout': 'circular_layout',
                   'Random layout': 'random_layout',
                   'Shell layout':'shell_layout',
                   'Spectral layout':'spectral_layout',
                   'Spring layout':'spring_layout',
                   'Graphviz layout':'draw_graphviz',
                   'HCsoft layout':'dh_spring_layout'}
        """

    def __init__(self, G,
                 default_params=LAYOUT_PARAMS):
        self.G = G.copy()
        self.default_params = default_params
        self.params_w = sww.LayoutParams(G=self.G, default_params=default_params)
        self.params = self.params_w
        self.update()
        self.button = widgets.Button(description='Run')
        self.button.on_click(self.on_button_click)
        self.b_box = widgets.HBox(children=[self.button])
        self.widget = widgets.VBox(children=[self.params_w.widget,
                                             self.b_box])

    def on_button_click(self, b):
        """update trigger"""
        self.update()

    def update(self, G=None):
        """Starts the calculations from current LAYOUT_PARAMS"""
        if not G is None:
            del self.node
            del self.edge
            self.G = G.copy()

        self.params = sww.LayoutParams(self.G, self.default_params)   
        self.params.target = self.params_w.target.copy()                                     
        self.calculate_layouts()
        self.node = pd.Panel(self.node)
        self.edge = pd.Panel(self.edge)

    def one_layout(self, func, kwargs):
        """Calculates one arbitrary layout"""
        if func == 'dh_spring_layout':
            return self.dh_spring_layout(self.G, **kwargs)
        elif func == 'draw_graphviz':
            return graphviz_layout(self.G, **kwargs)
        else:
            return getattr(nx, func)(self.G, **kwargs)

    def calculate_layouts(self):
        """Will calculate de layour acording to its current LAYOUT_PARAMS configuration"""
        only_2d = ['circular_layout', 'shell_layout', 'draw_graphviz', 'graphviz_layout']
        self.node = {}
        self.edge = {}
        # both = self.params.dim.value not in self.params.target.keys()
        if True:#both:
            for sd in ['2d', '3d']:
                fun = list(self.params.target[sd].keys())[0]
                kwargs = self.params.target[sd][fun]
                layout = self.one_layout(fun, kwargs)
                df_ = pd.DataFrame(layout).T
                self.node[sd] = df_.copy()
                if sd == '2d':
                    if len(self.node[sd].columns) == 2:
                    #after the first one the df will have a 'z column filled with nan
                        df_.columns = ['x', 'y']
                        self.node[sd].columns = ['x', 'y']
                    edge_data = [(df_.x[e[0]], df_.y[e[0]], df_.x[e[1]], df_.y[e[1]])
                                 for e in self.G.edges_iter()]
                    edge_index = [e for e in self.G.edges_iter()]
                    self.edge[sd] = pd.DataFrame(index=edge_index,
                                                 data=edge_data,
                                                 columns=['x0', 'y0', 'x1', 'y1']
                                                )
                    self.edge[sd]['cx'] = (self.edge[sd]['x0']+self.edge[sd]['x1'])/2
                    self.edge[sd]['cy'] = (self.edge[sd]['y0']+self.edge[sd]['y1'])/2
                elif sd == '3d':
                    if fun in only_2d:
                        df_['z'] = 0
                        self.node[sd]['z'] = 0
                    if len(self.node[sd].columns) == 3:
                        df_.columns = ['x', 'y', 'z']
                        self.node[sd].columns = ['x', 'y', 'z']
                        
                    edge_data = [(df_.x[e[0]], df_.y[e[0]], df_.z[e[0]],
                                  df_.x[e[1]], df_.y[e[1]], df_.z[e[1]])
                                 for e in self.G.edges_iter()
                                ]
                    edge_index = [e for e in self.G.edges_iter()]
                    self.edge[sd] = pd.DataFrame(index=edge_index,
                                                 data=edge_data,
                                                 columns=['x0', 'y0', 'z0',
                                                          'x1', 'y1', 'z1']
                                                )
                    self.edge[sd]['cx'] = (self.edge[sd]['x0']+self.edge[sd]['x1'])/2
                    self.edge[sd]['cy'] = (self.edge[sd]['y0']+self.edge[sd]['y1'])/2
                    self.edge[sd]['cz'] = (self.edge[sd]['z0']+self.edge[sd]['z1'])/2
        else:#TODO: handle single layout manipulation and arbitrary dimension layoyt
            return

    def dh_spring_layout(self, G,
                         dim=2,
                         k=None,
                         pos=None,
                         fixed=None,
                         iterations=50,
                         weight='weight',
                         scale=1.0,
                         center=None,
                         kname='var'
                        ):
        """Position nodes using a modified spring layout that allows for different k for each node.
           Same interface as nx.spring_layout.

        Parameters
        ----------
        G : NetworkX graph or list of nodes

        dim : int
           Dimension of layout

        k : array (default=None)
           Optimal distance between nodes.  If you want it to make it None
           just use nx.spring_layout.

        pos : dict or None  optional (default=None)
           Initial positions for nodes as a dictionary with node as keys
           and values as a list or tuple.  If None, then use random initial
           positions.

        fixed : list or None  optional (default=None)
          Nodes to keep fixed at initial position.

        iterations : int  optional (default=50)
           Number of iterations of spring-force relaxation

        weight : string or None   optional (default='weight')
            The edge attribute that holds the numerical value used for
            the edge weight.  If None, then all edge weights are 1.

        scale : float (default=1.0)
            Scale factor for positions. The nodes are positioned
            in a box of size [0,scale] x [0,scale].

        center : array-like or None
           Coordinate pair around which to center the layout.


        Returns
        -------
        dict :
           A dictionary of positions keyed by node

        Examples
        --------
        >>> G=nx.path_graph(4)
        >>> pos=nx.spring_layout(G)

        # The same using longer function name
        >>> pos=nx.fruchterman_reingold_layout(G)
        """
        import numpy as np
        def _rescale_layout(pos, scale=1):
            # rescale to (-scale,scale) in all axes
            # shift origin to (0,0)
            lim = 0 # max coordinate for all axes
            for i in range(pos.shape[1]):
                pos[:, i] -= pos[:, i].mean()
                lim = max(pos[:, i].max(), lim)
            # rescale to (-scale,scale) in all directions, preserves aspect
            for i in range(pos.shape[1]):
                pos[:, i] *= scale/lim
            return pos

        def process_params(G, center, dim):
            """ Some boilerplate code."""
            import numpy as np

            if not isinstance(G, nx.Graph):
                empty_graph = nx.Graph()
                empty_graph.add_nodes_from(G)
                G = empty_graph

            if center is None:
                center = np.zeros(dim)
            else:
                center = np.asarray(center)

            if len(center) != dim:
                msg = "length of center coordinates must match dimension of layout"
                raise ValueError(msg)

            return G, center

        G, center = process_params(G, center, dim)

        if fixed is not None:
            nfixed = dict(zip(G, range(len(G))))
            fixed = np.asarray([nfixed[v] for v in fixed])

        if pos is not None:
            # Determine size of existing domain to adjust initial positions
            dom_size = max(np.array(list(pos.values())).flatten())
            shape = (len(G), dim)
            pos_arr = np.random.random(shape) * dom_size + center
            for i, n in enumerate(G):
                if n in pos:
                    pos_arr[i] = np.asarray(pos[n])
        else:
            pos_arr = None

        if len(G) == 0:
            return {}
        if len(G) == 1:
            return {G.nodes()[0]: center}

        try:
            # Sparse matrix
            if len(G) < 500:  # sparse solver for large graphs
                raise ValueError
            A = nx.to_scipy_sparse_matrix(G, weight=weight, dtype='f')
            k = nx.to_scipy_sparse_matrix(G, weight=kname, dtype='f')
            if k is None and fixed is not None:
                # We must adjust k by domain size for layouts that are not near 1x1
                nnodes, _ = A.shape
                k = dom_size / np.sqrt(nnodes)
            pos = _sparse_fruchterman_reingold(A, dim, k, pos_arr, fixed, iterations)
        except:
            A = nx.to_numpy_matrix(G, weight=weight)
            k = nx.to_numpy_matrix(G, weight=kname)
            k = np.asarray(k)
            if k is None and fixed is not None:
                # We must adjust k by domain size for layouts that are not near 1x1
                nnodes, _ = A.shape
                k = dom_size / np.sqrt(nnodes)
            pos = self._fruchterman_reingold(A, dim, k, pos_arr, fixed, iterations)
        if fixed is None:
            pos = _rescale_layout(pos, scale=scale) + center
        pos = dict(zip(G, pos))
        return pos


    def _fruchterman_reingold(self, A, dim=2, k=None, pos=None, fixed=None,
                              iterations=50):
        # Position nodes in adjacency matrix A using Fruchterman-Reingold
        # Entry point for NetworkX graph is fruchterman_reingold_layout()
        try:
            import numpy as np
        except ImportError:
            raise ImportError("_fruchterman_reingold() requires numpy: http://scipy.org/ ")

        try:
            nnodes, _ = A.shape
        except AttributeError:
            raise nx.NetworkXError(
                "fruchterman_reingold() takes an adjacency matrix as input")

        A = np.asarray(A) # make sure we have an array instead of a matrix

        if pos is None:
            # random initial positions
            pos = np.asarray(np.random.random((nnodes, dim)), dtype=A.dtype)
        else:
            # make sure positions are of same type as matrix
            pos = pos.astype(A.dtype)

        # optimal distance between nodes
        if k is None:
            k = np.sqrt(1.0/nnodes)

        # the initial "temperature"  is about .1 of domain area (=1x1)
        # this is the largest step allowed in the dynamics.
        # We need to calculate this in case our fixed positions force our domain
        # to be much bigger than 1x1

        #pos.T[0] is the first coordinate of the nnode vector
        t = max(max(pos.T[0]) - min(pos.T[0]), max(pos.T[1]) - min(pos.T[1]))*0.1
        # simple cooling scheme.
        # linearly step down by dt on each iteration so last iteration is size dt.
        dt = t/float(iterations+1)
        delta = np.zeros((pos.shape[0], pos.shape[0], pos.shape[1]), dtype=A.dtype)
        umatrix = np.zeros((pos.shape[0], pos.shape[0], pos.shape[1]), dtype=A.dtype)
        # the inscrutable (but fast) version
        # this is still O(V^2)
        # could use multilevel methods to speed this up significantly
        for iteration in range(iterations):
            # matrix of difference between points
            for i in range(pos.shape[1]):
                delta[:, :, i] = pos[:, i, None]-pos[:, i]
            # distance between points
            distance = np.sqrt((delta**2).sum(axis=-1))
            # enforce minimum distance of 0.01
            distance = np.where(distance < 0.01, 0.01, distance)
            A = np.where(A < 0.001, 0.001, A)

            for i in range(pos.shape[1]):
                umatrix[:, :, i] = delta[:, :, i]/distance
            # displacement "force"
            displacement = np.transpose(np.transpose(umatrix)*k*(distance-A)/A).sum(axis=1)

            # update positions
            length = np.sqrt((displacement**2).sum(axis=1))
            length = np.where(length < 0.01, 0.1, length)
            delta_pos = np.transpose(np.transpose(displacement)*t/length)
            if fixed is not None:
                # don't change positions of fixed nodes
                delta_pos[fixed] = 0.0
            pos += delta_pos
            # cool temperature
            t -= dt
        return pos

class CentralityComputer(object):
    """Based on the github repo of Miguel Vaz https://github.com/mvaz/
        This Class computes the node metrics available in netwokrx, ranks them and
        stores the metrics in a DataFrame
    """
    def __init__(self, G, metrics=None, custom=None):
        if metrics is None:
            self.ls_metrics = NODE_METRICS
        else:
            self.ls_metrics = metrics
        self.metrics = self.compute_metrics(G)

    def compute_metrics(self, g):
        """computes a given metric from a list of target metrics"""
        c = self.compute_one(g, self.ls_metrics[0])#first metrics must not be dependent
        for target in self.ls_metrics:
            c[target] = self.compute_one(g, target, c)
        return c.T

    def compute_one(self, g, target, c=None):
        """##How would yo like to define your custom metrics? just by passing
        #a function as parameter or something like custom={'Function name':fun}
        #or something different, i dont know wich one is better
        #quick example:
        #I you just set the attibute Y externally
        #self.Y = None
        #self.custom_params
        #elif target == 'Y':
        #    return self.Y(g,**self.custom_params)"""
        if target == 'betweenness_centrality':
            try:
                return self.betweenness_centrality(g, weighted=True)
            except:
                return np.nan
        elif target == 'betweenness':
            try:
                return self.betweenness_centrality(g, weighted=False)
            except:
                return np.nan
        elif target == 'degree':
            try:
                return self.degree_centrality(g, weighted=False)
            except:
                return np.nan
        elif target == 'degree_weighted':
            try:
                return self.degree_centrality(g, weighted=True)
            except:
                return np.nan
        elif target == 'X':
            try:
                return (c.betweenness + c.betweenness_weighted +
                        c.degree + c.degree_weighted - 4) / 4 / len(c.index)
            except:
                return np.nan
        elif target == 'eigenvector_weighted':
            try:
                return self.eigenvector_centrality(g)
            except:
                return np.nan
        elif target == 'eigenvector':
            try:
                return self.eigenvector_centrality(g, weighted=False)
            except:
                return np.nan
        elif target == ' closeness_weighted':
            try:
                return self.closeness(g)
            except:
                return np.nan
        elif target == 'closeness':
            try:
                return self.closeness(g, weighted=False)
            except:
                return np.nan
        elif target == 'eccentricity_weighted':
            try:
                return self.eccentricity(g)
            except:
                return np.nan
        elif target == 'eccentricity':
            try:
                return self.eccentricity(g, weighted=False)
            except:
                return np.nan

        elif target == 'Y':
            return (
                c.eccentricity_weighted + c.eigenvector +\
                c.closeness + c.closeness_weighted + \
                c.eccentricity + c.eccentricity_weighted - 6) / 6 / len(
                    c.index)

        elif target == 'Xmy':
            return c.Y - c.X
        elif target == 'XpY':
            return c.Y + c.X

    def calc_metric(self, metric, metric_name, g, **kwargs):
        """Calculates an arbitrary metric"""
        return pd.DataFrame.from_dict(metric(g, **kwargs),
                                      orient='index').rename(columns={0: metric_name})


    #def compute_rank(self,col, order='ascending'):
    #    return col.rank(ascending=(order == 'ascending'))


    def compute_rank(self, col, order='ascending'):
        """Ranks the metrics"""
        u, v = np.unique(col if order == 'ascending' else -col, return_inverse=True)
        return (np.cumsum(np.bincount(v, minlength=u.size)) - 1)[v]


    def betweenness_centrality(self, g, weighted=True):
        """computes the given metric and returns it as a series"""
        _name = 'betweenness' + ('_weighted' if weighted else '')
        _d = self.calc_metric(nx.algorithms.centrality.betweenness_centrality,
                              _name, g, weight='weight' if weighted else None)
        _d[_name] = self.compute_rank(_d[_name], order='descending')
        return _d


    def degree_centrality(self, g, weighted=True):
        """computes the given metric and returns it as a series"""
        # TODO weight not yet taken into account, make own function
        _name = 'degree' + ('_weighted' if weighted else '')
        _d = self.calc_metric(nx.algorithms.centrality.degree_centrality,
                              _name, g)  # , weight='weight' if weighted else None)
        _d[_name] = self.compute_rank(_d[_name], order='descending')
        return _d


    def eigenvector_centrality(self, g, weighted=True):
        """computes the given metric and returns it as a series"""
        _name = 'eigenvector' + ('_weighted' if weighted else '')
        _d = self.calc_metric(nx.algorithms.centrality.eigenvector_centrality_numpy, _name, g,
                              weight='weight' if weighted else None)
        _d[_name] = self.compute_rank(_d[_name], order='descending')
        return _d


    def eccentricity(self, g, weighted=True):
        """computes the given metric and returns it as a series"""
        ### weight not yet taken into accoutn
        _name = 'eccentricity' + ('_weighted' if weighted else '')
        _d = self.calc_metric(nx.algorithms.distance_measures.eccentricity,
                              _name, g)  # , weight='weight' if weighted else None)
        _d[_name] = self.compute_rank(_d[_name], order='ascending')
        return _d


    def closeness(self, g, weighted=True):
        """computes the given metric and returns it as a series"""
        def calc2(metric, metric_name, g, distance='weight', **kwargs):
            return pd.DataFrame.from_dict(metric(g, distance=distance),
                                          orient='index').rename(columns={0: metric_name})

        _name = 'closeness' + ('_weighted' if weighted else '')
        _d = self.calc_metric(nx.algorithms.centrality.closeness.closeness_centrality, _name, g,
                              distance='weight' if weighted else None)
        _d[_name] = self.compute_rank(_d[_name], order='ascending')
        return _d

class GraphMaker(object):
    """Transforms a matrix panel into a networkx Graph.
       Parameters
       ----------
       matrix_panel: pd.Panel.-Items axis:list of edge metrics
                              -Major and minor axis: list of node labels
       node_data: pd.Dataframe: Index: Node labels.
                               columns: node metrics.
       threshold: Minimum absolute value for node matrix items.

       matrix_params: see  selectors.wranglers.MatrixParams

       graph_type: kind of transformation in ('full', 'mst', 'pmfg'])
      """
    def __init__(self, matrix_panel,
                 node_data,
                 inv=False,
                 threshold=0.0,
                 matrix_params=[('raw', None)],
                 graph_type='full',
                 target='exchange'):

        self.params = matrix_params
        self.panel = matrix_panel
        data = matrix_panel[target].copy()
        self.df_distance = self.calculate_graph_matrix(data,
                                                       matrix_params)
        self.G = self.create_graph(node_data,
                                   graph_type=graph_type,
                                   inv=inv,
                                   threshold=threshold)

    def add_node_info(self, g, key, pds):
        """Inserts the info from node_data into node attributes of the created graph
        """
        new_attributes = map(lambda x: (x[0], x[1]),
                             filter(lambda i: g.has_node(i[0]),
                                    pds.iteritems()
                                   )
                            )
        nx.set_node_attributes(g, key, dict(new_attributes))

    def raw(self, data, attrs=None):
        """Do nothing to the graph matrix"""
        return data

    def zscore(self, data, attrs=None):
        """Zscore the graph matrix"""
        return (data-data.mean())/data.std

    def scale(self, data, attrs):
        """Scale the matrix. Attrs:(min,max)"""
        m, M = attrs
        return ((M-m)*(data-data.min())) / (data.max()-data.min()) + m

    def compute_distance(self, correlation_matrix, attrs):
        """Converts correlation into a distance"""
        return np.sqrt(2 * np.clip(1. - correlation_matrix ** 2, 0., 2.))

    def clip(self, data, attrs):
        """Limit a given matrix between (min,max)"""
        m, M = attrs
        return np.clip(data, m, M)

    def calculate_graph_matrix(self, data, matrix_params):
        """Convert the input matrix into the graph matrix
        applying an arbitrary set of transforms
        """
        for name, attrs in matrix_params:
            func = getattr(self, name)
            data = func(data, attrs)
        return data

    def create_graph(self,
                     data,
                     graph_type='mst',
                     inv=False,
                     threshold=0.0):
        """Converts the calculated graph adjacency matrix into a networkx Graph
        """
        df_distance = self.df_distance
        matrix_panel = self.panel
        if graph_type == 'mst':
            G = self.construct_mst(df_distance, matrix_panel,
                                   inv=inv, threshold=threshold)
            for col in data.columns:
                self.add_node_info(G, col, data[col])
        elif graph_type == 'pmfg':
            G = self.construct_pmfg(df_distance, matrix_panel,
                                    inv=inv, threshold=threshold)
            for col in data.columns:
                self.add_node_info(G, col, data[col])
        else:
            G = self.construct_full_graph(df_distance, matrix_panel,
                                          inv=inv, threshold=threshold)
            for col in data.columns:
                self.add_node_info(G, col, data[col])
        return G

    def construct_full_graph(self, df_distance, matrix_panel, inv=False, threshold=0.0):
        """Creates a graph with the provided adjacency
            matrix inserting all the node and edge metrics into the graph
        """
        if inv:
            df_distance = 1.0/df_distance

        g = nx.Graph()
        names = df_distance.columns.unique()
        for name in names:
            g.add_node(name)

        for i, n in enumerate(names):
            for j, m in enumerate(names):
                if j >= i:
                    break
                val = df_distance.loc[n, m]
                if np.abs(val) > threshold / len(names):
                    edgedict = {'weight': float(val)}
                    for item in matrix_panel.items:
                        edgedict[item] = float(matrix_panel.ix[item, n, m])
                    g.add_edge(n, m, edgedict)
        labels = {}
        for i, n in enumerate(names):
            name = names[i]
            labels[i] = name
        g = nx.relabel_nodes(g, labels)
        return g

    def construct_mst(self, df_distance, matrix_panel, inv=False, threshold=0.0):
        """Trim the provided adjacency matrix to create a Minimum Spanning Tree
            matrix inserting all the node and edge metrics into the graph
        """
        if inv:
            df_distance = 1.0/df_distance
        g = nx.Graph()
        names = df_distance.columns.unique()
        for name in names:
            g.add_node(name)
        for i, n in enumerate(names):
            for j, m in enumerate(names):
                if j >= i:
                    break
                val = df_distance.loc[n, m]
                # Bonferroni correction: TODO check implementation
                if np.abs(val) > threshold / len(names):
                    edgedict = {'weight': float(val)}
                    for item in matrix_panel.items:
                        edgedict[item] = float(matrix_panel.ix[item, n, m])
                    g.add_edge(n, m, edgedict)
        return nx.minimum_spanning_tree(g)

    def construct_pmfg(self, df_distance, matrix_panel, inv=False, threshold=0.0):
        """Trim the provided adjacency matrix to create a Planary Maximum Filtered Graph
            matrix inserting all the node and edge metrics into the graph
        """
        if inv:
            dist_matrix = 1.0/df_distance.values
        else:
            dist_matrix = df_distance.values
        index_upper_triangular = np.triu_indices(dist_matrix.shape[0], 1)
        isort = np.argsort(dist_matrix[index_upper_triangular])
        G = nx.Graph()
        names = df_distance.columns.unique()

        for k in np.arange(0, len(isort)):
            u = index_upper_triangular[0][isort[k]]
            v = index_upper_triangular[1][isort[k]]
            if np.abs(dist_matrix[u, v]) > threshold / len(names): # optional bonferroni correction
                edgedict = {'weight': float(dist_matrix[u, v])}
                for item in matrix_panel.items:
                    edgedict[item] = float(matrix_panel.ix[item, u, v])
                G.add_edge(u, v, edgedict)
                if not planarity.is_planar(G):
                    G.remove_edge(u, v)
        labels = {}
        for i, n in enumerate(names):
            name = names[i]
            labels[i] = name
        G = nx.relabel_nodes(G, labels)
        return G

class GraphCalculator(object):
    """Handles everything to do with graph managing.
       Attributes:
       ----------
       matrix_panel: pd.Panel of edge metrics/data
       gp: GraphParams object used to feed its graph parameters
       mp: MatrixParams object used to manage its graph's adjacency matrix
       gm: GraphMaker object in charge of graphs related calculations
       widget: GUI for selecting all the params related to graph calculations
    """
    def __init__(self, matrix_panel,
                 node_metrics,
                 only_layout=False):
        self.matrix_panel = matrix_panel
        self.gp = sww.GraphParams()
        self.mp = sww.MatrixParams()
        self.mp.widget.margin = 6
        self.gm = GraphMaker(self.matrix_panel, node_data=node_metrics,
                             inv=self.gp.inverted.value,
                             threshold=self.gp.threshold.value,
                             matrix_params=self.mp.value,
                             graph_type=self.gp.graph_type.value,
                             target=self.gp.target_attr.value)
        self.G = self.gm.G
        self.layout = LayoutCalculator(self.G)
        self.layout.button.visible = False

        if not only_layout:
            self.node_metrics = node_metrics
            self.init = True
            self.update()
            self.init = False

        self.layout.params.widget.margin = 6
        self.layout.params.widget.padding = 6

        self.display = widgets.HTML(value=self.display_str('Select and click run'),
                                    height="50px", width="175px")

        self.calculate = widgets.Button(description='Calculate', padding=6)
        self.calculate.on_click(self.on_calculate_click)

        self.toggle_gp = widgets.ToggleButton(description='Creation',
                                              value=True, padding=6)
        self.toggle_gp.observe(self.on_toggp_change, names='value')

        self.toggle_mp = widgets.ToggleButton(description='Math',
                                              value=True, padding=6)
        self.toggle_mp.observe(self.on_togmp_change, names='value')

        self.toggle_layout = widgets.ToggleButton(description='Layout',
                                                  value=True, padding=6)
        self.toggle_layout.observe(self.on_toglay_change, names='value')

        self.buttonbox = widgets.HBox(children=[self.calculate, self.toggle_gp,
                                                self.toggle_mp, self.toggle_layout,
                                                self.display])

        title_html = '''<div class="graph-mtrans" style=" font-size:22px;
                                                        font-weight: bold; 
                                                        text-align:right;">
                                                        Graph Parameters</div>'''
        self.title = widgets.HTML(value=title_html)
        self.body = widgets.HBox(children=[self.gp.widget,
                                           self.mp.widget,
                                           self.layout.widget])
        self.widget = widgets.VBox(children=[self.title,
                                             self.body,
                                             self.buttonbox])

    def on_togmp_change(self, change):
        self.mp.widget.visible = self.toggle_mp.value

    def on_toggp_change(self, change):
        self.gp.widget.visible = self.toggle_gp.value

    def on_toglay_change(self, change):
        self.layout.params.widget.visible = self.toggle_layout.value

    def display_str(self, s):
        html = '''<div class="graph-gc"
                     style=" font-size:18px;
                            font-weight: bold; 
                            text-align:right;">'''+s+'''</div>'''
        return html

    def on_calculate_click(self, b):
        self.display.value = self.display_str('Calculating...')
        self.update()
        self.display.value = self.display_str('Ready. You can select again.')

    def update(self):
        if not self.init:
            self.gm = GraphMaker(self.matrix_panel,
                                 node_data=self.node_metrics,
                                 inv=self.gp.inverted.value,
                                 threshold=self.gp.threshold.value,
                                 matrix_params=self.mp.value,
                                 graph_type=self.gp.graph_type.value,
                                 target=self.gp.target_attr.value
                                )

        self.comp = CentralityComputer(self.gm.G)
        self.G, self.node = self.add_graph_node_attributes(self.gm.G,
                                                           self.comp.metrics.T.copy()
                                                          )
        self.node.loc[:, 'label'] = self.node.index.values
        self.node.loc[:, 'index'] = np.arange(len(self.node.index.values))
        self.G = self.add_graph_edge_attributes(self.G)
        self.edge = pd.Panel(self.G.edge).swapaxes(0, 1)
        self.layout.update(self.G)

    def add_node_info(self, G, key, pds):
        new_attributes = map(lambda x: (x[0], x[1]), filter(lambda i: G.has_node(i[0]),
                                                            pds.iteritems())
                            )
        nx.set_node_attributes(G, key, dict(new_attributes))

    def add_edge_info(self, G, key, data):
        for i, E in enumerate(G.edges()):
            u, v = E
            G.edge[u][v][key] = data.iloc[i]

    def add_graph_edge_attributes(self, G, func_list=None):
        if func_list is None:
            func_list = [nx.edge_betweenness_centrality, nx.edge_betweenness,
                         nx.edge_current_flow_betweenness_centrality]#,nx.eigenvector_centrality]
        columns = [f.__name__ for f in func_list]
        dft = pd.DataFrame(index=G.edges(), columns=columns).sort_index()
        for i, name in enumerate(columns):
            vals = func_list[i](G)
            values = list(vals.values())
            dft[name] = values
        for name in columns:
            self.add_edge_info(G, name, dft[name])
        return G

    def add_graph_node_attributes(self, G, metrics):
        for name in metrics.columns:
            self.add_node_info(G, name, metrics[name])
        return G, pd.DataFrame(G.node).T
