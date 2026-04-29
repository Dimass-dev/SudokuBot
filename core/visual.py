import mss
import numpy as np
import cv2
import time

class Visual:
    def __init__(self):
        with mss.mss() as sct:
            print("У тебя есть 3 секунды, чтобы открыть судоку...")
            time.sleep(6) 
            raw_img = sct.grab(sct.monitors[1])
            self.img = np.array(raw_img)

    def order_points(self, points):
        points = points.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")
        sum_pts = points.sum(axis=1)
        rect[0] = points[np.argmin(sum_pts)]
        rect[2] = points[np.argmax(sum_pts)]
        diff = np.diff(points, axis=1)
        rect[1] = points[np.argmin(diff)]
        rect[3] = points[np.argmax(diff)]
        return rect

    def process_image(self):
        bgrimg = cv2.cvtColor(self.img, cv2.COLOR_BGRA2BGR)
        grayimg = cv2.cvtColor(bgrimg, cv2.COLOR_BGR2GRAY)
        blurimg = cv2.GaussianBlur(grayimg, (5, 5), 0)
        edges = cv2.Canny(blurimg, 50, 150)
        
        # ИСПРАВЛЕНО: RETR_LIST заставляет искать ВСЕ контуры, даже вложенные
        contures, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        Sudoku_board = None
        drawimg = self.img.copy()
        screenarea = self.img.shape[0] * self.img.shape[1]
        contures = sorted(contures, key=cv2.contourArea, reverse=True)
        
        for conture in contures:
            area = cv2.contourArea(conture)
            
            # ИСПРАВЛЕНО: Снизили порог мусора с 5% до 1% (0.01)
            if area > 0.90 * screenarea or area < 0.01 * screenarea:
                continue
                
            perimetr = cv2.arcLength(conture, True)
            approx = cv2.approxPolyDP(conture, 0.02 * perimetr, True)
            
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                ratio = w / float(h)
                
                # Фильтр на квадратность
                if ratio < 0.9 or ratio > 1.1:
                    continue
                    
                cv2.drawContours(drawimg, [approx], -1, (0, 255, 0), 3)
                
                rect = self.order_points(approx)
                rqdst = np.array([
                    [0, 0], 
                    [449, 0], 
                    [449, 449], 
                    [0, 449]], dtype="float32")
                    
                M = cv2.getPerspectiveTransform(rect, rqdst)   
                Sudoku_board = cv2.warpPerspective(grayimg, M, (450, 450))
                break    

        if Sudoku_board is not None:
            cv2.imshow("Perfect Sudoku Board", Sudoku_board)
        else:
            print("[Ошибка]: Поле судоку не найдено! Возможно оно слишком маленькое или перекрыто.")            
            
        cv2.imshow("Edges", edges)
        cv2.imshow("Result", drawimg)
        
        print("[Система]: Нажми ПРОБЕЛ, находясь в окне с картинкой, чтобы закрыть его.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    visual = Visual()
    visual.process_image()