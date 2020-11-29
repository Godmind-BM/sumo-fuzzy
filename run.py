'''
The main Entry-point of my programs
'''
# import traci
import sys

from app import RouteGenerator
from app import Config
from app.src.simulation import FixedTimeSimulation, FuzzyTimeSimulation

def main():
    subcommands = sys.argv[1:]
    if len(subcommands) > 0:
        if subcommands[0].strip() == 'fix':
            sim = FixedTimeSimulation()
            duration = sim.run()
            print('====================================================')
            print(f'duration : {duration: >20} s')
            print('====================================================')

        elif subcommands[0].strip() == 'fuzzy':
            sim = FuzzyTimeSimulation()
            duration  = sim.run()
            print('====================================================')
            print(f'duration : {duration: >20} s')
            print('====================================================')

        else:
            pass
    else:
        print('''
Usage: 
    python run.py fixed  --fixed-time simulation.
    python run.py fuzzy  --fuzzy-time simulation.
    python run.py        --this help.
        ''')
    
if __name__ == '__main__':
    main()
