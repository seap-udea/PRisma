from geotrans import *

System=dict2obj(dict(\
#########################################
#SYSTEM PRIMARY PARAMETERS
#########################################
#//////////////////////////////
#DETECTOR
#//////////////////////////////
Ddet=0.5,#Aperture, m
qeff=1.0,#Quantum efficiency
#//////////////////////////////
#STAR
#//////////////////////////////
Mstar=1.0*MSUN,
Rstar=1.0*RSUN,
Lstar=1.0*LSUN,
Tstar=1.0*TSUN,
Dstar=1*KILO*PARSEC,
c1=0.70,#Limb Darkening
c2=-0.24,#Limb Darkening
#//////////////////////////////
#ORBIT
#//////////////////////////////
ap=0.1*AU,
ep=0.0,
iorb=90.0*DEG,
#iorb=90.1*DEG,
wp=0.0*DEG,
#//////////////////////////////
#PLANET
#//////////////////////////////
Mplanet=1.0*MSAT,
Rplanet=1.0*RSAT,
fp=0.0, #Oblateness
#//////////////////////////////
#RINGS
#//////////////////////////////
fe=RSAT_ARING/RSAT, #Exterior ring (Rp)
fi=RSAT_BRING/RSAT, #Interior ring (Rp)
ir=10.0*DEG, #Ring inclination
phir=60.0*DEG, #Ring roll angle
tau=1.0, #Opacity
))

#########################################
#SYSTEM DERIVATIVE PARAMETERS
#########################################
derivedSystemProperties(System)
updatePlanetRings(System)
updatePosition(System,System.tcen)
