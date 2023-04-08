"""
    Enter your details below:

    Name: Dao Duc Thinh
    Student ID: V202100511
    Email: 21thinh.dd@vinuni.edu.vn
"""

from typing import Callable, List

from game_engine.util import raise_not_defined
from search_problems import SearchProblem
from search_strategies import SearchNode
from frontiers import PriorityQueueWithFunction

def solve(problem: SearchProblem, heuristic: Callable) -> List[str]:
    """See 2_implementation_notes.md for more details.

    Your search algorithms needs to return a list of actions that reaches the
    goal from the start state in the given problem. The elements of this list
    need to be one or more references to the attributes NORTH, SOUTH, EAST and
    WEST of the class Directions.
    """

    frontier = PriorityQueueWithFunction(lambda item: heuristic(item.state, problem) + item.path_cost, 'state')
    startNode = SearchNode(problem.get_initial_state())
    frontier.push(startNode)
    explored = set()

    while (not frontier.is_empty()):
        currNode = frontier.pop()
        if problem.goal_test(currNode.state):
            break
        for successor, action, cost in problem.get_successors(currNode.state):
            if successor not in explored:
                successorNode = successorNode = SearchNode(state=successor, action=action, path_cost=currNode.path_cost + cost, parent=currNode)
                explored.add(successor)
                frontier.push(successorNode)
    backward_path = []
    forward_path = []
    while currNode.state != problem.get_initial_state():
        backward_path.append(currNode.action)
        currNode = currNode.parent
        forward_path = list(reversed(backward_path))
    
    return forward_path






