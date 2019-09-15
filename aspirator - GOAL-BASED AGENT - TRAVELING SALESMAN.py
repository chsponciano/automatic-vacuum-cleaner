import matplotlib.pyplot as plt
import random
import copy


# init zero 2 .. n
_LIMIT_MAX = 5

# Robot home postion
_agent_position = (1,1)
_agent_x = 1
_agent_y = 1

# assemble random scenario, 6x6 matrix - 0 = clean | 1 = wall |  2 = dirty
_scenario = [[random.choice([0, 2]) if column % _LIMIT_MAX != 0 and line % _LIMIT_MAX != 0 else 1 for column in range(0, _LIMIT_MAX + 1)] for line in range(0, _LIMIT_MAX + 1)]

# Control Variable
_cleaned_up = True
_not_clean = True
_ld = None
_current = None
_counter = 0
_finish = False

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

# Method to find all current dirt
def locate_dirt(scenario, limit:int):
    _dirt = dict()
    _counter = 0

    for line in range(1, limit + 1):
        for column in range(1, limit + 1):
            if scenario[line][column] == 2:
                _dirt[_counter] = (line, column)
                _counter += 1
    
    return _dirt

#Method for calculating distance between dirt
def calculate_dirts_distance(dirts:dict):
    dist = dict()

    for k_i, d_i in dirts.items():
        for k_j, d_j in dirts.items():
            if k_i != k_j:
                dist[k_i, k_j] = _sum_dist(d_i, d_j)

    return dist

#Method for calculating the best route to clean up all dirt using the traveling cashier algorithm
def traveling_salesman(cost, total_size):
    _graph = {}
    _sequence = []

    def _go_through(cost, k, a):
        if (k, a) in _graph:
            return _graph[k, a]

        values = []
        all_min = []

        for current_element in a:
            set_element = copy.deepcopy(list(a))
            set_element.remove(current_element)
            all_min.append([current_element, tuple(set_element)])
            values.append(cost[k-1][current_element-1] + _go_through(cost,current_element, tuple(set_element)))

        _graph[k, a] = min(values)
        _sequence.append(((k,a), all_min[values.index(_graph[k, a])]))

        return _graph[k, a]

    for x in range(1, total_size):
        _graph[x + 1, ()] = cost[x][0]

    cost = _go_through(cost, 1, range(2, total_size+1))

    solution = _sequence.pop()
    path = [1]
    path.append(solution[1][0])

    for x in range(total_size - 2):
        for new_solution in _sequence:
            if tuple(solution[1]) == new_solution[0]:
                solution = new_solution
                path.append(solution[1][0])
                break
    path.append(1)

    return (cost, path)
    
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
        
# display and action
try:
    print('============ Initialized Cleaning ============')

    print('Locating dirt...')
    _dirts = locate_dirt(_scenario, _LIMIT_MAX)
    print(f'Total dirst found: {len(_dirts)}; {_dirts}')

    print('Calculating distances...')
    _dirts_distance = calculate_dirts_distance(_dirts)
    _cost_matrix = [[0 if i == j else _dirts_distance[i, j] for j in range(len(_dirts))] for i in range(len(_dirts))]

    print('Calculating the best route to clean up all dirt using the traveling cashier algorithm...')
    _total_cost, _circuit = traveling_salesman(_cost_matrix, len(_dirts))
    print(f'Best circuit total: {len(_circuit)}')

    while(True):
        #Paint the screen
        show_screen(_scenario, _agent_x, _agent_y)
        
        #Check if you are no longer looking for a dirt. If so, it will prompt you for the 
        #next step to find the dirt, when it finds it releases the flag to locate the next dirt.
        if _cleaned_up:
            if _circuit:
                _current = _dirts[int(_circuit.pop(0)) - 1]
            _cleaned_up = False
        
        _finish = not check_obj(_scenario, _LIMIT_MAX)
        _dirt_here, _agent_y, _agent_x, _print, _counter = next_step(_current, _agent_y, _agent_x, _counter, _finish)

        if _dirt_here:
            _scenario[_agent_y][_agent_x] = 0
            _cleaned_up = True
        
        if _not_clean and _finish:
            print(f'Point: {_counter}')
            _not_clean = False
        
        print(f'Perception State:{int(_dirt_here)} - Action Chosen: {_print}')  

except Exception as error:
    print(error)
finally:
    print('============ Finialized Cleaning ============')
