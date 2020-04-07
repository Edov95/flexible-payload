"""Module that model a beam.

This module model a satellite beam. The beam can be configured via file
"""

import numpy as np
# import model.environment as env
# import model.user as usr


class Beam(object):
    """Model the satellite beam.

    This class will model the single satellite beam and all the possible
    attribute that it can manage like assignated power, number of user served
    by the beam, the beam loss till the earth and many others.
    """

    def __init__(self):
        """Initialize the beam.

        Constructor for initializing the beam with default values
        min_pow = 56, max_pow = 66 and EIRP = 61
        """
        super(Beam, self).__init__()
        self._service_queue = []
        self._in_service = int(0)
        self._wait_queue = []
        self._in_wait = int(0)

        self._max_users = int(20)

        self._reward = int(0)

    def update_in_service(self, time):
        """Update the number of user in service."""
        indexes = []
        for i in range(self._in_service):
            temp, _ = self._service_queue[i].step(time)
            if 0 >= temp:
                indexes.append(i)

        # Remove users that have terminated the service
        for i in range(len(indexes)):
            self._service_queue.pop(indexes[i])
            self._reward += 2

        self._in_service = len(self._service_queue)

    def update_in_wait(self, time):
        """Update the number of user in wait."""
        indexes = []
        # print(self._in_wait)
        # print(len(self._wait_queue))
        for i in range(self._in_wait):
            _, temp = self._wait_queue[i].step(time)
            if 0 >= temp:
                indexes.append(i)

        # Remove users that have terminated the service
        for i in range(len(indexes)):
            self._wait_queue.pop(indexes[i])
            self._reward -= 2

        self._in_wait = len(self._wait_queue)

    def calculate_demand(self):
        """Return the demand capacity for the beam."""
        demand = 500 * self._in_service
        return demand

    def state(self):
        """Return the state for the beam."""
        state = np.zeros(2)
        state[0] = self._in_service
        state[1] = self._in_wait

        return state

    def step(self, action, user, time):
        """Calculate the next step for the beams.

        Update the service times for the users in the beam
        Remove the users that experied their service time

        Update the wait time for the users in the beam
        Remove the users that experied their wait time

        @param action indicate the action to be eexecuted
        0 add the user in service queue
        1 add the user in wait time
        2 add the user in service time and pop the first user
          from the wait queue.
        3 add the user in wait queue and pop the first user from the wait queue
        """
        self._reward = 0

        # print(self._in_wait)
        # print(self._wait_queue)

        self.update_in_service(time)
        self.update_in_wait(time)

        if ("" != user):
            if (0 == action):
                self.action_one(user)
            elif (1 == action):
                self.action_two(user)
            elif (2 == action):
                self.action_three(user)
            elif (3 == action):
                self.action_four(user)
            else:
                print("No valid action")

        state = np.zeros(2)
        state[0] = self._in_service
        state[1] = self._in_wait

        return state, self._reward

        """Modify all the parameters for the next step.

        This method will modify all the beam parameters that we want to change
        from one step to the other.
        @return the total demand for this step and the capacit offered for
        this step
        self.update_users()
        loss = self._ambient.step()
        # print("loss: " + str(loss))
        SNR = action - loss
        # print("SNR (dB): " + str(SNR))
        efficiency = self.DVB2S(SNR)
        # print("ro (dB): " + str(efficiency))
        total_demand = self.calculate_demand()
        # print("tot_dem: " + str(total_demand))
        SNR_lin = 10.0**((SNR + efficiency)/10)
        # print("SNR lin: " + str(SNR_lin))
        capacity_offered = 5000.0 * np.log2((1 + SNR_lin))
        # print("Cap. off.: " + str(capacity_offered))
        return total_demand, capacity_offered
        """

    def action_one(self, user):
        """Execute the action one."""
        if (self._in_service < self._max_users):
            self.add_user_in_service(user)
            # self._reward += 2
        else:
            self.add_user_in_wait(user)
            self._reward -= 2

    def action_two(self, user):
        """Put the user in wait queue."""
        self.add_user_in_wait(user)
        # self._reward += 1

    def action_three(self, user):
        """Add the arrived user and the firt user of wait queue in service."""
        if ((self._in_service - self._max_users) > 2):
            self.add_user_in_service(user)
            if (len(self._in_wait) > 0):
                temp_user = self._wait_queue.pop(0)
                self._in_wait -= 1
                self.add_user_in_service(temp_user)
                # self._reward += 3
            # else:
            # self._reward += -1
        else:
            self.add_user_in_wait(user)
            self._reward -= 2

    def action_four(self, user):
        """Execute the action four.

        Add the arrived user in wait queue the first of wait queue in service.
        """
        self.add_user_in_wait(user)
        if(self._in_service < self._max_users):
            temp_user = self._wait_queue.pop(0)
            self._in_wait -= 1
            self.add_user_in_service(temp_user)
            # self._reward += 2
        else:
            self._reward += -2

    def add_user_in_service(self, user):
        """Put the user in service queue."""
        user.put_in_service()
        self._service_queue.append(user)
        self._in_service += 1

    def add_user_in_wait(self, user):
        """Add user in wait queue."""
        user.put_in_wait()
        self._wait_queue.append(user)
        self._in_wait += 1

    def DVB2S(self, SNR):
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
