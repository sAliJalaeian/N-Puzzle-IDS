import math
cutoff = 0


def find_Actions(node, n, state):
    if node is not None:
        zero_index = node.state.index(0)
    zero_index = state.index(0)
    actions = []
    if (zero_index - n) > -1:
        actions.append("U")
    if (zero_index + 1) % n != 0:
        actions.append("R")
    if (zero_index + n) < (n ** 2):
        actions.append("D")
    if zero_index % n != 0:
        actions.append("L")
    return actions


class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.actions = find_Actions(parent, int(math.sqrt(len(state))), state)
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.state == other.state and self.parent == other.parent and self.action == other.action and \
                   self.path_cost == other.path_cost
        return NotImplemented

    def __hash__(self):
        return hash((self.state, self.parent, self.action, self.path_cost))

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.path_cost < other.path_cost
        return NotImplemented


#######################################################################################


class Problem:

    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal

    def is_Goal(self, answer):
        return answer == self.goal


#######################################################################################

def expand(node):
    child = []
    n = int(math.sqrt(len(node.state)))
    i = 0
    zero_index = node.state.index(0)
    while i < len(node.actions):
        initial1 = node.state.copy()
        if node.actions[i] == 'U':
            temp = initial1[zero_index - n]
            initial1[zero_index] = temp
            initial1[zero_index - n] = 0
            node_child = Node(initial1, node, 'U', node.path_cost + 1)
        elif node.actions[i] == 'R':
            temp = initial1[zero_index + 1]
            initial1[zero_index] = temp
            initial1[zero_index + 1] = 0
            node_child = Node(initial1, node, 'R', node.path_cost + 1)
        elif node.actions[i] == 'D':
            temp = initial1[zero_index + n]
            initial1[zero_index] = temp
            initial1[zero_index + n] = 0
            node_child = Node(initial1, node, 'D', node.path_cost + 1)
        elif node.actions[i] == 'L':
            temp = initial1[zero_index - 1]
            initial1[zero_index] = temp
            initial1[zero_index - 1] = 0
            node_child = Node(initial1, node, 'L', node.path_cost + 1)
        child.append(node_child)
        i += 1
    return child


def is_Cycle(node):
    node1 = node
    node = node.parent
    while node:
        if node1.state == node.state:
            return True
        node = node.parent
    return False


def depth_Limited_Search(problem, limit):
    global cutoff
    stack = [Node(problem.initial)]
    result = None
    counter = 0
    while len(stack) != 0:
        node = stack.pop()
        if problem.is_Goal(node.state):
            return node, counter
        if node.depth > limit:
            result = cutoff
        elif not is_Cycle(node):
            for child in expand(node):
                stack.append(child)
            counter += 1
    return result, counter


def iterative_Deepening_Search(problem):
    depth = 0
    sum = 0
    global cutoff
    while True:
        result, nods = depth_Limited_Search(problem, depth)
        sum += nods
        if result != cutoff:
            return result, sum
        depth += 1


def find_Way(state):
    way = []
    while state.parent:
        way.append(state.action)
        state = state.parent
    return way


n = input()
initial = [int(x) for x in input().split()]
goal_state = [int(x) for x in input().split()]
problem1 = Problem(initial, goal_state)
goal, expanded_node = iterative_Deepening_Search(problem1)
print(expanded_node)
if goal is None:
    print("No solution found")
    exit(0)
final = find_Way(goal)
if len(final) >= 2:
    final.reverse()
for i in final:
    print(i, end=" ")
