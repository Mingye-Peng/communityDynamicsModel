import pandas
import numpy
import scipy
import scipy.integrate as spint
from plotnine import *

#defines ode
def predpreysim(y,t,b,e,s,w,d,a):
    H=y[0]
    P=y[1]
    
    dHdt=b*H*(1-a*H)-w*(H/(d+H))*P
    dPdt=e*w*(H/(d+H))*P-s*P
    
    return[dHdt,dPdt]
    
#put list of parameters into dataframe
paramb=[0.8,1.6,0.8,0.8,0.8,0.8,0.8]
parame=[0.07,0.07,0.14,0.07,0.07,0.07,0.07]
params=[0.2,0.2,0.2,0.4,0.2,0.2,0.2]
paramw=[5,5,5,5,10,5,5]
paramd=[400,400,400,400,400,800,400]
parama=[0.001,0.001,0.001,0.001,0.001,0.001,0.002]


param_array=numpy.column_stack([paramb,parame,params,paramw,paramd,parama])
param_df=pandas.DataFrame(param_array,columns=['b','e','s','w','d','a'])

#define range for dictionary loop



d={}
for i in range(0,7):
    H0=500
    P0=120
    y0=[H0,P0]
    params=(param_df.b[i],param_df.e[i],param_df.s[i],param_df.w[i],param_df.d[i],param_df.a[i])
    t=np.arange(0.0,50.1,0.1)
    
    #simulate model using odeint and store in dictionary
    modelsimpredprey=spint.odeint(predpreysim,y0,t,params)
    d["Sim{0}".format(i)]=pandas.DataFrame({'t':t,'H':modelsimpredprey[:,0],'P':modelsimpredprey[:,1]})

g={}
A=list(d.keys())
for i in range(0,7):
    B=A[i]
    df=d[B]
    g['{0}'.format(i)]=ggplot(df,aes(x='t',y='H',))+geom_line(color='red')+ylab('Population Size')+xlab('Time')+geom_line(aes(x='t',y='P',),color='blue')+theme_classic()

print('Starting Conditions')
print(g['0'])

print('Double b')
print(g['1'])

print('Double e')
print(g['2'])

print('Double s')
print(g['3'])

print('Double w')
print(g['4'])

print('Double d')
print(g['5'])

print('Double a')
print(g['6'])