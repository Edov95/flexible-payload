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

    # _beams = []

    def __init__(self, beams):
        """Init for Satellite."""
        super(Satellite, self).__init__()
        self._num_beams = beams
        self._beams = [beam.Beam() for _ in range(beams)]
        self._to_assign = np.random.randint(self._num_beams)
        self._n_actions = 1 * beams + 1
        self._done = False
        self._info = {}
        self._user_generation = [usr.UserGenerationRate(np.random.randint(3))
                                 for i in range(beams)]
        self._users = int(0)
        self._reward = 0
        # self._tot_pow = 61
        # self._state = [61 for _ in range(beams)]
        # self._state.append(self._tot_pow)
        # self._demand_vector = []

    def step(self, action):
        """Apply the action to the satellite."""
        # user = usr.User()
        # time = np.random.poisson(3)
        observable = np.zeros((self._num_beams, 16))
        reward = 0
        self._done = True
        self._reward = 0

        state = self.state()
        in_service = 0
        for i in range(len(state)):
            in_service = in_service + len(np.argwhere(state[1:] > -1))

        if action != self._num_beams:
            if in_service < self._num_beams * 12:

                for i in range(self._num_beams):
                    # print("Beam: {}".format(i))
                    if (i == action):
                        state, rew, info = self._beams[i].step(0)
                    else:
                        state, rew, info = self._beams[i].step(-1)

                    reward += rew
                    observable[i] = state

                if reward < 0:
                    self._done = True
                    self._reward = -2
                elif self._reward >= 0:
                    self._reward = in_service / (12 * self._num_beams)
            else:
                return observable, -3, True, self._info
        else:
            self._done = True

            in_wait = np.zeros(self._num_beams)
            in_service = np.zeros(self._num_beams)

            for i in range(self._num_beams):
                state_2, _, info = self._beams[i].step(-1)
                observable[i] = state_2
                in_wait[i] = state[0]
                in_service[i] = len(np.argwhere(state[1:] > -1))

            self._reward = sum(in_service) / (12 * self._num_beams)

        return observable, self._reward, self._done, self._info

    def advance(self):
        """Advane one time step."""
        self._to_assign = np.random.randint(self._num_beams)
        self._users = self._user_generation[self._to_assign].step()

        for i in range(self._num_beams):
            self._beams[i].advance()

        if(self._to_assign != -1):
            for _ in range(self._users):
                self._beams[self._to_assign].add_user()

        return self.state()

    # def random_state(self):
        # for i in range(self._num_beams):
            # self._beams[i].random_state()

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
        observable = np.zeros((self._num_beams, 16))

        for i in range(self._num_beams):
            state = self._beams[i].state()
            observable[i] = state

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
