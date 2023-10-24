import unittest

from main import GameOfLife


class TestGameOfLife(unittest.TestCase):

    def setUp(self):
        self.game = GameOfLife(5, 5)

    # Тестирование корректности реализации правил игры
    def test_single_live_cell_dies(self):
        self.game.grid.grid_ = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.game.grid.next_generation()
        self.assertEqual(self.game.grid.grid_[1][2], 0)

    def test_live_cell_with_two_neighbors_survives(self):
        self.game.grid.grid_ = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.game.grid.next_generation()
        self.assertEqual(self.game.grid.grid_[2][2], 1)

    def test_dead_cell_with_three_neighbors_becomes_alive(self):
        self.game.grid.grid_ = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.game.grid.next_generation()
        self.assertEqual(self.game.grid.grid_[2][1], 1)

    def test_live_cell_with_four_neighbors_dies(self):
        self.game.grid.grid_ = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.game.grid.next_generation()
        self.assertEqual(self.game.grid.grid_[2][2], 0)

    # Тестирование на статических фигурах
    def test_static_figure(self):
        self.game.grid.grid_ = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        initial_state = [row.copy() for row in self.game.grid.grid_]
        self.game.grid.next_generation()
        self.assertEqual(self.game.grid.grid_, initial_state)

        # Тестирование на корректность

    def test_clear(self):
        self.game.grid.randomize()
        self.game.clear()
        self.assertEqual(sum(sum(row) for row in self.game.grid.grid_), 0)

    def test_randomize(self):
        self.game.clear()
        self.game.randomize()
        total_cells = sum(sum(row) for row in self.game.grid.grid_)
        # Проверяем, что после randomize на поле появились клетки
        self.assertGreater(total_cells, 0)

if __name__ == '__main__':
    unittest.main()
