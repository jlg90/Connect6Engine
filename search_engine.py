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

    def alpha_beta_search(self, depth, alpha, beta, ourColor, bestMove, preMove):
        if depth == 0:
            return self.evaluate_position()

        if ourColor == self.m_chess_type:
            bestValue = float('-inf')
            moves = self.generate_moves()
            for move in moves:
                # Realiza el movimiento
                make_move(self.m_board,move, ourColor)
                value = self.alpha_beta_search(depth - 1, alpha, beta, self.opponent_color(), bestMove, move)
                # Deshaz el movimiento
                unmake_move(self.m_board,move)
                

                if value > bestValue:
                    bestValue = value
                    if bestMove is not None:
                        bestMove.positions[0] = move.positions[0]
                        bestMove.positions[1] = move.positions[1]

                alpha = max(alpha, bestValue)
                if beta <= alpha:
                    break  # Poda alfa-beta

            return bestValue
        else:
            bestValue = float('inf')
            moves = self.generate_moves()
            for move in moves:
                # Realiza el movimiento
                
                make_move(self.m_board,move, ourColor)
                value = self.alpha_beta_search(depth - 1, alpha, beta, self.opponent_color(), bestMove, move)
                # Deshaz el movimiento
                unmake_move(self.m_board,move)

                if value < bestValue:
                    bestValue = value
                    if bestMove is not None:
                        bestMove.positions[0] = move.positions[0]
                        bestMove.positions[1] = move.positions[1]

                beta = min(beta, bestValue)
                if beta <= alpha:
                    break

            return bestValue

    def evaluate_position(self):
        # Aquí debes implementar la lógica para evaluar la posición y devolver la puntuación.
        # Puedes utilizar la lógica de tu función original 'evaluate_position'.
        player_color = self.m_chess_type
        opponent_color = self.opponent_color()

        player_score = 0
        opponent_score = 0

        # Direcciones posibles para buscar secuencias
        directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]

        for direction in directions:
            dx, dy = direction
            for x in range(1, len(self.m_board) - 1):
                for y in range(1, len(self.m_board[x]) - 1):
                    if self.m_board[x][y] == player_color:
                        sequence_length = 1
                        for i in range(1, 6):
                            nx, ny = x + i * dx, y + i * dy
                            if 1 <= nx < len(self.m_board) - 1 and 1 <= ny < len(self.m_board[x]) - 1:
                                if self.m_board[nx][ny] == player_color:
                                    sequence_length += 1
                                else:
                                    break
                            else:
                                break

                        if sequence_length >= 6:
                            player_score += 1000  # Jugador gana
                        elif sequence_length >= 5:
                            player_score += 100  # Potencialmente ganador

        return player_score - opponent_score

    def generate_moves(self):
        # Aquí debes implementar la lógica para generar movimientos y devolver una lista de movimientos válidos.
        # Puedes utilizar la lógica de tu función original 'generate_moves'.
        empty_moves = []

        for x in range(1, len(self.m_board) - 1):
            for y in range(1, len(self.m_board[x]) - 1):
                if self.m_board[x][y] == Defines.NOSTONE:
                    move = StoneMove()
                    move.positions[0].x = x
                    move.positions[0].y = y
                    move.positions[1].x = x
                    move.positions[1].y = y
                    empty_moves.append(move)

        return empty_moves

    def opponent_color(self):
        # Si el color es blanco, devuelve negro; si es negro, devuelve blanco
        return Defines.BLACK if self.m_chess_type == Defines.WHITE else Defines.WHITE

def flush_output():
    import sys
    sys.stdout.flush()