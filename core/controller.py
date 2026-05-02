from .visual import Visual
from .imgconvert import ImgConvert
from .solver import Solver
import numpy as np
import pyautogui
import cv2

class Controller:
    def __init__(self, log_callback=None):
        self.visual = Visual()
        self.converter = ImgConvert()
        self.solver = Solver()
        
        pyautogui.PAUSE = 0.05
        pyautogui.FAILSAFE = True
        
        if log_callback:
            self.log = log_callback
        else:
            self.log = lambda msg: print(msg, end='')

    def run(self):
        self.log("[System]: Taking screenshot...\n")
        img = self.visual.capture()
        Sudoku_board, edges, drawimg, approx = self.converter.get_board_logic(img)
        
        if Sudoku_board is not None:
            self.log("[System]: Board found! Reading digits...\n")
            boxes = self.converter.split_Sudoku_board(Sudoku_board)
            numbers = self.converter.read_board(boxes)
            
            if not numbers:
                self.log("[Error]: KNN model not loaded or reading failed.\n")
                return

            board_matrix = np.array(numbers).reshape((9,9)).tolist()
            original_board = [row[:] for row in board_matrix]
            self.log("\nOriginal board read by bot:")
            self.print_board_to_log(original_board)
            self.log("\n[System]: Solving...\n")
            if self.solver.solve(board_matrix):
                self.log("[SUCCESS]: Solution found! Auto-filling...\n")
                self.print_board_to_log(board_matrix)
                self.auto_fill(original_board, board_matrix, approx)
                self.log("[SUCCESS]: Auto-fill complete!\n")
            else:
                self.log("[ERROR]: Sudoku has no solution.\n")
                
        else:
            self.log("[Error]: Sudoku board not found on screen!\n")

    def auto_fill(self, original_board, solved_board, approx):
        x, y, w, h = cv2.boundingRect(approx)
        
        cell_w = w / 9.0
        cell_h = h / 9.0
        
        for row in range(9):
            for col in range(9):
                if original_board[row][col] == 0:
                    answer = solved_board[row][col]
                    
                    target_x = int(x + (col * cell_w) + (cell_w / 2))
                    target_y = int(y + (row * cell_h) + (cell_h / 2))
                    
                    pyautogui.click(x=target_x, y=target_y)
                    pyautogui.press(str(answer))

    def print_board_to_log(self, bo):
        board_str = "\n"
        for i in range(len(bo)):
            if i % 3 == 0 and i != 0:
                board_str += "- - - - - - - - - - - \n"
            row_str = ""
            for j in range(len(bo[0])):
                if j % 3 == 0 and j != 0:
                    row_str += "| "
                row_str += str(bo[i][j]) + " "
            board_str += row_str + "\n"
        board_str += "\n"
        
        self.log(board_str)