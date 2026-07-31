from exorings import *
"""
This script calculate exoring transit basic properties, such as:

    Orbital semimajor axis: a/R*
    Orbital inclination: iorb
    Transit depth: delta
    Observed Planetary Radius: pobs
    * Planetary radius ratio: pobs/p *
    Planet contact positions: x1, x2, x3, x4
    Ring contact positions: xR1, xR2, xR3, xR4
    Transit duration (non-ringed): T14p, T23p
    Transit duration (ringed): T14, T23
    Observed scaled semimajor axis: (a/Rs)_obs 
    Observed impact parameter: b_obs 
    Observed stellar density: rho_obs 
    * Photo-ring effect: log10(rho_obs/rho_true) *

Input parameters:

    rhotrue: Stellar density (in g/cm^3)
    P: Orbital period (in days)
    b: Impact parameter (in units of stellar radius).
    p: Planetary radius (in units of stellar radius).
    fi: Ring interior radius.
    fe: Ring exterior radius.
    tau: Ring normal opacity.
    theta: Projected tilt. 90 means that the image of the ring
           in perpendicular to the orbit in the plane of the sky
    ir: Projected inclindation. 90 for an edge-on ring.

Usage:

    $ python exorings-basic.py [<par>=<value>;<par>=<value>;...]
"""

#############################################################
# INPUT PARAMETERS
#############################################################

#DEFAULT PARAMETER VALUES
default=dict(
    #TRANSIT PARAMETERS
    rhotrue=1.40598,#g/cm^3
    P=365.2446,#days
    b=0.1875,#R*
    #PLANET AND RINGS
    p=0.08,#Rstar
    fi=1.5,#Rplanet
    fe=2.35,#Rplanet
    tau=1.0,
    theta=30.0,#degrees
    ir=80.0,#degrees
    )

#GET NEW PARAMETER VALUES FROM COMMAND-LINE (IF PROVIDED)
par=getParameters(default)

#############################################################
# PHYSICAL PROPERTIES
#############################################################

#==============================
#ORBITAL PROPERTIES
#==============================
#SEMIMAJOR AXIS (a/R*)
a=(GCONST*(par.rhotrue*1E3)/(3*np.pi)*(par.P*DAY)**2)**(1./3)

#ORBITAL INCLINATION
cosiorb=par.b/a
siniorb=(1-cosiorb**2)**0.5

#==============================
#EXTERNAL RING PROPERTIES
#==============================
#Projected semimajor axis
A=par.fe*par.p

#Projected semiminor axis
B=A*np.cos(par.ir*DEG)

#==============================
#CHECK TRANSIT CONDITION
#==============================
#Approximate semiheight of the box containing the ringed-planet
hp=max(par.p,A*np.sin(par.theta*DEG),B*np.cos(par.theta*DEG))

#Transit condition
if par.b>1.0-hp:
    print("No transit (or a grazing transit) occurrs with this impact parameter, b = %.2f."%par.b)
    print("Maximum impact parameter: bmax ~ %.3f"%(1.0-hp))
    exit(1)

#############################################################
# BASIC TRANSIT PROPERTIES
#############################################################

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#TRANSIT DEPTH
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#==============================
#AUXILIAR VARIABLES
#==============================
cosir=np.cos(par.ir*DEG)
sinir=np.sin(par.ir*DEG)

#==============================
#ABSORTION/SCATTERING FACTOR
#==============================
beta=1-np.exp(-par.tau/cosir)

#==============================
#INTERNAL RING EFFECTIVE RADIUS
#==============================
if par.fi*cosir>1:
    ri2=par.fi**2*cosir-1
else:
    yi=np.sqrt(par.fi**2-1)/(par.fi*sinir)
    ri2=par.fi**2*cosir*2/np.pi*np.arcsin(yi)-\
        2/np.pi*np.arcsin(yi*par.fi*cosir)
ri2=beta*ri2

#==============================
#EXTERNAL RING EFFECTIVE RADIUS
#==============================
if par.fe*cosir>1:
    re2=par.fe**2*cosir-1
else:
    ye=np.sqrt(par.fe**2-1)/(par.fe*sinir)
    re2=par.fe**2*cosir*2/np.pi*np.arcsin(ye)-\
        2/np.pi*np.arcsin(ye*par.fe*cosir)
re2=beta*re2

#==============================
#RINGED-PLANET AREA
#==============================
ARp=np.pi*par.p**2+np.pi*(re2-ri2)*par.p**2

#==============================
#TRANSIT DEPTH (delta=ARp/As)
#==============================
delta=ARp/np.pi

#==============================
#OBSERVED RADIUS (p=Rp,obs/Rp)
#==============================
pobs=np.sqrt(delta)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#CONTACT POSITIONS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Contact positions for planetary disk
xp14=np.sqrt((1+par.p)**2-par.b**2)
xp1=-xp14;xp4=+xp14
xp23=np.sqrt((1-par.p)**2-par.b**2)
xp2=-xp23;xp3=+xp23

#Contact prosition for external ring (approximate solution)
xR13=1-A**2*(np.sin(par.theta*DEG)-par.b/A)**2*(1-B**2/A)
xR24=1-A**2*(np.sin(par.theta*DEG)+par.b/A)**2*(1-B**2/A)

xR1=-np.sqrt(xR13)-A*np.cos(par.theta*DEG)
xR2=-np.sqrt(xR24)+A*np.cos(par.theta*DEG)
xR3=+np.sqrt(xR13)-A*np.cos(par.theta*DEG)
xR4=+np.sqrt(xR24)+A*np.cos(par.theta*DEG)

#Determining which contact positions should be used
x1=min(xp1,xR1)
x2=max(xp2,xR2)

x3=min(xp3,xR3)
x4=max(xp4,xR4)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#TRANSIT TIMES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Non-ringed planet
T14p=(par.P*DAY)*np.arcsin((xp4-xp1)/(a*siniorb))/(2*np.pi)/HOUR
T23p=(par.P*DAY)*np.arcsin((xp3-xp2)/(a*siniorb))/(2*np.pi)/HOUR

#Ringed planet
T14=(par.P*DAY)*np.arcsin((x4-x1)/(a*siniorb))/(2*np.pi)/HOUR
T23=(par.P*DAY)*np.arcsin((x3-x2)/(a*siniorb))/(2*np.pi)/HOUR

#############################################################
# DERIVED TRANSIT PROPERTIES
#############################################################

#Observed scaled semimajor axis
aobs=2*(par.P*DAY/HOUR)/np.pi*delta**0.25/(T14**2-T23**2)**0.5

#Observed impact parameter
bobs=((T14**2*(1-np.sqrt(delta))-T23**2*(1+np.sqrt(delta)))/\
          (T14**2-T23**2))**0.5

#Observed stellar density
rhoobs=(3*np.pi/GCONST)*aobs**3/(par.P*DAY)**2/1E3

#Photo ring effect
PR=rhoobs/par.rhotrue
logPR=np.log10(PR)

#############################################################
# REPORT
#############################################################
L="*"*60+"\n";R="\n"+"*"*60
print(L,"INPUT PARAMETERS",R)
print("Stellar properties:")
print("\tStellar Density: rho_true = %.2f g/cm^3."%par.rhotrue)
print("Planetary properties:")
print("\tPlanetary radius: p = Rp/R* = %.4f."%par.p)
print("Orbital properties:")
print("\tOrbital period: P = %.4f days."%par.P)
print("\tImpact parameter: b/R*= %.4f"%par.b)
print("Ring properties:")
print("\tInternal Ring Radius: Ri/Rp = %.3f Rp."%par.fi)
print("\tExternal Ring Radius: Re/Rp = %.3f Rp."%par.fe)
print("\tNormal opacity: tau = %.3f."%par.tau)
print("\tProjected inclination (90 deg for edge on): ir = %.2f deg."%par.ir)
print("\tProjected tilt: theta = %.2f deg."%par.theta)
print("\tBlocking factor: beta = %e."%beta)

print(L,"DERIVED PROPERTIES",R)

print("Orbital properties:")
print("\tSemimajor axis: a/R*= %.4f"%a)
print("\tOrbital Inclination: iorb = %.3f deg"%(np.arccos(cosiorb)*RAD))

print("Ring derived properties:")
print("\tProjected exrenal ring axes: A/R* = %.4f, B/R* = %.4f"%(A,B))
print("\tEffective ring interior radius: r_i/R* = %e"%np.sqrt(ri2))
print("\tEffective ring exterior radius: r_e/R* = %e"%np.sqrt(re2))
print("\tProjected ring Area: A_Rp/R*^2 = %e"%ARp)

print(L,"TRANSIT PROPERTIES",R)
print("Transit Depth: delta = %.2f ppm"%(delta*1E6))
print("Observed Planetary Radius: pobs = sqrt(delta) = %.6f"%(pobs))
print("Scaled planetary radius: p = Rp/R* = %.6f"%(par.p))
print("Planetary radius ratio: pobs/p = %.2f"%(pobs/par.p))
print("Planet contact positions:")
print("\tx1 = %.3f, x2 = %.3f"%(xp1,xp2))
print("\tx3 = %.3f, x4 = %.3f"%(xp3,xp4))
print("Ring contact positions:")
print("\tx1 = %.3f, x2 = %.3f"%(xR1,xR2))
print("\tx3 = %.3f, x4 = %.3f"%(xR3,xR4))
print("Final Contact positions:")
print("\tx1 = %.3f, x2 = %.3f"%(x1,x2))
print("\tx3 = %.3f, x4 = %.3f"%(x3,x4))
print("Transit duration (non-ringed): T14 = %.4f h, T23 = %.4f"%(T14p,
                                                                 T23p))
print("Transit duration (ringed): T14 = %.4f h, T23 = %.4f"%(T14,T23))
print("Observed scaled semimajor axis: (a/Rs)_obs = %.2f"%(aobs))
print("Observed impact parameter: b_obs/R* = %.4f"%(bobs))
print("Observed stellar density: rho_obs = %.2f g/cm^3"%rhoobs)
print("Photo-ring effect: PR = %.4f, log10(PR) = %.2f"%(PR,logPR))
