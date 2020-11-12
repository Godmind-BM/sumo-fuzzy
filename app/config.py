'''
Porject Configuration file.
'''
import os
import sys


class Config(object):
    NETWORK_URI:str = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'network')
    SAMPLES_URI:str = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'samples')
    PLOTS_URI:str   = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'plots')  
    SEED:int        = 10000 
    MAX_STEPS:int   = 5430
    GUI:bool        = True
    TOTAL_VEHICLE:int = 2000


    @classmethod
    def setup_sumo(cls) -> list:
        '''
        set-up sumo important python modules (traci, sumolib)
        '''

        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit('please set "SUMO_HOME" environment variables.')


        # sumo useful library interoperability libraries
        from sumolib import checkBinary
    
        if  not cls.GUI:
            sumo_binary:str = checkBinary('sumo')
        else:
            sumo_binary:str = checkBinary('sumo-gui')

        # sumocmd = [sumo_binary, '-c', os.path.join(cls.NETWORK_URI, 'cross.sumo.cfg'), '--waiting-time-memory', str(cls.MAX_STEPS), '--quit-on-end', ]
        sumocmd = [sumo_binary, "-c", os.path.join(cls.NETWORK_URI, 'cross.sumo.cfg'),"--waiting-time-memory", str(cls.MAX_STEPS), "--quit-on-end", ]
        return sumocmd
