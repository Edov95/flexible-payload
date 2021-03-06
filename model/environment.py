"""This module model the user demand and the environment conditions.

The main aim of this module is implementing a random process to generata data
for the RL algorithm.
It will also implement the environment condition like raining, ICI with other
communication systems.
"""
import numpy as np


class Ambient(object):
    """docstring for environment."""

    def __init__(self):
        """Docstring for Constructor.

        Default Constructor
        """
        super(Ambient, self).__init__()
        # self._gtx = 50.2
        self._ag = 20
        self._FPSL = 209.0
        self._bolzBW = 17 * 10 * np.log10(655*1.38)
        # self._rain = 0
        pass

    def step(self):
        """Returnt the updated losses for the choosen environment (in dB)."""
        loss = - self._ag + \
            self._FPSL - self._bolzBW
        return loss
        # Eventually add the environment conditions


"""self._CNR = self._EIRP - self._OBO + self._gtx + self._grx + \
    self._FPSL - self._rain - self._bolz"""
