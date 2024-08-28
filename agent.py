from pysc2.agents import base_agent

from server import Server
from utils import State


class RemoteAgent(base_agent.BaseAgent):
    """RemoteAgent starts a server thread that it uses to interface with
    a remote decision client. This agent does not employ a policy directly.
    Instead, it takes actions as directed by the client."""

    def __init__(self, name):
        super().__init__()
        self.name = name
        self._state = State()
        self.server = None

    def setup(self, obs_spec, action_spec):
        super(RemoteAgent, self).setup(obs_spec, action_spec)
        if "raw_units" not in obs_spec:
            raise Exception("This agent requires the raw_units observation.")

    def step(self, obs):
        super(RemoteAgent, self).step(obs)
        observation = self._state.parse_obs(obs)
        return self._step(observation)

    def run(self):
        self.server = Server()
        server_t = threading.Thread(target=server.run, daemon=True)
        server_t.start()

    def _step(self):
        # request action from remote policy client via server
        pass


class LocalAgent(base_agent.BaseAgent):
    """LocalAgent takes actions based on the game state (its observations)
    and the policy it is using. Calling _step() requests an action from the
    policy object."""

    def __init__(self, policy, name=""):
        super().__init__()
        self._policy = policy()
        self._step = self._policy.execute
        self._state = State()
        self.name = self._policy.name or name

    def setup(self, obs_spec, action_spec):
        super(LocalAgent, self).setup(obs_spec, action_spec)
        if "raw_units" not in obs_spec:
            raise Exception("This agent requires the raw_units observation.")

    def step(self, obs):
        super(LocalAgent, self).step(obs)
        observation = self._state.parse_obs(obs)
        return self._step(observation)


class Bot:

    def __init__(self, name):
        self.name = name
