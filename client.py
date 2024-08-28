import socket

from policies import Ostrich, Avoid


class Client:
    """Client is run in a seperate process from the game. It instantiates
    a policy and selects actions based on the observations received from the
    server."""

    def run(self):
        pass


if __name__ == "__main__":
    exit(Client().run())
