from defines import *
import time
from  tools import *
from defines import StoneMove


class SearchEngine():
    def __init__(self):
        self.m_board = None
        self.m_chess_type = None
        self.m_alphabeta_depth = None
        self.m_total_nodes = 0

    def before_search(self, board, color, alphabeta_depth):
        self.m_board = [row[:] for row in board]
        self.m_chess_type = color
        self.m_alphabeta_depth = alphabeta_depth
        self.m_total_nodes = 0
        
    def alpha_beta_search(self, depth, alpha, beta, maximizing_player, best_move, current_move):
        if depth == 0 or self.is_terminal_node():
            return self.evaluate_board(maximizing_player)

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_possible_moves():
                if self.is_valid_move(move):
                    self.make_move(move, self.m_chess_type)
                    eval = self.alpha_beta_search(depth - 1, alpha, beta, False, best_move, current_move)
                    self.undo_move(move)
                    if eval > max_eval:
                        max_eval = eval
                        if current_move is not None:
                            current_move.positions[0].x = move.positions[0].x
                            current_move.positions[0].y = move.positions[0].y
                            current_move.positions[1].x = move.positions[1].x
                            current_move.positions[1].y = move.positions[1].y
                            current_move.score = move.score
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves():
                if self.is_valid_move(move):
                    self.make_move(move, self.m_chess_type)
                    eval = self.alpha_beta_search(depth - 1, alpha, beta, True, best_move, current_move)
                    self.undo_move(move)
                    if eval < min_eval:
                        min_eval = eval
                        if current_move is not None:
                            current_move.positions[0].x = move.positions[0].x
                            current_move.positions[0].y = move.positions[0].y
                            current_move.positions[1].x = move.positions[1].x
                            current_move.positions[1].y = move.positions[1].y
                            current_move.score = move.score
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def is_valid_move(self, move):
        x, y = move.positions[0].x, move.positions[0].y
        return self.m_board[x][y] == Defines.NOSTONE

    
    def evaluate_board(self, maximizing_player):
        if maximizing_player:
            player_color = Defines.BLACK
            opponent_color = Defines.WHITE
        else:
            player_color = Defines.WHITE
            opponent_color = Defines.BLACK

        player_score = self.calculate_score(player_color)
        opponent_score = self.calculate_score(opponent_color)

        return player_score - opponent_score

    def make_move(self, move, color):
        self.m_board[move.positions[0].x][move.positions[0].y] = color

    def undo_move(self, move):
        self.m_board[move.positions[0].x][move.positions[0].y] = Defines.NOSTONE

    def get_possible_moves(self):
        moves = []
        for i in range(1, Defines.GRID_NUM - 1):
            for j in range(1, Defines.GRID_NUM - 1):
                if self.m_board[i][j] == Defines.NOSTONE:
                    move = StoneMove()
                    move.positions[0].x = i
                    move.positions[0].y = j
                    move.score = 0
                    moves.append(move)
        return moves

    def calculate_score(self, color):
        # Inicializamos la puntuación del jugador
        player_score = 0

        # Definimos direcciones en las que buscar piedras conectadas
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for i in range(1, Defines.GRID_NUM - 1):
            for j in range(1, Defines.GRID_NUM - 1):
                if self.m_board[i][j] == color:
                    # Buscamos patrones de piedras en línea en todas las direcciones
                    for direction in directions:
                        stones_in_line = 1
                        for step in range(1, 6):  # Buscamos hasta 6 piedras en línea
                            x = i + step * direction[0]
                            y = j + step * direction[1]
                            if isValidPos(x, y) and self.m_board[x][y] == color:
                                stones_in_line += 1
                            else:
                                break
                        # Calificamos el patrón de piedras en línea
                        if stones_in_line == 6:
                            # El jugador tiene 6 en línea, ¡ganó el juego!
                            return Defines.MAXINT
                        player_score += stones_in_line

        return player_score

    def is_terminal_node(self):
        # Verificamos si el juego ha llegado a su fin
        for i in range(1, Defines.GRID_NUM - 1):
            for j in range(1, Defines.GRID_NUM - 1):
                if self.m_board[i][j] == Defines.NOSTONE:
                    # Todavía hay espacios vacíos en el tablero, el juego no ha terminado.
                    return False

    # Si no hay espacios vacíos, el juego termina en empate.
        return True

def flush_output():
    import sys
    sys.stdout.flush()