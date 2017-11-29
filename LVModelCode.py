#import packages
import os
import numpy as np
import pandas as pd
import scipy
import sklearn
import scipy.integrate as spint
from plotnine import *
from ggplot import *
import matplotlib.pyplot as plt

#defining the function
def LVSim(y,t0,b,a,e,s):
    #unpack state variables from list y
    H=y[0]
    P=y[1]
    #calculate changes in state variables
    dHdt=(b*H)-(a*P*H)
    dPdt=(e*a*P*H)-(s*P)
    #return lists containing changes in state variables with time
    return [dHdt,dPdt]
    
#define initial values for state variables
H0=25
P0=5
N0=[H0,P0]

#define parameters in dataframe
##define intial values make lists
b=0.5
a=0.02
e=0.1
s=0.2
##define multiple to reduce/increase parameters
m=1.5

b=[b,b/m,b*m,b,b,b,b,b,b]
a=[a,a,a,a/m,a*m,a,a,a,a]
e=[e,e,e,e,e,e/m,e*m,e,e]
s=[s,s,s,s,s,s,s,s/m,s*m]
##make lists to data frame and rearrange order of columns and make to list
parameters=pd.DataFrame({'b':b, 'a':a, 'e':e, 's':s})
parameters=parameters[['b','a','e','s']]
parameters=parameters.values.tolist()

#define time steps
times=np.arange(0,75,0.1)

#create data frame for function output and fill with time values in first column
modelOutput=pd.DataFrame(columns=["t", "H", "P", "bHlow", "bPlow", "bHhigh", "bPhigh", "aHlow", "aPlow", "aHhigh", "aPhigh", "eHlow", "ePlow", "eHhigh", "ePhigh", "sHlow", "sPlow", "sHhigh", "sPhigh"])
modelOutput.t=times

#Simulate the model
count=0
z=2
for item in parameters:
    #run siumulation with odeint and iterate over different sets of parameters
    modelSim=spint.odeint(func=LVSim,y0=N0,t=times,args=tuple(parameters[count]))

    #convert output from array to data frame
    modelSim=pd.DataFrame(data=modelSim)
    
    #add results to Model Output data frame
    modelOutput.iloc[:, z-1]=modelSim[0]
    modelOutput.iloc[:, z]=modelSim[1]
    
    #add to iterative values
    count=count+1
    z=z+2

#Graph Results
plot_b=ggplot(modelOutput,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="P"), color='red')+geom_line(aes(y="bHlow"), color='blue', linetype='dotted')+geom_line(aes(y="bPlow"), color='red', linetype='dotted')+geom_line(aes(y="bHhigh"), color='blue', linetype='dashed')+geom_line(aes(y="bPhigh"), color='red', linetype='dashed')+ggtitle("different b's")+ylab("count")+xlab("time")
plot_a=ggplot(modelOutput,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="P"), color='red')+geom_line(aes(y="aHlow"), color='blue', linetype='dotted')+geom_line(aes(y="aPlow"), color='red', linetype='dotted')+geom_line(aes(y="aHhigh"), color='blue', linetype='dashed')+geom_line(aes(y="aPhigh"), color='red', linetype='dashed')+ggtitle("different a's")+ylab("count")+xlab("time")
plot_e=ggplot(modelOutput,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="P"), color='red')+geom_line(aes(y="eHlow"), color='blue', linetype='dotted')+geom_line(aes(y="ePlow"), color='red', linetype='dotted')+geom_line(aes(y="eHhigh"), color='blue', linetype='dashed')+geom_line(aes(y="ePhigh"), color='red', linetype='dashed')+ggtitle("different e's")+ylab("count")+xlab("time")
plot_s=ggplot(modelOutput,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="P"), color='red')+geom_line(aes(y="sHlow"), color='blue', linetype='dotted')+geom_line(aes(y="sPlow"), color='red', linetype='dotted')+geom_line(aes(y="sHhigh"), color='blue', linetype='dashed')+geom_line(aes(y="sPhigh"), color='red', linetype='dashed')+ggtitle("different s's")+ylab("count")+xlab("time")

#Show Plots
plot_b.show()
plot_a.show()
plot_e.show()
plot_s.show()