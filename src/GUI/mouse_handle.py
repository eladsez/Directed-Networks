from tkinter import Tk, Button, Canvas, LEFT


def draw(event):
    x, y = event.x, event.y
    if int(event.type) == 4:  # mouse clicked
        canvas.old_coords = x, y
    elif int(event.type) == 5:  # mouse released
        x_old, y_old = canvas.old_coords
        if x_old + 3 > x > x_old - 3 and y_old + 3 > y > y_old - 3:
            canvas.create_oval(x, y, x + 7, y + 7, fill='black')
        else:
            canvas.create_line(x, y, x_old, y_old)
        canvas.old_coords = None


def draw_line_move(event):
    global line
    if line:
        canvas.delete(line)
    x, y = event.x, event.y
    if canvas.old_coords:
        x1, y1 = canvas.old_coords
        line = canvas.create_line(x, y, x1, y1)


root = Tk()

canvas = Canvas(root, width=400, height=400)
canvas.pack()
canvas.old_coords = None
line = None
root.bind('<ButtonPress>', draw)
root.bind('<ButtonRelease>', draw)
root.bind('<Motion>', draw_line_move)
root.mainloop()
