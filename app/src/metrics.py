'''
The metric module provides metrics used to evaluate Fixed-time based simulation 
Fuzzy-timed based one. 
'''
import traci

def get_queue_length() -> int:
    '''
    Returns maximun queue lenght per steps.
    '''
    total = 0
    lad_ids = traci.lanearea.getIDList()
    for lad in lad_ids:
        total += traci.lanearea.getLastStepVehicleNumber(lad)

    return total


def get_waiting_time() -> float:
    '''
    Returns total avreage waiting time per steps
    '''
    times = {}
    lad_ids = traci.lanearea.getIDList()
    for lad in lad_ids:
        vehicles_ids = traci.lanearea.getLastStepVehicleIDs(lad)
        for veh in vehicles_ids:
           time = traci.vehicle.getAccumulatedWaitingTime(veh)
           times.update({veh:time})
    
    return times 