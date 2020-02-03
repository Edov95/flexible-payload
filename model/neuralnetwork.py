import numpy as np
import tensorflow as tf
import keras
from keras.models import Input, Model, Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, BatchNormalization
from keras.models import load_model
from keras.layers import Activation
from keras import initializers
from keras import optimizers
from keras import backend as K
from keras.utils.generic_utils import get_custom_objects

from keras_radam import RAdam
from keras import regularizers

##NN
def create_step_model():
    x          = Input(shape=(None,1))
    x2         = (Dense(16,activation='relu'))(x)
    x3         = (Dense(16,activation='relu'))(x2)
    x4         = (Dense(1,activation='tanh'))(x3)
    step_model = Model(inputs=[x],outputs=x4)
    opt        = RAdam()
    step_model.compile(optimizer = opt, loss = 'mean_squared_error')
    return step_model

def clone_model (model):
    return keras.models.clone_model(model)
