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
import model.environment as env
import model.user as usr


class Satellite(object):
    """docstring for Satellite."""

    def __init__(self, beams):
        """Init for Satellite."""
        super(Satellite, self).__init__()
        self._num_of_ch = beams
        self._beams = [Beam() for _ in range(beams)]
        self._tot_pow = 61
        self._state = [61 for _ in range(beams)]
        self._state.append(self._tot_pow)

    def next_state(self, actions):
        """Calculate the next state action for the satellite.

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

    def step(self, action):
        """Apply the action to the satellite."""
        previous_demand = self._demand_vector.copy()
        self._demand_vector = []
        offer_vector = []
        for i in len(self._beams):
            demand, offer = self._beams[i].step(action[i])
            self._demand_vector.append(demand)
            offer_vector.append(offer)

        observable = [previous_demand, self._demand_vector]
        reward = ((self._demand_vector - offer_vector)**2).sum()
        return observable, reward

    def actions_state(self, arg):
        """Get the action state for the satellite."""
        pass

    def reward(self):
        """Return the reward for the given action."""
        demand = self.get_demand()
        offered = self.calculate_offered()
        # Eucledean norm to calculate the distance between the vecors/matricies
        reward = np.sqrt(((offered - demand)**2).sum())
        return reward


class Beam(object):
    """Model the satellite beam.

    This class will model the single satellite beam and all the possible
    attribute that it can manage like assignated power, number of user served
    by the beam, the beam loss till the earth and many others.
    """

    _gen_rate = 0
    _total_users = []
    _users = 0

    def __init__(self):
        """Initialize the beam.

        Constructor for initializing the beam with default values
        min_pow = 56, max_pow = 66 and EIRP = 61
        """
        super(Beam, self).__init__()
        self._EIRP = 61.0  # Should be parametrized
        self._max_pow = 66  # Should be parametrized
        self._min_pow = 56  # Should be parametrized
        self._EIRP_step = 0.5  # Should be parametrized
        # self._EIRP_action = range(self._min_pow, self._max_pow,
        #                           self._EIRP_step)
        self._EIRP_actions = np.linspace(self._min_pow, self._max_pow, 20)

        self._ambient = env.Ambient()

        self._gen_rate = usr.UserGenerationRate()
        """rate = self._gen_rate.step()
        self._users = np.random.poisson(rate)
        self._total_users = [usr.User() for i in range(self._users)]"""

    def update_users(self):
        """Update the connected users to the channel."""
        # Append the next time step users
        users_to_append = self._gen_rate.step()
        for i in range(users_to_append):
            self._total_users.append(usr.User())

        indexes = []
        for i in range(self._users):
            temp = self._total_users[i].step()  # È stato in servizio 2 min
            if 0 >= temp:
                indexes.append(i)

        # Remove users that have terminated the service
        for i in range(len(indexes)):
            self._total_users.pop(indexes[i])

        self._users = len(self._total_users)

    def calculate_demand(self):
        """Returnt the demand capacity for the beam."""
        demand = 500 * self._users  # Each user has 500kbps const cap. demand
        return demand

    def action_space(self):
        """Return the possible action for the beam.

        May be that we need to return always 3 actions
        """
        return {'EIRP': self._EIRP_actions}

    def step(self, action):
        """Modify all the parameters for the next step.

        This method will modify all the beam parameters that we want to change
        from one step to the other.
        @return the total demand for this step and the capacit offered for
        this step
        """
        loss = self._ambient.step()
        self.update_users()
        SNR = action - loss
        efficiency = self.DVB2S(SNR)
        total_demand = self.calculate_demand()
        capacity_offered = SNR + efficiency
        return total_demand, capacity_offered

    def DVB2S(SNR):
        """Rerturn the spectral efficiency given an SNR in dB."""
        efficiency = 0
        if (SNR > 16.05):
            efficiency = 4.443027
        elif (SNR > 15.69):
            efficiency = 4.397854
        elif (SNR > 14.28):
            efficiency = 4.119540
        elif (SNR > 13.64):
            efficiency = 3.951571
        elif (SNR > 13.13):
            efficiency = 3.567342
        elif (SNR > 12.89):
            efficiency = 3.523143
        elif (SNR > 12.73):
            efficiency = 3.703295
        elif (SNR > 11.61):
            efficiency = 3.300184
        elif (SNR > 11.03):
            efficiency = 3.165623
        elif (SNR > 10.98):
            efficiency = 2.679207
        elif (SNR > 10.69):
            efficiency = 2.646012
        elif (SNR > 10.21):
            efficiency = 2.966728
        elif (SNR > 9.35):
            efficiency = 2.478562
        elif (SNR > 8.97):
            efficiency = 2.637201
        elif (SNR > 7.91):
            efficiency = 2.228124
        elif (SNR > 6.62):
            efficiency = 1.980636
        elif (SNR > 6.42):
            efficiency = 1.788612
        elif (SNR > 6.20):
            efficiency = 1.766451
        elif (SNR > 5.50):
            efficiency = 1.779991
        elif (SNR > 5.18):
            efficiency = 1.654663
        elif (SNR > 4.68):
            efficiency = 1.587196
        elif (SNR > 4.03):
            efficiency = 1.487473
        elif (SNR > 3.10):
            efficiency = 1.322253
        elif (SNR > 2.23):
            efficiency = 1.188304
        elif (SNR > 1):
            efficiency = 0.988858
        elif (SNR > -0.30):
            efficiency = 0.789412
        elif (SNR > -1.24):
            efficiency = 0.656448
        elif (SNR > -2.35):
            efficiency = 0.490243
        else:
            efficiency = 0.250000

        efficiency = 10 * np.log10(efficiency)
        return efficiency


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
