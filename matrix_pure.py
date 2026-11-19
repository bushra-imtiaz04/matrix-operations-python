"""
3x3 Matrix Operations - PURE PYTHON version (no NumPy)
Run:  python matrix_pure.py          (interactive menu)
      python matrix_pure.py --demo   (fixed demo matrices, no input needed)
"""
import sys

SIZE = 3


# ---------- helpers ----------
def read_matrix(name):
    """Read a 3x3 matrix from the keyboard, row by row."""
    print(f"Enter matrix {name} ({SIZE} rows, {SIZE} numbers each, space separated):")
    matrix = []
    for i in range(SIZE):
        while True:
            try:
                row = [float(x) for x in input(f"  Row {i + 1}: ").split()]
                if len(row) != SIZE:
                    raise ValueError
                matrix.append(row)
                break
            except ValueError:
                print(f"  Invalid input. Enter exactly {SIZE} numbers.")
    return matrix


def show(title, matrix):
    """Pretty-print a matrix."""
    print(f"\n{title}")
    for row in matrix:
        print("  [ " + "  ".join(f"{v + 0.0:9.3f}" for v in row) + " ]")  # +0.0 turns -0.0 into 0.0


# ---------- operations (all written with loops) ----------
def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(SIZE)] for i in range(SIZE)]


def subtract(a, b):
    return [[a[i][j] - b[i][j] for j in range(SIZE)] for i in range(SIZE)]


def scalar_multiply(a, k):
    return [[a[i][j] * k for j in range(SIZE)] for i in range(SIZE)]


def multiply(a, b):
    result = [[0.0] * SIZE for _ in range(SIZE)]
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                result[i][j] += a[i][k] * b[k][j]
    return result


def transpose(a):
    return [[a[j][i] for j in range(SIZE)] for i in range(SIZE)]


def determinant(a):
    # Cofactor expansion along the first row
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


def trace(a):
    return sum(a[i][i] for i in range(SIZE))


def inverse(a):
    """Inverse = adjugate / determinant. Returns None if matrix is singular."""
    det = determinant(a)
    if abs(det) < 1e-12:
        return None
    cof = [[0.0] * SIZE for _ in range(SIZE)]
    for i in range(SIZE):
        for j in range(SIZE):
            # minor = 2x2 matrix left after removing row i and column j
            minor = [[a[r][c] for c in range(SIZE) if c != j]
                     for r in range(SIZE) if r != i]
            m_det = minor[0][0] * minor[1][1] - minor[0][1] * minor[1][0]
            cof[i][j] = ((-1) ** (i + j)) * m_det
    adj = transpose(cof)
    return scalar_multiply(adj, 1.0 / det)


# ---------- CLI ----------
MENU = """
===== 3x3 MATRIX CALCULATOR (Pure Python) =====
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
    A = [[2, 1, 3], [0, 4, 1], [5, 2, 6]]
    B = [[1, 0, 2], [3, 1, 0], [4, 5, 1]]
    print("===== DEMO: Pure Python =====")
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
