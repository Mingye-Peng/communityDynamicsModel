######################################################################
### Code for Biocomputing Final Project
### Stability of Predator-Prey Dynamics
### Authors: Brittni Bertolet, Josh Hobgood, Aaron Long, Om Neelay

#Import packages
import os
import numpy as np
import pandas as pd
import scipy
import sklearn
import scipy.integrate as spint
from plotnine import *

######################################################################
#Part 1 - Lotka Volterra Model
#Define a custom function for Lotka Volterra model
def LVSim(y,t0,b,a,e,s):
    #unpack state variables from list y
    H=y[0]
    P=y[1]
    #calculate changes in state variables
    dHdt=(b*H)-(a*P*H)
    dPdt=(e*a*P*H)-(s*P)
    #return lists containing changes in state variables with time
    return [dHdt,dPdt]

#Simulate model dynamics with one set of parameter values
##define initial values for state variables
H0=25; P0=5; N0=[H0,P0]
##define parameters
b=0.5; a=0.02; e=0.1; s=0.2
##put parameters in tuple
params=(b,a,e,s)
#define time steps
times=np.arange(0,75,0.1)
##simulate
modelSim=spint.odeint(func=LVSim,y0=N0,t=times,args=params)
##put output in a dataframe with time
modelSim=pd.DataFrame(data=modelSim)
modelSim['t']=times
modelSim.columns=["H", "P", "t"]

#Plot dynamics
LV_plot=ggplot(modelSim, aes(x="t"))+geom_line(aes(y="H"), color="blue")+geom_line(aes(y="P"), color="red")+theme_bw()+xlab("Time")+ylab("Count")+ggtitle("Initial Parameter Values")
print(LV_plot)

#Simulate model dynamics, changing one parameter at a time 
##define multiple to reduce/increase parameters
m=1.5
##make list of each parameter and whether or not it changes
b=[b,b/m,b*m,b,b,b,b,b,b]
a=[a,a,a,a/m,a*m,a,a,a,a]
e=[e,e,e,e,e,e/m,e*m,e,e]
s=[s,s,s,s,s,s,s,s/m,s*m]
##put lists into a data frame, rearrange order of columns, and make to list
parameters=pd.DataFrame({'b':b, 'a':a, 'e':e, 's':s})
parameters=parameters[['b','a','e','s']]
parameters=parameters.values.tolist()
##create seperate data frames for output of H and P for each iteration
modelH_Output=pd.DataFrame(columns=["t", "H", "bHlow", "bHhigh", "aHlow", "aHhigh", "eHlow", "eHhigh", "sHlow", "sHhigh"])
modelP_Output=pd.DataFrame(columns=["t", "P", "bPlow", "bPhigh", "aPlow", "aPhigh", "ePlow", "ePhigh", "sPlow", "sPhigh"])
##fill time values in first column
modelH_Output.t=times
modelP_Output.t=times

##simulate model dynamics using a for loop
for i in range(0,len(parameters)):
    #set paramters for the iteration
    params=parameters[i]
    #run siumulation with odeint
    modelSim=spint.odeint(func=LVSim,y0=N0,t=times,args=tuple(params))
    #convert output from array to data frame
    modelSim=pd.DataFrame(data=modelSim)
    #add results to model output data frame
    modelH_Output.iloc[:, i+1]=modelSim[0]
    modelP_Output.iloc[:, i+1]=modelSim[1]

##graph results manually from model output 
###plot of prey counts vs time, in which only paramter b is changing -- solid: initial b value, dotted: lower b value, dashed: higher b value
LVplot_Hb=ggplot(modelH_Output,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="bHlow"), color='blue', linetype='dotted')+geom_line(aes(y="bHhigh"), color='blue', linetype='dashed')+ggtitle("Different b values")+ylab("Prey counts")+xlab("Time")+theme_bw()
###plot of predator counts vs time, in which only paramter b is changing -- solid: initial b value, dotted: lower b value, dashed: higher b value
LVplot_Pb=ggplot(modelP_Output,aes(x="t"))+geom_line(aes(y="P"), color='red')+geom_line(aes(y="bPlow"), color='red', linetype='dotted')+geom_line(aes(y="bPhigh"), color='red', linetype='dashed')+ggtitle("Different b values")+ylab("Predator counts")+xlab("Time")+theme_bw()
###same as above, now only parameter a is changing
LVplot_Ha=ggplot(modelH_Output,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="aHlow"), color='blue', linetype='dotted')+geom_line(aes(y="aHhigh"), color='blue', linetype='dashed')+ggtitle("Different a values")+ylab("Prey counts")+xlab("Time")+theme_bw()
LVplot_Pa=ggplot(modelP_Output,aes(x="t"))+geom_line(aes(y="P"), color='red')+geom_line(aes(y="aPlow"), color='red', linetype='dotted')+geom_line(aes(y="aPhigh"), color='red', linetype='dashed')+ggtitle("Different a values")+ylab("Predator counts")+xlab("Time")+theme_bw()
###same as above, now only parameter e is changing
LVplot_He=ggplot(modelH_Output,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="eHlow"), color='blue', linetype='dotted')+geom_line(aes(y="eHhigh"), color='blue', linetype='dashed')+ggtitle("Different e values")+ylab("Prey counts")+xlab("Time")+theme_bw()
LVplot_Pe=ggplot(modelP_Output,aes(x="t"))+geom_line(aes(y="P"), color='red')+geom_line(aes(y="ePlow"), color='red', linetype='dotted')+geom_line(aes(y="ePhigh"), color='red', linetype='dashed')+ggtitle("Different e values")+ylab("Predator counts")+xlab("Time")+theme_bw()
###same as above, now only parameter s is changing
LVplot_Hs=ggplot(modelH_Output,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="sHlow"), color='blue', linetype='dotted')+geom_line(aes(y="sHhigh"), color='blue', linetype='dashed')+ggtitle("Different s values")+ylab("Prey counts")+xlab("Time")+theme_bw()
LVplot_Ps=ggplot(modelP_Output,aes(x="t"))+geom_line(aes(y="P"), color='red')+geom_line(aes(y="sPlow"), color='red', linetype='dotted')+geom_line(aes(y="sPhigh"), color='red', linetype='dashed')+ggtitle("Different s values")+ylab("Predator counts")+xlab("Time")+theme_bw()
###Show all plots
print(LVplot_Hb); print(LVplot_Pb) 
print(LVplot_Ha); print(LVplot_Pa)
print(LVplot_He); print(LVplot_Pe)
print(LVplot_Hs); print(LVplot_Ps)

######################################################################
#Part 2 - Rosenzweig-MacArthur Model
#Define a custom function for Rosenzweig-MacArthur model
def RMSim(y,t0,b,a,e,s,d,w):
    #unpack state variables from list y
    H=y[0]
    P=y[1]
    #calculate changes in state variables
    dHdt=(b*H)*(1-a*H)-(w*P)*(H/(d+H))
    dPdt=(e*w*P)*(H/(d+H))-s*P
    #return lists containing changes in state variables with time
    return [dHdt,dPdt]

#Simulate model dynamics with one set of parameter values
##define initial values for state variables
H0=500; P0=120; N0=[H0,P0]
##define parameters
b=0.8; a=0.001; e=0.07; s=0.2; d=400; w=5
##put parameters in tuple
params=(b,a,e,s,d,w)
##define time steps
times=np.arange(0,75,0.1)
##simulate
modelSim=spint.odeint(func=RMSim,y0=N0,t=times,args=params)
##put output in a dataframe with time
modelSim=pd.DataFrame(data=modelSim)
modelSim['t']=times
modelSim.columns=["H", "P", "t"]

#Plot dynamics
RM_plot=ggplot(modelSim, aes(x="t"))+geom_line(aes(y="H"), color="blue")+geom_line(aes(y="P"), color="red")+theme_bw()+xlab("Time")+ylab("Count")+ggtitle("Initial Parameter Values")
print(RM_plot)

#Simulate model dynamics, changing one parameter at a time 
##define multiple to reduce/increase parameters
m=1.5
##make list of each parameter and whether or not it changes
b=[b,b/m,b*m,b,b,b,b,b,b,b,b,b,b]
a=[a,a,a,a/m,a*m,a,a,a,a,a,a,a,a]
e=[e,e,e,e,e,e/m,e*m,e,e,e,e,e,e]
s=[s,s,s,s,s,s,s,s/m,s*m,s,s,s,s]
d=[d,d,d,d,d,d,d,d,d,d/m,d*m,d,d]
w=[w,w,w,w,w,w,w,w,w,w,w,w/m,w*m]
##put lists into a data frame
parameters=pd.DataFrame({'b':b, 'a':a, 'e':e, 's':s, 'd':d, 'w':w})
##rearrange order of columns
parameters=parameters[['b','a','e','s','d','w']]
##make into a list
parameters=parameters.values.tolist()
##create seperate data frames for output of H and P for each iteration
modelH_Output=pd.DataFrame(columns=["t", "H", "bHlow", "bHhigh", "aHlow", "aHhigh", "eHlow", "eHhigh", "sHlow", "sHhigh", "dHlow", "dHhigh", "wHlow", "wHhigh"])
modelP_Output=pd.DataFrame(columns=["t", "P", "bPlow", "bPhigh", "aPlow", "aPhigh", "ePlow", "ePhigh", "sPlow", "sPhigh", "dPlow", "dPhigh", "wPlow", "wPhigh"])
##fill time values in first column
modelH_Output.t=times
modelP_Output.t=times
##simulate model dynamics using a for loop
for i in range(0,len(parameters)):
    #set paramters for the iteration
    params=parameters[i]
    #run siumulation with odeint
    modelSim=spint.odeint(func=RMSim,y0=N0,t=times,args=tuple(params))
    #convert output from array to data frame
    modelSim=pd.DataFrame(data=modelSim)
    #add results to model output data frame
    modelH_Output.iloc[:, i+1]=modelSim[0]
    modelP_Output.iloc[:, i+1]=modelSim[1]

#Graph results manually from model output 
###plot of prey counts vs time, in which only paramter b is changing -- solid: initial b value, dotted: lower b value, dashed: higher b value
RMplot_Hb=ggplot(modelH_Output,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="bHlow"), color='blue', linetype='dotted')+geom_line(aes(y="bHhigh"), color='blue', linetype='dashed')+ggtitle("Different b values")+ylab("Prey counts")+xlab("Time")+theme_bw()
###plot of predator counts vs time, in which only paramter b is changing -- solid: initial b value, dotted: lower b value, dashed: higher b value
RMplot_Pb=ggplot(modelP_Output,aes(x="t"))+geom_line(aes(y="P"), color='red')+geom_line(aes(y="bPlow"), color='red', linetype='dotted')+geom_line(aes(y="bPhigh"), color='red', linetype='dashed')+ggtitle("Different b values")+ylab("Predator counts")+xlab("Time")+theme_bw()
###same as above, now only parameter a is changing
RMplot_Ha=ggplot(modelH_Output,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="aHlow"), color='blue', linetype='dotted')+geom_line(aes(y="aHhigh"), color='blue', linetype='dashed')+ggtitle("Different a values")+ylab("Prey counts")+xlab("Time")+theme_bw()
RMplot_Pa=ggplot(modelP_Output,aes(x="t"))+geom_line(aes(y="P"), color='red')+geom_line(aes(y="aPlow"), color='red', linetype='dotted')+geom_line(aes(y="aPhigh"), color='red', linetype='dashed')+ggtitle("Different a values")+ylab("Predator counts")+xlab("Time")+theme_bw()
###same as above, now only parameter e is changing
RMplot_He=ggplot(modelH_Output,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="eHlow"), color='blue', linetype='dotted')+geom_line(aes(y="eHhigh"), color='blue', linetype='dashed')+ggtitle("Different e values")+ylab("Prey counts")+xlab("Time")+theme_bw()
RMplot_Pe=ggplot(modelP_Output,aes(x="t"))+geom_line(aes(y="P"), color='red')+geom_line(aes(y="ePlow"), color='red', linetype='dotted')+geom_line(aes(y="ePhigh"), color='red', linetype='dashed')+ggtitle("Different e values")+ylab("Predator counts")+xlab("Time")+theme_bw()
###same as above, now only parameter s is changing
RMplot_Hs=ggplot(modelH_Output,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="sHlow"), color='blue', linetype='dotted')+geom_line(aes(y="sHhigh"), color='blue', linetype='dashed')+ggtitle("Different s values")+ylab("Prey counts")+xlab("Time")+theme_bw()
RMplot_Ps=ggplot(modelP_Output,aes(x="t"))+geom_line(aes(y="P"), color='red')+geom_line(aes(y="sPlow"), color='red', linetype='dotted')+geom_line(aes(y="sPhigh"), color='red', linetype='dashed')+ggtitle("Different s values")+ylab("Predator counts")+xlab("Time")+theme_bw()
###same as above, now only parameter d is changing
RMplot_Hd=ggplot(modelH_Output,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="dHlow"), color='blue', linetype='dotted')+geom_line(aes(y="dHhigh"), color='blue', linetype='dashed')+ggtitle("Different d values")+ylab("Prey counts")+xlab("Time")+theme_bw()
RMplot_Pd=ggplot(modelP_Output,aes(x="t"))+geom_line(aes(y="P"), color='red')+geom_line(aes(y="dPlow"), color='red', linetype='dotted')+geom_line(aes(y="dPhigh"), color='red', linetype='dashed')+ggtitle("Different d values")+ylab("Predator counts")+xlab("Time")+theme_bw()
###same as above, now only parameter w is changing
RMplot_Hw=ggplot(modelH_Output,aes(x="t"))+geom_line(aes(y="H"), color='blue')+geom_line(aes(y="wHlow"), color='blue', linetype='dotted')+geom_line(aes(y="wHhigh"), color='blue', linetype='dashed')+ggtitle("Different w values")+ylab("Prey counts")+xlab("Time")+theme_bw()
RMplot_Pw=ggplot(modelP_Output,aes(x="t"))+geom_line(aes(y="P"), color='red')+geom_line(aes(y="wPlow"), color='red', linetype='dotted')+geom_line(aes(y="wPhigh"), color='red', linetype='dashed')+ggtitle("Different w values")+ylab("Predator counts")+xlab("Time")+theme_bw()

#Show all plots
print(LVplot_Hb); print(LVplot_Pb)
print(LVplot_Ha); print(LVplot_Pa) 
print(LVplot_He); print(LVplot_Pe) 
print(LVplot_Hs); print(LVplot_Ps)
print(RMplot_Hd); print(RMplot_Pd) 
print(RMplot_Hw); print(RMplot_Pw)

######################################################################
#Part 3 - Paradox of Enrichment
#Simulate model dynamics, changing the carrying capacity (alpha)
##define parameters
b=0.8
e=0.07
s=0.2
d=400
w=5
a=[0.001, .0009, .0007, .0006, .0005]
##make lists to data frame
parameters=pd.DataFrame({'b':b, 'a':a, 'e':e, 's':s, 'd':d, 'w':w})
##rearrange order of columns
parameters=parameters[['b','a','e','s','d','w']]
##make to list
parameters=parameters.values.tolist()
##create seperate data frames for output of H and P for each iteration
modelH_Output=pd.DataFrame(columns=["t", "H1", "H2", "H3", "H4", "H5"])
modelP_Output=pd.DataFrame(columns=["t", "P1", "P2", "P3", "P4", "P5"])
##fill time values in first column
modelH_Output.t=times
modelP_Output.t=times
##simulate model dynamics using a for loop
for i in range(0,len(parameters)):
    #set paramters for the iteration
    params=parameters[i]
    #run siumulation with odeint
    modelSim=spint.odeint(func=RMSim,y0=N0,t=times,args=tuple(params))
    #convert output from array to data frame
    modelSim=pd.DataFrame(data=modelSim)
    #add results to model output data frame
    modelH_Output.iloc[:, i+1]=modelSim[0]
    modelP_Output.iloc[:, i+1]=modelSim[1]

#Plot the results
plot_PoE_H=ggplot(modelH_Output,aes(x="t"))+geom_line(aes(y="H1"), color='lightcoral')+geom_line(aes(y="H2"), color='indianred')+geom_line(aes(y="H3"), color='brown')+geom_line(aes(y="H4"), color='maroon')+geom_line(aes(y="H5"), color='black')+ggtitle("Paradox of Enrichment - Prey")+ylab("Prey Population")+xlab("time")+theme_bw()
plot_PoE_P=ggplot(modelP_Output,aes(x="t"))+geom_line(aes(y="P1"), color='lightcoral')+geom_line(aes(y="P2"), color='indianred')+geom_line(aes(y="P3"), color='brown')+geom_line(aes(y="P4"), color='maroon')+geom_line(aes(y="P5"), color='black')+ggtitle("Paradox of Enrichment - Predator")+ylab("Predator Population")+xlab("Time")+theme_bw()
