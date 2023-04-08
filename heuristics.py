# heuristics.py
# ----------------
# COMP2050 Artificial Intelligence

""" This class contains heuristics which are used for the search procedures that
    you write in search_strategies.py.

    The first part of the file contains heuristics to be used with the algorithms
    that you will write in search_strategies.py.

    In the second part you will write a heuristic for Q4 to be used with a
    MultiplePositionSearchProblem.
"""

from typing import Tuple
import heapq

from search_problems import (MultiplePositionSearchProblem,
                             PositionSearchProblem)

Position = Tuple[int, int]
YellowBirds = Tuple[Position]
State = Tuple[Position, YellowBirds]

# -------------------------------------------------------------------------------
# A set of heuristics which are used with a PositionSearchProblem
# You do not need to modify any of these.
# -------------------------------------------------------------------------------


def null_heuristic(pos: Position, problem: PositionSearchProblem) -> int:
    """The null heuristic. It is fast but uninformative. It always returns 0"""

    return 0


def manhattan_heuristic(pos: Position, problem: PositionSearchProblem) -> int:
    """The Manhattan distance heuristic for a PositionSearchProblem."""

    return abs(pos[0] - problem.goal_pos[0]) + abs(pos[1] - problem.goal_pos[1])


def euclidean_heuristic(pos: Position, problem: PositionSearchProblem) -> float:
    """The Euclidean distance heuristic for a PositionSearchProblem"""

    return ((pos[0] - problem.goal_pos[0]) ** 2 + (pos[1] - problem.goal_pos[1]) ** 2) ** 0.5


# Abbreviations
null = null_heuristic
manhattan = manhattan_heuristic
euclidean = euclidean_heuristic

# -------------------------------------------------------------------------------
# You have to implement the following heuristics for Q4 of the homework.
# It is used with a MultiplePositionSearchProblem
# -------------------------------------------------------------------------------

# You can make helper functions here, if you need them


def bird_counting_heuristic(state: State,
                            problem: MultiplePositionSearchProblem) -> float:
    position, yellow_birds = state
    heuristic_value = 0

    """ *** YOUR CODE HERE *** """
    heuristic_value = len(state[1])
    return heuristic_value


bch = bird_counting_heuristic




def every_bird_heuristic(state: State,
                         problem: MultiplePositionSearchProblem) -> float:
    position, yellow_birds = state
    heuristic_value = 0
    """
    Implement Minimum Spanning Tree (MST) heuristics. Because MST is the tree with minimum possible weight, it is 
    guaranteed to be an admissible heuristics.
    """
    agent_loc = state[0]
    goals = set(state[1])

    def MST_weight(state, vertices):
        "Use Prim's algorithm to compute the total weight of MST"
        visited = set()
        key = dict()
        key[state] = 0
        total_weight = 0

        heap = []
        heapq.heapify(heap)
        heapq.heappush(heap, (key[state], state))

        while len(visited) != len(vertices) + 1:
            element = heapq.heappop(heap)
            node = element[1]
            weight = element[0]

            if node not in visited: 
                visited.add(node)
                total_weight += weight
            
            for vertice in vertices:
                if vertice not in visited:
                    dist = problem.maze_distance(node, vertice)
                    if vertice not in key or key[vertice] > dist:
                        key[vertice] = dist
                    heapq.heappush(heap, (key[vertice], vertice))
        return total_weight

    return MST_weight(agent_loc, goals) 







every_bird = every_bird_heuristic
