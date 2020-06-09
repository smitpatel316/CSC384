#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files


# RUSH HOUR GOAL TEST
import os

from rushhour import Rushhour, Vehicle
from search import SearchEngine


class BoardHelper:
    def __init__(self, state: Rushhour):
        self.state = state

        goal = state.get_board_properties()
        board_size: (int, int) = goal[0]
        self.total_x = board_size[1]
        self.total_y = board_size[0]

        self.goal_entrance: (int, int) = goal[1]
        self.goal_direction: str = goal[2]
        self.is_entrance_inverted = self.goal_direction in ["E", "S"]

        for vehicle in self.state.vehicle_list:
            if vehicle.is_goal:
                self.goal_vehicle: Vehicle = vehicle

        self.goal_vehicle_tail = self.get_vehicle_tail(self.goal_vehicle)

    def get_vehicle_tail(self, vehicle: Vehicle) -> (int, int):
        head = vehicle.loc
        if vehicle.is_horizontal:
            new_x = head[0] + vehicle.length - 1
            if new_x >= self.total_x:
                new_x -= self.total_x
            return (new_x, head[1])
        else:
            new_y = head[1] + vehicle.length - 1
            if new_y >= self.total_y:
                new_y -= self.total_y
            return (head[0], new_y)

    def is_vehicle_blocking_goal_vehicle(self, vehicle: Vehicle):
        # i = 0 if vertical and 1 if horizontal
        i = int(self.goal_vehicle.is_horizontal)
        if self.goal_vehicle.is_horizontal:
            total = self.total_y
        else:
            total = self.total_x

        vehicle_tail = self.get_vehicle_tail(vehicle)
        if vehicle.loc[i] <= self.goal_vehicle.loc[i] <= vehicle_tail[i]:
            return True
        elif vehicle.length >= total:
            return True
        # # Wrapping
        # elif vehicle_tail[i] < vehicle.loc[i] and (
        #     vehicle.loc[i] <= self.goal_vehicle.loc[i] <= total
        #     or self.goal_vehicle.loc[i] <= vehicle_tail[i]
        # ):
        #     return True
        else:
            return False


def rushhour_goal_fn(state: Rushhour):
    """Have we reached a goal state?"""
    helper = BoardHelper(state)

    if helper.goal_vehicle is None:
        return None

    if helper.is_entrance_inverted:
        return helper.goal_vehicle_tail == helper.goal_entrance
    else:
        return helper.goal_vehicle.loc == helper.goal_entrance


# RUSH HOUR HEURISTICS
def heur_zero(state):
    # IMPLEMENT
    """Zero Heuristic can be used to make A* search perform uniform cost search"""
    return 0  # replace this


def heur_min_moves_wrapper(state, helper=None):
    if helper is None:
        helper = BoardHelper(state)
    if helper.goal_vehicle.is_horizontal:
        goal_vehicle = helper.goal_vehicle.loc[0]
        entrance = helper.goal_entrance[0]
        if helper.is_entrance_inverted:
            goal_vehicle = helper.goal_vehicle_tail[0]
        total = helper.total_x
    else:
        goal_vehicle = helper.goal_vehicle.loc[1]
        entrance = helper.goal_entrance[1]
        if helper.is_entrance_inverted:
            goal_vehicle = helper.goal_vehicle_tail[1]
        total = helper.total_y

    if entrance > goal_vehicle:
        moves_1 = goal_vehicle + total - entrance
        moves_2 = entrance - goal_vehicle
    else:
        moves_1 = goal_vehicle - entrance
        moves_2 = total - goal_vehicle + entrance
    return moves_1, moves_2


def heur_min_moves(state):
    # IMPLEMENT
    """basic rushhour heuristic"""
    # An admissible heuristic is nice to have. Getting to the goal may require
    # many moves and each moves the goal vehicle one tile of distance.
    # Since the board wraps around, there are two different
    # directions that lead to the goal.
    # NOTE that we want an estimate of the number of ADDITIONAL
    #     moves required from our current state
    # 1. Proceeding in the first direction, let MOVES1 =
    #   number of moves required to get to the goal if it were unobstructed
    # 2. Proceeding in the second direction, let MOVES2 =
    #   number of moves required to get to the goal if it were unobstructed
    #
    # Our heuristic value is the minimum of MOVES1 and MOVES2 over all goal vehicles.
    # You should implement this heuristic function exactly, even if it is
    # tempting to improve it.

    return min(*heur_min_moves_wrapper(state))


def heur_alternate(state: Rushhour):
    # IMPLEMENT
    """a better heuristic"""
    """INPUT: a rush hour state"""
    """OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal."""
    # heur_min_moves has an obvious flaw.
    # Write a heuristic function that improves a little upon heur_min_moves to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.
    helper = BoardHelper(state)
    moves_1, moves_2 = heur_min_moves_wrapper(state, helper)

    blocked_1, blocked_2 = 1, 1
    if helper.goal_vehicle.is_horizontal:
        goal_vehicle_x_1 = helper.goal_vehicle.loc[0]
        goal_vehicle_x_2 = helper.goal_vehicle_tail[0]
        entrance_x_1 = helper.goal_entrance[0]
        entrance_x_2 = helper.goal_entrance[0]

        if helper.is_entrance_inverted:
            entrance_x_1 -= helper.goal_vehicle.length - 1
            if entrance_x_1 < 0:
                entrance_x_1 = helper.total_x - entrance_x_1
        else:
            entrance_x_2 += helper.goal_vehicle.length - 1
            if entrance_x_2 >= helper.total_x:
                entrance_x_2 -= helper.total_x

        for vehicle in state.vehicle_list:
            if vehicle.loc != helper.goal_vehicle.loc and not vehicle.is_horizontal:
                # vehicle_tail = helper.get_vehicle_tail(vehicle)
                # if vehicle.loc[1] <= helper.goal_vehicle.loc[1] <= vehicle_tail[1]:
                if helper.is_vehicle_blocking_goal_vehicle(vehicle):
                    if entrance_x_1 > goal_vehicle_x_1:
                        if (
                            vehicle.loc[0] < goal_vehicle_x_1
                            or vehicle.loc[0] > entrance_x_1
                        ):
                            blocked_1 += 1
                    else:
                        if goal_vehicle_x_1 > vehicle.loc[0] > entrance_x_1:
                            blocked_1 += 1
                    if entrance_x_2 > goal_vehicle_x_2:
                        if goal_vehicle_x_2 < vehicle.loc[0] < entrance_x_2:
                            blocked_2 += 1
                    else:
                        if (
                            vehicle.loc[0] > goal_vehicle_x_2
                            or vehicle.loc[0] < entrance_x_2
                        ):
                            blocked_2 += 1
    else:
        goal_vehicle_y_1 = helper.goal_vehicle.loc[1]
        goal_vehicle_y_2 = helper.goal_vehicle_tail[1]
        entrance_y_1 = helper.goal_entrance[1]
        entrance_y_2 = helper.goal_entrance[1]

        if helper.is_entrance_inverted:
            entrance_y_1 -= helper.goal_vehicle.length - 1
            if entrance_y_1 < 0:
                entrance_y_1 = helper.total_y - entrance_y_1
        else:
            entrance_y_2 += helper.goal_vehicle.length - 1
            if entrance_y_2 >= helper.total_y:
                entrance_y_2 -= helper.total_y

        for vehicle in state.vehicle_list:
            if vehicle.loc != helper.goal_vehicle.loc and vehicle.is_horizontal:
                if helper.is_vehicle_blocking_goal_vehicle(vehicle):
                    if entrance_y_1 > goal_vehicle_y_1:
                        if (
                            vehicle.loc[1] < goal_vehicle_y_1
                            or vehicle.loc[1] > entrance_y_1
                        ):
                            blocked_1 += 1
                    else:
                        if goal_vehicle_y_1 > vehicle.loc[1] > entrance_y_1:
                            blocked_1 += 1
                    if entrance_y_2 > goal_vehicle_y_2:
                        if goal_vehicle_y_2 < vehicle.loc[1] < entrance_y_2:
                            blocked_2 += 1
                    else:
                        if (
                            vehicle.loc[1] > goal_vehicle_y_2
                            or vehicle.loc[1] < entrance_y_2
                        ):
                            blocked_2 += 1
    return min(moves_1 + blocked_1, moves_2 + blocked_2)


def fval_function(sN, weight):
    # IMPLEMENT
    """
  Provide a custom formula for f-value computation for Anytime Weighted A star.
  Returns the fval of the state contained in the sNode.

  @param sNode sN: A search node (containing a rush hour state)
  @param float weight: Weight given by Anytime Weighted A star
  @rtype: float
  """

    # Many searches will explore nodes (or states) that are ordered by their f-value.
    # For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    # You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    # The function must return a numeric f-value.
    # The value will determine your state's position on the Frontier list during a 'custom' search.
    # You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return (weight * sN.hval) + sN.gval  # replace this


def anytime_weighted_astar(initial_state, heur_fn, weight=1.0, timebound=10):
    # IMPLEMENT
    """Provides an implementation of anytime weighted a-star, as described in the HW1 handout"""
    """INPUT: a rush hour state that represents the start state and a timebound (number of seconds)"""
    """OUTPUT: A goal state (if a goal is found), else False"""
    """implementation of weighted astar algorithm"""
    time_remaining = timebound
    se = SearchEngine("custom", "full")
    fval_wrap = lambda sN: fval_function(sN, weight)
    se.init_search(initial_state, rushhour_goal_fn, heur_fn, fval_wrap)
    best_solution = float("inf")

    start_time = os.times()[0]
    result = se.search(
        time_remaining, costbound=(float("inf"), float("inf"), best_solution)
    )
    end_time = os.times()[0]

    time_remaining = time_remaining - (end_time - start_time)

    if result:
        best_solution = result.gval + heur_fn(result)
    else:
        return False

    while time_remaining > 0 and not se.open.empty():
        start_time = os.times()[0]
        better_result = se.search(
            time_remaining, (float("inf"), float("inf"), best_solution)
        )
        end_time = os.times()[0]
        time_remaining = time_remaining - (end_time - start_time)
        if better_result:
            best_solution = better_result.gval + heur_fn(better_result)
            result = better_result
        else:
            break

    return result


def anytime_gbfs(initial_state, heur_fn, timebound=10):
    # IMPLEMENT
    """Provides an implementation of anytime greedy best-first search, as described in the HW1 handout"""
    """INPUT: a rush hour state that represents the start state and a timebound (number of seconds)"""
    """OUTPUT: A goal state (if a goal is found), else False"""
    """implementation of anytime greedybfs algorithm"""
    search_engine = SearchEngine("best_first", "full")
    search_engine.init_search(initial_state, rushhour_goal_fn, heur_fn)

    gval_cost_bound = float("inf")
    time_left = timebound

    init_time = os.times()[0]
    solution = search_engine.search(
        timebound=time_left, costbound=(gval_cost_bound, float("inf"), float("inf"))
    )
    finish_time = os.times()[0]

    time_left -= finish_time - init_time

    if solution:
        gval_cost_bound = solution.gval
    else:
        return False

    while time_left > 0:
        init_time = os.times()[0]
        improved_solution = search_engine.search(
            timebound=time_left, costbound=(gval_cost_bound, float("inf"), float("inf"))
        )
        time_left -= os.times()[0] - init_time
        if improved_solution:
            gval_cost_bound = improved_solution.gval
            solution = improved_solution
        else:
            break

    return solution
