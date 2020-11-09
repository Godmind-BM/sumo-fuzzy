'''
Porject Configuration file.
'''
import os
import sys


class Config(object):
    NETWORK_URI:str = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'network')
    SAMPLES_URI:str = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'samples')
    PLOTS_URI:str   = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'plots')
    SEED:int = 10000 
    MAX_STEPS:int = 5430
    TOTAL_VEHICLE:int = 2000
    
    if 'SUMO_HOME' in os.environ: 
        tools:str   = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")