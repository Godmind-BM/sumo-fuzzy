'''
The main Entry-point of my programs
'''
# import traci
import sys

from app import RouteGenerator
from app import Config
from app.src.simulation import FixedTimeSimulation

def main():
    sim = FixedTimeSimulation()
    sim.run()
    
if __name__ == '__main__':
    main()
