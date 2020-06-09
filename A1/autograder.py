import os
import pickle

# import student's functions
from solution import *
from rushhour import *

# Select what to test
test_min_moves = True
test_fval_function = True
test_alternate = True
test_anytime_gbfs = True
test_anytime_weighted_astar = True

# load the test problems
TESTPROBLEMS = []
with (open("rushhour_tests.pkl", "rb")) as openfile:
    while True:
        try:
            TESTPROBLEMS.append(pickle.load(openfile))
        except EOFError:
            break

if test_min_moves:

    ##############################################################
    # TEST MIN MOVES HEURISTIC
    print('TESTING MIN MOVES')
    PROBLEMS = TESTPROBLEMS[40:]

    # Correct MIN MOVES distances for the initial states of the provided problem set
    correct_min_moves = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 7, 10, 14, 14, 17, 24, 28, 31, 29];

    solved = 0;
    unsolved = [];

    for i in range(0, len(PROBLEMS)):
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]

        min_moves = heur_min_moves(s0)
        print('calculated min_moves:', str(min_moves))
        # To see state uncomment below
        # print(s0.state_string())

        if min_moves == correct_min_moves[i]:
            solved += 1
        else:
            unsolved.append(i)

    print("*************************************")
    print("In the problem set provided, you calculated the correct Min Moves distance for {} states out of {}.".format(
        solved, len(PROBLEMS)))
    print("States that were incorrect: {}".format(unsolved))
    print("*************************************\n")
    ##############################################################

if test_alternate:

    ##############################################################
    # TEST ALTERNATE HEURISTIC
    print('Testing alternate heuristic with best_first search')

    benchmark = 15;
    solved = 0;
    unsolved = [];
    timebound = 1  # time limit

    PROBLEMS = TESTPROBLEMS[20:40]

    for i in range(0, len(PROBLEMS)):

        print("*************************************")
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]  # Problems get harder as i gets bigger
        se = SearchEngine('best_first', 'full')
        se.init_search(s0, goal_fn=rushhour_goal_fn, heur_fn=heur_alternate)
        final = se.search(timebound)

        if final:
            solved += 1
        else:
            unsolved.append(i)

    print("\n*************************************")
    print("Of {} initial problems, {} were solved in less than {} seconds by this solver.".format(len(PROBLEMS), solved,
                                                                                                  timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print(
        "Heur min moves alone solved {} out of {} practice problems given {} seconds.".format(benchmark, len(PROBLEMS),
                                                                                              timebound))
    print("*************************************\n")
    ##############################################################

if test_fval_function:

    test_state = Rushhour("START", 6, None, None, None)

    correct_fvals = [6, 11, 16, 1006]

    ##############################################################
    # TEST fval_function
    print("*************************************")
    print('Testing fval_function')

    solved = 0
    weights = [0., .5, 1., 100]
    for i in range(len(weights)):

        test_node = sNode(test_state, hval=10, fval_function=fval_function)

        fval = fval_function(test_node, weights[i])
        print('Test', str(i), 'calculated fval:', str(fval), 'correct:', str(correct_fvals[i]))

        if fval == correct_fvals[i]:
            solved += 1

    print("\n*************************************")
    print("Your fval_function calculated the correct fval for {} out of {} tests.".format(solved, len(correct_fvals)))
    print("*************************************\n")
    ##############################################################

if test_anytime_gbfs:

    ##############################################################
    # TEST ANYTIME GBFS
    print('Testing Anytime GBFS')

    improved = 0;
    same = 0;
    worsened = 0;
    solved = 0;
    unsolved = [];
    timebound1 = 1;
    timebound2 = 5;  # 1 second vs 5 seconds
    PROBLEMS = TESTPROBLEMS[20:40]  # first ones are too easy!

    for i in range(0, len(PROBLEMS)):

        print("*************************************")
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]  # Problems get harder as i gets bigger
        final1 = anytime_gbfs(s0, heur_fn=heur_min_moves, timebound=timebound1)
        final2 = anytime_gbfs(s0, heur_fn=heur_min_moves, timebound=timebound2)

        if not final2 and not final1:
            print("Problem {}: not solveable with more time (no solution vs. no solution).".format(i))
            unsolved.append(i)
        elif final1 and not final2:
            worsened += 1
            print("Problem {}: ERROR -- not solveable with more time ({} vs. no solution).".format(i, final1.gval))
        elif final2 and not final1:
            solved += 1
            print("Problem {}: solveable with more time (no solution vs. {}).".format(i, final2.gval))
        elif final2.gval == final1.gval:
            same += 1
            print("Problem {}: same with more time (length {} vs. {}).".format(i, final1.gval, final2.gval))
        elif final2.gval < final1.gval:
            improved += 1
            print("Problem {}: improved with more time (length {} vs. {}).".format(i, final1.gval, final2.gval))
        else:
            worsened += 1
            print("Problem {}: ERROR -- longer solution with more time (length {} vs. {}).".format(i, final1.gval,
                                                                                                   final2.gval))

    print("\n*************************************")
    print(
        "More time allows {} unsolved problems to be solved, improved solution lengths of {} problems, produced equal length solutions for {} problems.".format(
            solved, improved, same))
    print("More time worsened {} solution lengths".format(worsened))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("*************************************\n")

if test_anytime_weighted_astar:

    ##############################################################
    # TEST ANYTIME WEIGHTED A STAR
    print('Testing Anytime Weighted A Star')

    improved = 0;
    same = 0;
    worsened = 0;
    solved = 0;
    unsolved = [];
    timebound1 = 1;
    timebound2 = 5;  # 1 second vs 5 seconds
    PROBLEMS = TESTPROBLEMS[20:40]  # first ones are too easy!

    for i in range(0, len(PROBLEMS)):
        print("*************************************")
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]  # Problems get harder as i gets bigger
        weight = 100
        final1 = anytime_weighted_astar(s0, heur_fn=heur_min_moves, weight=weight, timebound=timebound1)
        final2 = anytime_weighted_astar(s0, heur_fn=heur_min_moves, weight=weight, timebound=timebound2)

        if not final2 and not final1:
            print("Problem {}: not solveable with more time (no solution vs. no solution).".format(i))
            unsolved.append(i)
        elif final1 and not final2:
            worsened += 1
            print("Problem {}: ERROR -- not solveable with more time ({} vs. no solution).".format(i, final1.gval))
        elif final2 and not final1:
            solved += 1
            print("Problem {}: solveable with more time (no solution vs. {}).".format(i, final2.gval))
        elif final2.gval == final1.gval:
            same += 1
            print("Problem {}: same with more time (length {} vs. {}).".format(i, final1.gval, final2.gval))
        elif final2.gval < final1.gval:
            improved += 1
            print("Problem {}: improved with more time (length {} vs. {}).".format(i, final1.gval, final2.gval))
        else:
            worsened += 1
            print("Problem {}: ERROR -- longer solution with more time (length {} vs. {}).".format(i, final1.gval,
                                                                                                   final2.gval))

    print("\n*************************************")
    print(
        "More time allows {} unsolved problems to be solved, improved solution lengths of {} problems, produced equal length solutions for {} problems.".format(
            solved, improved, same))
    print("More time worsened {} solution lengths".format(worsened))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("*************************************\n")

    ##############################################################
