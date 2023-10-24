import tkinter as tk
from tkinter import ttk
from random import randint


class Grid:
    def __init__(self, rows, cols, prob_alive=0.2):
        self.rows = rows
        self.cols = cols
        self.grid_ = [[0 for _ in range(cols)] for _ in range(rows)]
        self.prob_alive = prob_alive

    def randomize(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid_[i][j] = 1 if randint(0, 100) < self.prob_alive * 100 else 0

    def next_generation(self):
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                total = sum(
                    [self.grid_[(i + x) % self.rows][(j + y) % self.cols] for x in [-1, 0, 1] for y in [-1, 0, 1] if
                     (x, y) != (0, 0)])
                if self.grid_[i][j] == 1 and total in [2, 3]:
                    new_grid[i][j] = 1
                elif self.grid_[i][j] == 0 and total == 3:
                    new_grid[i][j] = 1
        self.grid_ = new_grid
        return self.grid_


class Visualizer:
    def __init__(self, canvas, grid, cell_size=20):
        self.canvas = canvas
        self.grid = grid
        self.cell_size = cell_size
        self.rectangles = [[None for _ in range(grid.cols)] for _ in range(grid.rows)]
        self.create_rectangles()

    def create_rectangles(self):
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                self.rectangles[i][j] = self.canvas.create_rectangle(
                    j * self.cell_size, i * self.cell_size,
                    j * self.cell_size + self.cell_size, i * self.cell_size + self.cell_size,
                    fill="white", outline="gray"
                )

    def update(self):
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                color = "black" if self.grid.grid_[i][j] else "white"
                self.canvas.itemconfig(self.rectangles[i][j], fill=color)


class UIElements:
    def __init__(self, master, game):
        self.master = master
        self.game = game

        self.start_btn = ttk.Button(self.master, text="Start", command=self.game.start)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(self.master, text="Stop", command=self.game.stop)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = ttk.Button(self.master, text="Clear", command=self.game.clear)
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        self.random_btn = ttk.Button(self.master, text="Randomize", command=self.game.randomize)
        self.random_btn.pack(side=tk.LEFT, padx=5)


class GameOfLife(tk.Tk):
    def __init__(self, rows=20, cols=20, cell_size=20, prob_alive=0.2):
        super().__init__()
        self.geometry(f"{cols * cell_size + 10}x{rows * cell_size + 100}")

        self.grid = Grid(rows, cols, prob_alive)
        self.canvas = tk.Canvas(self, width=cols * cell_size, height=rows * cell_size, bg="white")
        self.canvas.pack(pady=20)
        self.visualizer = Visualizer(self.canvas, self.grid, cell_size)
        self.ui = UIElements(self, self)

        self.running = False
        self.ani = None

        self.canvas.bind("<Button-1>", self.toggle_cell)

    def toggle_cell(self, event):
        i = event.y // self.visualizer.cell_size
        j = event.x // self.visualizer.cell_size
        self.grid.grid_[i][j] = 1 - self.grid.grid_[i][j]
        color = "black" if self.grid.grid_[i][j] else "white"
        self.canvas.itemconfig(self.visualizer.rectangles[i][j], fill=color)

    def start(self):
        if not self.running:
            self.running = True
            self.run_game()

    def stop(self):
        self.running = False
        if self.ani:
            self.after_cancel(self.ani)
            self.ani = None

    def clear(self):
        self.stop()
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                self.grid.grid_[i][j] = 0
        self.visualizer.update()

    def randomize(self):
        self.stop()
        self.grid.randomize()
        self.visualizer.update()

    def run_game(self):
        if self.running:
            self.grid.next_generation()
            self.visualizer.update()
            self.ani = self.after(100, self.run_game)


game = GameOfLife()
game.mainloop()
