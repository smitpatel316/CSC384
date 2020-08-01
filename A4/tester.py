from bnetbase import *

if __name__ == "__main__":
    print("Testing Multiply Factors")
    a = Variable("A", [True, False])
    b = Variable("B", [True, False])
    c = Variable("C", [True, False])
    F1 = Factor("F1", [a, b])
    F1.add_values(
        [[True, True, 0.9], [True, False, 0.1], [False, True, 0.4], [False, False, 0.6]]
    )
    F2 = Factor("F2", [b, c])
    F2.add_values(
        [[True, True, 0.7], [True, False, 0.3], [False, True, 0.8], [False, False, 0.2]]
    )
    F3 = multiply_factors([F1, F2])
    F3.print_table()

