import mss
import numpy as np
import cv2

class Visual:
    def capture(self):
        with mss.mss() as sct:
            raw_img = sct.grab(sct.monitors[1])
            return np.array(raw_img)

    def display_results(self, Sudoku_board, edges, drawimg):
        if Sudoku_board is not None:
            cv2.imshow("Perfect Sudoku Board", Sudoku_board)
        else:
            print("[Error]: Sudoku board not found!")
            
        cv2.imshow("Edges", edges)
        cv2.imshow("Result", drawimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()