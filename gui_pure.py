"""
3x3 Matrix Calculator - GUI, PURE PYTHON version (no NumPy)
Needs matrix_pure.py in the same folder.   Run:  python gui_pure.py
"""
import tkinter as tk
from tkinter import messagebox
import matrix_pure as M          # all maths comes from the pure-Python module

SIZE = 3


class MatrixApp:
    def __init__(self, root):
        self.root = root
        root.title("3x3 Matrix Calculator - Pure Python (no NumPy)")
        root.resizable(False, False)

        # ---- input grids: Matrix A and Matrix B ----
        top = tk.Frame(root, padx=12, pady=10)
        top.pack()
        self.a_cells = self.make_grid(top, "Matrix A", 0)
        self.b_cells = self.make_grid(top, "Matrix B", 1)

        # ---- scalar input ----
        sc = tk.Frame(root)
        sc.pack(pady=(0, 6))
        tk.Label(sc, text="Scalar k:").pack(side="left")
        self.k_entry = tk.Entry(sc, width=6, justify="center")
        self.k_entry.insert(0, "2")
        self.k_entry.pack(side="left", padx=6)

        # ---- operation buttons ----
        ops = [
            ("A + B", lambda: self.run("A + B", True, M.add)),
            ("A - B", lambda: self.run("A - B", True, M.subtract)),
            ("A x B", lambda: self.run("A x B", True, M.multiply)),
            ("k x A", self.run_scalar),
            ("Transpose A", lambda: self.run("Transpose of A", False, M.transpose)),
            ("Determinant A", lambda: self.run("Determinant of A", False, M.determinant)),
            ("Inverse A", self.run_inverse),
            ("Trace A", lambda: self.run("Trace of A", False, M.trace)),
        ]
        bf = tk.Frame(root, padx=12)
        bf.pack()
        for i, (text, cmd) in enumerate(ops):
            tk.Button(bf, text=text, width=14, command=cmd).grid(
                row=i // 4, column=i % 4, padx=3, pady=3)

        util = tk.Frame(root, pady=4)
        util.pack()
        tk.Button(util, text="Clear all", width=14, command=self.clear).pack(side="left", padx=4)
        tk.Button(util, text="Load example", width=14, command=self.load_example).pack(side="left", padx=4)

        # ---- result area ----
        res = tk.LabelFrame(root, text="Result", padx=10, pady=8)
        res.pack(fill="x", padx=12, pady=(6, 12))
        self.title_lbl = tk.Label(res, text="Choose an operation", font=("Arial", 11, "bold"))
        self.title_lbl.pack()
        grid = tk.Frame(res)
        grid.pack(pady=4)
        self.res_cells = []
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                lbl = tk.Label(grid, text="", width=10, relief="groove", bg="#f4f7fb")
                lbl.grid(row=i, column=j, padx=2, pady=2)
                row.append(lbl)
            self.res_cells.append(row)
        self.value_lbl = tk.Label(res, text="", font=("Arial", 12))
        self.value_lbl.pack()

        self.load_example()

    # ---------- building blocks ----------
    def make_grid(self, parent, title, col):
        frame = tk.LabelFrame(parent, text=title, padx=8, pady=8)
        frame.grid(row=0, column=col, padx=10)
        cells = []
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                e = tk.Entry(frame, width=7, justify="center")
                e.grid(row=i, column=j, padx=2, pady=2)
                row.append(e)
            cells.append(row)
        return cells

    def read(self, cells, name):
        """Return the grid as a list of lists of floats (shows an error if invalid)."""
        try:
            return [[float(cells[i][j].get()) for j in range(SIZE)] for i in range(SIZE)]
        except ValueError:
            messagebox.showerror("Invalid input", f"Matrix {name} must contain only numbers.")
            return None

    def show_matrix(self, title, m):
        self.title_lbl.config(text=title)
        self.value_lbl.config(text="")
        for i in range(SIZE):
            for j in range(SIZE):
                self.res_cells[i][j].config(text=f"{m[i][j] + 0.0:.3f}")

    def show_value(self, title, value):
        self.title_lbl.config(text=title)
        for row in self.res_cells:
            for lbl in row:
                lbl.config(text="")
        self.value_lbl.config(text=f"{value:.3f}")

    # ---------- actions ----------
    def run(self, title, needs_b, func):
        a = self.read(self.a_cells, "A")
        if a is None:
            return
        if needs_b:
            b = self.read(self.b_cells, "B")
            if b is None:
                return
            result = func(a, b)
        else:
            result = func(a)
        if isinstance(result, float) or isinstance(result, int):
            self.show_value(title, result)
        else:
            self.show_matrix(title, result)

    def run_scalar(self):
        a = self.read(self.a_cells, "A")
        if a is None:
            return
        try:
            k = float(self.k_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Scalar k must be a number.")
            return
        self.show_matrix(f"{k:g} x A", M.scalar_multiply(a, k))

    def run_inverse(self):
        a = self.read(self.a_cells, "A")
        if a is None:
            return
        inv = M.inverse(a)
        if inv is None:
            self.title_lbl.config(text="Inverse of A")
            for row in self.res_cells:
                for lbl in row:
                    lbl.config(text="")
            self.value_lbl.config(text="Singular matrix (det = 0): no inverse")
        else:
            self.show_matrix("Inverse of A", inv)

    def clear(self):
        for cells in (self.a_cells, self.b_cells):
            for row in cells:
                for e in row:
                    e.delete(0, tk.END)
                    e.insert(0, "0")

    def load_example(self):
        A = [[2, 1, 3], [0, 4, 1], [5, 2, 6]]
        B = [[1, 0, 2], [3, 1, 0], [4, 5, 1]]
        for cells, data in ((self.a_cells, A), (self.b_cells, B)):
            for i in range(SIZE):
                for j in range(SIZE):
                    cells[i][j].delete(0, tk.END)
                    cells[i][j].insert(0, str(data[i][j]))


if __name__ == "__main__":
    root = tk.Tk()
    MatrixApp(root)
    root.mainloop()
