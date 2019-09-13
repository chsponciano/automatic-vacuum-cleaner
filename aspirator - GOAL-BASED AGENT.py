import matplotlib.pyplot as plt
import random
from math import inf as INFINITY


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

# Calculates the distance between one dirt to another
def _sum_dist(dirt_one, dirt_two):
    return abs(dirt_one[0] - dirt_two[0]) + abs(dirt_one[1] - dirt_two[1])

def find_shortest_path(current_dirt, available_next, total_dist, dirts_traveled, result):
    for _next in available_next:
        # Creates a copy of the list containing the next possiblies paths to the target
        new_one = available_next.copy()
        # Removes itself from the newlly created list
        new_one.remove(_next)
        # Creates a copy of the list containing the path traveled so far to pass on to the next iteration 
        new_dirts_traveled = dirts_traveled.copy()
        # And appends itself to the traveles path
        new_dirts_traveled.append(_next)
        # And calculates de distance between the current dirt to the next to pass on the iteration
        new_total_dist = total_dist + _sum_dist(current_dirt, _next)
        # Passes on the variables recursively
        find_shortest_path(_next, new_one, new_total_dist, new_dirts_traveled, result)
    
    if len(available_next) == 0 and result['dist'] > total_dist:
        result['dist'] = total_dist
        result['traveled_dirts'] = dirts_traveled

# Method to find all current dirt
def locate_dirt(scenario, limit:int):
    _dirt = list()

    for line in range(1, limit + 1):
        for column in range(1, limit + 1):
            if scenario[line][column] == 2:
                _dirt.append((line, column))
    
    return _dirt

# Method for defining next agent step
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

def get_cell():
    global _counter_dirts
    
    cell = random.choice([0, 2])
    if cell == 2:
        _counter_dirts += 1

    return cell
    

# init zero 2 .. n
_LIMIT_MAX = 5

# Robot home postion
_agent_y = 1
_agent_x = 1
_counter_dirts = 0

# assemble random scenario, 6x6 matrix - 0 = clean | 1 = wall |  2 = dirty
_scenario = [[get_cell() if column % _LIMIT_MAX != 0 and line % _LIMIT_MAX != 0 and (_counter_dirts == 0 or not(_counter_dirts % 11 == 0)) \
     else 1 for column in range(0, _LIMIT_MAX + 1)] for line in range(0, _LIMIT_MAX + 1)]

# Scan Continuity Control Variable
_not_clean = True
_cleaned_up = True
_dirts = None
_counter = 0
_finish = False

out_result = {
    'dist': INFINITY,
    'traveled_dirts': None
}

print('============ Initialized Cleaning ============')

# display and action
try:
    print('Locating dirt...')
    _dirts = locate_dirt(_scenario, _LIMIT_MAX)
    print(f'Total dirst found: {_counter_dirts}; {_dirts}')
   
    _start_has_dirt = False
    if  (_agent_x, _agent_y) in _dirts:
        _start_has_dirt = True
        _dirts.remove((_agent_x, _agent_y))

    print('Calculating best route to clean all of the dirt...')
    find_shortest_path((_agent_x, _agent_y), _dirts, 0, [(_agent_x, _agent_y)], out_result)

    aux = out_result['traveled_dirts']
    print(f'Best route: {aux}')

    if not _start_has_dirt:
        aux.pop(0)

    while(True):
        # Paint the screen
        show_screen(_scenario, _agent_x, _agent_y)

        _finish = not check_obj(_scenario, _LIMIT_MAX)
        _dirt_here, _agent_y, _agent_x, _print, _counter = next_step(aux[0] if not _finish else None, _agent_y, _agent_x, _counter, _finish)

        if _dirt_here:
            _scenario[_agent_y][_agent_x] = 0
            aux.pop(0)

        if _not_clean and _finish:
            print(f'Point: {_counter}')
            _not_clean = False

        print(f'Perception State:{int(_dirt_here)} - Action Chosen: {_print}')  
            
except Exception as error:
    print(error)

print('============ Finialized Cleaning ============')
