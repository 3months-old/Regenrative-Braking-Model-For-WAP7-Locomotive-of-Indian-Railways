from cProfile import label
from cmath import sin
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
#settting up the locomotive profile 
wap7={'mass':123000,'area':13.4,'fstart':322400,'fconti':228000,'pmax':4740000,'beffort':18600,'kneespeed':14.44,'constspeed':19.44,'maxspeed':50}
wag9={'mass':123000,'area':13.4,'fstart':475000,'fconti':325000,'pmax':6711000,'beffort':16000,'kneespeed':9.167,'constSpeed':13.89,'maxspeed':27.78}
#taking requiered inputs
#locotype=input('Please input the type of locomotive, wap7 or wag9 ')
locotype='wap7'
carriages=18
grad=1/150
carriages=int(carriages)
loc_profile=dict()
if locotype=='wap7':
    loc_profile=wap7
elif locotype=='wag9':
    loc_profile=wag9
#setup the route profile
route_file=input("Input the name of excel file with route details, ex- 'test.xlsx'")
route_profile=pd.read_excel(route_file)

#excel file with three columns Station, Wait time and Run time
#define the drive cycle function
area=loc_profile['area']
mass=loc_profile['mass']
cspeed=loc_profile['kneespeed']
umax=loc_profile['maxspeed']
fstart=loc_profile['fstart']
fconti=loc_profile['fconti']
pmax=loc_profile['pmax']
beffort=loc_profile['beffort']
timelist=route_profile['Travel Time'].tolist()
waittime=route_profile['waiting time'].tolist()
distance=route_profile['Distance'].tolist()
net_mass=(mass+carriages*46500)
fgrad=net_mass*(9.8)*(math.sin(math.atan(grad)))
print(fgrad)
friction=0.0064*net_mass+130*carriages*4+fgrad
#friction=1.78*9.8*mass+0.029*9.8*mass*0+0.0002557*area*0**2+carriages*(1.0903*46720*9.8+0.0098331*9.8*46720*0)

Astart=(fstart-friction)/net_mass
brake=3000*carriages
#Acont=int()
#print(Astart)

#print(mass,fstart,fconti,pmax,beffort,timelist,waittime,dist)
time=int(0)
#power=0
ebr=[(0,0)]
etr=[(0,0)]
ew=[(0,0)]

bre=0
tre=0
we=0

powerplot=[(0,0)]
Vplot=[(0,0)]
Aplot=[(0,0)]

for i,j,k in zip(timelist,distance,waittime):
    wt=0
    t1=int(0)
    u=0
    while wt<=k:
            wt+=1
            Vpoint=(0,wt+time)
            Vplot.append(Vpoint)
            Apoint=(0,wt+time)
            Aplot.append(Apoint)
    time+=wt
    #acc=Astart
    dist=int(0)
    braking=False
    stop=False
    while t1<=i:
        acc=Astart
        #t1+=1
        if braking==False and stop==False:
           #print('still here')
            if u==0: 
                v=u+acc
                p=fstart*v
            elif u<cspeed:
                fres=((0.0069*net_mass)+130*20)+(504*10**-6)*net_mass*u+(0.046+0.0065*(carriages-1))*13.4*3.6*3.6*u*u+fgrad
                ftrac=min(pmax/u,fconti)
                if stop==False:
                    acc=(ftrac-fres)/net_mass
                else: acc=0
                v=u+acc
                p=ftrac*v
            elif u>=cspeed and u<umax:
                fres=((0.0069*net_mass)+130*20)+(504*10**-6)*net_mass*u+(0.046+0.0065*(carriages-1))*13.4*3.6*3.6*u*u+fgrad
                ftrac=min(pmax/u,fconti)
                #ftrac=fconti
                if stop==False:
                    acc=(ftrac-fres)/net_mass
                    v=u+acc
                else: acc=0
                if v>umax:
                    v=umax
                p=ftrac*v
            elif u==umax:
                acc=0
                v=u
                fres=((0.0069*net_mass)+130*20)+fgrad
                p=fres*v
            tre+=p*1
            we+=p*1
            deacc=(brake+fgrad)/net_mass
            dist+=u+(acc/2)
            brtime=v/deacc
            brakdist=(v*v)/(2*deacc)
            midtime=i-(brtime+t1)
            middist=v*midtime
            
            if (j)<=(dist+brakdist+middist):
                st=1
            else: st=0
            u=v
        elif stop==True:
            acc=0
            dist+=u+acc/2
            v=u+acc
            u=v
            fres=((0.0069*net_mass)+130*20)+(504*10**-6)*net_mass*u+(0.046+0.0065*(carriages-1))*13.4*3.6*3.6*u*u+fgrad
            #fres=1.78*9.8*mass+0.029*9.8*mass*u+0.0002557*area*u**2+carriages*(1.0903*46720*9.8+0.0098331*9.8*46720*u)
            p=(fres)*v*0.1+0.029*u*+(0.046+0.0065*(carriages-1))*13.4*3.6*3.6*u*u
            if t1>=i-brtime: 
                braking=True
                st=0
            tre+=p
            we+=p
        elif braking==True:
            #print('finally')
            deacc=-1*(brake+fgrad)/net_mass
            v=u+deacc
            acc=deacc
            dist+=u+0.5*acc
            u=v
            if v<=0:
                v=0
                acc=0
                braking=False
            p=-(brake+fgrad)*v
            bre+=-1*p
            we+=p
        if st==1: stop=True
        elif st==0: stop=False
        #power+=p
        wepoint=(we,time+t1)
        brepoint=(bre,time+t1)
        trepoint=(tre,time+t1)
        ebr.append(brepoint)
        etr.append(trepoint)
        ew.append(wepoint)
        ppoint=(p,time+t1)
        powerplot.append(ppoint)
        Vpoint=(v,time+t1)
        Apoint=(acc,time+t1)
        Aplot.append(Apoint)
        Vplot.append(Vpoint)
        t1+=1   
    time+=t1
#print('These are etr points',etr)
x_val=[x[1] for x in Vplot]
y_val=[x[0] for x in Vplot]
plt.plot(x_val,y_val)
plt.xlabel('Time (sec)')
plt.ylabel('Velocity (m/s)')
plt.show()
x_val1=[x[1] for x in Aplot]
y_val1=[x[0] for x in Aplot]
plt.plot(x_val1,y_val1)
plt.xlabel('Time (sec)')
plt.ylabel('Accelration (m/s^2)')
plt.show()
x_val2=[x[1] for x in powerplot]
y_val2=[x[0] for x in powerplot]
plt.plot(x_val2,y_val2)
plt.xlabel('Time (sec)')
plt.ylabel('Power (watts)')
plt.show()
x_val3=[x[1]for x in etr]
y_val3=[x[0] for x in etr]
plt.plot(x_val3,y_val3)
plt.xlabel('Time (sec)')
plt.ylabel('Traction Energy (Wh)')
plt.show()
x_val4=[x[1]for x in ebr]
y_val4=[x[0] for x in ebr]
plt.plot(x_val4,y_val4)
plt.xlabel('Time (sec)')
plt.ylabel('Braking Energy (Wh)')
plt.show()
x_val5=[x[1]for x in ew]
y_val5=[x[0] for x in ew]
plt.plot(x_val5,y_val5, label='With FESS')
x_val6=[x[1]for x in etr]
y_val6=[x[0] for x in etr]
plt.plot(x_val6,y_val6, label='Without FESS')
plt.xlabel('Time')
plt.ylabel('Energy Consumed')
plt.legend()
plt.show()
#print('These are accelration points ',Aplot)