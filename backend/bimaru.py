# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 23:
# 102082 Simão Sanguinho
# 103252 José Pereira

import numpy as np
import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    """ Representação interna de um estado do jogo Bimaru."""
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, cells, rows: list, columns: list,
                 current_boat_rows: list, current_boat_columns: list,
                 available_boats: list, available_rows: list,
                 available_cols: list, is_valid: bool, waters: int):
        """ Inicializa o tabuleiro com as dimensões dadas."""
        self.cells = cells
        self.limit_rows = rows
        self.limit_columns = columns
        self.current_boat_rows = current_boat_rows
        self.current_boat_columns = current_boat_columns
        self.available_boats = available_boats
        self.available_rows = available_rows
        self.available_cols = available_cols
        self.is_valid = is_valid
        self.waters = waters

    def deepcopy(self, board):
        """ Retorna uma cópia do tabuleiro."""

        new_cells = np.copy(board.cells)
        current_boat_rows = board.current_boat_rows.copy()
        current_boat_columns = board.current_boat_columns.copy()
        available_boats = board.available_boats.copy()
        available_rows = board.available_rows.copy()
        available_cols = board.available_cols.copy()
        is_valid = board.is_valid
        waters = board.waters
        return Board(new_cells, board.limit_rows, board.limit_columns,
                     current_boat_rows, current_boat_columns, available_boats,
                     available_rows, available_cols, is_valid, waters)

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if (self.valid_cell(row, col)):
            return self.cells[row, col]

    def valid_cell(self, row: int, col: int) -> bool:
        """Verifica se a célula é válida."""
        return not (row < 0 or row > 9 or col < 0 or col > 9)

    def temp_set_value(self, row: int, col: int, value: str) -> None:
        """ Atribui temporariamente o valor na posição do tabuleiro."""
        self.cells[row, col] = value
        if value == " ":
            self.current_boat_columns[col] -= 1
            self.current_boat_rows[row] -= 1
            self.available_rows[row] -= 1
            self.available_cols[col] -= 1
        else:
            self.current_boat_columns[col] += 1
            self.current_boat_rows[row] += 1
            self.available_rows[row] += 1
            self.available_cols[col] += 1

    def set_value(self, row: int, col: int, value: str) -> None:
        """Atribui o valor na respetiva posição do tabuleiro."""
        if (self.valid_cell(row, col) and self.cells[row, col] == " "):
            self.cells[row, col] = value
            self.available_rows[row] -= 1
            self.available_cols[col] -= 1
            if (value == '.'):
                self.waters += 1
            if (value not in ['W', '.']):
                self.current_boat_rows[row] += 1
                self.current_boat_columns[col] += 1

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (self.get_value(row-1, col), self.get_value(row+1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_value(row, col-1), self.get_value(row, col+1))

    def is_adjacent_water_horizontal(self, row: int, col: int) -> bool:
        """Verifica se a célula está adjacente a água."""
        up, down = self.adjacent_vertical_values(row, col)
        return (up in ['.', 'W',] or down in ['.', 'W',])

    def is_adjacent_water_vertical(self, row: int, col: int) -> bool:
        """Verifica se a célula está adjacente a água."""
        left, right = self.adjacent_horizontal_values(row, col)
        return (left in ['.', 'W',] or right in ['.', 'W',])

    def surrounded_by_water(self, row: int, col: int) -> bool:
        """Verifica se a célula está rodeada de água."""
        up, down = self.adjacent_vertical_values(row, col)
        left, right = self.adjacent_horizontal_values(row, col)
        up_left, up_right = self.adjacent_horizontal_values(row-1, col)
        down_left, down_right = self.adjacent_horizontal_values(row+1, col)
        return (up in ['.', 'W', None] and down in ['.', 'W', None] and
                left in ['.', 'W', None] and right in ['.', 'W', None]
                and up_left in ['.', 'W', None] and up_right in ['.', 'W', None]
                and down_left in ['.', 'W', None] and down_right in ['.', 'W', None])

    def fill_row_with_water(self, row: int) -> None:
        """Preenche a linha 'row' com água."""
        for col in range(10):
            self.set_value(row, col, '.')

    def fill_column_with_water(self, col: int) -> None:
        """Preenche a coluna 'col' com água."""
        for row in range(10):
            self.set_value(row, col, '.')

    def fill_segments_with_water(self, row: int, col: int,
                                 length: int, orientation: str) -> None:
        """Preenche segmentos de água"""
        if (orientation == "H"):
            for i in range(length):
                self.set_value(row, col+i, '.')
        elif (orientation == "V"):
            for i in range(length):
                self.set_value(row+i, col, '.')

    def fill_exausted_rows_cols(self) -> None:
        """Preenche as linhas e colunas que já estão completas."""
        for i in range(10):
            if (self.current_boat_rows[i] == self.limit_rows[i]):
                self.fill_row_with_water(i)
            if (self.current_boat_columns[i] == self.limit_columns[i]):
                self.fill_column_with_water(i)

    def surround_circle(self, row: int, col: int) -> None:
        """ Preenche os segmentos de água em volta de um circulo."""
        for i in range(3):
            self.fill_segments_with_water(row - 1 + i, col - 1, 3, "H")

    def surround_top(self, row: int, col: int) -> None:
        """ Preenche os segmentos de água em volta de um top."""
        for i in range(3):
            if (i == 1):
                self.fill_segments_with_water(row - 1, col, 1, "V")
            else:
                self.fill_segments_with_water(row - 1, col - 1 + i, 4, "V")

    def surround_bottom(self, row: int, col: int) -> None:
        """ Preenche os segmentos de água em volta de um bottom."""
        for i in range(3):
            if (i == 1):
                self.fill_segments_with_water(row + 1, col, 1, "V")
            else:
                self.fill_segments_with_water(row - 2, col - 1 + i, 4, "V")

    def surround_left(self, row: int, col: int) -> None:
        """ Preenche os segmentos de água em volta de um left. """
        for i in range(3):
            if (i == 1):
                self.fill_segments_with_water(row, col - 1, 1, "H")
            else:
                self.fill_segments_with_water(row - 1 + i, col - 1, 4, "H")

    def surround_right(self, row: int, col: int) -> None:
        """ Preenche os segmentos de água em volta de um right. """
        for i in range(3):
            if (i == 1):
                self.fill_segments_with_water(row, col + 1, 1, "H")
            else:
                self.fill_segments_with_water(row - 1 + i, col - 2, 4, "H")

    def surround_middle(self, row: int, col: int) -> None:
        """ Preenche os segmentos de água em volta de um middle. """
        if (self.is_adjacent_water_vertical(row, col)):
            self.fill_segments_with_water(row - 2, col - 1, 5, "V")
            self.fill_segments_with_water(row - 2, col + 1, 5, "V")
        elif (self.is_adjacent_water_horizontal(row, col)):
            self.fill_segments_with_water(row - 1, col - 2, 5, "H")
            self.fill_segments_with_water(row + 1, col - 2, 5, "H")

    def surround_hint_with_water(self, row: int, col: int, value: str) -> None:
        """ Preenche os segmentos de água em volta de uma hint. """

        if (value == 'C'):
            self.surround_circle(row, col)
        elif (value == 'T'):
            self.surround_top(row, col)
        elif (value == 'B'):
            self.surround_bottom(row, col)
        elif (value == 'R'):
            self.surround_right(row, col)
        elif (value == 'L'):
            self.surround_left(row, col)
        elif (value == 'M'):
            self.surround_middle(row, col)

    def check_valid_laterals(self, l1: int, l2: int, l3: int, 
                             l4: int, l5: int, l6: int) -> bool:
        """ Verifica se os laterais de um barco são válidos."""
        if (l1 not in [' ', '.', 'W', None] or l2 not in [' ', '.', 'W', None]):
            return False
        if (l3 not in [' ', '.', 'W', None] or l4 not in [' ', '.', 'W', None]):
            return False
        if (l5 not in [' ', '.', 'W', None] or l6 not in [' ', '.', 'W', None]):
            return False
        return True

    def is_possible_to_add_boat(self, row: int, col: int, length: int, orientation: str) -> bool:
        """ Verifica se é possível adicionar um barco de tamanho 'length' na posição (row, col) com orientação 'orientation'."""
        # se a posição não está vazia
        if (self.get_value(row, col) != " "):
            return False

        if (orientation == "H"):
            # se o barco não cabe no tabuleiro
            if (col + length > 10):
                return False
            # se o barco exceede o limite de barcos na linha
            if (self.limit_rows[row] < self.current_boat_rows[row] + length):
                return False

            left_up, left_down = self.adjacent_vertical_values(row, col-1)
            right_up, right_down = self.adjacent_vertical_values(
                row, col+length)
            left = self.get_value(row, col-1)
            right = self.get_value(row, col+length)
            # se os laterais do barco não são válidos
            if not self.check_valid_laterals(left, right, left_up, left_down, 
                                             right_up, right_down):
                return False

            for i in range(length):
                # se as possiveis posicoes do barco esta livres
                if (self.get_value(row, col+i) != " "):
                    return False
                # se o barco está rodeado por outro barco
                up, down = self.adjacent_vertical_values(row, col+i)
                if (up not in [' ', '.', 'W', None] or down not in [' ', '.', 'W', None]):
                    return False

        elif (orientation == "V"):
            if (row + length > 10):  # se o barco não cabe no tabuleiro
                return False
            # se o barco exceede o limite de barcos na coluna
            if (self.limit_columns[col] < self.current_boat_columns[col] + length):
                return False

            top_left, top_right = self.adjacent_horizontal_values(row-1, col)
            bottom_left, bottom_right = self.adjacent_horizontal_values(
                row+length, col)
            top = self.get_value(row-1, col)
            bottom = self.get_value(row+length, col)
            # se os laterais do barco não são válidos
            if not self.check_valid_laterals(top, bottom, top_left, top_right, bottom_left, bottom_right):
                return False

            # se o barco está rodeado por outro barco
            for i in range(length):
                if (self.get_value(row+i, col) != " "):
                    return False
                left, right = self.adjacent_horizontal_values(row+i, col)
                if (left not in [' ', '.', 'W', None] or right not in [' ', '.', 'W', None]):
                    return False

        return True

    def get_possible_actions(self) -> list:
        """ Retorna uma lista de ações possíveis."""
        actions = []
        if self.is_valid == False:
            return actions

        # se é possível adicionar um barco de tamanho 4
        if (4 in self.available_boats):
            for i in range(10):
                for j in range(10):
                    value = self.get_value(i, j)
                    if value in ['.', 'W']:
                        continue
                    if (self.is_possible_to_add_boat(i, j, 4, "H")):
                        actions.append((i, j, 4, "H"))

                    if (self.is_possible_to_add_boat(i, j, 4, "V")):
                        actions.append((i, j, 4, "V"))

                    if (value == "T"):
                        self.temp_set_value(i, j, " ")
                        if (self.is_possible_to_add_boat(i+1, j, 3, "V")):
                            actions.append((i, j, 4, "V"))
                        self.temp_set_value(i, j, value)

                    if (value == "B"):
                        self.temp_set_value(i, j, " ")
                        if (self.is_possible_to_add_boat(i - 3, j, 3, "V")):
                            actions.append((i - 3, j, 4, "V"))
                        self.temp_set_value(i, j, value)

                    if (value == "R"):
                        self.temp_set_value(i, j, " ")
                        if (self.is_possible_to_add_boat(i, j - 3, 3, "H")):
                            actions.append((i, j - 3, 4, "H"))
                        self.temp_set_value(i, j, value)

                    if (value == "L"):
                        self.temp_set_value(i, j, " ")
                        if (self.is_possible_to_add_boat(i, j + 1, 3, "H")):
                            actions.append((i, j, 4, "H"))
                        self.temp_set_value(i, j, value)
                    if (value == "M"):
                        self.temp_set_value(i, j, " ")
                        if (self.is_possible_to_add_boat(i, j - 1, 4, "H")):
                            actions.append((i, j-1, 4, "H"))
                        if (self.is_possible_to_add_boat(i, j - 2, 4, "H")):
                            actions.append((i, j-2, 4, "H"))
                        if (self.is_possible_to_add_boat(i-1, j, 4, "V")):
                            actions.append((i-1, j, 4, "V"))
                        if (self.is_possible_to_add_boat(i-2, j, 4, "V")):
                            actions.append((i-2, j, 4, "V"))
                        self.temp_set_value(i, j, value)

            return actions

        # se é possível adicionar um barco de tamanho 3
        if (3 in self.available_boats):
            for i in range(10):
                for j in range(10):
                    value = self.get_value(i, j)
                    if value in ['.', 'W']:
                        continue
                    if (self.is_possible_to_add_boat(i, j, 3, "H")):
                        actions.append((i, j, 3, "H"))

                    if (self.is_possible_to_add_boat(i, j, 3, "V")):
                        actions.append((i, j, 3, "V"))

                    if (value == "T"):
                        self.temp_set_value(i, j, " ")
                        if (self.is_possible_to_add_boat(i+1, j, 2, "V")):
                            actions.append((i, j, 3, "V"))
                        self.temp_set_value(i, j, value)

                    if (value == "B"):
                        self.temp_set_value(i, j, " ")
                        if (self.is_possible_to_add_boat(i - 2, j, 2, "V")):
                            actions.append((i - 2, j, 3, "V"))
                        self.temp_set_value(i, j, value)

                    if (value == "R"):
                        self.temp_set_value(i, j, " ")
                        if (self.is_possible_to_add_boat(i, j - 2, 2, "H")):
                            actions.append((i, j - 2, 3, "H"))
                        self.temp_set_value(i, j, value)

                    if (value == "L"):
                        self.temp_set_value(i, j, " ")
                        if (self.is_possible_to_add_boat(i, j + 1, 2, "H")):
                            actions.append((i, j, 3, "H"))
                        self.temp_set_value(i, j, value)

                    if (value == "M"):
                        value = self.get_value(i, j)
                        self.temp_set_value(i, j, " ")
                        if (self.is_possible_to_add_boat(i, j - 1, 3, "H")):
                            actions.append((i, j-1, 3, "H"))
                        if (self.is_possible_to_add_boat(i-1, j, 3, "V")):
                            actions.append((i-1, j, 3, "V"))
                        self.temp_set_value(i, j, value)
            return actions

        # se é possível adicionar um barco de tamanho 2
        if (2 in self.available_boats):
            for i in range(10):
                for j in range(10):
                    value = self.get_value(i, j)
                    if value in ['.', 'W']:
                        continue
                    if (self.is_possible_to_add_boat(i, j, 2, "H")):
                        actions.append((i, j, 2, "H"))
                    if (self.is_possible_to_add_boat(i, j, 2, "V")):
                        actions.append((i, j, 2, "V"))

                    if (value == "T"):
                        self.temp_set_value(i, j, " ")
                        if (self.is_possible_to_add_boat(i+1, j, 1, "V")):
                            actions.append((i, j, 2, "V"))
                        self.temp_set_value(i, j, value)

                    if (value == "B"):
                        self.temp_set_value(i, j, " ")
                        if (self.is_possible_to_add_boat(i - 1, j, 1, "V")):
                            actions.append((i-1, j, 2, "V"))
                        self.temp_set_value(i, j, value)

                    if (value == "R"):
                        self.temp_set_value(i, j, " ")
                        if (self.is_possible_to_add_boat(i, j - 1, 1, "H")):
                            actions.append((i, j-1, 2, "H"))
                        self.temp_set_value(i, j, value)

                    if (value == "L"):
                        self.temp_set_value(i, j, " ")
                        if (self.is_possible_to_add_boat(i, j + 1, 1, "H")):
                            actions.append((i, j, 2, "H"))
                        self.temp_set_value(i, j, value)
            return actions

        # se é possível adicionar um barco de tamanho 1
        if (1 in self.available_boats):
            for i in range(10):
                for j in range(10):
                    value = self.get_value(i, j)
                    if value in ['.', 'W']:
                        continue
                    if (self.is_possible_to_add_boat(i, j, 1, "H")):
                        actions.append((i, j, 1, "H"))
            return actions
        return actions

    def add_boat_size_1(self, row: int, col: int) -> None:
        """ Adiciona um barco de tamanho 1 na posição (row, col)."""
        self.set_value(row, col, "c")
        self.surround_circle(row, col)
        self.available_boats.remove(1)

    def add_boat_size_2_H(self, row: int, col: int) -> None:
        """ Adiciona um barco de tamanho 2 na posição (row, col) com orientação horizontal."""
        self.set_value(row, col, "l")
        self.set_value(row, col + 1, "r")
        self.surround_left(row, col)
        self.surround_right(row, col + 1)
        self.available_boats.remove(2)

    def add_boat_size_2_V(self, row: int, col: int) -> None:
        """ Adiciona um barco de tamanho 2 na posição (row, col) com orientação vertical."""
        self.set_value(row, col, "t")
        self.set_value(row + 1, col, "b")
        self.surround_top(row, col)
        self.surround_bottom(row + 1, col)
        self.available_boats.remove(2)

    def add_boat_size_3_H(self, row: int, col: int) -> None:
        """ Adiciona um barco de tamanho 3 na posição (row, col) com orientação horizontal."""
        self.set_value(row, col, "l")
        self.set_value(row, col + 1, "m")
        self.set_value(row, col + 2, "r")
        self.surround_left(row, col)
        self.surround_middle(row, col + 1)
        self.surround_right(row, col + 2)
        self.available_boats.remove(3)

    def add_boat_size_3_V(self, row: int, col: int) -> None:
        """ Adiciona um barco de tamanho 3 na posição (row, col) com orientação vertical."""
        self.set_value(row, col, "t")
        self.set_value(row + 1, col, "m")
        self.set_value(row + 2, col, "b")
        self.surround_top(row, col)
        self.surround_middle(row + 1, col)
        self.surround_bottom(row + 2, col)
        self.available_boats.remove(3)

    def add_boat_size_4_H(self, row: int, col: int) -> None:
        """ Adiciona um barco de tamanho 4 na posição (row, col) com orientação horizontal. """
        self.set_value(row, col, "l")
        self.set_value(row, col + 1, "m")
        self.set_value(row, col + 2, "m")
        self.set_value(row, col + 3, "r")
        self.surround_left(row, col)
        self.surround_middle(row, col + 1)
        self.surround_middle(row, col + 2)
        self.surround_right(row, col + 3)
        self.available_boats.remove(4)

    def add_boat_size_4_V(self, row: int, col: int) -> None:
        """ Adiciona um barco de tamanho 4 na posição (row, col) com orientação vertical. """
        self.set_value(row, col, "t")
        self.set_value(row + 1, col, "m")
        self.set_value(row + 2, col, "m")
        self.set_value(row + 3, col, "b")
        self.surround_top(row, col)
        self.surround_middle(row + 1, col)
        self.surround_middle(row + 2, col)
        self.surround_bottom(row + 3, col)
        self.available_boats.remove(4)

    def add_boat(self, row: int, col: int, length: int, orientation: str) -> None:
        """ Adiciona um barco de tamanho 'length' na posição (row, col) com orientação 'orientation'."""
        if length == 1:
            self.add_boat_size_1(row, col)
        elif length == 2:
            if (orientation == "H"):
                self.add_boat_size_2_H(row, col)
            elif (orientation == "V"):
                self.add_boat_size_2_V(row, col)
        elif length == 3:
            if (orientation == "H"):
                self.add_boat_size_3_H(row, col)
            elif (orientation == "V"):
                self.add_boat_size_3_V(row, col)
        elif length == 4:
            if (orientation == "H"):
                self.add_boat_size_4_H(row, col)
            elif (orientation == "V"):
                self.add_boat_size_4_V(row, col)
        else:
            raise ValueError("Invalid boat length")

    def check_valid(self) -> None:
        """ Verifica se a instância é válida."""
        for i in range(10):
            for j in range(10):
                if (self.get_value(i, j) not in [" ", ".", "W", "C", "c"]):
                    if self.surrounded_by_water(i, j):
                        self.is_valid = False
            if self.limit_rows[i] > self.available_rows[i] + self.current_boat_rows[i]:
                self.is_valid = False
            elif self.limit_columns[i] > self.available_cols[i] + self.current_boat_columns[i]:
                self.is_valid = False

    @staticmethod
    def parse_instance() -> None:
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        rows = []
        columns = []
        hints = []
        
        with open('input.txt', 'r') as f:
            for line in f:
                instance = line.split()
                line = [int(x) if x.isdigit() else x for x in instance]
                if not line:
                    break
                entry = line[0]
                if entry == "ROW":
                    rows = line[1:]
                elif entry == "COLUMN":
                    columns = line[1:]
                elif entry == "HINT":
                    hints.append(line[1:])


        current_boat_rows = [0] * 10
        current_boat_columns = [0] * 10
        available_boats = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        available_rows = [10] * 10
        available_cols = [10] * 10
        is_valid = True
        waters = 0
        cells = np.array([[' ' for x in range(len(rows))]
                          for y in range(len(columns))])

        new_board = Board(cells, rows, columns, current_boat_rows, current_boat_columns,
                          available_boats, available_rows, available_cols, is_valid, waters)

        # adiciona hints e remove barcos se estiverem inteiros
        for hint in hints:
            row, col, value = hint[0], hint[1], hint[2]
            new_board.set_value(row, col, value)
            # tamanho 1
            if value == 'C':
                new_board.available_boats.remove(1)
            # tamanho 2
            if value == 'T':
                if [row + 1, col, "B"] in hints:
                    new_board.available_boats.remove(2)
            if value == 'R':
                if [row, col - 1, "L"] in hints:
                    new_board.available_boats.remove(2)
            if value == 'M':
                # tamanho 3
                if [row, col - 1, "L"] in hints and [row, col + 1, "R"] in hints:
                    new_board.available_boats.remove(3)
                if [row - 1, col, "T"] in hints and [row + 1, col, "B"] in hints:
                    new_board.available_boats.remove(3)
                # tamanho 4
                if [row, col - 1, "L"] in hints and [row, col + 1, "M"] in hints and [row, col + 2, "R"] in hints:
                    new_board.available_boats.remove(4)
                if [row - 1, col, "T"] in hints and [row + 1, col, "M"] in hints and [row + 2, col, "B"] in hints:
                    new_board.available_boats.remove(4)
        # preencher as linhas/colunas que já estão cheias
        new_board.fill_exausted_rows_cols()

        for hint in hints:
            row, col, value = hint[0], hint[1], hint[2]
            new_board.surround_hint_with_water(row, col, value)

        return new_board

    def fill_exhausted_around_boat(self, row: int, col: int, length: int, orientation: str) -> None:
        """Preenche as linhas e colunas que ja estao cheias e que intersetam o barco."""
        if orientation == "H":
            if (self.current_boat_rows[row] == self.limit_rows[row]):
                self.fill_row_with_water(row)
            for i in range(length):
                if (self.current_boat_columns[col + i] == self.limit_columns[col + i]):
                    self.fill_column_with_water(col + i)
        elif orientation == "V":
            if (self.current_boat_columns[col] == self.limit_columns[col]):
                self.fill_column_with_water(col)
            for i in range(length):
                if (self.current_boat_rows[row + i] == self.limit_rows[row + i]):
                    self.fill_row_with_water(row + i)

    def __str__(self) -> str:
        """Retorna uma string que representa o tabuleiro."""
        # new_board  = self.deepcopy(self)
        # return str(c.parse_to_debug(new_board.cells))

        board = ""
        for i in range(10):
            for j in range(10):
                board += self.get_value(i, j)
            board += "\n"
        return board[:-1]


class Bimaru(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)
        self.steps = []

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        return state.board.get_possible_actions()

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        new_board = state.board.deepcopy(state.board)
        row, col, length, orientation = action
        new_board.add_boat(row, col, length, orientation)
        new_board.fill_exhausted_around_boat(row, col, length, orientation)
        new_board.check_valid()
        self.steps.append(new_board.cells)
        return BimaruState(new_board)

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return state.board.current_boat_rows == state.board.limit_rows and \
            state.board.current_boat_columns == state.board.limit_columns

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        if node.action is None:
            return np.inf

        x = node.state.board.available_rows
        y = node.state.board.limit_rows
        z = node.state.board.current_boat_rows
        x1 = node.state.board.available_cols
        y1 = node.state.board.limit_columns
        z1 = node.state.board.current_boat_columns
        heu = 1
        filled = 1
        filled_rows = node.state.board.available_rows
        filled_cols = node.state.board.available_cols
        for i in range(10):
            if x[i] == y[i] - z[i]:
                heu += x[i]
            if x1[i] == y1[i] - z1[i]:
                heu += x1[i]
            if filled_rows[i] == 0:
                filled += 1
            if filled_cols[i] == 0:
                filled += 1
        remaining_boats = max(len(node.state.board.available_boats), 1)

        water_cells = node.state.board.waters  # alto é bom
        index_sum = 0  # alto é mau
        for i in range(10):
            index_sum += node.state.board.limit_rows[i] - \
                node.state.board.current_boat_rows[i]
        empty_cells = 100 - water_cells - index_sum  # alto é mau
        return 1/water_cells + index_sum + empty_cells * 1/heu + 1/filled + 1/remaining_boats

def get_steps():
    board = Board.parse_instance()
    problem = Bimaru(board)
    depth_first_tree_search(problem)
    return  problem.steps

def get_limits():
    board = Board.parse_instance()
    return [board.limit_rows, board.limit_columns]

if __name__ == "__main__":
    # Ler o ficheiro do standard input
    board = Board.parse_instance()
    # Usar uma técnica de procura para resolver a instância e obter o nó solução
    problem = Bimaru(board)
    goal_node = depth_first_tree_search(problem)
    # Imprimir para o standard output no formato indicado
    if goal_node:
        print(goal_node.state.board)
    else:
        print("No solution found.")
