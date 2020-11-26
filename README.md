### SUMO-FUZZY 
Sumo-fuzzy is an implementation of a fuzzy-logic based system for single road intersection flow control enhancement. It uses the open source road traffic management system **Simulator Of Urban Mobility** [sumo](https://github.com/eclipse/sumo) in combinaison with a fuzzy inference system to enhance traffic management in a single intersection.

### Requirements
+ SUMO ( Simulator Of Urban Mobility ) [sumo](https://github.com/eclipse/sumo)
+ Matplotlib
+ Numpy
+ skfuzzy 


### Installation
Aftter installing Simulator Of Urban Mobility on your System, follow below bullets:

1. Clone the repository in a folder.
2. move to the new created folder on the above folder.
3. activate the virtual environment with
```
pipenv shell
```
4. Install requirements with
```
pipenv install
```
### Loading the Simulation

```
python run.py fuzzy --fuzzy time simulation
python run.py fix   --fix time simulation
python run.py       --help
```
