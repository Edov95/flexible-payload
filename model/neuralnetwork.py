"""Module for work with the neural network."""
import numpy as np
import keras
from keras.models import Input, Model
from keras.layers import Dense, Flatten
# import tensorflow as tf
# from keras.layers import BatchNormalization
# from keras import backend as K
# from keras.utils.generic_utils import get_custom_objects

from keras_radam import RAdam
# from keras import regularizers


class Agent(object):
    """docstring for Agent."""

    def __init__(self, n_actions, actions, n_state):
        """Create the class."""
        super(Agent, self).__init__()
        self._step_model = self.create_step_model(n_actions, n_state)

        self._target_model = keras.models.clone_model(self._step_model)
        self._target_model.set_weights(self._step_model.get_weights())

        self._n_actions = n_actions
        self._actions = np.ndarray((1, self._n_actions))
        for i in range(self._n_actions):
            self._actions[0, i] = 1

        self._n_state = n_state
        self._gamma = 0.4

    def create_step_model(self, n_actions, n_state):
        """Create the models for the neaural network."""
        x = Input(shape=(1, n_state))
        x1 = Flatten()(x)
        x2 = (Dense(32, activation='relu'))(x1)
        x3 = (Dense(32, activation='relu'))(x2)
        x4 = (Dense(n_actions))(x3)

        actions_input = Input((n_actions,), name='mask')
        actions_input2 = keras.layers.Reshape((1, n_actions))(actions_input)
        filtered_output = keras.layers.Multiply()([actions_input2, x4])
        filtered_output = keras.layers.Reshape((n_actions, 1))(filtered_output)

        step_model = Model(inputs=[x, actions_input], outputs=filtered_output)
        opt = RAdam()
        step_model.compile(optimizer=opt, loss='mean_squared_error')

        return step_model

    def train(self, samples):
        """Train the model."""
        fit_input = []  # Input batch of the model
        fit_output = []  # Desired output batch for the input
        fit_actions = []
        for sample in samples:
            state = sample[0].reshape((1, 1, self._n_state))  # Previous state
            action = sample[1]  # Action made
            new_state = sample[2].reshape(
                                  (1, 1, self._n_state)
                                  )  # Arrival state
            reward = sample[3]  # Obtained reward

            sample_goal = reward + self._gamma * np.max(
                          self._target_model.predict([new_state,
                                                     self._actions],
                                                     use_multiprocessing=True))
            sample_output = self._step_model.predict([np.asarray(state),
                                                      self._actions],
                                                     use_multiprocessing=True
                                                     )[0]
            act = np.ndarray((1, self._n_actions))
            act[0, action] = 1

            sample_output[:, 0] = 0
            sample_output[action, 0] = sample_goal

            fit_input.append(state[0])  # Input of the model
            fit_output.append(sample_output)  # Output of the model
            fit_actions.append(act[0])

        self._step_model.fit([np.asarray(fit_input),
                             np.asarray(fit_actions)],
                             np.asarray(fit_output),
                             batch_size=None,
                             epochs=1,
                             steps_per_epoch=1,
                             verbose=0,
                             use_multiprocessing=True)

    def update(self):
        """Update the target model of the agent."""
        self._target_model.set_weights(self._step_model.get_weights())

    def predict(self, old_state):
        """Predict the action using the target model."""
        actions = self._target_model.predict([old_state.reshape(
                                             (1, 1, self._n_state)
                                             ),
                                             self._actions],
                                             use_multiprocessing=True)
        return np.argmax(actions)


def create_step_model2():
    """Create the neaural network."""
    x = Input(shape=(None, 1))
    x2 = (Dense(16, activation='relu'))(x)
    x3 = (Dense(16, activation='relu'))(x2)
    x4 = (Dense(1, activation='tanh'))(x3)
    step_model = Model(inputs=[x], outputs=x4)
    opt = RAdam()
    step_model.compile(optimizer=opt, loss='mean_squared_error')
    return step_model


def clone_model(model):
    """Model krapper for the keras function."""
    return keras.models.clone_model(model)
