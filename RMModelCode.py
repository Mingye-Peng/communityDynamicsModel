#import packages
import os
import numpy as np
import pandas as pd
import scipy
import sklearn
import scipy.integrate as spint
from plotnine import *
import matplotlib.pyplot as plt

#defining the function
def RMSim(y,t0,b,a,e,s,d,w):
    #unpack state variables from list y
    H=y[0]
    P=y[1]
    #calculate changes in state variables
    dHdt=(b*H)*(1-a*H)-(w*P)*(H/(d+H))
    dPdt=(e*w*P)*(H/(d+H))-s*P
    #return lists containing changes in state variables with time
    return [dHdt,dPdt]
    
#define initial values for state variables
H0=500
P0=120
N0=[H0,P0]

#define parameters in dataframe
##define intial values make lists
b=0.8
a=0.001
e=0.07
s=0.2
d=400
w=5
##define multiple to reduce/increase parameters
m=1.5

b=[b,b/m,b*m,b,b,b,b,b,b,b,b,b,b]
a=[a,a,a,a/m,a*m,a,a,a,a,a,a,a,a]
e=[e,e,e,e,e,e/m,e*m,e,e,e,e,e,e]
s=[s,s,s,s,s,s,s,s/m,s*m,s,s,s,s]
d=[d,d,d,d,d,d,d,d,d,d/m,d*m,d,d]
w=[w,w,w,w,w,w,w,w,w,w,w,w/m,w*m]
##make lists to data frame and rearrange order of columns and make to list
parameters=pd.DataFrame({'b':b, 'a':a, 'e':e, 's':s, 'd':d, 'w':w})
parameters=parameters[['b','a','e','s','d','w']]
parameters=parameters.values.tolist()

#define time steps
times=np.arange(0,75,0.1)

#create data frame for function output and fill with time values in first column
modelOutput=pd.DataFrame(columns=["t", "H", "P", "bHlow", "bPlow", "bHhigh", "bPhigh", "aHlow", "aPlow", "aHhigh", "aPhigh", "eHlow", "ePlow", "eHhigh", "ePhigh", "sHlow", "sPlow", "sHhigh", "sPhigh", "dHlow", "dPlow", "dHhigh", "dPhigh", "wHlow", "wPlow", "wHhigh", "wPhigh"])
modelOutput.t=times

#Simulate the model
count=0
z=2
for item in parameters:
    #run siumulation with odeint and iterate over different sets of parameters
    modelSim=spint.odeint(func=RMSim,y0=N0,t=times,args=tuple(parameters[count]))

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
plot_d=ggplot(modelOutput,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="P"), color='red')+geom_line(aes(y="dHlow"), color='blue', linetype='dotted')+geom_line(aes(y="dPlow"), color='red', linetype='dotted')+geom_line(aes(y="dHhigh"), color='blue', linetype='dashed')+geom_line(aes(y="dPhigh"), color='red', linetype='dashed')+ggtitle("different d's")+ylab("count")+xlab("time")
plot_w=ggplot(modelOutput,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="P"), color='red')+geom_line(aes(y="wHlow"), color='blue', linetype='dotted')+geom_line(aes(y="wPlow"), color='red', linetype='dotted')+geom_line(aes(y="wHhigh"), color='blue', linetype='dashed')+geom_line(aes(y="wPhigh"), color='red', linetype='dashed')+ggtitle("different w's")+ylab("count")+xlab("time")

#Show Plots
print(plot_b)
print(plot_a)
print(plot_e)
print(plot_s)
print(plot_d)
print(plot_w)

###Paradox of Enrichment 
##define intial values make lists
b=0.8
e=0.07
s=0.2
d=400
w=5
a=[0.00125, .000125, .0002, .0003, .0005]



##make lists to data frame and rearrange order of columns and make to list
parameters=pd.DataFrame({'b':b, 'a':a, 'e':e, 's':s, 'd':d, 'w':w})
parameters=parameters[['b','a','e','s','d','w']]
parameters=parameters.values.tolist()

#define time steps
times=np.arange(0,75,0.1)

#create data frame for function output and fill with time values in first column
modelOutput=pd.DataFrame(columns=["t", "H", "P", "bHlow", "bPlow", "bHhigh", "bPhigh", "aHlow", "aPlow", "aHhigh", "aPhigh", "eHlow", "ePlow", "eHhigh", "ePhigh", "sHlow", "sPlow", "sHhigh", "sPhigh", "dHlow", "dPlow", "dHhigh", "dPhigh", "wHlow", "wPlow", "wHhigh", "wPhigh"])
modelOutput.t=times

#Simulate the model
#Simulate the model
count=0
z=2
for item in parameters:
    #run siumulation with odeint and iterate over different sets of parameters
    modelSim=spint.odeint(func=RMSim,y0=N0,t=times,args=tuple(parameters[count]))

    #convert output from array to data frame
    modelSim=pd.DataFrame(data=modelSim)
    
    #add results to Model Output data frame
    modelOutput.iloc[:, z-1]=modelSim[0]
    modelOutput.iloc[:, z]=modelSim[1]
    
    #add to iterative values
    count=count+1
    z=z+2
    #Graph Results
plot_a=ggplot(modelOutput,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="P"), color='red')+geom_line(aes(y="aHlow"), color='blue', linetype='dotted')+geom_line(aes(y="aPlow"), color='red', linetype='dotted')+geom_line(aes(y="aHhigh"), color='blue', linetype='dashed')+geom_line(aes(y="aPhigh"), color='red', linetype='dashed')+ggtitle("different a's")+ylab("count")+xlab("time")

#Show Plots
print(plot_a)