# minimax_agent.py
# --------------
# COMP2050 Artificial Intelligence

"""
    Enter your details below:

    Name: Dao Duc Thinh
    Student ID: V202100511
    Email: 21thinh.dd@vinuni.edu.vn
"""

from typing import Tuple

from agents import Agent
from game_engine.actions import Directions
from search_problems import AdversarialSearchProblem
import math
import copy

Position = Tuple[int, int]
Positions = Tuple[Position]
State = Tuple[int, Position, Position, Positions, float, float]


class MinimaxAgent(Agent):
    """ The agent you will implement to compete with the black bird to try and
        save as many yellow birds as possible. """

    def __init__(self, max_player, depth="2"):
        """ Make a new Adversarial agent with the optional depth argument.
        """
        self.max_player = max_player
        self.depth = int(depth)

    def evaluation(self, problem: AdversarialSearchProblem, state: State) -> float:
        """
            (MinimaxAgent, AdversarialSearchProblem,
                (int, (int, int), (int, int), ((int, int)), number, number))
                    -> number
        """
        player, red_pos, black_pos, yellow_birds, score, yb_score = state
        """ 
        Encourage the agent to go to the state with the most potential to eat the most number of remaining yellow_birds. 
        We have the assumption that if red bird is closer to some yellow birds, then these yellow birds will be eaten by red birds in the
        future. To the contrary, if the black bird is closer to the yellow bird, the black bird is assumed to eat it in the future (in fact
        it aligns with its greedy approach). So we should include the score for yellow birds into the score for the current state. 

        For map aiDenseAdversarial: Uncomment line 66, then we can get the score of 1034! The idea is as follows: As the red bird has eaten a yellow bird, then it will move to that location, so we updated the red_bird position to yellow_bird position. We
        don't update the location of the black bird because that would complicates the problem, since while black bird moves to the new position,
        red bird must also move to somewhere. Also, we only want to update the location of red bird because we are optimistic that it will
        eat the bird. However, because this idea only works well for complex matrix, it doesn't work for the testAdversarial map.

        To avoid being captured, we only care when the red bird is close to black bird: dist(red_pos, black_pos) <= 3. Since we encourage that
        the red bird move to the location of yellow bird that is far of black bird, the threshold of 3 is enough and also guarantee high score!.
        """

        black_dist = problem.maze_distance(red_pos, black_pos)
        # if black_dist == 0:
        #     return -math.inf
        if problem.terminal_test(state):
            return math.inf

        addition = 0
        for goal in yellow_birds:
            red_dist = problem.maze_distance(red_pos, goal)
            black_dist = problem.maze_distance(black_pos, goal)
            if red_dist < black_dist:
                addition += math.pow(0.99, red_dist) * yb_score * 1/red_dist
                red_pos = goal
        
        if problem.maze_distance(red_pos, black_pos) < 2:
            if problem.get_maximizing_player() == problem.opponent(state):
                score += 250 
            else:
                score -= 250 
        return score + addition

    def maximize(self, problem: AdversarialSearchProblem, state: State,
                 current_depth: int, alpha=float('-inf'), beta=float('inf')) -> Tuple[float, str]:
        """ This method should return a pair (max_utility, max_action).
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.
        """
        if current_depth == self.depth:
            return (self.evaluation(problem, state), Directions.STOP)
        if problem.terminal_test(state):
            return (problem.utility(state), Directions.STOP)
        util = -math.inf
        best_action = None

        for next_state, action, _ in problem.get_successors(state):
            v = self.minimize(problem, next_state, current_depth + 1, alpha=alpha, beta=beta)
            if v > util:
                util = v
                best_action = action
            if util >= beta:
                return (util, action)
            alpha = max(alpha, util)
        return (util, best_action)

    def minimize(self, problem: AdversarialSearchProblem, state: State,
                 current_depth: int, alpha=float('-inf'), beta=float('inf')) -> float:
        """ This function should just return the minimum utility.
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.
        """
        if current_depth == self.depth:
            return self.evaluation(problem, state)
        if problem.terminal_test(state) or current_depth == self.depth:
            return problem.utility(state)
        util = math.inf

        for next_state, action, _ in problem.get_successors(state):
            v = self.maximize(problem, next_state, current_depth + 1, alpha=alpha, beta=beta)[0]
            util = min(util, v)
            if util <= alpha:
                return util
            beta = min(beta, util)
        return util

    def get_action(self, game_state):
        """ This method is called by the system to solicit an action from
            MinimaxAgent. It is passed in a State object.

            Like with all of the other search problems, we have abstracted
            away the details of the game state by producing a SearchProblem.
            You will use the states of this AdversarialSearchProblem to
            implement your minimax procedure. The details you need to know
            are explained at the top of this file.
        """
        # We tell the search problem what the current state is and which player
        # is the maximizing player (i.e. who's turn it is now).
        problem = AdversarialSearchProblem(game_state, self.max_player)
        state = problem.get_initial_state()
        utility, max_action = self.maximize(problem, state, 0)
        print("At Root: Utility:", utility, "Action:",
              max_action, "Expanded:", problem._expanded)
        return max_action
