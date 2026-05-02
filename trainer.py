import cv2
import numpy as np
import time
import os
from core.visual import Visual
from core.imgconvert import ImgConvert

def collect_data():
    if not os.path.exists('data'):
        os.makedirs('data')

    vis = Visual()
    conv = ImgConvert()

    print("[Система]: Открой Судоку. Захват экрана через 3 секунды...")
    time.sleep(10)

    img = vis.capture()
    Sudoku_board, edges, drawimg, approx = conv.get_board_logic(img)

    if Sudoku_board is None:
        print("Поле не найдено! Убедись, что судоку открыто.")
        return

    boxes = conv.split_Sudoku_board(Sudoku_board)
    print("Начинаем сбор данных! Вводи цифры с клавиатуры.")
    print("Если видишь мусор/ошибку - нажми ПРОБЕЛ для пропуска.")
    print("Для выхода нажми ESC.")

    samples = []
    responses = []

    for box in boxes:
        clean_box = box[5:-5, 5:-5]
        
        thresh = cv2.adaptiveThreshold(clean_box, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        
        if cv2.countNonZero(thresh) < 50:
            continue
            
        resized = cv2.resize(thresh, (20, 20))
        
        show_img = cv2.resize(resized, (200, 200), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("Training - Press 1-9 (Space to skip)", show_img)
        
        key = cv2.waitKey(0)
        
        if 49 <= key <= 57:
            number = key - 48
            print(f"Сохранено: {number}")
            samples.append(resized.reshape((1, 400))) 
            responses.append(number)
        elif key == 27:
            break
            
    cv2.destroyAllWindows()

    if len(samples) > 0:
        samples = np.float32(samples).reshape((len(samples), 400))
        responses = np.array(responses, np.float32).reshape((len(responses), 1))
        
        if os.path.exists('data/samples.data'):
            old_samples = np.loadtxt('data/samples.data', np.float32).reshape(-1, 400)
            old_responses = np.loadtxt('data/responses.data', np.float32).reshape(-1, 1)
            
            samples = np.append(old_samples, samples, axis=0)
            responses = np.append(old_responses, responses, axis=0)

        np.savetxt('data/samples.data', samples)
        np.savetxt('data/responses.data', responses)
        print(f"Successfully saved! Total examples in database: {len(responses)}")
if __name__ == "__main__":
    collect_data()