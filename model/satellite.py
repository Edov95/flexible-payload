"""Module for modeling a satellite.

The main aim of this module is model the satellite behaviour.
This is not the agent of a RL problem.
A better solution for modeling the environment described in a RL problem
is split that in two submodules. One that model the environment like rain
user capacity demand etc.
The other (this file) modeling the satellite behaviour providing to the agent
the solution space, the satellite state and other information for computing
the optimization function.
"""

import numpy as np
import model.beam as beam
import model.user as usr


class Satellite(object):
    """docstring for Satellite."""

    _beams = []

    def __init__(self, beams):
        """Init for Satellite."""
        super(Satellite, self).__init__()
        self._num_beams = beams
        self._beams = [beam.Beam() for _ in range(beams)]
        self._to_assign = np.random.randint(self._num_beams)
        # self._tot_pow = 61
        # self._state = [61 for _ in range(beams)]
        # self._state.append(self._tot_pow)
        # self._demand_vector = []

    def step(self, action):
        """Apply the action to the satellite."""
        user = usr.User()
        time = np.random.poisson(3)
        observable = np.zeros(0)
        reward = 0

        for i in range(self._num_beams):
            # print("Beam: {}".format(i))
            if (i == self._to_assign):
                state, reward = self._beams[i].step(action, user, time)
            else:
                state, _ = self._beams[i].step(action, "", time)

            observable = np.append(observable, state)

        self._to_assign = np.random.randint(self._num_beams)

        observable = np.append(observable, [self._to_assign, 0])
        observable = observable.reshape((self._num_beams + 1, 2))
        # observable.append(self._to_assign)

        return observable, reward

    def random_action(self):
        """Get a random action."""
        return np.random.randint(4)

    def action_space(self):
        """Get the action space."""
        actions = []

        for i in range(4):
            actions.append(i)

        return actions

    def state(self):
        """Return the state of the satellite."""
        observable = np.zeros(0)

        for i in range(self._num_beams):
            state = self._beams[i].state()

            observable = np.append(observable, state)

        self._to_assign = np.random.randint(self._num_beams)
        observable = np.append(observable, [self._to_assign, 0])

        observable = observable.reshape((self._num_beams + 1, 2))

        return observable

    # def action_space(self):
    #     """Get the action state for the satellite."""
    #     actions = [self._beams[i].action_space()
    #                for i in range(len(self._beams))]
    #     return actions

    """def reward(self):
        Return the reward for the given action
        demand = self.get_demand()
        offered = self.calculate_offered()
        # Eucledean norm to calculate the distance between the vecors/matricies
        reward = np.sqrt(((offered - demand)**2).sum())
        return reward"""


def random_state():
    """Return a random satellite state."""
    SNR_difference = np.random.uniform()
    return SNR_difference - 1


def random_action():
    """Return a random statellite possible action."""
    Power_difference = np.random.uniform()
    return (Power_difference - 1) / 10


def reward(SNR_difference):
    """Calculate the reward."""
    return 1 - SNR_difference ** 2
