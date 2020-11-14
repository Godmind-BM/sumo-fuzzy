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
                get_queue_length, save_samples, Visualizer, GreenExtend, PhaseUrgency)

TLS_INDEX = '0'

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
            # print(f' step : {step}  veh : {traci.simulation.getMinExpectedNumber()}')
        traci.close()
        simulation_delay = round(timeit.default_timer() - start_time, 1)
        save_samples(['queue-fixed', 'waiting-fixed'], [self.queue_samples, self.waiting_samples])
        Visualizer().plot_data([('Cycle', 'Queue Length'), ('Cycle', 'Average Waiting')], [
            self.queue_samples, self.waiting_samples], ['fixed-queue', 'fixed-waiting'])
        return simulation_delay

        
    def __repr__(self):
        f'{self.__class__.__name__}()'


detectors = {
    '1': ['laneAreaS2', ],
    '2': ['laneAreaN0', 'laneAreaN1', ],
    '3': ['laneAreaW2', ],
    '4': ['laneAreaE0', 'laneAreaE1', ],
    '5': ['laneAreaN2', ],
    '6': ['laneAreaS0', 'laneAreaS1', ],
    '7': ['laneAreaE2', ],
    '8': ['laneAreaW0', 'laneAreaW1', ],
}

LINK_INDEX_N0 = 0
LINK_INDEX_N1 = 1
LINK_INDEX_N2 = 2
LINK_INDEX_N3 = 3

LINK_INDEX_E0 = 4
LINK_INDEX_E1 = 5
LINK_INDEX_E2 = 6
LINK_INDEX_E3 = 7

LINK_INDEX_S0 = 8
LINK_INDEX_S1 = 9
LINK_INDEX_S2 = 10
LINK_INDEX_S3 = 11

LINK_INDEX_W0 = 12
LINK_INDEX_W1 = 13
LINK_INDEX_W2 = 14
LINK_INDEX_W3 = 15

PHASE = [None] * 9
PHASE[2] = [LINK_INDEX_N0, LINK_INDEX_N1, LINK_INDEX_N2, ]
PHASE[6] = [LINK_INDEX_S0, LINK_INDEX_S1, LINK_INDEX_S2, ]
PHASE[4] = [LINK_INDEX_E0, LINK_INDEX_E1, LINK_INDEX_E2, ]
PHASE[8] = [LINK_INDEX_W0, LINK_INDEX_W1, LINK_INDEX_W2, ]
# Left turn phases
PHASE[5] = [LINK_INDEX_N3, ]
PHASE[1] = [LINK_INDEX_S3, ]
PHASE[7] = [LINK_INDEX_E3, ]
PHASE[3] = [LINK_INDEX_W3, ]

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
        self.init()
        start_time = timeit.default_timer()
        queue_length = [0]
        urgency = PhaseUrgency()
        ext = GreenExtend()
        next_phase_index = 0  # next green phase index
        phase_index = 0  # current green phase index
        yellow_phase_index = phase_index + 1  # current yellow phase index
        min_green = 5  # minimum green time
        # max_green = None  # maximun green  time
        new_duration = min_green  # new max duration (new_duration < max_green)
        yellow_time = 0  # check when tls turn to yellow
        max_urgency = 0  # retreive the phase that have the maximun urgency
        is_green = True  # check whether the light is green
        step = 0

        traci.start(sumocmd)
        traci.trafficlight.setPhase(TLS_INDEX, phase_index)  # first phase is 0
        max_green = traci.trafficlight.getPhaseDuration(TLS_INDEX)
        while traci.simulation.getMinExpectedNumber() > 0 or step < Config.MAX_STEPS + 600:
            traci.simulationStep()
            current_time = traci.simulation.getTime()
            queue_length.append(get_queue_length())
            self.waiting_per_cycle.update(get_waiting_time())
            if is_green:
                # gets the current phase duration
                if current_time == new_duration:
                    # print("time to act : ", current_time)
                    # print("phase index : ", phase_index)
                    current_states = list(
                        traci.trafficlight.getRedYellowGreenState(TLS_INDEX))
                    flow_queues = {}
                    flow_queues = self.get_green_phases_queue(current_states)
                    flow_1 = list(flow_queues.values())[0]
                    flow_2 = list(flow_queues.values())[1]
                    try:
                        extension = ext.compute_extended_time(
                            flow_1, flow_2)  # gets extension
                    except AssertionError as ass:
                        extension = 9
                    # print(extension)
                    if current_time + extension > max_green:
                        red_queues = self.get_red_phases_queue(current_states)
                        red_waiting = self.get_red_phases_waiting(
                            current_states)
                        for phase in red_queues.keys():
                            try:
                                urge = urgency.compute_urgency(
                                    red_queues[phase], red_waiting[phase])
                            except AssertionError as ass:
                                urge = 10
                            if max_urgency < urge:
                                max_urgency = urge
                                next_phase_index = self.find_index(phase)
                        is_green = False
                        yellow_time = current_time
                        traci.trafficlight.setPhase(
                            TLS_INDEX, yellow_phase_index)
                    else:
                        new_duration = current_time + extension
            else:
                if current_time - yellow_time == 4:  # if yellow time is expired
                    is_green = True
                    traci.trafficlight.setPhase(TLS_INDEX, next_phase_index)
                    # Reinitialize parameters
                    yellow_time = 0
                    phase_index = next_phase_index
                    new_duration = current_time + min_green
                    max_green = current_time + \
                        traci.trafficlight.getPhaseDuration(TLS_INDEX)
                    max_urgency = 0
                    yellow_phase_index = phase_index + 1

            # Gets samples
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

                #  Re-initialisation
                queue_length.clear()
                self.waiting_per_cycle.clear()

            step += 1

        traci.close()
        simulation_delay = round(timeit.default_timer() - start_time, 1)
        save_samples(['queue-fuzzy', 'waiting-fuzzy'],
                     [self.queue_samples, self.waiting_samples])
        Visualizer().plot_data([('Cycle', 'Queue Length'), ('Cycle', 'Average Waiting')], [
            self.queue_samples, self.waiting_samples], ['fuzzy-queue', 'fuzzy-waiting'], color='#FF5733')

        return simulation_delay

    def get_red_phases_queue(self, current_phase):
        '''Returns the queue length of red phase_combi.'''
        # print("call red_phase queue...")
        phases_queues = {}
        queues = []
        vehicle_number = 0
        _, red_phases = self.get_green_red_phases(current_phase)
        for combi_phase in red_phases:
            for x in combi_phase:
                lad_ids = detectors[str(x)]
                for lad in lad_ids:
                    vehicle_number = traci.lanearea.getLastStepVehicleNumber(
                        lad)
                    queues.append(vehicle_number)
                phases_queues[combi_phase] = max(queues)
                queues.clear()

        return phases_queues

    def get_red_phases_waiting(self, current_phase):
        # print("call red_phase waiting...")
        """Returns the waiting time of red combi-phase."""
        all_phase_waiting = {}
        one_phase_waiting = np.array([])
        waiting = np.array([])
        lane_waiting = np.array([])

        _, red_phases = self.get_green_red_phases(current_phase)
        for combi_phase in red_phases:
            for x in combi_phase:
                lad_ids = detectors[str(x)]
                for lad in lad_ids:
                    vehicles = traci.lanearea.getLastStepVehicleIDs(lad)
                    for veh in vehicles:
                        waiting = np.append(
                            waiting, traci.vehicle.getAccumulatedWaitingTime(veh))

                    if waiting.any():
                        lane_waiting = np.append(
                            lane_waiting, np.average(waiting))
                        waiting = list(lane_waiting)
                        waiting.clear()
                        waiting = np.array(waiting)

                if lane_waiting.any():
                    one_phase_waiting = np.append(
                        one_phase_waiting, np.average(lane_waiting))
                    lane_waiting = list(lane_waiting)
                    lane_waiting.clear()
                    lane_waiting = np.array(lane_waiting)
                else:
                    pass

            if one_phase_waiting.any():
                all_phase_waiting[combi_phase] = max(one_phase_waiting)
            else:
                all_phase_waiting[combi_phase] = 0

        return all_phase_waiting

    def get_green_phases_queue(self, current_phase):
        # print("call green_phase queue...")
        green_phase, _ = self.get_green_red_phases(current_phase)
        flow_queues = {}
        if green_phase:
            queues = []
            vehicle_number = 0
            for combi_phase in green_phase:
                for x in combi_phase:
                    lad_ids = detectors[str(x)]
                    for lad in lad_ids:
                        vehicle_number = traci.lanearea.getLastStepVehicleNumber(
                            lad)
                        queues.append(vehicle_number)
                    flow_queues[x] = max(queues)
                    queues.clear()
        else:
            pass

        return flow_queues

    def get_green_red_phases(self, current_phase):
        green_phase = []
        red_phases = []
        for index, phase in enumerate(PHASE):
            if phase is not None:
                for link_index in phase:
                    if current_phase[link_index] == 'r':
                        if (index + 4) <= 8:
                            red_phases.append((index, index + 4))
                        else:
                            red_phases.append((index, index - 4))
                        break
                    elif current_phase[link_index] == 'G':
                        if (index + 4) <= 8:
                            green_phase.append((index, index + 4))
                        else:
                            green_phase.append((index, index - 4))
                        break
                    else:
                        pass
            else:
                pass
        # removes duplicates in red phases
        mid = int(len(red_phases) / 2)
        for i in range(0, mid):
            red_phases.pop()

        if green_phase:
            green_phase.pop()

        return green_phase, red_phases

    def find_index(self, combi_phase):

        phase_index = None
        if (combi_phase[0] + combi_phase[1]) == 8:
            phase_index = 0
        elif (combi_phase[0] + combi_phase[1]) == 6:
            phase_index = 3
        elif (combi_phase[0] + combi_phase[1]) == 12:
            phase_index = 6
        elif (combi_phase[0] + combi_phase[1]) == 10:
            phase_index = 9

        return phase_index
        
        

    def __repr__(self):
        f'{self.__class__.__name__}()'


