"""
    Enter your details below:

    Name: Dao Duc Thinh
    Student ID: V202100511
    Email: 21thinh.dd@vinuni.edu.vn
"""

from typing import List

from game_engine.util import raise_not_defined
from search_problems import SearchProblem
from search_strategies import SearchNode
from frontiers import Queue


def solve(problem: SearchProblem) -> List[str]:
    """See 2_implementation_notes.md for more details.

    Your search algorithms needs to return a list of actions that reaches the
    goal from the start state in the given problem. The elements of this list
    need to be one or more references to the attributes NORTH, SOUTH, EAST and
    WEST of the class Directions.
    """
    # *** YOUR CODE HERE ***

    start = SearchNode(problem.get_initial_state())
    explored = set()
    explored.add(start.state)
    frontier = Queue()
    frontier.push(start)
    
    foundGoal = False
    while not frontier.is_empty() and not foundGoal:
        currState = frontier.pop()
        for successor, action, cost in problem.get_successors(currState.state):
            if successor in explored:
                continue
            successorNode = SearchNode(state=successor, action=action, parent=currState)   
            if problem.goal_test(successor):
                currState = successorNode
                foundGoal = True
                break
            explored.add(successor)
            frontier.push(successorNode)
    
    backward_path = []
    if foundGoal:
        while currState.state != problem.get_initial_state():
            backward_path.append(currState.action)
            currState = currState.parent
        forward_path = list(reversed(backward_path))
        return forward_path
    else:
        print("No Goal found!")

        






