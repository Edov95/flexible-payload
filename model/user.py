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
        self.demand = 500  # Capacity in kbps, a number (articolo cinesi)
        self._service_time = np.random.poisson(60)  # service time in minutes

    def step(self):
        """Calculate the next state, the action take doesn't affect the choice.

        Since it supposed that the satellite can serve the user always,
        the action taken doesn't affect the user next step calculation.
        Returnt the remaing service time
        """
        self._service_time -= 2  # Decrement the user service time by two units
        return self._service_time
        pass

    """def service_time():
        "Service time.""
        doc = "The service_time property."

        def fget(self):
            return self._service_time

        def fset(self, value):
            self._service_time = value

        def fdel(self):
            del self._service_time
        return locals()
    service_time = property(**service_time())"""

    def get_demand(self):
        """Returnt the user demand."""
        return self.demand


class UserGenerationRate(object):
    """Docstring for UserGenerationRate.

    Generate the user arrival rate to the satellite beam.
    It a variable data rate for each time interval and generate the users
    according to a poisson random process
    """

    def __init__(self):
        """Docstring for Constructor.

        Default Constructor
        """
        super(UserGenerationRate, self).__init__()
        self.time_stamp = 0  # The index for the vector
        self.stamps = 1440  # One sample every two minutes for 48h
        # Punto di inizio modellato come una uniforme tra -pi/6 e pi/6,
        # così modello lo spazio tra il traffico in funzione del fuso orario
        # È la fase del mio rate
        start_point = np.random.uniform(-np.pi/3, np.pi/3)
        # Modello il mio traffico come processo nel tempo, la cui media
        # La cui media segue l'andamento di una sinusoide, x sono i ounti per
        # calcolare la media
        x = np.linspace(start_point, 4 * np.pi + start_point, self.stamps)
        # Ora ho un processo che è anche negativo
        arrival_rate = np.sin(x) + 10
        # Devo rendere il processo positivo, non esiste capacità negativa.
        # Ora non è negativa, di "notte" posso avere uno 0, improbabile
        # Risolvere in future versioni
        self.arrival_rate = arrival_rate - np.min(arrival_rate)

    def stamps():
        """Stamps."""
        doc = "The stamps property."

        def fget(self):
            return self.stamps

        def fdel(self):
            del self.stamps
        return locals()
    stamps = property(**stamps())

    def step(self):
        """Get the user for the step.

        Returnt the number of unser in the for the step. It is not related
        with the action taken.
        """
        # Numbers of arrivail in the timestep
        ret = np.random.poisson(self.arrival_rate[self.time_stamp])
        self.time_stamp += 1
        return ret
