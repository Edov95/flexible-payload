import model.satellite as sat

def memory_replay ():
    MR = []
    for i in range(100):
        for j in range(100):
            Old_state = sat.random_state()
            Action    = sat.random_action()
            New_state = Old_state + Action
            if New_state > 1:
                New_state = 1
            elif New_state < -1:
                New_state = -1
                Reward = sat.reward(New_state)
                MR.append([Old_state,Action,New_state,Reward])
    return MR
