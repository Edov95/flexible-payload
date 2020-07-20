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
        self._cnt = 0
        self._max_users = 24 * self._num_beams
        # self._tot_pow = 61
        # self._state = [61 for _ in range(beams)]
        # self._state.append(self._tot_pow)
        # self._demand_vector = []

    def step(self, action):
        """Apply the action to the satellite."""
        # user = usr.User()
        # time = np.random.poisson(3)
        observable = np.zeros((self._num_beams, 2))
        reward = 0
        self._done = False
        self._reward = 0

        in_service = 0
        in_wait = 0
        for i in range(self._num_beams):
            state, _, info = self._beams[i].step(-1)
            # observable[i][0] = 0 if state[0] == 0 else 1
            observable[i][0] = state[0]
            observable[i][1] = len(np.argwhere(state[1:] > -1))
            in_wait += state[0]
            in_service += len(np.argwhere(state[1:] > -1))

        if action != self._num_beams:
            if in_service < self._max_users:

                in_wait = np.zeros(self._num_beams)
                in_service = np.zeros(self._num_beams)

                for i in range(self._num_beams):
                    # print("Beam: {}".format(i))
                    if (i == action):
                        state, reward, info = self._beams[i].step(0)
                    else:
                        state, _, _ = self._beams[i].step(-1)
                    # observable[i][0] = 0 if state[0] == 0 else 1
                    observable[i][0] = state[0]
                    observable[i][1] = len(np.argwhere(state[1:] > -1))
                    in_service[i] = len(np.argwhere(state[1:] > -1))
                    in_wait[i] = state[0]

                self._info = {"in_wait": in_wait}

                if reward < 0:
                    self._done = True
                    self._reward = -3
                else:
                    # self._reward = 0.1
                    """if sum(in_service + in_wait) > 0:
                        if sum(in_service + in_wait) < 9 * self._num_beams:
                            self._reward = sum(in_service) / sum(in_service + in_wait)
                        else:
                            self._reward = sum(in_service) / (9 * self._num_beams)
                    else:
                        self._reward = 0
                    # self._reward = sum(in_service) / (12 * self._num_beams)"""
                    self._reward = 0.1

                # if 0 == action:
                #     self._reward = 1
                # else:
                #     self._reward = 0
            else:
                return observable, -2, True, self._info
        else:
            self._done = True

            in_wait = np.zeros(self._num_beams)
            in_service = np.zeros(self._num_beams)

            for i in range(self._num_beams):
                state_2, _, info = self._beams[i].step(-1)
                # observable[i][0] = 0 if state_2[0] == 0 else 1
                observable[i][0] = state_2[0]
                observable[i][1] = len(np.argwhere(state_2[1:] > -1))
                in_wait[i] = state_2[0]
                in_service[i] = len(np.argwhere(state_2[1:] > -1))

            self._info = {"in_wait": in_wait}

            # print("User in service: {}".format(sum(in_service)))
            # print(sum(in_service + in_wait))
            if sum(in_service + in_wait) > 0:
                if sum(in_service + in_wait) < self._max_users:
                    self._reward = sum(in_service) / sum(in_service + in_wait)
                else:
                    self._reward = sum(in_service) / self._max_users
            else:
                self._reward = 0
            # print("Associated reward: {}".format(self._reward))"""

            # self._reward = 0

        return observable, self._reward, self._done, self._info

    def advance(self):
        """Advane one time step."""
        self._to_assign = np.random.randint(self._num_beams)
        self._users = self._user_generation[self._to_assign].step()
        # self._users = np.random.randint(2) + 1

        # for i in range(self._num_beams):
        #     self._beams[i].advance()

        for _ in range(self._users):
        # if self._to_assign != self._num_beams:
            self._beams[self._to_assign].add_user()

        for i in range(self._num_beams):
            self._beams[i].advance()
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
        observable = np.zeros((self._num_beams, 2))

        for i in range(self._num_beams):
            state = self._beams[i].state()
            # observable[i][0] = 0 if state[0] == 0 else 1
            observable[i][0] = state[0]
            observable[i][1] = len(np.argwhere(state[1:] > -1))

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
