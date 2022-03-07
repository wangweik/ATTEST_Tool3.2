# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 14:24:19 2021

@author: p96677wk

DC OPF 
"""

from __future__ import (division, print_function)
from pyomo.core import ConcreteModel, Constraint, minimize, NonNegativeReals, \
 Objective, Var,  Binary, Set, Reals
from pyomo.environ import SolverFactory
from pyomo.core import value as Val
import networkx as nx
import pyomo.environ as pyo

import json
import os
import math
import numpy as np

# import data class for network information
from a_network_dataclass import network_variable, network_parameter, nodes_info_network

# read paras and vars from mpc (.json)
from a_readVarPara import readVarPara

# ####################################################################
    
def DCOPF_function(mpc,NoTime):
    
            
    '''Network model to record var and para in graph and get values from node'''
    class NetworkModel():
        def __init__(self):
            self.readVarPara = readVarPara(mpc,network_parameter,network_variable)
            self.network_parameters = self.readVarPara[0] # nw_parameters
            self.network_variables = self.readVarPara[1]  # nw_variables
            self._create_graph()
            
            
        def _create_nodes_graph(self):
               nodes_graph = []
               exist = False
               counter = 0
               
               # Creating list of nodes  and adding parameters
               for parameter in self.network_parameters:
                     if nodes_graph:
                         for node_g in nodes_graph:
                             if node_g.ID == parameter.ID:
                                 exist = True
                                 node_g.parameters.append(parameter)
                                 break
                     if not exist:
                         node = nodes_info_network() 
                         node.node = counter
                         node.type = parameter.type
                         node.sub_type = parameter.sub_type
                         node.ID = parameter.ID
                         node.parameters = [parameter]
                         node.bus = parameter.bus
                         node.ends = parameter.ends
                         counter += 1
                         nodes_graph.append(node)
                     exist = False
    
               # Adding variables to nodes 
               for variable in self.network_variables:
                   for node_g in nodes_graph:
                       if node_g.ID == variable.ID:
                           if node_g.variables:
                               node_g.variables.append(variable)
                           else:
                               node_g.variables = [variable]
                           break
        
               # Adding nodes to graph
               for node_g in nodes_graph:
                   self.network.add_node(node_g.node, obj=node_g)
        
        
        def _create_edges_graph(self):
            # Creating branches of graph
            branches_graph = []
            for node_g in self.network.nodes(data=True):
                if node_g[1]['obj'].type == "generator":
                    for aux in self.network.nodes(data=True):
                        if aux[1]['obj'].type == "bus" and node_g[1]['obj'].bus == aux[1]['obj'].bus:
                            branches_graph.append([aux[1]['obj'].node, node_g[1]['obj'].node])
                            break
                elif node_g[1]['obj'].type == "branch":
                    flag = [False, False]
                    for aux in self.network.nodes(data=True):
                        if aux[1]['obj'].type == "bus" and node_g[1]['obj'].ends[0] == aux[1]['obj'].bus:
                            branches_graph.append([aux[1]['obj'].node, node_g[1]['obj'].node])
                            flag[0] = True
                        elif aux[1]['obj'].type == "bus" and node_g[1]['obj'].ends[1] == aux[1]['obj'].bus:
                            branches_graph.append([node_g[1]['obj'].node, aux[1]['obj'].node])
                            flag[1] = True
                        if flag[0] and flag[1]:
                            break
            self.branches_graph = branches_graph
            for branches in  branches_graph:
                self.network.add_edge(branches[0], branches[1])
        
        
        def _create_graph(self):
            self.network = nx.MultiGraph()
            self._create_nodes_graph()
            self._create_edges_graph()
            
            
        
    
    
        def get_value_network(self, ID=None, name=None, position_tree=None, hour=None, typ=None):
                ''' This function retrieves the values of variables and parameters
        
                    Parameters
                    ----------
                    Mandatory:\\
                    ID              :   Unique ID of the network element\\
                    name            :   Name of variable or parameter to be retrieved\\
                    position_tree   :   Dictionary containing information of the location of the information
                                        in relation with the energy tree. If the value does not vary with
                                        the energy tree then this value should be left in None\\
                    hour            :   integer that indicates the specific hour of the requested data. If
                                        the data does not change in time then this input must be left in
                                        None\\
                    typ             :   This refers to the type of element to be retrieved. This value
                                        can be either "variable" or "parameter". Other values will not
                                        be accepted
                '''
                if not position_tree:
                    for node in self.network.nodes(data=True):
                        if node[1]['obj'].ID == ID and typ == "parameter":
                            for parameter in node[1]['obj'].parameters:
                                if parameter.name == name and (not hour or hour == parameter.hour):
                                    return parameter.value
                        if node[1]['obj'].ID == ID and typ == "variable":
                            for variable in node[1]['obj'].variables:
                                if variable.name == name and (not hour or hour == variable.hour):
                                    return variable.value
                else:
                    number_node = self._get_initial_tree_node(position_tree)
                    return self._calculate_value_tree(number_node, ID, position_tree, hour, typ, False)
        
                return None
     
    
    
    # ####################################################################
    
    
    '''optimization (pyomo) model'''
    
    #  Sets 
    def addSet(m):
        m.Set={}
        ''' Add pyomo sets '''
        m.Set['Bra'] = range(mpc['NoBranch'])
        m.Set['Bus'] = range(mpc['NoBus'])
        m.Set['Gen'] = range(mpc['NoGen'])
        m.Set['Tim'] = range(NoTime) #range(24)
        #m.zset = range(3) # piece wise generator cost
    
        return m
    
    
    #   Parameters 
    def addPara(m):
        m.para={}
    
        for node in NetworkModel.network.nodes(data=True):
            for NoPar in range(len(node[1]['obj'].parameters)):  
                m.para [node[1]['obj'].ID + str('_') + node[1]['obj'].parameters[NoPar].name ] \
                    = node[1]['obj'].parameters[NoPar].value
       
        return m
    
        
    
     
    # Var          
    def addVar(m):
      
        # Gen
        m.Pgen = Var(m.Set['Gen'],m.Set['Tim'], domain=Reals, initialize=0)
        m.Cgen = Var(m.Set['Gen'],m.Set['Tim'], domain=Reals, initialize=0)
#
        # Branch
        m.Pbra = Var(m.Set['Bra'], m.Set['Tim'], domain=Reals, initialize=0) # Branch power flow
        #m.ICbra = Var(m.Set['Bra'], m.Set['Tim'], domain=NonNegativeReals, initialize=0) # invest capacity
        
        # Bus angle
        m.Ang = Var(m.Set['Bus'], m.Set['Tim'], bounds=(-2*math.pi, 2*math.pi), initialize=0) # from 0
        
        # Load curtailment
        m.Plc = Var(m.Set['Bus'], m.Set['Tim'], domain=NonNegativeReals, initialize=0)
        
        return m
         
    
    class rules:
    
        # Gen output constraint rules
        def genMax_rule(m, xg, xt):
            pmax=[]
            for node in NetworkModel.network.nodes(data=True):
                if node[1]['obj'].type == "generator":
                    pmax.append( node[1]['obj'].parameters[0].value)
            return m.Pgen[xg,xt] <= pmax[xg]  # Gpout<=Pmax
            del pmax
        
        def genMin_rule(m,xg,xt):
            pmin=[]
            for node in NetworkModel.network.nodes(data=True):
                if node[1]['obj'].type == "generator":
                    pmin.append( node[1]['obj'].parameters[1].value)
            return m.Pgen[xg,xt] >= pmin[xg]  # Gpout>=Pmin
            del pmin
        
        
        # Branch constraint
        # DC power flow
        def DCPF_rule(m, xbr,xt):
            br_X=[]
            fbus = []
            tbus = []
            pu2value = mpc['bus']['BASE_KV'][0]**2 / mpc['baseMVA']
            for node in NetworkModel.network.nodes(data=True):
                if node[1]['obj'].type == "branch":
                    fbus.append ( node[1]['obj'].ends[0] -1 )
                    tbus.append ( node[1]['obj'].ends[1] -1 )
                    br_X.append ( node[1]['obj'].parameters[2].value/100 )
            
            return  m.Pbra[xbr,xt] == ( m.Ang[fbus[xbr],xt] - m.Ang[tbus[xbr],xt]) / br_X[xbr]
        
        
        def slackBus_rule(m,xt):
            for i in range(mpc['NoBus']):
                if mpc['bus']['BUS_TYPE'][i] == 3:
                    slc_bus = i
            
            return m.Ang[slc_bus,xt] == 0
        
    
            # Branch capacity 
        def braCapacity_rule(m,xbr,xt):
            noDiff = mpc['NoGen'] + mpc['NoBus'] # change node number to branch number
            if NetworkModel.network._node[xbr + noDiff]['obj'].parameters[3].value != 0:
                return  m.Pbra[xbr,xt] <= NetworkModel.network._node[xbr + noDiff]['obj'].parameters[3].value #\
            else:
                return  m.Pbra[xbr,xt] <= float('inf')
    
        # both flow directions
        def braCapacityN_rule(m,xbr,xt):
            noDiff = mpc['NoGen'] + mpc['NoBus'] # change node number to branch number
            if NetworkModel.network._node[xbr + noDiff]['obj'].parameters[3].value != 0:
                return  -m.Pbra[xbr,xt] <=   NetworkModel.network._node[xbr + noDiff]['obj'].parameters[3].value #\
            else:
                return  -m.Pbra[xbr,xt] <= float('inf')
        
        
    
        # Nodal power balance
        def nodeBalance_rule(m, xb,xt):
            
            noDiff = nodeConnections[0]
            genCbus = nodeConnections[1]
            braFbus = nodeConnections[2]
            braTbus = nodeConnections[3]
            Pd = nodeConnections[4]
    
            return sum( m.Pgen[genCbus[xb][i],xt]  for i in range(len(genCbus[xb])) )  \
                    + sum( m.Pbra[braTbus[xb][i]-noDiff,xt]  for i in range(len(braTbus[xb])) )  \
                    == sum( m.Pbra[braFbus[xb][i]-noDiff,xt]  for i in range(len(braFbus[xb])) ) \
                      + Pd[xb][xt] - m.Plc[xb,xt]
    
    
        
        # # Cost Constraints
        # Piece wise gen cost: Number of piece = 3
        def pwcost_rule(m,xg,xt):
            if Val(m.Pgen[xg,xt]) <= xval[1][xg]:
                return m.Cgen[xg,xt] == m.Pgen[xg,xt] * lcost[0][xg]
            else:
                if Val(m.Pgen[xg,xt]) <= xval[2][xg]:
                    return m.Cgen[xg,xt] == m.Pgen[xg,xt] * lcost[1][xg]
                else:
                    return m.Cgen[xg,xt] == m.Pgen[xg,xt] * lcost[2][xg]
            
        
        
        
        
    
              
    def addConstraints(m):
        
        # Add Gen constraint rules
        m.genMax = Constraint( m.Set['Gen'], m.Set['Tim'], rule=rules.genMax_rule )
        m.genMin = Constraint( m.Set['Gen'], m.Set['Tim'], rule=rules.genMin_rule )
       
        # piecve wise gen cost
        m.pwcost = Constraint(m.Set['Gen'],  m.Set['Tim'], rule=rules.pwcost_rule)
        
        # Add branch flow DC OPF
        m.DCPF = Constraint( m.Set['Bra'], m.Set['Tim'], rule=rules.DCPF_rule ) 
        
        # Set slack bus angle to 0
       # m.slackBus = Constraint( m.Set['Tim'], rule=rules.slackBus_rule ) 
        
        
        # Add branch capacity constraints
        m.braCapacity = Constraint( m.Set['Bra'], m.Set['Tim'], rule=rules.braCapacity_rule )
        m.braCapacityN = Constraint( m.Set['Bra'], m.Set['Tim'], rule=rules.braCapacityN_rule )
        
    
        # Add nodal balance constraint rules
        m.nodeBalance = Constraint( m.Set['Bus'],m.Set['Tim'], rule=rules.nodeBalance_rule )    
    
        return m
      
    
    # Objective function 
    def OFrule(m):
    
        # investment cost: £200/MVA #TODO: update the cost
        return (        # investment cost
                       # sum(m.ICbra[xbr,xt]*1e-5 for xbr in m.Set['Bra'] for xt in m.Set['Tim'] ) +
                        # generation cost
                        sum( m.Cgen[xg,xt] for xg in m.Set['Gen'] for xt in m.Set['Tim'] ) +
                        # load curtailment cost
                        sum( m.Plc[xb,xt]*1e3 for xb in m.Set['Bus'] for xt in m.Set['Tim'])
                
                )
    
    
    
    # piece wise gen cost
    def genCost_rule(xLen=0):
            # Define piece wise cost curve approximation 
            LGcost = []
            xval = np.zeros((4,mpc['NoGen']), dtype=float)
            yval = np.zeros((4,mpc['NoGen']), dtype=float)
            lcost = np.zeros((3, mpc['NoGen']), dtype=float)
            
            for NoGen in range(mpc['NoGen']):
                if mpc['gencost']['MODEL'][NoGen] == 1:          # Piece-wise model
                    NoPieces = mpc['gencost']['NCOST'][NoGen]
                    xval = np.zeros(NoPieces, dtype=float)
                    yval = np.zeros(NoPieces, dtype=float)
                    xp = 0
                    for x in range(NoPieces):
                        xval[x] = mpc['gencost']['COST'][xp]
                        yval[x] = mpc['gencost']['COST'][xp+1]
                        xp += 2
                    # Convert to LP constraints 
                    for xv in range(NoPieces):
                        lcost[xv][NoGen] = (yval[xv+1][NoGen]-yval[xv][NoGen]) / (xval[xv+1][NoGen] - xval[xv][NoGen])
         
                
                else:                                                 # Polinomial model
                    # Select number of pieces for the approximation
                    if xLen == 0:  # Default case
                        
                        Delta = mpc['gen']['PMAX'][NoGen]
                        
                        
                        if Delta == 0:
                            lcost[0][NoGen]=1
                            lcost[1][NoGen]=1
                            lcost[2][NoGen]=1
                        else:
                            Delta /= 3
                       
                            NoPieces = int(np.floor(mpc['gen']['PMAX'][NoGen]/Delta))
                            
                            
                            aux = mpc['gen']['PMIN'][NoGen]
                            
                                
                            for xp in range(NoPieces+1):
                                xval[xp][NoGen] = aux
                                xc = mpc['gencost']['NCOST'][NoGen]-1 
                                yval[xp][NoGen] = mpc['gencost']['COST'][NoGen][xc]
                                for x in range(1, mpc['gencost']['NCOST'][NoGen]):
                                    xc -= 1
                                    yval[xp][NoGen] += mpc['gencost']['COST'][NoGen][xc]*xval[xp][NoGen]**x
                                aux += Delta
            
                            # Convert to LP constraints 
                            for xv in range(NoPieces):
                                lcost[xv][NoGen] = (yval[xv+1][NoGen]-yval[xv][NoGen]) / (xval[xv+1][NoGen] - xval[xv][NoGen])
                
                            
                            # lcost = [ k1  y0-k1*x0
                            #           k1  y0-k1*x0
                            #           k1  y0-k1*x0  ]
                            
                            LGcost.append(lcost[1][0])  
                    
            return  (lcost, xval,yval)
    
    # find all connections
    def nodeConnections_rule():
        # Node recorded: gen + bus + branch
        # Node numbers : mpc['NoGen'] + mpc['NoBus'] + mpc['NoBranch']
        # gen from node: 0
        #     to   node: (mpc['NoGen'] - 1)
        # bus from node: (mpc['NoGen'] )
        #     to   node: (mpc['NoGen'] + mpc['NoBus'] - 1)
        # bra from node: (mpc['NoGen'] + mpc['NoBus'])
        #     to   node: (mpc['NoGen'] + mpc['NoBus'] + mpc['NoBranch'] -1)
         
        noDiff = mpc['NoGen'] + mpc['NoBus'] # change node number to branch number
        
        genCbus = {} # all the generators connected to each bus
        braFbus = {} # all the branches from each bus
        braTbus = {} # all the branches to each bus
        for NoBus in range(mpc['NoBus']):
            genCbus[NoBus] = []
            braFbus[NoBus] = []
            braTbus[NoBus] = []
      
    
        for connect in range(len(NetworkModel.branches_graph)):
            for node in NetworkModel.network.nodes(data=True): 
                if node[1]['obj'].type == "generator" :
                    if node[1]['obj'].node == NetworkModel.branches_graph[connect][0] \
                        or node[1]['obj'].node == NetworkModel.branches_graph[connect][1]:
                        
                        NoBus = node[1]['obj'].bus - 1
                        genCbus[NoBus].append (node[1]['obj'].node)
                
                elif node[1]['obj'].type == "branch" :
                    if node[1]['obj'].node == NetworkModel.branches_graph[connect][1]:
                        NoBus = node[1]['obj'].ends[0] - 1
                        braFbus[NoBus].append (node[1]['obj'].node)
                    
                    elif node[1]['obj'].node == NetworkModel.branches_graph[connect][0]:
                        NoBus = node[1]['obj'].ends[1] - 1
                        braTbus[NoBus].append (node[1]['obj'].node)
                        
        
        
        Pd={}
        for xn in range(mpc['NoBus']):
            Pd[xn] = []
            
            
        if NoTime == 1:
    
            for xn in range(mpc['NoBus']):
                Pd[xn].append( mpc['bus']['PD'][xn])
        
        else :
          
            demP = np.zeros(NoTime, dtype=float) 
            for xn in range(mpc['NoBus']):
                
                if mpc['bus']['PD'][xn] != 0:          
                    for xt in range(NoTime): 
                        demP[xt] = mpc['demandP'][str(xt)][xn]
                        Pd[xn].append(demP[xt])
                else:
                    for xt in range(NoTime): 
                        demP[xt] = 0
                        Pd[xn].append(demP[xt])
    
                
            
        return (noDiff, genCbus, braFbus, braTbus, Pd)
    
    
    
    ###############################################################################################
    ###############################################################################################   
    ###############################################################################################
    ###############################################################################################
    
    '''
    
        Main function starts here
        
    '''
    
    
    
    # # Number of time points
    # NoTime = 2
    
    # # load json file from file directory
    # mpc = json.load(open(os.path.join(os.path.dirname(__file__), 
    #                                   'tests', 'json', 
    #                                   'Transmission_Network_UK2.json')))    # Transmission_Network_UK2.json
    
    # """  change load in mpc """
    # for tempi in range(30): #[21,22]: #
    #     for i in range(NoTime):
    #         mpc["demandP"][str(i)][tempi] = mpc["demandP"][str(i)][tempi]*100
       
    
    
    # build network model use graph
    NetworkModel = NetworkModel()
    
    
    
    # read mpc file and find info, define gen cost
    genCost = genCost_rule()
    lcost = genCost[0]
    xval = genCost[1]
    yval = genCost[2]
    
    nodeConnections = nodeConnections_rule()
    
    
    ''' Build a pyomo model '''
    
    # Defining concrete optimisation model
    model = ConcreteModel()
    model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT_EXPORT)
    # Adding sets
    model = addSet(model)
    
    # Adding parameters
    model = addPara(model)
    
    # Adding variables
    model = addVar(model)
    
    # Adding constraints
    model = addConstraints(model)
    
    # Adding objective function
    model.obj = Objective(rule=OFrule, sense=minimize)
    
    # def test_rule(model,xt):
    #         return model.Pgen[0,0] >= 400 #139-183
    # model.test = Constraint(  rule=test_rule )
    
    
    # solve pyomo model
    solver = SolverFactory('glpk')
    results = solver.solve(model)
    # solver.solve(model)
    
    
    
    
   #  ''' Print results '''
    
   # # print('min obj cost:',Val(model.obj))
   
   #  print('min obj cost:',Val(model.obj))
   #  print("generation cost:", Val(sum( model.Cgen[xg,xt].value for xg in model.Set['Gen'] for xt in model.Set['Tim'] )))
   #  print("lc cost: ", Val(sum( model.Plc[xb,xt]*1e3 for xb in model.Set['Bus'] for xt in model.Set['Tim'])))
        
    
  
    plc_result=[]
    dual_bus=[]
    for xb in range(mpc['NoBus']):
        temp = []
        for xt in range(NoTime):
            temp.append( Val(model.Plc[xb,xt]) )
            dual_bus.append( model.dual[model.nodeBalance[xb,xt]])
            
        plc_result.append( max(temp) )
        if plc_result[xb] > 0:
           print('Load curtailment of '+ str(plc_result[xb])+" at bus "+str(xb) )

            
            
           # print("nodal price (dual variable) on bus "+str(xb)+" : "+str(dual_bus[xb]))
    
    
    
    dual_bra=[]
    for xb in range(mpc['NoBranch']):
        for xt in range(NoTime):
            
            
            if model.dual[model.braCapacity[xb,xt]] == 0:
                if model.dual[model.braCapacityN[xb,xt]]== 0:
                    dual_bra.append(0)
                else:
                    dual_bra.append(-1*model.dual[model.braCapacityN[xb,xt]])
            else:
                if model.dual[model.braCapacity[xb,xt]] == 0:
                    dual_bra.append(0)
                else:
                    dual_bra.append(-1*model.dual[model.braCapacity[xb,xt]])
            
           # print(model.dual[model.braCapacity[xb,xt]])
            #print(model.dual[model.braCapacityN[xb,xt]])
    
    # print("nodal price")
    # for xb in range(mpc["NoBus"]):
    #     for xt in range(NoTime):
    #         print (model.dual[model.nodeBalance[xb,xt]])
    # print("dual branch")
    # print(dual_bra)
            
    # print("Gen output:")
    # model.Pgen.pprint()  
    # model.Pbra.pprint()      

    return (Val(model.obj), plc_result, dual_bra, model.Pbra)