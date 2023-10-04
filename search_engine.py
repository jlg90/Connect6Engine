from tools import *

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
        if depth == 0 or is_win_by_premove(self.m_board, preMove):
            return self.evaluate_position()

        if ourColor==1:
            opponent_color=2
        else:
            opponent_color=1
        
        #opponent_color = self.opponent_color()  # Obtener el color del oponente

        if ourColor == self.m_chess_type:
            max_eval = float('-inf')
            for move in self.generate_moves():
                make_move(self.m_board, move, ourColor)
                eval = self.alpha_beta_search(depth - 1, alpha, beta, opponent_color, bestMove, move)
                unmake_move(self.m_board, move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.generate_moves():
                make_move(self.m_board, move, opponent_color)
                eval = self.alpha_beta_search(depth - 1, alpha, beta, ourColor, bestMove, move)
                unmake_move(self.m_board, move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval


    def evaluate_position(self):
        # Evaluación para el juego Conecta 6:
        # Contaremos la cantidad de fichas consecutivas del jugador actual en todas las direcciones (horizontal, vertical y diagonal)
        # y otorgaremos una puntuación en función de la longitud de la secuencia.
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

        return player_score - opponent_score

    def generate_moves(self):
        # Generación de movimientos para el juego Conecta 6:
        # Devolver una lista de objetos Move con todas las posiciones vacías en el tablero
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


    # def alpha_beta_search(self, depth, alpha, beta, ourColor, bestMove, preMove):
    

    #     if (is_win_by_premove(self.m_board, preMove)):
    #         if (ourColor == self.m_chess_type):

    #             return 0;
    #         else:
    #             return Defines.MININT + 1;
        
    #     alpha = 0
    #     if(self.check_first_move()):
    #         bestMove.positions[0].x = 10
    #         bestMove.positions[0].y = 10
    #         bestMove.positions[1].x = 10
    #         bestMove.positions[1].y = 10
    #     else:   
    #         move1 = self.find_possible_move()
    #         bestMove.positions[0].x = move1[0]
    #         bestMove.positions[0].y = move1[1]
    #         bestMove.positions[1].x = move1[0]
    #         bestMove.positions[1].y = move1[1]
    #         make_move(self.m_board,bestMove,ourColor)
            
    #         '''#Check game result
    #         if (is_win_by_premove(self.m_board, bestMove)):
    #             Self wins.
    #             return Defines.MININT + 1;'''
            
    #         move2 = self.find_possible_move()
    #         bestMove.positions[1].x = move2[0]
    #         bestMove.positions[1].y = move2[1]
    #         make_move(self.m_board,bestMove,ourColor)

    #     return alpha
        
    

    def check_first_move(self):
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i])-1):
                if(self.m_board[i][j] != Defines.NOSTONE):
                    return False
        return True
        
    def find_possible_move(self):
        for i in range(1,len(self.m_board)-1):
            for j in range(1, len(self.m_board[i])-1):
                if(self.m_board[i][j] == Defines.NOSTONE):
                    return (i,j)
        return (-1,-1)





def flush_output():
    import sys
    sys.stdout.flush()
