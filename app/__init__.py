import importlib

from app.config import Config
from app.src.generator import RouteGenerator
# set traci configuration
sumocmd = Config.setup_sumo()

from app.src.metrics import get_queue_length, get_waiting_time





