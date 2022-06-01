# -*- coding: utf-8 -*-
"""
@author: Wangwei Kong

Part 2 of the investment model
"""
from __future__ import (division, print_function)
from pyomo.core import ConcreteModel, Constraint, minimize, NonNegativeReals, \
 Objective, Var, RangeSet, Binary, Set, Reals
from pyomo.environ import SolverFactory
from pyomo.core import value as Val
import json
import os
import math
import numpy as np
import copy
from SCACOPF import run_SCACOPF_jl, output2json, process_flex_result
from run_OPF_pp import ACOPF_function

from process_data import record_bra_from_pyo_result,record_bus_from_pyo_result, record_invest_from_pyo_result,record_investCost_from_pyo_result


def InvPt2_function(OPF_option,test_case,model,mpc, penalty_cost, NoCon, prob,DF, CRF, SF, NoSce,path_sce, S_ci, Cflex_pt1, Pflex_pt1,Qflex_pt1, ci_pt1,obj_pt1,multiplier_bus,):
    
    
    # run for the 24 h
    NoTime = 24 # Number of time points
    
    print("\n--> Part 2 of the investment model")


    def pt2_Pflex_rule(m,xb,xy,xsc,xse,xd,xt):
        return m.Pflex[xb,xy,xsc,xse,xd, xt] == Pflex_pt1[xy][xsc][xb]

    def pt2_Qflex_rule(m,xb,xy,xsc,xse,xd,xt):
        return m.Qflex[xb,xy,xsc,xse,xd,xt] == Qflex_pt1[xy][xsc][xb]



    # TODO: update obj2
    # New Objective function 
    def OFrule2(m):

        return (        # load curtailment cost
                        sum(  m.Plc[xb, xy,xsc, xse, xd,xt]*penalty_cost 
                            for xb in m.Set['Bus'] for xy,xsc in m.Set['YSce'] 
                            for xse in m.Set['Sea'] for xd in m.Set['Day'] for xt in m.Set['Tim'] ) +
                       
                        sum( m.Qlc[xb, xy,xsc, xse, xd,xt]*penalty_cost 
                            for xb in m.Set['Bus'] for xy,xsc in m.Set['YSce'] 
                            for xse in m.Set['Sea'] for xd in m.Set['Day'] for xt in m.Set['Tim'] ) +
                         
                        # pathway cost
                        sum(prob[xp] * m.Cpath[xp] for xp in m.Set['Path']) +
           
                        
                        # CO change
                        sum( CRF[xy] * DF[xy] * SF *
                                 (yearly_CO[xy][xsc] -
                                  
                                      sum( yearly_dual_Pbra[xy][xsc][xbr] *
                                            (
                                                sum( m.ci[xbr,xintv,xy, xsc]*S_ci[str(xbr)][xintv]  for xintv in model.Set["Intev"][xbr] ) 
                                                 - ci_pt1[xy][xsc][xbr]  ) 
                                          for xbr in m.Set['Bra']  )
                                    )
                              for xy,xsc in m.Set["YSce"] 
                              )
                        
                     
                )
    
                         
    def runACOPF(mpc, ci,Pflex,Qflex, multiplier_bus,penalty_cost,SF):
        # print("Run OPF ") 
       
        
        yearly_CO = [] #[xy][xsc] 
        yearly_dual_Pbra = [] #[xy][xsc][xbr]  
        
        # TODO:  run 24h ACOPF, remove contingency  
        # run ACOPF to get obj value for part 1
        for xy in model.Set["Year"]:
                       
            yearly_CO.append([])
            yearly_dual_Pbra.append([])
            
            for xsc in range(NoSce**xy):   
                mult = multiplier_bus[xy][xsc][0]
                
                yearly_CO[xy].append([])
                yearly_dual_Pbra[xy].append([])
                
                # output investment plans for each year each scnenaior
                output2json(mpc,ci[xy][xsc],Pflex[xy][xsc], Qflex[xy][xsc] )
                Pflex_up , Pflex_dn , Qflex_up ,Qflex_dn = process_flex_result(Pflex[xy][xsc], Qflex[xy][xsc] )
                
                # run ACOPF, get CO and duals for each year each scnenaior
    
                if OPF_option == "jl":
                    # run julia model
                    #TODO: get the yearly sum of CO and duals
                    CO, cos_pf, sin_pf, plc_result,plc_result_con, qlc_result, \
                        OPF_Pbra , OPF_Pbra_con ,OPF_Qbra, dual_Pbra,dual_Pbra_con, dual_Qbra, \
                            dual_Pbus,dual_Pbus_con , dual_Qbus,dual_Qbus_con = run_SCACOPF_jl(mpc, 0, penalty_cost)
                    
                if OPF_option == "pp":
                    # run pandapower model
                    CO, dual_Pbra = ACOPF_function(test_case,mpc, ci[xy][xsc],Pflex_up , Pflex_dn, mult,penalty_cost)
                    

                
                print('Year:',xy,', Scenario:', xsc,', CO:', CO)
                
                # TODO: update the scaling factor
                
                yearly_CO[xy][xsc] = CO 
                yearly_dual_Pbra[xy][xsc] = dual_Pbra
                
        return (yearly_CO, yearly_dual_Pbra )
    

    
            
    
    # fix flex power for pt2
    model.add_component("pt2_Pflex", Constraint(model.Set['Bus'],model.Set['YSce'] ,model.Set['Sea'], model.Set['Day'],model.Set['Tim'],rule=pt2_Pflex_rule ))
    model.add_component("pt2_Qflex", Constraint(model.Set['Bus'],model.Set['YSce'] ,model.Set['Sea'], model.Set['Day'],model.Set['Tim'],rule=pt2_Qflex_rule ))
    
    
    
            
    yearly_CO, yearly_dual_Pbra = runACOPF(mpc, ci_pt1,Pflex_pt1,Qflex_pt1, multiplier_bus, penalty_cost,SF)
     
    obj_pt1 += sum(yearly_CO[xy][xsc] for xy, xsc in model.Set["YSce"])
    
    
    # iteration
    obj_ref = obj_pt1
    ite_z = 0
    obj_change = True
    
    while obj_change:
        print("\n---- iteration: ", ite_z)
           
        
        # Change Obj based on outputs from ACOPF
        model.del_component(model.obj)
        model.obj = Objective(rule=OFrule2, sense=minimize)
        
        # solve pyomo model
        solver = SolverFactory('glpk')
        results = solver.solve(model)
        
        print ('solver termination condition: ', results.solver.termination_condition)
        print('min obj cost:',Val(model.obj))
        
        # new obj cost includes operation cost
        obj_pt2 =  Val(model.obj)
        
    
        # record new ci
        ci_pt2_update = record_invest_from_pyo_result(model, mpc,NoSce, model.ci, S_ci)   
        print( ci_pt2_update )
        
        # print( ci_pt2_update)
     
        # find the min obj cost
        if obj_pt2 >= obj_ref:
            
            obj_change = False
            
            CO_pt2 = sum(yearly_CO[xy][xsc] for xy, xsc in model.Set["YSce"])
            print(CO_pt2)
            
            
            
        else:
            # update obj cost 
            obj_ref = obj_pt2
            # rerun ACOPF with new investment plans
            # TODO:  run 24h ACOPF, remove contingency     
            
            yearly_CO, yearly_dual_Pbra = runACOPF(mpc, ci_pt2_update,Pflex_pt1,Qflex_pt1,multiplier_bus,penalty_cost,SF)
            
            CO_pt2 = sum(yearly_CO[xy][xsc] for xy, xsc in model.Set["YSce"])
            
            ite_z += 1 
            

    ciCost_pt2 = Val( sum( model.ciCost[xy,xsc] for xy,xsc in model.Set["YSce"] ) )       
    yearly_ciCost = record_investCost_from_pyo_result(model,mpc,NoSce, model.ciCost)
    
    # TODO: Check if still need 
    # flex invest check
    Cflex_pt2 = Cflex_pt1
    Pflex_pt2 = Pflex_pt1
    
    print("Part 2 finished")
    print( ci_pt2_update )
    
    return (model, CO_pt2, yearly_CO, ci_pt2_update, ciCost_pt2, yearly_ciCost, Cflex_pt2,Pflex_pt2)

