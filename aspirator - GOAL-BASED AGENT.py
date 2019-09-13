import matplotlib.pyplot as plt
import random
from math import inf as INFINITY

def check_obj(scenario, limit:int):
    for line in range(1, limit + 1):
        for column in range(1, limit + 1):
            if scenario[line][column] == 2:
                return True
    
    return False

def _sum_dist(dirt_one, dirt_two):
    return abs(dirt_one[0] - dirt_two[0]) + abs(dirt_one[1] - dirt_two[1])

def find_shortest_path(current_coordinate, available_next, total_dist, coordinates_passed, result):
    for _next in available_next:
        new_one = available_next.copy()
        new_one.remove(_next)
        new_coordinates_passed = coordinates_passed.copy()
        new_coordinates_passed.append(_next)
        find_shortest_path(_next, new_one, total_dist + _sum_dist(current_coordinate, _next), new_coordinates_passed, result)
    if len(available_next) == 0 and result['dist'] > total_dist:
        result['dist'] = total_dist
        result['traveled_dirts'] = coordinates_passed

#Method to find all current dirt
def locate_dirt(scenario, limit:int):
    _dirt = list()

    for line in range(1, limit + 1):
        for column in range(1, limit + 1):
            if scenario[line][column] == 2:
                _dirt.append((line, column))
    
    return _dirt

#Method for defining next agent step
def next_step(closer_dirt:tuple, agent_y, agent_x, counter:int):
    counter += 1

    if closer_dirt == (agent_y, agent_x):
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
_not_clean = True
_cleaned_up = True
_dirts = None
_cd = None
_counter = 0

out_result = {
    'dist': INFINITY,
    'traveled_dirts': None
}

print('============ Initialized Cleaning ============')

#display and action
try:
    _dirts = locate_dirt(_scenario, _LIMIT_MAX)

    if  (_agent_x, _agent_y) in _dirts:
        _dirts.remove((_agent_x, _agent_y))

    find_shortest_path((_agent_x, _agent_y), _dirts, 0, [(_agent_x, _agent_y)], out_result)

    aux = out_result['traveled_dirts']

    while(check_obj(_scenario, _LIMIT_MAX)):
        #Paint the screen
        plt.imshow(_scenario, 'gray')
        plt.show(block=False)
        plt.plot(_agent_x, _agent_y, '*r', 'Vacuum Cleaner Agent', 5, linewidth=2.0)
        plt.pause(0.5)
        plt.clf()
        
        _dirt_here, _agent_y, _agent_x, _print, _counter = next_step(aux[0], _agent_y, _agent_x, _counter)

        if _dirt_here:
            _scenario[_agent_y][_agent_x] = 0
            aux.pop(0)

        print(f'Perception State:{int(_dirt_here)} - Action Chosen: {_print}')    
        
    print(f'Point: {_counter}')

except Exception as error:
    print(error)

print('============ Finialized Cleaning ============')