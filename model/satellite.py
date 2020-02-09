"""Module for modeling a satellite."""

import numpy as np

"""
The main aim of this module is model the satellite behaviour.
This is not the agent of a RL problem.
A better solution for modeling the environment described in a RL problem
is split that in two submodules. One that model the environment like rain
user capacity demand etc.
The other (this file) modeling the satellite behaviour providing to the agent
the solution space, the satellite state and other information for computing
the optimization function.
"""


class Satellite(object):
    """docstring for Satellite."""

    def __init__(self, beams):
        """Init for Satellite."""
        super(Satellite, self).__init__()
        self._num_of_ch = beams
        self._beams = [Beam() for _ in range(beams)]
        self._tot_pow = (61 + 2) * beams
        self._state = [61 for _ in range(beams)]
        self._state.append(self._tot_pow)

    def next_state(self, actions):
        """Calculate the next state action for the satellite."""
        """
        Function that calculate the next state action for the satellite given
        the action taked in this step
        @param actions is a list containing all the actions for the satellite
        in the given step
        @return the next state vector
        """
        temp = sum(actions['EIRP'])
        tot_new_pow = sum([self._beams[i].EIRP
                          for i in range(self._num_of_ch)]) + temp

        if (tot_new_pow <= self._tot_pow):
            # If the condition of total power is respected the update is done
            new_state = []
            for i in range(self._num_of_ch):
                self._beams[i].EIRP += actions['EIRP'][i]
                new_state.append(self._beams[i].EIRP)

            new_state.append(sum([self._beams[i].EIRP
                                 for i in range(self._num_of_ch)]))
            self._state = new_state

        return self._state


class Beam(object):
    """Model the satellite beam."""

    """
    This class will model the single satellite beam and all the possible
    attribute that it can manage like assignated power, number of user served
    by the beam, the beam loss till the earth and many others.
    """

    def __init__(self):
        """Initialize the beam."""
        """
        Constructor for initializing the beam with default values
        min_pow = 56, max_pow = 66 and EIRP = 61
        """
        super(Beam, self).__init__()
        self._EIRP = 61
        self._max_pow = 66
        self._min_pow = 56
        self._EIRP_step = 0.1

        self._users = 0
        self._min_usr = 0
        self._max_urs = 10
        self._user_step = 1

    def EIRP():
        """EIRP property."""
        doc = "The EIRP property."

        def fget(self):
            return self._EIRP

        def fset(self, value):
            if(self._min_pow <= value <= self._max_pow):
                self._EIRP = value

        def fdel(self):
            del self._EIRP
        return locals()
    EIRP = property(**EIRP())

    def users():
        """User property."""
        doc = "The users property."

        def fget(self):
            return self._users

        def fset(self, value):
            if (self._min_usr <= value <= self._max_urs):
                self._users = value

        def fdel(self):
            del self._users
        return locals()
    users = property(**users())

    def lighting(self, arg):
        """Set the lighting for the beam."""
        pass

    def get_actions(self):
        """Return the possible action for the beam."""
        """May be that we need to return always 3 actions"""

        tmp_min = self._min_usr
        tmp_max = self._max_urs
        tmp = self._users
        step = self._user_step

        usr_actions = [i for i in range(tmp_min - tmp,
                                        tmp_max - tmp + step,
                                        step)]

        tmp_min = self._min_pow
        tmp_max = self._max_pow
        tmp = self._EIRP
        step = self._EIRP_step

        EIRP_actions = [i for i in range((tmp_min - tmp) * 1 / step,
                                         (tmp_max - tmp + step) * 1 / step, 1)]

        return {'user': usr_actions, 'EIRP': EIRP_actions}


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
