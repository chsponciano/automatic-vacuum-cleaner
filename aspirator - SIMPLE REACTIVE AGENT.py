import matplotlib.pyplot as plt
import random

#Method for defining next agent step
def next_step(agent_y, agent_x, limit:int, _scenario, right:bool, down:bool):
    if _scenario[agent_y][agent_x] == 2:
        return (True, agent_y, agent_x, 'aspire', right)
    if right and agent_x + 1 < limit:
        return (False, agent_y, agent_x + 1, 'right', True)
    elif not right and agent_x - 1 > 0:
        return (False, agent_y, agent_x - 1, 'left', False)
    elif down: 
        return (False, agent_y + 1, agent_x, 'down', not(right))
    else:
        return (False, agent_y - 1, agent_x, 'up', not(right))
        

#init zero 2 .. n
_LIMIT_MAX = 5

#Robot home postion
_agent_y = random.randint(1, _LIMIT_MAX - 1)
_agent_x = random.randint(1, _LIMIT_MAX - 1)

#assemble random scenario, 6x6 matrix - 0 = clean | 1 = wall |  2 = dirty
_scenario = [[random.choice([0, 2]) if column % _LIMIT_MAX != 0 and line % _LIMIT_MAX != 0 else 1 for column in range(0, _LIMIT_MAX + 1)] for line in range(0, _LIMIT_MAX + 1)]

# Scan Continuity Control Variable
_aspire = True
_right = True
_down = True

#display and action
try:
    print('============ Initialized Cleaning ============')

    while(_aspire):
        #Paint the screen
        plt.imshow(_scenario, 'gray')
        plt.show(block=False)
        plt.plot(_agent_x, _agent_y, '*r', 'Vacuum Cleaner Agent', 5, linewidth=2.0)
        plt.pause(0.5)
        plt.clf()

        if _agent_y + 1 == _LIMIT_MAX:
            _down = False
        elif _agent_y - 1 == 0:
            _down = True

        _dirt_here, _agent_y, _agent_x, _print, _right = \
                next_step(_agent_y, _agent_x, _LIMIT_MAX, _scenario, _right, _down)
    
        if _dirt_here:
            _scenario[_agent_y][_agent_x] = 0
                
        


        print(f'Action Chosen: {_print}')

except Exception as error:
    print(error)
finally:
    print('============ Finialized Cleaning ============')
