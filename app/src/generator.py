'''
Generate the routefile containing vehicles and differents routes according to weibull distribustion.
https://fr.wikipedia.org/wiki/Loi_de_Weibull
'''

import numpy as np
import os

from app.config import Config

class RouteGenerator(object):
    '''
    Route file Generator object:
    >>> route = RouteGenerator()
    '''
    def __init__(self) -> None:
        self.max_step = Config.MAX_STEPS
        self.total_veh = Config.TOTAL_VEHICLE
        self.seed = Config.SEED 

    def generate(self) -> None:
        np.random.seed(self.seed) # reproductibility os the generation.

        timing = np.random.weibull(2, self.total_veh)
        timing = np.sort(timing)

        # reshaping the distribustion
        entry_times = np.array([])
        min_old = np.math.floor(timing[1])
        max_old = np.math.ceil(timing[-1])
        min_new = 0
        max_new = self.max_step
        for time in timing:
            entry_times = np.append(entry_times, ((max_new - min_new) / (max_old - min_old)) * \
                (time - max_old ) + max_new)

        entry_times = np.rint(entry_times) # get time without float point. 
        routes_path = os.path.join(Config.NETWORK_URI,'cross.rou.xml')
        
        with open(routes_path, mode='w') as demand:
            print('''
            <routes>
                <vType id="passenger" accel="0.8" decel="4.5" sigma="0.5" length="5.0" minGap="2.5" maxSpeed="16.67" guiShape="passenger" color="255,255,0"/>
                    <route id="Eastbound.L"  edges="2_0 0_3" />
                    <route id="Eastbound.T"  edges="2_0 0_1" />
                    <route id="Eastbound.TR" edges="2_0 0_4" />
                    <route id="Westbound.L"  edges="1_0 0_4" />
                    <route id="Westbound.T"  edges="1_0 0_2" />
                    <route id="Westbound.TR" edges="1_0 0_3" />
                    <route id="Northbound.L" edges="4_0 0_2" />
                    <route id="Northbound.T" edges="4_0 0_3" />
                    <route id="Northbound.TR" edges="4_0 0_1" />
                    <route id="Southbound.L" edges="3_0 0_1" />
                    <route id="Southbound.T" edges="3_0 0_4" />
                    <route id="Southbound.TR" edges="3_0 0_2" />
            ''', file=demand) 

            # 60 % of traffic is north-south and 40% east-west 
            # 80 % of vehicle goes through or right and 20 % goes left.
            for counter, time in enumerate(entry_times): 
                side = np.random.uniform(0, 1)
                if side < 0.9:
                    direction = np.random.uniform(0, 1)
                    if direction < 0.6:
                        road = np.random.randint(1, 5)
                        if road == 1:
                            print('''
                            <vehicle id="Northbound.T_%i" route="Northbound.T" depart="%s" type="passenger" departSpeed="10" />
                            ''' % (counter, time), file=demand)
                        elif road == 2:
                            print('''
                            <vehicle id="Northbound.TR_%i" route="Northbound.TR" depart="%s" type="passenger" departSpeed="10" />
                            ''' % (counter, time), file=demand)
                        elif road == 3:
                            print('''
                            <vehicle id="Southbound.T_%i" route="Southbound.T" depart="%s" type="passenger" departSpeed="10" />
                            ''' % (counter, time), file=demand)
                        elif road == 4:
                            print('''
                            <vehicle id="Southbound.TR_%i" route="Southbound.TR" depart="%s" type="passenger" departSpeed="10" />
                            ''' % (counter, time), file=demand)
                        else:
                            pass

                    else:
                        road = np.random.randint(1, 5)
                        if road == 1:
                            print('''
                            <vehicle id="Eastbound.T_%i" route="Eastbound.T" depart="%s" type="passenger" departSpeed="10" />
                            ''' % (counter, time), file=demand)
                        elif road == 2:
                            print('''
                            <vehicle id="Eastbound.TR_%i" route="Eastbound.TR" depart="%s" type="passenger" departSpeed="10" />
                            ''' % (counter, time), file=demand)
                        elif road == 3:
                            print('''
                            <vehicle id="Westbound.T_%i" route="Westbound.T" depart="%s" type="passenger" departSpeed="10" />
                            ''' % (counter, time), file=demand)
                        elif road == 4:
                            print('''
                            <vehicle id="Westbound.TR_%i" route="Westbound.TR" depart="%s" type="passenger" departSpeed="10" />
                            ''' % (counter, time), file=demand)
                        else:
                            pass
                
                else:
                    road = np.random.randint(1, 5)
                    if road == 1:
                            print('''
                            <vehicle id="Northbound.L_%i" route="Northbound.L" depart="%s" type="passenger" departSpeed="10" />
                            ''' % (counter, time), file=demand)
                    elif road == 2:
                        print('''
                        <vehicle id="Southbound.L_%i" route="Southbound.L" depart="%s" type="passenger" departSpeed="10" />
                        ''' % (counter, time), file=demand)
                    elif road == 3:
                        print('''
                        <vehicle id="Eastbound.L_%i" route="Eastbound.L" depart="%s" type="passenger" departSpeed="10" />
                        ''' % (counter, time), file=demand)
                    elif road == 4:
                        print('''
                        <vehicle id="Westbound.L_%i" route="Westbound.L" depart="%s" type="passenger" departSpeed="10" />
                        ''' % (counter, time), file=demand)
                    else:
                        pass
            
            print('''
            </routes>
            ''', file=demand)
        
        return None

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'
