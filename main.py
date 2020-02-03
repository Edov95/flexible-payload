import numpy as np

from tqdm import tqdm
import random
import matplotlib
import matplotlib.pyplot as plt

import model.satellite as sat
import model.neuralnetwork as nn
import model.memoryreplay as mr

#Memory replay creation
MR = mr.memory_replay ()

step_model   = nn.create_step_model()
target_model = nn.clone_model (step_model)
target_model.set_weights(step_model.get_weights())

#Training
number_episodes = 101
steps           = 100
training_step   = 10
batch_size      = 50
gamma           = 0.9
update          = 10
validation      = 10
test_episodes   = 100
Rewards         = np.array([])

for i in tqdm (range(number_episodes)):
    Old_state = sat.random_state()
    for j in range(steps):
        probability = np.random.rand(1)

        if probability < 1 - (i / number_episodes):
            Action = sat.random_action()
        else:
            inputNN    = np.zeros(1)
            inputNN[0] = Old_state
            Action     = target_model.predict([inputNN.reshape(1,1,1)]) / 10

            New_state = Old_state + Action
            if New_state > 1:
                New_state = 1
            elif New_state < -1:
                New_state = -1

            Reward = sat.reward(New_state)

            MR.append([Old_state,Action,New_state,Reward])
            Old_state = New_state

        if j == training_step:
            samples = []
            samples_indexes = random.sample(list(range(len(MR))), batch_size)
            for s_index in samples_indexes:
                samples.append(MR[s_index])

            fit_input  = []  # Input batch of the model
            fit_output = []  # Desired output batch for the input

            for sample in samples:
                sample_state        = np.zeros(1)
                sample_state[0]     = sample[0]  # Previous sat.state
                sample_action       = sample[1]  # Action made
                sample_new_state    = np.zeros(1)
                sample_new_state[0] = sample[2]  # Arrival sat.state
                sample_reward       = sample[3]  # Obtained reward
                sample_new_state    = sample_new_state.reshape(1,1,1)
                sample_goal         = sample_reward + gamma * np.max(target_model.predict([sample_new_state]))
                sample_state        = np.asarray(sample_state)
                sample_state        = sample_state.reshape(1,1,1)
                sample_output       = step_model.predict([np.asarray(sample_state)])[0]

                fit_input.append(sample_state[0])  # Input of the model
                fit_output.append(sample_output)   # Output of the model

                # Fit the model with the given batch
                history = step_model.fit([np.asarray(fit_input)], np.asarray(fit_output),
                    batch_size = None, epochs = 1, steps_per_epoch = 1, verbose = 0)

        if j % update == 0:
            target_model.set_weights(step_model.get_weights())

    if i % validation == 0:
        REWARD = 0
        for m in range(test_episodes):
            Old_state  = sat.random_state()
            for n in range(steps):
                inputNN    = np.zeros(1)
                inputNN[0] = Old_state
                Action     = target_model.predict([inputNN.reshape(1,1,1)])

                New_state  = Old_state + Action
                if New_state > 1:
                    New_state = 1
                elif New_state < -1:
                    New_state = -1

                Reward = sat.reward(New_state)
                Old_state = New_state
                REWARD += Reward

        REWARD  = REWARD / (test_episodes * steps)
        Rewards = np.append(Rewards, REWARD)
#print (REWARD)

x = np.arange(validation + 1)
print (x + 1)
print (Rewards)

fig, ax = plt.subplots()

ax.plot(x + 1, Rewards)

ax.set(xlabel='Validation step', ylabel='Mean Reward', title='Mean rewards for each step')
ax.grid()

#fig.savefig("test_1.png")
plt.show()
