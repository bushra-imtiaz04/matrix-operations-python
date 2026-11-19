"""
Verifies both versions give the same answers and benchmarks them.
Run:  python compare.py
"""
import random
import timeit
import numpy as np
import matrix_pure as P
import matrix_numpy as N


def close(pure, npy):
    return np.allclose(np.array(pure, dtype=float), np.array(npy, dtype=float), atol=1e-9)


def main():
    random.seed(7)
    tests = 200
    ok = {k: 0 for k in ["add", "sub", "mul", "T", "det", "inv", "trace"]}
    for _ in range(tests):
        a = [[random.randint(-9, 9) for _ in range(3)] for _ in range(3)]
        b = [[random.randint(-9, 9) for _ in range(3)] for _ in range(3)]
        na, nb = np.array(a), np.array(b)
        ok["add"] += close(P.add(a, b), N.add(na, nb))
        ok["sub"] += close(P.subtract(a, b), N.subtract(na, nb))
        ok["mul"] += close(P.multiply(a, b), N.multiply(na, nb))
        ok["T"] += close(P.transpose(a), N.transpose(na))
        ok["det"] += abs(P.determinant(a) - N.determinant(na)) < 1e-6
        ok["trace"] += abs(P.trace(a) - N.trace(na)) < 1e-9
        pi, ni = P.inverse(a), N.inverse(na)
        ok["inv"] += (pi is None and ni is None) or (pi is not None and ni is not None and close(pi, ni))

    print(f"Correctness check on {tests} random 3x3 matrices")
    print(f"{'Operation':<10}{'Matches':>10}")
    for k, v in ok.items():
        print(f"{k:<10}{v:>7}/{tests}")

    A = [[2, 1, 3], [0, 4, 1], [5, 2, 6]]
    B = [[1, 0, 2], [3, 1, 0], [4, 5, 1]]
    nA, nB = np.array(A), np.array(B)
    n = 20000
    print(f"\nBenchmark ({n} runs each, seconds, lower = faster)")
    print(f"{'Operation':<10}{'Pure':>10}{'NumPy':>10}")
    for name, fp, fn in [
        ("add", lambda: P.add(A, B), lambda: N.add(nA, nB)),
        ("multiply", lambda: P.multiply(A, B), lambda: N.multiply(nA, nB)),
        ("det", lambda: P.determinant(A), lambda: N.determinant(nA)),
        ("inverse", lambda: P.inverse(A), lambda: N.inverse(nA)),
    ]:
        tp = timeit.timeit(fp, number=n)
        tn = timeit.timeit(fn, number=n)
        print(f"{name:<10}{tp:>10.4f}{tn:>10.4f}")


if __name__ == "__main__":
    main()
