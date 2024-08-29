# StarCraft-II-Python-Challenge
A challenge environment for controlling SC2 units. Based on [PySC2](https://github.com/google-deepmind/pysc2) specifically for exploring competitive heuristic tactics.

## Installation Instructions
1. Install dependencies in virtual environment `pip install -r requirements.txt`
2. Move challenge maps to `\<StarCraft II Installation Directory\>\Maps\EEE466\\*.SC2Map`
3. Add line `import challenge_maps  # use locally created maps` to `venv\Lib\site-packages\pysc2\maps\__init__.py`
4. Add `Version("5.0.13", 92174,"D44E66924A56B2D4BC94786D8A7EB5B8", None),` to `venv\Lib\site-packages\pysc2\run_configs\lib.py VERSIONS`

## Running the game
Use `run.py` to configure and run games. There are a few parameters you can change, notably the player1 and player2 agents. An agent can be a `LocalAgent` which takes a policy object in its constructor (remember to import the class into `run.py`), a `RemoteAgent`, or a `Bot`. Agents need to be named with the exception of the `LocalAgent` which will take the name given by its policy if none is selected for it. Note that for the competition, you are submitting only a policy class. Make sure that it can play on either side of the map as a `LocalAgent`.

## Challenge 1: Policy Design
You are provided with a `LocalAgent` class that inherits from the PySC2 `BaseAgent` (see `agent.py`). This is an object that the simulation expects to receive game observations and to perform the step function. The agent's `_step()` is bound to the policy that it was instantiated with. Each policy (see `policy.py`) is given a unique name and implements the `execute()` method. This is where the input (observations) are interpreted and an action is selected. Observations are a named tuple with various information about friendly and enemy units, notably their position and health (see `utils.py`). The policy `execute()` method must return an `Action` object. `utils.action_cmd()` is a constructor for `Action` objects.

## Challenge 2: Remote Agent
To complete the implementation of `RemoteAgent` you will need to create a server object (to run "locally" WRT the simulation) and a client object running remotely. The client must be started as a separate process. The client is responsible to instantiating and running the policy. Which policy to use can be selected at the client or at the server. You must use protobuf to format the exchange of messages.

## Observations
Observations are defined in the code block below:
```
Observation = namedtuple('observation', ['steps', 'last_actions', 'friendly_units', 'enemy_units'])
Unit = namedtuple('unit', ['tag', 'type', 'player', 'health', 'shields', 'x', 'y'])
```

### A sample observation
```
steps = 1
last_actions = np.array([], dtype=np.int32)
enemy_units = [
Unit(tag=np.int64(4297588737), type=np.int64(48), player=np.int64(4), health=np.int64(45), shields=np.int64(0), x=np.int64(23), y=np.int64(16)), 
Unit(tag=np.int64(4297850881), type=np.int64(48), player=np.int64(4), health=np.int64(45), shields=np.int64(0), x=np.int64(23), y=np.int64(16))
]
friendly_units = [
Unit(tag=np.int64(4295491585), type=np.int64(48), player=np.int64(1), health=np.int64(45), shields=np.int64(0), x=np.int64(9), y=np.int64(16)),
Unit(tag=np.int64(4295753729), type=np.int64(48), player=np.int64(1), health=np.int64(45), shields=np.int64(0), x=np.int64(9), y=np.int64(15))
]

obs = Observation(steps, last_actions, friendly_units, enemy_units)

# Try selecting a single unit
print(obs.friendly_units[5])

# Get unit's health and location
sample_unit = obs.friendly_units[5]
print(f"Unit number {sample_unit.tag} is at x,y ({sample_unit.x},{sample_unit.y}) with {sample_unit.health} health.")
```

## Actions
There are four action types available: move, patrol, attack, stop.
- Move: Units will go to a designated location without engaging enemies, even if attacked.
- Attack: Units will move towards a location while attacking any enemies they encounter on the way.
- Patrol: The unit moves back and forth between two points (current location and selected location)automatically attacking enemies it encounters.
- Cancel: Cancel last action and do nothing.
- There is also a NO-OP command that may be used directly without parameters.

Actions can be targeted at a single unit or a group of units. Move, attack, and patrol actions have a target location which can either be an x,y coordinate or another unit. There is error checking in the State object to prevent you from controlling enemy units. The map allows coordinates: x=[0,32], y=[0,32].

Note: when playing against others you could be placed on the right or the left part of the map, be careful about hard-coding coordinates.

```
from utils import action_cmd as Action

# def action_cmd(obs, action: str, units, target=None):
#     """
#     param obs: parsed observations
#     param action: move, patrol, attack, cancel
#     param units: list of friendly units or single friendly unit
#     param target: unit or list of x,y coords
#     """

# Some possible actions
Action(obs, "attack", obs.friendly_units[9], target=obs.enemy_units[3])
Action(obs, "move", obs.friendly_units, target=[0, 16])
Action(obs, "cancel", obs.friendly_units)

# Do not submit an action
from pysc2.lib.actions import RAW_FUNCTIONS
RAW_FUNCTIONS.no_op()
```
