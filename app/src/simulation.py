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

from app import ( Config, RouteGenerator, sumocmd, get_waiting_time, 
                get_queue_length, save_samples, Visualizer )

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
        while traci.simulation.getMinExpectedNumber() > 0 or step < Config.MAX_STEPS + 600:
            traci.simulationStep()
            queue_length.append(get_queue_length())
            self.waiting_per_cycle.update(get_waiting_time())

            # Each cycle have  120s delay 
            if int(traci.simulation.getTime()) % 120 == 0:
                self.queue_samples = np.append(self.queue_samples, max(queue_length))
                waiting = list(self.waiting_per_cycle.values())
                # remove nan values from list
                if waiting:
                    # waiting = [x for x in waiting if x is not math.nan]
                    avg_waiting = np.nanmean(waiting)
                else:
                    avg_waiting = 0
                self.waiting_samples = np.append(self.waiting_samples, avg_waiting)
                queue_length.clear()
                self.waiting_per_cycle.clear()
            step += 1
            print(f' step : {step}  veh : {traci.simulation.getMinExpectedNumber()}')
        traci.close()
        simulation_delay = round(timeit.default_timer() - start_time, 1)
        save_samples(['queue-fixed', 'waiting-fixed'], [self.queue_samples, self.waiting_samples])
        Visualizer().plot_data([('Cycle', 'Queue Length'), ('Cycle', 'Average Waiting')], [
            self.queue_samples, self.waiting_samples], ['fixed-queue', 'fixed-waiting'])
        return simulation_delay

        
    def __repr__(self):
        f'{self.__class__.__name__}()'


class FuzzyTimeSimulation(Simulation):

    def __init__(self) -> None:
        super().__init__()
        self.queue_samples: list = np.array([])
        self.waiting_samples: list = np.array([])
        self.waiting_per_cycle = {}

    def init(self) -> None:
        route = RouteGenerator()
        route.generate()
        pass

    def run(self) -> int:
        pass

    def __repr__(self):
        f'{self.__class__.__name__}()'


