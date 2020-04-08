"""Module for modelling the user behaviour.

In this module the user behaviour is modeleded, all r.p.s associated with
the user must be changed here.
"""
import numpy as np


class User(object):
    """docstring for User."""

    def __init__(self):
        """Docstring for the constructor.

        Default constructor
        """
        super(User, self).__init__()
        self._demand = 500  # Capacity in kbps, a number (articolo cinesi)
        self._service_time = np.random.poisson(25)  # service time in seconds
        self._wait_time = 50  # constant wait time for the user can be random
        self._queue = "None"  # indicate in which queue the user is
        # calcolo priorità in funzione di una uniforme e dei limiti
        # Si potrebbe mettere domanda in funzione della priorità e non tenedola
        # fissa
        p = np.random.uniform(0, 1)
        if 0 < p and 0.25 >= p:
            self._priority = 1
        else:
            self._priority = 2

    def step(self, time):
        """Step funciton for the user, the user discount the interarrival time.

        @parm time the seconds to discount in both the time
        """
        if ("service" == self._queue):
            self._service_time -= time
        elif ("wait" == self._queue):
            self._wait_time -= time
        else:
            print("Error in user queue state: " + self._queue)

        return self._service_time, self._wait_time

    def change_queue_state(self, new_state):
        """Change the queue for the user.

        @param new_state the new state for the user
        """
        self._queue = new_state

    def put_in_service(self):
        """Put the user in service state."""
        self.change_queue_state("service")

    def put_in_wait(self):
        """Put the user in the wait queue."""
        self.change_queue_state("wait")

    def get_demand(self):
        """Returnt the user demand."""
        return self.demand

    def get_priority(self, arg):
        """Return the user priority."""
        return self._priority

    def get_beam(self):
        """Return the beams the user belong to."""
        return self._beam


"""class UserGenerationRate(object):
    Docstring for UserGenerationRate.

    Generate the user arrival rate to the satellite beam.
    It a variable data rate for each time interval and generate the users
    according to a poisson random process


    _arrival_rate = 0

    def __init__(self):
        Docstring for Constructor.

        Default Constructor

        super(UserGenerationRate, self).__init__()
        self._time_stamp = 0  # The index for the vector
        self._stamps = 1440  # One sample every two minutes for 48h
        # Punto di inizio modellato come una uniforme tra -pi/6 e pi/6,
        # così modello lo spazio tra il traffico in funzione del fuso orario
        # È la fase del mio rate
        self._start_point = np.random.uniform(0, 2*np.pi)
        print(self._start_point)
        self.calculate_lambda()

    def stamps():
        Stamps
        doc = "The stamps property."

        def fget(self):
            return self._stamps

        def fdel(self):
            del self._stamps
        return locals()
    stamps = property(**stamps())

    def step(self):
        Get the user for the step.

        Returnt the number of unser in the for the step. It is not related
        with the action taken.

        # Numbers of arrivail in the timestep
        if 1440 == self._time_stamp:
            self.calculate_lambda()
            self._time_stamp = 0
        ret = np.random.poisson(self._arrival_rate[self._time_stamp])
        self._time_stamp += 1
        return ret

    def calculate_lambda(self):
        Private method for update the arrival rate
        # Modello il mio traffico come processo nel tempo, la cui media
        # La cui media segue l'andamento di una sinusoide, x sono i ounti per
        # calcolare la media
        x = np.linspace(self._start_point, 4 * np.pi + self._start_point,
                        self.stamps)
        # Ora ho un processo che è anche negativo
        arrival_rate = 21*np.sin(x) + 32
        # Devo rendere il processo positivo, non esiste capacità negativa.
        # Ora non è negativa, di "notte" posso avere uno 0, improbabile
        # Risolvere in future versioni
        self._arrival_rate = arrival_rate
"""
