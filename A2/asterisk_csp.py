# Look for #IMPLEMENT tags in this file.
"""
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = asterisk_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the asterisk puzzle.

1. asterisk_csp_model_1 (worth 20/100 marks)
    - A model of an Asterisk grid built using only 
      binary not-equal constraints

2. asterisk_csp_model_2 (worth 20/100 marks)
    - A model of an Asterisk grid built using only 9-ary 
      all-different constraints

"""
from cspbase import *
import itertools

ASTERISK = [(1, 4), (2, 2), (2, 6), (4, 1), (4, 4), (4, 7), (6, 2), (6, 6), (7, 4)]


def generate_variables(ast_grid):
    csp = CSP("Asterisk Sudoku")
    variables = list()
    for (row_i, row) in enumerate(ast_grid):
        row_variables = list()
        for (col_i, elem) in enumerate(row):
            var = Variable(f"{row_i},{col_i}", [])
            if elem is None:
                var.add_domain_values(range(1, 10))
            else:
                var.add_domain_values([elem])
            csp.add_var(var)
            row_variables.append(var)
        variables.append(row_variables)
    return csp, variables


def generate_diff_perms(v1: Variable, v2: Variable):
    return [
        [val1, val2]
        for val1 in v1.cur_domain()
        for val2 in v2.cur_domain()
        if val1 != val2
    ]


def generate_all_diff(variables):
    tuples = []
    for combination in itertools.product(*[var.cur_domain() for var in variables]):
        if len(set(combination)) == len(combination):
            tuples.append(combination)
    return tuples


def asterisk_csp_model_1(ast_grid):
    csp, variables = generate_variables(ast_grid)
    seen = {}
    for (row_i, row) in enumerate(variables):
        for (col_i, var) in enumerate(row):
            for row_j in range(row_i + 1, len(ast_grid)):
                if f"({row_i},{col_i}),({row_j},{col_i})" not in seen:
                    constraint = Constraint(
                        f"({row_i},{col_i}),({row_j},{col_i})",
                        [var, variables[row_j][col_i]],
                    )
                    constraint.add_satisfying_tuples(
                        generate_diff_perms(var, variables[row_j][col_i])
                    )
                    csp.add_constraint(constraint)
                    seen[f"({row_i},{col_i}),({row_j},{col_i})"] = True

            for col_j in range(col_i + 1, len(row)):
                if f"({row_i},{col_i}),({row_i},{col_j})" not in seen:
                    constraint = Constraint(
                        f"({row_i},{col_i}),({row_i},{col_j})",
                        [var, variables[row_i][col_j]],
                    )
                    constraint.add_satisfying_tuples(
                        generate_diff_perms(var, variables[row_i][col_j])
                    )
                    csp.add_constraint(constraint)
                    seen[f"({row_i},{col_i}),({row_i},{col_j})"] = True
            for i in range(int(row_i / 3) * 3, (int(row_i / 3) + 1) * 3):
                for j in range(int(col_i / 3) * 3, (int(col_i / 3) + 1) * 3):
                    if (
                        i != row_i
                        and j != col_i
                        and f"({row_i},{col_i}),({i},{j})" not in seen
                    ):
                        constraint = Constraint(
                            f"({row_i},{col_i}),({i},{j})", [var, variables[i][j]]
                        )
                        constraint.add_satisfying_tuples(
                            generate_diff_perms(var, variables[i][j])
                        )
                        csp.add_constraint(constraint)
                        seen[f"({row_i},{col_i}),({i},{j})"] = True
            for (i, asterisk) in enumerate(ASTERISK):
                for j in range(i + 1, len(ASTERISK)):
                    if (
                        f"({asterisk[0]},{asterisk[1]}),({ASTERISK[j][0]},{ASTERISK[j][1]})"
                        not in seen
                    ):
                        var_1 = variables[asterisk[0]][asterisk[1]]
                        var_2 = variables[ASTERISK[j][0]][ASTERISK[j][1]]
                        constraint = Constraint(
                            f"({asterisk[0]},{asterisk[1]}),({ASTERISK[j][0]},{ASTERISK[j][1]})",
                            [var_1, var_2],
                        )
                        constraint.add_satisfying_tuples(
                            generate_diff_perms(var_1, var_2)
                        )
                        csp.add_constraint(constraint)
                        seen[
                            f"({asterisk[0]},{asterisk[1]}),({ASTERISK[j][0]},{ASTERISK[j][1]})"
                        ] = True
    return csp, variables


def asterisk_csp_model_2(ast_grid):
    csp, variables = generate_variables(ast_grid)

    for (row_i, row) in enumerate(variables):
        constraint = Constraint(f"Row: {row_i}", row)
        constraint.add_satisfying_tuples(generate_all_diff(row))
        csp.add_constraint(constraint)

    for col_i in range(len(variables[0])):
        col = []
        for row_i in range(len(variables)):
            col.append(variables[row_i][col_i])
        constraint = Constraint(f"Column: {col_i}", col)
        constraint.add_satisfying_tuples(generate_all_diff(col))
        csp.add_constraint(constraint)

    squares = [(1, 1), (4, 1), (7, 1), (1, 4), (4, 4), (7, 4), (1, 7), (4, 7), (7, 7)]
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    for (i, square) in enumerate(squares):
        scope = [variables[square[0]][square[1]]]
        for direction in directions:
            scope.append(variables[direction[0] + square[0]][direction[1] + square[1]])
        constraint = Constraint(f"Square: {i}", scope)
        constraint.add_satisfying_tuples(generate_all_diff(scope))
        csp.add_constraint(constraint)

    scope = []
    for asterisk in ASTERISK:
        scope.append(variables[asterisk[0]][asterisk[1]])
    constraint = Constraint("Asterisk", scope)
    constraint.add_satisfying_tuples(generate_all_diff(scope))
    csp.add_constraint(constraint)
    return csp, variables
