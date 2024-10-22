import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

# Функция для выбора изображения
def select_image():
    global img_path, original_image, canvas, image_on_canvas

    # Открытие диалогового окна для выбора файла
    img_path = filedialog.askopenfilename()

    if len(img_path) > 0:
        # Загрузка изображения с помощью OpenCV
        image = cv2.imread(img_path)

        # Проверка, что изображение загружено успешно
        if image is not None:
            original_image = image.copy()

            # Конвертация изображения из BGR в RGB (OpenCV использует BGR, а tkinter – RGB)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image_tk = ImageTk.PhotoImage(image)

            # Очистка предыдущего изображения
            canvas.delete(image_on_canvas)

            # Установка нового изображения на холст
            image_on_canvas = canvas.create_image(0, 0, anchor='nw', image=image_tk)
            canvas.image = image_tk

            # Настройка размеров холста по размерам изображения
            canvas.config(scrollregion=canvas.bbox(tk.ALL))

        else:
            print("Ошибка загрузки изображения. Пожалуйста, выберите другое изображение.")

# Функция для линейного контрастирования и поэлементных операций
def linear_contrast():
    global original_image, canvas, image_on_canvas
    if original_image is not None:
        # Разделяем оригинальное изображение на три канала
        b_channel, g_channel, r_channel = cv2.split(original_image)

        # Применение поэлементных операций для каждого канала
        b_channel = cv2.add(b_channel, 50)  # Увеличение яркости для синего канала
        g_channel = cv2.add(g_channel, 50)  # Увеличение яркости для зеленого канала
        r_channel = cv2.add(r_channel, 50)  # Увеличение яркости для красного канала

        # Увеличение контраста для каждого канала
        b_channel = cv2.multiply(b_channel, 1.2)  # Увеличение контраста для синего канала
        g_channel = cv2.multiply(g_channel, 1.2)  # Увеличение контраста для зеленого канала
        r_channel = cv2.multiply(r_channel, 1.2)  # Увеличение контраста для красного канала

        # Объединяем каналы обратно в одно изображение
        enhanced_image = cv2.merge((b_channel, g_channel, r_channel))

        # Преобразуем изображение в формат float32 для точных вычислений
        f_image = enhanced_image.astype(np.float32)

        # Вычислим минимальное и максимальное значения пикселей
        min_val = np.min(f_image)
        max_val = np.max(f_image)

        # Применим линейное контрастирование
        scaled_image = 255 * (f_image - min_val) / (max_val - min_val)
        scaled_image = np.clip(scaled_image, 0, 255).astype(np.uint8)  # Убедитесь, что значения в пределах [0, 255]

        # Конвертируем результат в RGB для отображения
        result_image_rgb = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2RGB)  # Правильная конвертация из BGR в RGB
        result_image_rgb = Image.fromarray(result_image_rgb)
        result_image_tk = ImageTk.PhotoImage(result_image_rgb)

        # Обновить изображение на холсте
        canvas.delete(image_on_canvas)
        image_on_canvas = canvas.create_image(0, 0, anchor='nw', image=result_image_tk)
        canvas.image = result_image_tk
    else:
        print("Нет изображения для обработки.")


# Функция для эквализации гистограммы и линейного контрастирования
def equalize_histogram():
    global original_image, canvas, image_on_canvas
    if original_image is not None:
        # Преобразуем изображение в формат YUV для работы с яркостью
        yuv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2YUV)

        # Эквализация гистограммы по каналу яркости (Y)
        yuv_image[:, :, 0] = cv2.equalizeHist(yuv_image[:, :, 0])

        # Преобразование обратно в BGR
        equalized_image = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR)

        # Применение линейного контрастирования после эквализации
        f_image = equalized_image.astype(np.float32)
        min_val = np.min(f_image)
        max_val = np.max(f_image)

        # Применим линейное контрастирование
        scaled_image = 255 * (f_image - min_val) / (max_val - min_val)
        scaled_image = scaled_image.astype(np.uint8)

        # Конвертируем результат в RGB для отображения
        result_image_rgb = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2RGB)
        result_image_rgb = Image.fromarray(result_image_rgb)
        result_image_tk = ImageTk.PhotoImage(result_image_rgb)

        # Обновить изображение на холсте
        canvas.delete(image_on_canvas)
        image_on_canvas = canvas.create_image(0, 0, anchor='nw', image=result_image_tk)
        canvas.image = result_image_tk
    else:
        print("Нет изображения для обработки.")

original_image = None
# Создание основного окна
root = tk.Tk()
root.title("Обработка изображений с помощью OpenCV")

# Добавление заголовка
title = tk.Label(root, text="Обработка изображений с помощью OpenCV", font=("Helvetica", 16))
title.pack(padx=10, pady=10)

# Кнопка для выбора файла
btn_select = tk.Button(root, text="Выбрать изображение", command=select_image)
btn_select.pack(padx=10, pady=10)

# Создание холста для отображения изображения
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# Добавление вертикального скроллбара
v_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Добавление горизонтального скроллбара
h_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# Привязка скроллбаров к холсту
canvas.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

# Переменная для хранения текущего изображения на холсте
image_on_canvas = None

# Кнопка для линейного контрастирования и поэлементных операций
btn_contrast = tk.Button(root, text="Поэлементные операции\nи линейное контрастирование", command=linear_contrast)
btn_contrast.pack(side="left", padx=10, pady=10)

# Кнопка для эквализации гистограммы и линейного контрастирования
btn_histogram = tk.Button(root, text="Эквализация гистограммы\nи линейное контрастирование", command=equalize_histogram)
btn_histogram.pack(side="right", padx=10, pady=10)

# Запуск главного цикла приложения
root.mainloop()
