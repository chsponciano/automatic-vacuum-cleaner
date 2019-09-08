import matplotlib.pyplot as plt
import random

#Method to find all current dirt
def locate_dirt(scenario):
    _dirt = list()

    for line in range(1, 6):
        for column in range(1, 6):
            if scenario[line][column] == 2:
                _dirt.append(''.join([str(line), str(column)]))
    
    return _dirt

#Method to locate dirt closest to agent
def _closer_dirt(scenario, dirt:list, agent_y, agent_x):
    _closer_sum = None
    _closer = None
    _agent_localtion = int(''.join([str(agent_y), str(agent_x)]))

    for d in dirt:
        if _closer_sum is None or abs(_agent_localtion - int(d)) < _closer_sum:
            _closer_sum = abs(_agent_localtion - int(d))
            _closer = d

    return (int(_closer[0]), int(_closer[1])) if _closer is not None else None

#Method for defining next agent step
def next_step(closer_dirt:tuple, agent_y, agent_x):
    if closer_dirt == (agent_y, agent_x):
        return (True, agent_y, agent_x)
    else:
        if agent_y > closer_dirt[0]:
            print('Action Chosen: down')
            return (False, agent_y - 1, agent_x)
        elif agent_y < closer_dirt[0]:
            print('Action Chosen: up')
            return (False, agent_y + 1, agent_x)
        elif agent_x > closer_dirt[1]:
            print('Action Chosen: right')
            return (False, agent_y, agent_x - 1)
        elif agent_x < closer_dirt[1]:
            print('Action Chosen: left')
            return (False, agent_y, agent_x + 1)

#Robot home postion 5x5 matrix
_agent_y = random.randint(1, 4)
_agent_x = random.randint(1, 4)

#assemble random scenario, 6x6 matrix - 0 = clean | 1 = wall |  2 = dirty
_scenario = [[random.choice([0, 2]) if column % 5 != 0 and line % 5 != 0 else 1 for column in range(0, 6)] for line in range(0, 6)]

# Scan Continuity Control Variable
_not_clean = True
_cleaned_up = True
_ld = None
_cd = None

print('============ Initialized Cleaning ============')

#display and action
while(_not_clean):
    #Paint the screen
    plt.imshow(_scenario, 'gray')
    plt.show(block=False)
    plt.plot(_agent_x, _agent_y, '*r', 'Vacuum Cleaner Agent', 5, linewidth=2.0)
    plt.pause(0.5)
    plt.clf()
    
    #Check if you are no longer looking for a dirt. If so, it will prompt you for the 
    #next step to find the dirt, when it finds it releases the flag to locate the next dirt.
    if _cleaned_up:
        _ld = locate_dirt(_scenario)
        _cd = _closer_dirt(_scenario, _ld, _agent_y, _agent_x)

        if(_cd is None):
            _not_clean = False
            continue
        
        _cleaned_up = False
    
    _dirt_here, _agent_y, _agent_x = next_step(_cd, _agent_y, _agent_x)

    if _dirt_here:
        print('Action Chosen: aspire')
        _scenario[_agent_y][_agent_x] = 0
        _cleaned_up = True

print('============ Finialized Cleaning ============')