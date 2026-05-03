import cv2
import numpy as np
import os

class ImgConvert:
    def __init__(self):
        self.knn = cv2.ml.KNearest_create()
        self.model_loaded = False
        
        if os.path.exists('data/samples.data') and os.path.exists('data/responses.data'):
            samples = np.loadtxt('data/samples.data', np.float32)
            responses = np.loadtxt('data/responses.data', np.float32)
            self.knn.train(samples, cv2.ml.ROW_SAMPLE, responses)
            self.model_loaded = True
        else:
            print("[Warning]: Training files (samples.data) not found!")

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

    def get_board_logic(self, img):
        bgrimg = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        grayimg = cv2.cvtColor(bgrimg, cv2.COLOR_BGR2GRAY)
        blurimg = cv2.GaussianBlur(grayimg, (5, 5), 0)
        edges = cv2.Canny(blurimg, 50, 150)
        
        edges = cv2.dilate(edges, np.ones((3,3), np.uint8), iterations=1)
        
        contures, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        Sudoku_board = None
        drawimg = img.copy()
        screenarea = img.shape[0] * img.shape[1]
        contures = sorted(contures, key=cv2.contourArea, reverse=True)
        
        for conture in contures:
            area = cv2.contourArea(conture)
            
            if area < 0.05 * screenarea:
                continue
                
            perimetr = cv2.arcLength(conture, True)
            approx = cv2.approxPolyDP(conture, 0.05 * perimetr, True)
            
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                ratio = w / float(h)
                
                if ratio < 0.8 or ratio > 1.2:
                    continue
                    
                rect = self.order_points(approx)
                rqdst = np.array([
                    [0, 0], 
                    [449, 0], 
                    [449, 449], 
                    [0, 449]], dtype="float32")
                    
                M = cv2.getPerspectiveTransform(rect, rqdst)   
                Sudoku_board = cv2.warpPerspective(grayimg, M, (450, 450))
                
                cv2.drawContours(drawimg, [approx], -1, (0, 255, 0), 5)
                
                return Sudoku_board, edges, drawimg, approx
        
        return None, edges, drawimg, None

    def split_Sudoku_board(self, Sudoku_board):
        rows = np.vsplit(Sudoku_board, 9)
        boxes = []
        for row in rows:
            cols = np.hsplit(row, 9)
            for box in cols:
                boxes.append(box)
        return boxes

    def read_board(self, boxes):
        if not self.model_loaded:
            return []
            
        board_numbers = []
        
        for box in boxes:
            clean_box = box[5:-5, 5:-5]
            thresh = cv2.adaptiveThreshold(clean_box, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
            
            if cv2.countNonZero(thresh) < 50:
                board_numbers.append(0)
            else:
                resized = cv2.resize(thresh, (20, 20))
                rois = resized.reshape((1, 400)).astype(np.float32)
                
                ret, results, neighbours, dist = self.knn.findNearest(rois, k=1)
                number = int(results[0][0])
                board_numbers.append(number)
                
        return board_numbers