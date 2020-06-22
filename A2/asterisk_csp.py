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
from propagators import prop_BT

ASTERISK = [(1, 4), (2, 2), (2, 6), (4, 1), (4, 4), (4, 7), (6, 2), (6, 6), (7, 4)]


def generate_variables(ast_grid):
    csp = CSP("Asterisk Sudoku")
    # variables = [[None] * len(ast_grid) for _ in range(len(ast_grid))]
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


def asterisk_csp_model_1_other_way(ast_grid):
    csp, variables = generate_variables(ast_grid)
    for (row_i, row) in enumerate(ast_grid):
        for (col_i, elem) in enumerate(row):
            # Constraint downwards
            if row_i + 1 < len(ast_grid):
                var_1 = variables[row_i][col_i]
                var_2 = variables[row_i + 1][col_i]
                constraint = Constraint(
                    f"({row_i},{col_i}),({row_i+1},{col_i})", [var_1, var_2]
                )
                constraint.add_satisfying_tuples(generate_diff_perms(var_1, var_2))
                csp.add_constraint(constraint)

            # Constraint to the right
            if col_i + 1 < len(row):
                var_1 = variables[row_i][col_i]
                var_2 = variables[row_i][col_i + 1]
                constraint = Constraint(
                    f"({row_i},{col_i}),({row_i},{col_i+1})", [var_1, var_2]
                )
                constraint.add_satisfying_tuples(generate_diff_perms(var_1, var_2))
                csp.add_constraint(constraint)

    for i in range(1, len(ASTERISK)):
        cell_1 = ASTERISK[i - 1]
        cell_2 = ASTERISK[i]
        var_1 = variables[cell_1[0]][cell_1[1]]
        var_2 = variables[cell_2[0]][cell_2[1]]
        constraint = Constraint(
            f"({cell_1[0]},{cell_1[1]}),({cell_2[0]},{cell_2[1]}", [var_1, var_2]
        )
        constraint.add_satisfying_tuples(generate_diff_perms(var_1, var_2))
        csp.add_constraint(constraint)
    return csp, variables


def asterisk_csp_model_1(ast_grid):
    csp, variables = generate_variables(ast_grid)
    seen = {}
    for (row_i, row) in enumerate(variables):
        for (col_i, var) in enumerate(row):
            for row_j in range(row_i+1, len(ast_grid)):
                if f"({row_i},{col_i}),({row_j},{col_i})" not in seen:
                    constraint = Constraint(
                        f"({row_i},{col_i}),({row_j},{col_i})", [var, variables[row_j][col_i]]
                    )
                    constraint.add_satisfying_tuples(generate_diff_perms(var, variables[row_j][col_i]))
                    csp.add_constraint(constraint)
                    seen[f"({row_i},{col_i}),({row_j},{col_i})"] = True

            for col_j in range(col_i+1, len(row)):
                if f"({row_i},{col_i}),({row_i},{col_j})" not in seen:
                    constraint = Constraint(
                        f"({row_i},{col_i}),({row_i},{col_j})", [var, variables[row_i][col_j]]
                    )
                    constraint.add_satisfying_tuples(generate_diff_perms(var, variables[row_i][col_j]))
                    csp.add_constraint(constraint)
                    seen[f"({row_i},{col_i}),({row_i},{col_j})"] = True
            for i in range(int(row_i / 3) * 3, (int(row_i / 3) + 1) * 3):
                for j in range(int(col_i / 3) * 3, (int(col_i / 3) + 1) * 3):
                    if i != row_i and j != col_i and f"({row_i},{col_i}),({i},{j})" not in seen:
                        constraint = Constraint(f"({row_i},{col_i}),({i},{j})", [var, variables[i][j]])
                        constraint.add_satisfying_tuples(generate_diff_perms(var, variables[i][j]))
                        csp.add_constraint(constraint)
                        seen[f"({row_i},{col_i}),({i},{j})"] = True
            for (i, asterisk) in enumerate(ASTERISK):
                for j in range(i+1, len(ASTERISK)):
                    if f"({asterisk[0]},{asterisk[1]}),({ASTERISK[j][0]},{ASTERISK[j][1]})" not in seen:
                        var_1 = variables[asterisk[0]][asterisk[1]]
                        var_2 = variables[ASTERISK[j][0]][ASTERISK[j][1]]
                        constraint = Constraint(
                            f"({asterisk[0]},{asterisk[1]}),({ASTERISK[j][0]},{ASTERISK[j][1]})", [var_1, var_2]
                        )
                        constraint.add_satisfying_tuples(generate_diff_perms(var_1, var_2))
                        csp.add_constraint(constraint)
                        seen[f"({asterisk[0]},{asterisk[1]}),({ASTERISK[j][0]},{ASTERISK[j][1]})"] = True
    return csp, variables
def asterisk_csp_model_2(ast_grid):
    ##IMPLEMENT
    pass


if __name__ == "__main__":
    grid_1 = [
        [None, 1, None, None, None, None, None, 6, None],
        [3, None, 9, None, None, None, 1, None, 5],
        [None, 8, None, 3, None, 5, None, 7, None],
        [None, None, 2, None, 7, None, 8, None, None],
        [None, None, None, 6, None, 8, None, None, None],
        [None, None, 8, None, 9, None, 2, None, None],
        [None, 2, None, 4, None, 1, None, 9, None],
        [9, None, 4, None, None, None, 6, None, 1],
        [None, 3, None, None, None, None, None, 8, None],
    ]

    csp, var_array = asterisk_csp_model_1(grid_1)
    cons = csp.get_all_cons()
    bin_flag = True
    for c in cons:
        if len(c.get_scope()) != 2:
            bin_flag = False
            print("Non binary constraint")
            break
        print(c.get_scope())