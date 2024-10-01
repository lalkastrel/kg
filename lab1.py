import tkinter as tk
from tkinter import colorchooser, Toplevel
import colorsys
from PIL import ImageColor

R, G, B = (0, 0, 0)

# Функции для преобразования цветов
def rgb_to_cmyk(r, g, b):
    if (r == 0) and (g == 0) and (b == 0):
        return 0, 0, 0, 1
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255
    k = min(c, m, y)
    c = (c - k) / (1 - k)
    m = (m - k) / (1 - k)
    y = (y - k) / (1 - k)
    return round(c, 2), round(m, 2), round(y, 2), round(k, 2)

def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return int(r), int(g), int(b)

def rgb_to_hls(r, g, b):
    hls = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
    return round(hls[0]*360, 2), round(hls[1]*100, 2), round(hls[2]*100, 2)

def hls_to_rgb(h, l, s):
    rgb = colorsys.hls_to_rgb(h/360, l/100, s/100)
    return int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)

def update_displayed_color(r, g, b):
    color = f'#{r:02x}{g:02x}{b:02x}'
    color_display.config(bg=color)

def update_colors_from_rgb():
    r = int(red_slider.get())
    g = int(green_slider.get())
    b = int(blue_slider.get())
    print(r, g, b)
    update_displayed_color(r, g, b)
    global R
    global G
    global B
    R, G, B = (r, g, b)
    
    rgb_label.config(text=f"RGB: {r}, {g}, {b}")
    c, m, y, k = rgb_to_cmyk(r, g, b)
    cmyk_label.config(text=f"CMYK: {c}, {m}, {y}, {k}")
    cyan_slider.set(c * 100)
    magenta_slider.set(m * 100)
    yellow_slider.set(y * 100)
    black_slider.set(k * 100)
    
    h, l, s = rgb_to_hls(r, g, b)
    hls_label.config(text=f"HLS: {int(h)}, {int(l)}, {int(s)}")
    hue_slider.set(h)
    lightness_slider.set(l)
    saturation_slider.set(s)



def update_colors_from_cmyk():
    c = cyan_slider.get() / 100
    m = magenta_slider.get() / 100
    y = yellow_slider.get() / 100
    k = black_slider.get() / 100
    print(c, m, y, k)
    
    global R
    global G
    global B
    r, g, b = cmyk_to_rgb(c, m, y, k)
    if abs(R - r) < 5 and abs(G - g) < 5 and abs(B - b) < 5:
        r, g, b = R, G, B
        print('RGB', R, G, B)
    red_slider.set(r)
    green_slider.set(g)
    blue_slider.set(b)

    update_displayed_color(r, g, b)

    h, l, s = rgb_to_hls(r, g, b)
    hls_label.config(text=f"HLS: {int(h)}, {int(l)}, {int(s)}")
    hue_slider.set(h)
    lightness_slider.set(l)
    saturation_slider.set(s)
    
    # update_colors_from_rgb()

def update_colors_from_hls():
    h = hue_slider.get()
    l = lightness_slider.get()
    s = saturation_slider.get()
    print(h, l, s)
    
    r, g, b = hls_to_rgb(h, l, s)
    red_slider.set(r)
    green_slider.set(g)
    blue_slider.set(b)

    update_displayed_color(r, g, b)

    c, m, y, k = rgb_to_cmyk(r, g, b)
    cmyk_label.config(text=f"CMYK: {c}, {m}, {y}, {k}")
    cyan_slider.set(c * 100)
    magenta_slider.set(m * 100)
    yellow_slider.set(y * 100)
    black_slider.set(k * 100)

    if abs(R - r) < 5 and abs(G - g) < 5 and abs(B - b) < 5:
        r, g, b = R, G, B
        print('RGB', R, G, B)
    red_slider.set(r)
    green_slider.set(g)
    blue_slider.set(b)

    # update_colors_from_rgb()

def choose_color():
    color = colorchooser.askcolor()[0]
    if color:
        red_slider.set(color[0])
        green_slider.set(color[1])
        blue_slider.set(color[2])
        update_colors_from_rgb()

# Открытие окна для ручного ввода RGB значений
def open_rgb_window():
    window = Toplevel(root)
    window.title("Введите RGB")
    
    tk.Label(window, text="Red:").pack()
    red_entry = tk.Entry(window)
    red_entry.pack()
    
    tk.Label(window, text="Green:").pack()
    green_entry = tk.Entry(window)
    green_entry.pack()
    
    tk.Label(window, text="Blue:").pack()
    blue_entry = tk.Entry(window)
    blue_entry.pack()
    
    def apply_rgb():
        try:
            r = int(red_entry.get())
            g = int(green_entry.get())
            b = int(blue_entry.get())
            red_slider.set(r)
            green_slider.set(g)
            blue_slider.set(b)
            update_colors_from_rgb()
        except ValueError:
            pass  # Игнорировать неправильный ввод
        window.destroy()
    
    tk.Button(window, text="Применить", command=apply_rgb).pack()

# Открытие окна для ручного ввода CMYK значений
def open_cmyk_window():
    window = Toplevel(root)
    window.title("Введите CMYK")
    
    tk.Label(window, text="Cyan:").pack()
    cyan_entry = tk.Entry(window)
    cyan_entry.pack()
    
    tk.Label(window, text="Magenta:").pack()
    magenta_entry = tk.Entry(window)
    magenta_entry.pack()
    
    tk.Label(window, text="Yellow:").pack()
    yellow_entry = tk.Entry(window)
    yellow_entry.pack()
    
    tk.Label(window, text="Black:").pack()
    black_entry = tk.Entry(window)
    black_entry.pack()
    
    def apply_cmyk():
        try:
            c = float(cyan_entry.get()) / 100
            m = float(magenta_entry.get()) / 100
            y = float(yellow_entry.get()) / 100
            k = float(black_entry.get()) / 100
            cyan_slider.set(c * 100)
            magenta_slider.set(m * 100)
            yellow_slider.set(y * 100)
            black_slider.set(k * 100)
            update_colors_from_cmyk()
        except ValueError:
            pass
        window.destroy()
    
    tk.Button(window, text="Применить", command=apply_cmyk).pack()

# Открытие окна для ручного ввода HLS значений
def open_hls_window():
    window = Toplevel(root)
    window.title("Введите HLS")
    
    tk.Label(window, text="Hue:").pack()
    hue_entry = tk.Entry(window)
    hue_entry.pack()
    
    tk.Label(window, text="Lightness:").pack()
    lightness_entry = tk.Entry(window)
    lightness_entry.pack()
    
    tk.Label(window, text="Saturation:").pack()
    saturation_entry = tk.Entry(window)
    saturation_entry.pack()
    
    def apply_hls():
        try:
            h = float(hue_entry.get())
            l = float(lightness_entry.get())
            s = float(saturation_entry.get())
            hue_slider.set(h)
            lightness_slider.set(l)
            saturation_slider.set(s)
            update_colors_from_hls()
        except ValueError:
            pass  # Игнорировать неправильный ввод
        window.destroy()
    
    tk.Button(window, text="Применить", command=apply_hls).pack()

# Основное окно
root = tk.Tk()
root.title("Цветовое приложение")

# Площадка для отображения цвета
color_display = tk.Label(root, text="", width=40, height=10, bg="white")
color_display.pack()

# Кнопки для ручного ввода значений
tk.Button(root, text="Ввести RGB", command=open_rgb_window).pack()
tk.Button(root, text="Ввести CMYK", command=open_cmyk_window).pack()
tk.Button(root, text="Ввести HLS", command=open_hls_window).pack()

# RGB компоненты
tk.Label(root, text="RGB:").pack()
red_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Red", command=lambda x: update_colors_from_rgb())
red_slider.pack()
green_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Green", command=lambda x: update_colors_from_rgb())
green_slider.pack()
blue_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Blue", command=lambda x: update_colors_from_rgb())
blue_slider.pack()

# CMYK компоненты
tk.Label(root, text="CMYK:").pack()
cyan_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Cyan", command=lambda x: update_colors_from_cmyk())
cyan_slider.pack()
magenta_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Magenta", command=lambda x: update_colors_from_cmyk())
magenta_slider.pack()
yellow_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Yellow", command=lambda x: update_colors_from_cmyk())
yellow_slider.pack()
black_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Black", command=lambda x: update_colors_from_cmyk())
black_slider.pack()

# HLS компоненты
tk.Label(root, text="HLS:").pack()
hue_slider = tk.Scale(root, from_=0, to=360, orient="horizontal", label="Hue", command=lambda x: update_colors_from_hls())
hue_slider.pack()
lightness_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Lightness", command=lambda x: update_colors_from_hls())
lightness_slider.pack()
saturation_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Saturation", command=lambda x: update_colors_from_hls())
saturation_slider.pack()

# Кнопка для выбора цвета
color_button = tk.Button(root, text="Выбрать цвет", command=choose_color)
color_button.pack()

# Метки для отображения текущих значений
rgb_label = tk.Label(root, text="RGB: ")
rgb_label.pack()
cmyk_label = tk.Label(root, text="CMYK: ")
cmyk_label.pack()
hls_label = tk.Label(root, text="HLS: ")
hls_label.pack()

# Запуск главного цикла
root.mainloop()
