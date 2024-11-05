import tkinter as tk
from tkinter import ttk
import time

# Function to draw the grid and labels on the canvas
def draw_grid(canvas, width, height, step=20):
    # Draw vertical and horizontal lines
    for i in range(0, width, step):
        canvas.create_line([(i, 0), (i, height)], tag='grid_line', fill='gray')
        if i != width // 2:  # Avoid adding a label at the origin
            # X-axis labels
            x_label = (i - width // 2) // step
            canvas.create_text(i, height // 2 + 10, text=str(x_label), fill="black", font=("Arial", 8))
    for i in range(0, height, step):
        canvas.create_line([(0, i), (width, i)], tag='grid_line', fill='gray')
        if i != height // 2:  # Avoid adding a label at the origin
            # Y-axis labels
            y_label = (height // 2 - i) // step
            canvas.create_text(width // 2 + 15, i, text=str(y_label), fill="black", font=("Arial", 8))

    # Draw the axes
    canvas.create_line(width // 2, 0, width // 2, height, arrow=tk.LAST, fill='black', width=2)
    canvas.create_line(0, height // 2, width, height // 2, arrow=tk.LAST, fill='black', width=2)
    
    # Add labels for the axes
    canvas.create_text(width - 10, height // 2 - 10, text="X", fill="black", font=("Arial", 10, "bold"))
    canvas.create_text(width // 2 + 10, 10, text="Y", fill="black", font=("Arial", 10, "bold"))

def step_by_step_line(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    if abs(dx) > abs(dy):
        return step_by_step_line_x_based(x0, y0, x1, y1)
    else:
        return step_by_step_line_y_based(x0, y0, x1, y1)

def step_by_step_line_x_based(x0, y0, x1, y1):
    start_time = time.perf_counter()
    points = []
    
    dx = x1 - x0
    dy = y1 - y0

    # Проверяем, что наклон не горизонтальный
    if dx == 0:
        return [(x0, y) for y in range(min(y0, y1), max(y0, y1) + 1)]

    # Вычисляем наклон и сдвиг
    K = dy / dx
    b = y0 - K * x0  # преобразуем уравнение y = Kx + b

    # Определяем направление изменения x
    step_x = 1 if x1 > x0 else -1

    # Генерируем точки
    x = x0
    while (x <= x1 if step_x > 0 else x >= x1):
        y = K * x + b  # Вычисляем точное значение y для текущего x
        points.append((x, round(y)))  # Округляем y и добавляем точку
        x += step_x

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    global label
    label.config(text='Time: '+ str(execution_time * 1000) + 'ms')
    return points

def step_by_step_line_y_based(x0, y0, x1, y1):
    start_time = time.perf_counter()
    points = []
    
    dx = x1 - x0
    dy = y1 - y0

    # Проверяем, что наклон не вертикальный
    if dy == 0:
        return [(x, y0) for x in range(min(x0, x1), max(x0, x1) + 1)]

    # Вычисляем наклон и сдвиг
    K = dx / dy
    b = x0 - K * y0  # преобразуем уравнение y = Kx + b

    # Определяем направление изменения y
    step_y = 1 if y1 > y0 else -1

    # Генерируем точки
    y = y0
    while (y <= y1 if step_y > 0 else y >= y1):
        x = K * y + b  # Вычисляем точное значение x для текущего y
        print(x, y)
        points.append((round(x), y))  # Округляем x и добавляем точку
        y += step_y

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    global label
    label.config(text='Time: '+ str(execution_time * 1000) + 'ms')
    return points


def dda_line(x0, y0, x1, y1):
    start_time = time.perf_counter()
    points = []
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x0, y0
    for _ in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    global label
    label.config(text='Time: '+ str(execution_time * 1000) + 'ms')
    return points

# Bresenham's line algorithm to draw line pixel by pixel
def bresenham_line(x0, y0, x1, y1):
    start_time = time.perf_counter()
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    global label
    label.config(text='Time: '+ str(execution_time * 1000) + 'ms')
    return points

def bresenham_circle(xc, yc, r):
    start_time = time.perf_counter()
    points = []
    x, y = 0, r
    d = 3 - 2 * r
    while x <= y:
        points += [(xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
                   (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)]
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    global label
    label.config(text='Time: '+ str(execution_time * 1000) + 'ms')
    return points

def ipart(x):
    # Возвращает целую часть x
    return int(x)

def fpart(x):
    # Возвращает дробную часть x
    return x - ipart(x)

def wu_line(x1, y1, x2, y2):
    start_time = time.perf_counter()
    points = []
    def plot(x, y, c):
        # Функция для рисования точки с координатами (x, y) и яркостью c
        # Здесь просто печатаем значения, в реальном случае можно рисовать на холсте
        points.append((x,y,c))
    # Основная функция рисования линии
    if x2 < x1:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1
    gradient = dy / dx if dx != 0 else 1

    # Обработать начальную точку
    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = 1 - fpart(x1 + 0.5)
    xpxl1 = xend  # Будет использоваться в основном цикле
    ypxl1 = ipart(yend)

    # Рисуем точки в начальной позиции
    plot(xpxl1, ypxl1, (1 - fpart(yend)) * xgap)
    plot(xpxl1, ypxl1 + 1, fpart(yend) * xgap)

    intery = yend + gradient  # Первое y-пересечение для цикла

    # Обработать конечную точку
    xend = round(x2)
    yend = y2 + gradient * (xend - x2)
    xgap = fpart(x2 + 0.5)
    xpxl2 = xend  # Будет использоваться в основном цикле
    ypxl2 = ipart(yend)

    # Рисуем точки в конечной позиции
    plot(xpxl2, ypxl2, (1 - fpart(yend)) * xgap)
    plot(xpxl2, ypxl2 + 1, fpart(yend) * xgap)

    # Основной цикл
    for x in range(xpxl1 + 1, xpxl2):
        plot(x, ipart(intery), 1 - fpart(intery))
        plot(x, ipart(intery) + 1, fpart(intery))
        intery += gradient

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    global label
    label.config(text='Time: '+ str(execution_time))
    return points



# Function to draw the line on the canvas using Bresenham's algorithm
def draw_shape():
    # Clear previous line
    # canvas.delete("line")

    # Retrieve coordinates from entries
    x0 = int(entry_x0.get())
    y0 = int(entry_y0.get())
    x1 = int(entry_x1.get())
    y1 = int(entry_y1.get())
    
    selected_alg = algorithm.get()
    if selected_alg == "Step-by-Step":
        points = step_by_step_line(x0, y0, x1, y1)
    elif selected_alg == "DDA":
        points = dda_line(x0, y0, x1, y1)
    elif selected_alg == "Bresenham":
        points = bresenham_line(x0, y0, x1, y1)
    elif selected_alg == "Bresenham Circle":
        r = abs(x1 - x0)  # Radius from (x0, y0) to (x1, y1)
        points = bresenham_circle(x0, y0, r)
    elif selected_alg == "Wu's Algorithm":
        points = wu_line(x0, y0, x1, y1)
        for (x, y, intensity) in points:
            print(intensity)
            x_canvas = canvas_width // 2 + x * step
            y_canvas = canvas_height // 2 - y * step - step
            color_intensity = int(255 * abs(1 -intensity))
            color = f'#{color_intensity:02x}{color_intensity:02x}{color_intensity:02x}'
            canvas.create_rectangle(x_canvas, y_canvas, x_canvas + step, y_canvas + step, fill=color, outline="", tag="line")
        return


    # Draw each pixel on the grid
    for (x, y) in points:
        x_canvas = canvas_width // 2 + x * step
        y_canvas = canvas_height // 2 - y * step - step
        canvas.create_rectangle(x_canvas, y_canvas, x_canvas + step, y_canvas + step, fill="black", outline="black", tag="line")

def clear_canvas():
    canvas.delete("line")

# GUI setup
root = tk.Tk()
root.title("Line Drawing Algorithms")

# Canvas settings
canvas_width = 600
canvas_height = 600
step = 20
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.grid(row=0, column=0, rowspan=10)
draw_grid(canvas, canvas_width, canvas_height, step)

label = ttk.Label(root, text="Time:", font=("Arial", 10))
label.grid(row=11, column=0, padx=10, pady=5, sticky="w")

# Control Panel
control_frame = tk.Frame(root)
control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

# Algorithm selection radio buttons
algorithm = tk.StringVar()
algorithm.set("Step-by-Step")
algorithms = ["Step-by-Step", "DDA", "Bresenham", "Bresenham Circle", "Wu's Algorithm"]
for alg in algorithms:
    ttk.Radiobutton(control_frame, text=alg, variable=algorithm, value=alg).pack(anchor="w")

# Entry fields for coordinates
entry_x0 = ttk.Entry(control_frame, width=5)
entry_x1 = ttk.Entry(control_frame, width=5)
entry_y0 = ttk.Entry(control_frame, width=5)
entry_y1 = ttk.Entry(control_frame, width=5)

# Coordinate Labels
ttk.Label(control_frame, text="x0:").pack()
entry_x0.pack()
ttk.Label(control_frame, text="y0:").pack()
entry_y0.pack()
ttk.Label(control_frame, text="x1:").pack()
entry_x1.pack()
ttk.Label(control_frame, text="y1:").pack()
entry_y1.pack()

ttk.Button(control_frame, text="Draw", command=draw_shape).pack(pady=10)
ttk.Button(control_frame, text="Clear Canvas", command=clear_canvas).pack(pady=5)
# ttk.Button(control_frame, text="Change Scale").pack()

root.mainloop()
