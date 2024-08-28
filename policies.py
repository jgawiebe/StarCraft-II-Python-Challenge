from abc import ABC, abstractmethod
from pysc2.lib.actions import RAW_FUNCTIONS

from utils import action_cmd as Action


class Policy(ABC):
    """Policies implement the strategy pattern"""

    @abstractmethod
    def execute(self, obs):
        pass


class Ostrich(Policy):

    def __init__(self):
        self.name = ""

    def execute(self, obs):
        if obs.steps == 1:
            return Action(obs, "cancel", obs.friendly_units)
        return RAW_FUNCTIONS.no_op()
    
    
class Run(Policy):
    """
    Example policy - This is designed to be bad, you can do much better.
    """
    def __init__(self):
        self.name = ""
        
    def execute(self, obs):
        if not obs.enemy_units or not obs.friendly_units: # in case game end
            return RAW_FUNCTIONS.no_op()
        
        # try attacking enemy
        if obs.steps < 10:
            return Action(obs, "move", obs.friendly_units, obs.enemy_units[0])
        
        # then do something more tactical
        # assign an index for each living unit
        idx_unit = (obs.steps - 1) % len(obs.friendly_units)
        unit = obs.friendly_units[idx_unit]
        # move units one at a time
        return Action(obs, "patrol", unit, [idx_unit + 10, idx_unit + 10])


class YourPolicyHere(Policy):

    def __init__(self):
        self.name = "Player (?)"  # Put the name of your policy/player here

    def execute(self, obs):
        return RAW_FUNCTIONS.no_op()
