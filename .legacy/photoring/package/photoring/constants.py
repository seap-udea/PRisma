from scipy import constants as const
import numpy as np

#########################################
#CONSTANTS
#########################################
#//////////////////////////////
#NUMERIC
#//////////////////////////////
RAD = 180/np.pi
DEG = np.pi/180

#////////////////////
#UNITS AND MULTIPLES
#////////////////////
KM = 1E3
DAY = const.day
YEAR = const.year
HOUR = const.hour
MINUTE = const.minute
LIGHTY = const.light_year
PARSEC = 3.2616*LIGHTY

NANO = 1E-9
KILO = 1E3
MEGA = 1E6
GIGA = 1E9

#////////////////////
#PLANETARY
#////////////////////
RJUP = 69911.0*KM
MJUP = 1.898E27 #kg
RSAT = 58232.0*KM
MSAT = 5.6846E26 #kg
REARTH = 6371.0*KM
MEARTH = 5.97219E24 #kg
RSAT_BRING = 92000.0*KM
RSAT_ARING = 136775.0*KM
RSUN = 696342.0*KM
MSUN = 1.98855E30 #kg
LSUN = 3.846E26 #W
TSUN = 5778.0 #K
RHOSUN = MSUN/(4*np.pi/3*RSUN**3)

#////////////////////
#PHYSICAL CONSTANTS
#////////////////////
AU = 149597871.0*KM
GCONST = const.G
HP = const.h
KB = const.k
CSPEED = const.c