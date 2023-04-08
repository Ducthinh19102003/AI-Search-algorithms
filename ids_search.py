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
import sys

def depth_limited_search(problem: SearchProblem, node: SearchNode, limit: int, explored: List) -> SearchNode:
    """
    Return None if cutoff occurs, goal node otherwise
    """
    if problem.goal_test(node.state):
        return node
    elif limit == 0:
        return None
    result = None
    for successor, action, cost in problem.get_successors(node.state):
        if successor not in explored:
            successorNode = SearchNode(state=successor, action=action, parent=node)
            result = depth_limited_search(problem, successorNode, limit - 1,  explored + [successor])
            if result != None:
                return result
                
    return result


def solve(problem: SearchProblem) -> List[str]:
    """See 2_implementation_notes.md for more details.

    Your search algorithms needs to return a list of actions that reaches the
    goal from the start state in the given problem. The elements of this list
    need to be one or more references to the attributes NORTH, SOUTH, EAST and
    WEST of the class Directions.
    """
    #The cost for each iteration of the depth should be the depth
    start = SearchNode(state=problem.get_initial_state())
    backward_path = []
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, start, depth, [start.state]) 
        if result == None:
            print("Lower bound of cost:", depth)
        else:
            currNode = result
            while currNode.state != problem.get_initial_state():
                backward_path.append(currNode.action)
                currNode = currNode.parent
                forward_path = list(reversed(backward_path))
            break
    if len(forward_path) == 0:
        print("No Goal found!")
    else:
        return forward_path

