# Simulation tool

This is a simulation tool made for simulating satellite and manage the payload
with a neural Network. In order to be as flexible as possible this tool is created
with a modular structure.

## How it works

The simulator is done in this way
1. Payload setting
1. Characterize the satelite to ground link:
  1. Ground antennas characterization
  1. Channel characterization
  1. Satelite antenna characterization
1. Create the ground segment requested traffic
1. Optimization using Neural Network

Every steps on the above list can be configured via the configurations files

### Detailed description of the above steps

## Configuration files description
The configurations file can be found in the config folder.
They are formatted in a simple key-value pair. Each file will be parsed and the
system confgure itself using this parameters.
The aim of this division is create a good simulation tool for this and future
works.
### Payload setting
### Channel
### Satelite antennas
### Ground antennas
### Ground segment requested traffic
### Neural Network
(still don't know if this is possible)


## Model
How the satellite system is modeled, states, actions and rewards.
