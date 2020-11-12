'''
Simulations modules, contains two kinds of simulation traffic management algorithms:
Fixe-time based management.
Fuzzy-time based management. 
'''
import timeit
import math
import numpy as  np
import sys
import os
import traci

from abc import ABC, abstractmethod

from app import Config, RouteGenerator, sumocmd, get_waiting_time, get_queue_length

class Simulation(object):
    
    def __init__(self):
        super().__init__()

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def run(self):
        pass


class FixedTimeSimulation(Simulation):
    
    def __init__(self):
        super().__init__()
        self.queue_samples:list = np.array([])
        self.waiting_samples: list = np.array([])
        self.waiting_per_cycle = {}

    def init(self) -> None:
        route = RouteGenerator()
        route.generate()

    def run(self):
        self.init()
        start_time = timeit.default_timer()
        traci.start(sumocmd)
        queue_length = [0]
        step = 0
        while traci.simulation.getMinExpectedNumber() > 0 and step < Config.MAX_STEPS + 600:
            traci.simulationStep()
            queue_length.append(get_queue_length())
            self.waiting_per_cycle.update(get_waiting_time())

            # Each cycle have  120s delay 
            if int(traci.simulation.getTime()) % 120 == 0:
                self.queue_samples = np.append(self.queue_samples, max(queue_length))
                waiting = list(self.waiting_per_cycle.values())
                # remove nan values from list
                waiting = [x for x in waiting if x is not math.nan]
                avg_waiting = np.average(waiting)
                self.waiting_samples = np.append(self.waiting_samples, avg_waiting)
                queue_length.clear()
                step += 1

        traci.close()
        simulation_delay = round(timeit.default_timer() - start_time, 1)

        return simulation_delay

    def save_samples(self) -> None:
        queue_file = os.path.join(Config.SAMPLES_URI, 'fixed-queue')
        waiting_file = os.path.join(Config.SAMPLES_URI, 'fixed-waiting')

        with open(queue_file, 'w') as queue, open(waiting_file, 'w') as waiting:
            for q, w in zip(self.queue_samples, self.waiting_samples):
                queue.write(str(q) + '\n')
                waiting.write(str(w) + '\n')                
        
    def __repr__(self):
        f'{self.__class__.__name__}()'


class FuzzyTimeSimulation(Simulation):

    def __init__(self):
        super().__init__()

    def init(self):
        pass

    def run(self):
        pass

    def __repr__(self):
        f'{self.__class__.__name__}()'


