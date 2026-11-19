"""
3x3 Matrix Operations - NUMPY version
Run:  python matrix_numpy.py          (interactive menu)
      python matrix_numpy.py --demo   (fixed demo matrices, no input needed)
Install:  pip install numpy
"""
import sys
import numpy as np

SIZE = 3


# ---------- helpers ----------
def read_matrix(name):
    """Read a 3x3 matrix from the keyboard, row by row."""
    print(f"Enter matrix {name} ({SIZE} rows, {SIZE} numbers each, space separated):")
    rows = []
    for i in range(SIZE):
        while True:
            try:
                row = [float(x) for x in input(f"  Row {i + 1}: ").split()]
                if len(row) != SIZE:
                    raise ValueError
                rows.append(row)
                break
            except ValueError:
                print(f"  Invalid input. Enter exactly {SIZE} numbers.")
    return np.array(rows)


def show(title, matrix):
    """Pretty-print a matrix."""
    print(f"\n{title}")
    for row in matrix:
        print("  [ " + "  ".join(f"{v:9.3f}" for v in row) + " ]")


# ---------- operations (one NumPy call each) ----------
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def scalar_multiply(a, k):
    return a * k


def multiply(a, b):
    return a @ b            # same as np.matmul(a, b)


def transpose(a):
    return a.T


def determinant(a):
    return np.linalg.det(a)


def trace(a):
    return np.trace(a)


def inverse(a):
    """Returns None if matrix is singular."""
    if abs(np.linalg.det(a)) < 1e-12:
        return None
    return np.linalg.inv(a)


# ---------- CLI ----------
MENU = """
===== 3x3 MATRIX CALCULATOR (NumPy) =====
 1. Add            (A + B)
 2. Subtract       (A - B)
 3. Multiply       (A x B)
 4. Scalar multiply (k x A)
 5. Transpose      (A^T)
 6. Determinant    (|A|)
 7. Inverse        (A^-1)
 8. Trace          (tr A)
 0. Exit
"""


def interactive():
    while True:
        print(MENU)
        choice = input("Choose option: ").strip()
        if choice == "0":
            print("Bye!")
            break
        if choice not in "12345678" or choice == "":
            print("Invalid option.")
            continue
        a = read_matrix("A")
        if choice in "123":
            b = read_matrix("B")
        if choice == "1":
            show("A + B =", add(a, b))
        elif choice == "2":
            show("A - B =", subtract(a, b))
        elif choice == "3":
            show("A x B =", multiply(a, b))
        elif choice == "4":
            k = float(input("Enter scalar k: "))
            show(f"{k} x A =", scalar_multiply(a, k))
        elif choice == "5":
            show("A^T =", transpose(a))
        elif choice == "6":
            print(f"\n|A| = {determinant(a):.3f}")
        elif choice == "7":
            inv = inverse(a)
            if inv is None:
                print("\nMatrix is singular (determinant = 0), inverse does not exist.")
            else:
                show("A^-1 =", inv)
        elif choice == "8":
            print(f"\ntrace(A) = {trace(a):.3f}")


def demo():
    A = np.array([[2, 1, 3], [0, 4, 1], [5, 2, 6]])
    B = np.array([[1, 0, 2], [3, 1, 0], [4, 5, 1]])
    print("===== DEMO: NumPy =====")
    show("Matrix A", A)
    show("Matrix B", B)
    show("A + B", add(A, B))
    show("A - B", subtract(A, B))
    show("A x B", multiply(A, B))
    show("2 x A", scalar_multiply(A, 2))
    show("Transpose of A", transpose(A))
    print(f"\nDeterminant of A = {determinant(A):.3f}")
    print(f"Trace of A       = {trace(A):.3f}")
    show("Inverse of A", inverse(A))


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else interactive()
