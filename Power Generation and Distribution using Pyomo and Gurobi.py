import pandas as pd
file1= pd.read_excel(r"C:\Users\Asus\Desktop\This\inputs.xlsx", sheet_name=0)
file2= pd.read_excel(r"C:\Users\Asus\Desktop\This\inputs.xlsx", sheet_name=1)

import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

model=pyo.ConcreteModel()
model.Pg= pyo.Var(range(0,5),bounds=(0,None))
Pg=model.Pg

pg_sum= (sum([Pg[i] for i in file1['id']]))

model.balance=pyo.Constraint(expr=pg_sum==file2['value'].sum())
model.cond=pyo.Constraint(expr=file2['value'][0]<=Pg[0]+Pg[3])
model.limits=pyo.ConstraintList()

for g in file1['id']:
    model.limits.add(expr=Pg[g]<=file1['limit'][g])
    
model.obj=pyo.Objective(expr=sum([Pg[g]*file1['cost'][g] for g in file1['id']]))
opt= SolverFactory('gurobi')
opt.solve(model)
model.pprint()

#[pyo.value(Pg[g] for g in file1['id'])]

list1=[]
for g in file1['id']:
    list1.append(pyo.value(Pg[g]))
    
file1["Vals"]=list1