import threading

from absl import app

from pysc2 import maps
from pysc2.env import run_loop
import sc2_env

from agent import RemoteAgent, LocalAgent, Bot
from policies import Ostrich, Run
from solution_policies import Banana


def main(argv):
    """
    Runner application for Lab 6. Set run parameters here.
    """
    # Select map from: 3v3, 10v10, bonus, bonus_pvp
    map_name = "10v10"
    realtime = False  # if false game rendering is sped up
    visualize = False  # show pygame views
    replay = False  # save replay file

    # Select agent class from: LocalAgent, RemoteAgent, Bot
    # If using LocalAgent specify a policy, built-in policies: Ostrich, Avoid
    player1_agent = LocalAgent(policy=Run, name="player1")
    player2_agent = Bot(name="player2")

    agents = []  # Agent object that interacts with the environment
    users = []  # Player object for game engine

    for player_agent in [player1_agent, player2_agent]:
        if isinstance(player_agent, Bot):
            users.append(sc2_env.Bot(sc2_env.Race.terran, sc2_env.Difficulty.easy))
        else:
            agents.append(player_agent)
            users.append(sc2_env.Agent(sc2_env.Race.terran, player_agent.name))
            if isinstance(player_agent, RemoteAgent):
                player_agent.run()

    with sc2_env.SC2Env(
        map_name=maps.get(map_name),
        players=users,
        agent_interface_format=sc2_env.parse_agent_interface_format(
            use_raw_units=True, use_raw_actions=True
        ),
        step_mul=1,
        score_index=-1,
        realtime=realtime,
        disable_fog=True,
        visualize=visualize,
    ) as env:
        # Run game
        run_loop.run_loop(agents, env, max_frames=0, max_episodes=1)
        print(
            f"""Scores -
                  {player1_agent.name}: {env.outcome[0]}
                  {player2_agent.name}: {env.outcome[1] if len(env.outcome) > 1 else 'N/A'}\n-"""
        )
        if replay:
            env.save_replay("", player1_agent.name)


if __name__ == "__main__":
    app.run(main)
