from collections import namedtuple

from pysc2.lib.actions import RAW_FUNCTIONS
from pysc2.lib import features

_PLAYER_SELF = features.PlayerRelative.SELF
_PLAYER_ENEMY = features.PlayerRelative.ENEMY

Observation = namedtuple('observation', ['steps', 'last_actions', 'friendly_units', 'enemy_units'])
Unit = namedtuple('unit', ['tag', 'type', 'player', 'health', 'shields', 'x', 'y'])

class State:
    """
    Utility class that stores game state and handles obervations.
    DAN Agents should instantiate this class on initialization.
    DO NOT MODIFY.
    """
    def __init__(self):
        self.steps = 0
        self._all_units = None
        self._friendly_units = None 
        self._enemy_units = None
        
    def get_units(self, units):
        # 0 unit_type, (marine is type 48)
        # 1 player_relative,
        # 2 health,
        # 3 shields, (protoss only)
        # 12 screen_pos.x,
        # 13 screen_pos.y
        # 29 tag
        indices = [29, 0, 1, 2, 3, 12, 13]
        self._all_units = [Unit(*(unit[i] for i in indices)) for unit in units]
        
        self._friendly_units = [unit for unit in self._all_units if unit.player == _PLAYER_SELF]
        self._enemy_units = [unit for unit in self._all_units if unit.player == _PLAYER_ENEMY]
    
    def parse_obs(self, obs):
        self.steps += 1
        last_actions = obs.observation.last_actions
        self.get_units(obs.observation.raw_units)
        
        return Observation(self.steps, last_actions, self._friendly_units, self._enemy_units)
    
def action_cmd(obs, action: str, units: list, target=None):
    """
    param obs: parsed observations
    param action: move, patrol, attack, cancel
    param units: list of friendly units
    param target: unit or list of x,y coords
    """
    def build_action(func_unit, func_pt):
        """Selects action for unit or point target"""
        if isinstance(target, list) and len(target) == 2: # position target
            return func_pt("now", selected_units, target)
        elif target.tag in valid_targets: # unit target
            return func_unit("now", selected_units, target.tag)
        else:
            raise Exception(f"Cannot parse {action} command")
    
    if not isinstance(units, list):
        units = [units]
    
    all_units = obs.friendly_units + obs.enemy_units
    selected_units = [unit.tag for unit in units]
    valid_units = [unit.tag for unit in obs.friendly_units]
    valid_targets = [unit.tag for unit in all_units]
    
    
    try:
        for tag in selected_units:
                assert tag in valid_units
    except AssertionError:
        raise Exception("Invalid units selected")
    except TypeError:
        raise Exception("Cannot iterate over single unit, pass in a list of tags")

    match action:
        case 'move':
            return build_action(RAW_FUNCTIONS.Move_unit, RAW_FUNCTIONS.Move_pt)
        case 'patrol':
            return build_action(RAW_FUNCTIONS.Patrol_unit, RAW_FUNCTIONS.Patrol_pt)
        case 'attack':
            return build_action(RAW_FUNCTIONS.Attack_unit, RAW_FUNCTIONS.Attack_pt)
        case 'cancel':
            return RAW_FUNCTIONS.Stop_quick("now", selected_units)
        case _:
            raise Exception("Unknown command")