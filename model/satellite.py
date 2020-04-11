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
# import model.user as usr


class Satellite(object):
    """docstring for Satellite."""

    _beams = []

    def __init__(self, beams):
        """Init for Satellite."""
        super(Satellite, self).__init__()
        self._num_beams = beams
        self._beams = [beam.Beam() for _ in range(beams)]
        self._to_assign = np.random.randint(self._num_beams)
        self._n_actions = beams * 3
        self._done = False
        self._info = {}
        # self._tot_pow = 61
        # self._state = [61 for _ in range(beams)]
        # self._state.append(self._tot_pow)
        # self._demand_vector = []

    def step(self, action):
        """Apply the action to the satellite."""
        # user = usr.User()
        # time = np.random.poisson(3)
        observable = np.zeros((self._num_beams + 1, 2))
        reward = 0
        self._done = False

        if (-1 != self._to_assign):
            self._beams[self._to_assign].add_user()
            self._to_assign = -1

        if action != self._num_beams:
            beam = int(action / 3)
            if (beam != 0):
                act = int(action % beam)
            else:
                act = action

            for i in range(self._num_beams):
                # print("Beam: {}".format(i))
                if (i == beam):
                    state, rew, info = self._beams[i].step(act)
                else:
                    state, rew, info = self._beams[i].step(-1)

                reward += rew
                observable[i] = state

            if rew < 0:
                self._done = True
        else:
            self._done = True

            for i in range(self._num_beams):
                state, rew, info = self._beams[i].step(-1)
                observable[i] = state
                reward += rew

            prob = np.random.rand(1)
            if (prob < 0.5):
                self._to_assign = -1
            elif(prob < 0.75):
                self._to_assign = 0
            else:
                self._to_assign = 1

        observable[self._num_beams] = np.asarray([self._to_assign, 0])

        return observable, reward, self._done, self._info

    def advance(self):
        """Advane one time step."""
        self._to_assign = np.random.randint(self._num_beams)
        for i in range(self._num_beams):
            self._beams[i].advance()

    def random_action(self):
        """Get a random action."""
        return np.random.randint(self._n_actions)

    def action_space(self):
        """Get the action space."""
        actions = []

        for i in range(self._n_actions):
            actions.append(i)

        return actions

    def state(self):
        """Return the state of the satellite."""
        observable = np.zeros((self._num_beams + 1, 2))

        for i in range(self._num_beams):
            state = self._beams[i].state()

            observable[i] = state

        # self._to_assign = np.random.randint(self._num_beams)
        observable[self._num_beams] = np.asarray([self._to_assign, 0])

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
