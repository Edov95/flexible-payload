'''
    Module for modeling a satellite
'''

import numpy as np
import random

def random_state ():
  SNR_difference = np.random.uniform()
  return SNR_difference - 1

def random_action ():
  Power_difference = np.random.uniform()
  return (Power_difference - 1) / 10

def reward (SNR_difference):
  return 1 - SNR_difference ** 2
