import matplotlib.pyplot as plt
import random

def show_screen(scenario, agent_x, agent_y):
    plt.imshow(scenario, 'gray')
    plt.show(block=False)
    plt.plot(agent_x, agent_y, '*r', 'Vacuum Cleaner Agent', 5, linewidth=2.0)
    plt.pause(0.5)
    plt.clf()

# Checks if theres is any dirt left in the scenario
def check_obj(scenario, limit:int):
    for line in range(1, limit + 1):
        for column in range(1, limit + 1):
            if scenario[line][column] == 2:
                return True
    
    return False

#Method to find all current dirt
def locate_dirt(scenario, limit:int):
    _dirt = list()

    for line in range(1, limit + 1):
        for column in range(1, limit + 1):
            if scenario[line][column] == 2:
                _dirt.append((line, column))
    
    return _dirt

#Method to locate dirt closest to agent
def _closer_dirt(scenario, dirts:list, agent_localtion:tuple):
    _closer_sum = None
    _closer = None

    for dirt in dirts:
        _aux = abs(dirt[0] - agent_localtion[0]) + abs(dirt[1] - agent_localtion[1])

        if _closer_sum is None or _aux < _closer_sum:
            _closer_sum = _aux
            _closer = dirt

    return _closer

#Method for defining next agent step
def next_step(closer_dirt:tuple, agent_y, agent_x, counter:int, is_finish:bool):
    counter += 1

    if is_finish:
        return (False, agent_y, agent_x, 'NoOp', counter)
    elif closer_dirt == (agent_y, agent_x):
        return (True, agent_y, agent_x, 'aspire', counter)
    elif agent_y > closer_dirt[0]:
        return (False, agent_y - 1, agent_x, 'up', counter)
    elif agent_y < closer_dirt[0]:
        return (False, agent_y + 1, agent_x, 'down', counter)
    elif agent_x > closer_dirt[1]:
        return (False, agent_y, agent_x - 1, 'left', counter)
    elif agent_x < closer_dirt[1]:
        return (False, agent_y, agent_x + 1, 'right', counter)

#init zero 2 .. n
_LIMIT_MAX = 5

#Robot home postion
_agent_y = 1
_agent_x = 1

#assemble random scenario, 6x6 matrix - 0 = clean | 1 = wall |  2 = dirty
_scenario = [[random.choice([0, 2]) if column % _LIMIT_MAX != 0 and line % _LIMIT_MAX != 0 else 1 for column in range(0, _LIMIT_MAX + 1)] for line in range(0, _LIMIT_MAX + 1)]

# Scan Continuity Control Variable
_cleaned_up = True
_not_clean = True
_ld = None
_cd = None
_counter = 0
_finish = False

print('============ Initialized Cleaning ============')

#display and action
try:
    while(True):
        #Paint the screen
        show_screen(_scenario, _agent_x, _agent_y)
        
        #Check if you are no longer looking for a dirt. If so, it will prompt you for the 
        #next step to find the dirt, when it finds it releases the flag to locate the next dirt.
        if _cleaned_up:
            _ld = locate_dirt(_scenario, _LIMIT_MAX)
            _cd = _closer_dirt(_scenario, _ld, (_agent_y, _agent_x))            
            _cleaned_up = False
        
        _finish = not check_obj(_scenario, _LIMIT_MAX)
        _dirt_here, _agent_y, _agent_x, _print, _counter = next_step(_cd, _agent_y, _agent_x, _counter, _finish)

        if _dirt_here:
            _scenario[_agent_y][_agent_x] = 0
            _cleaned_up = True
        
        if _not_clean and _finish:
            print(f'Point: {_counter}')
            _not_clean = False
        
        print(f'Perception State:{int(_dirt_here)} - Action Chosen: {_print}')  

except Exception as error:
    print(error)

print('============ Finialized Cleaning ============')