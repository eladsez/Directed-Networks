from tkinter import Tk, Frame, BOTH, YES
from GUI.Canvas import ResizingCanvas
from Logic.GraphAlgo import GraphAlgo


class DrawGraph:
    def __init__(self):
        self.algo = GraphAlgo()
        self.root = Tk()
        self.frame = Frame(self.root)
        self.frame.pack(fill=BOTH, expand=YES)
        self.canvas = ResizingCanvas(self.frame, width=800, height=500, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.old_coords = None
        self.movement = None
        self.root.bind('<ButtonPress>', self.draw)
        self.root.bind('<ButtonRelease>', self.draw)
        self.root.bind('<Motion>', self.draw_line_move)
        self.root.mainloop()

    def draw(self, event):
        x, y = event.x, event.y
        if int(event.type) == 4:  # mouse clicked
            self.canvas.old_coords = x, y

        elif int(event.type) == 5:  # mouse released
            x_old, y_old = self.canvas.old_coords

            if x_old + 5 > x > x_old - 5 and y_old + 5 > y > y_old - 5:
                self.canvas.create_oval(x, y, x + 12, y + 12, fill='black')
                self.algo.graph.add_node(self.algo.graph.MC, (x, y))
                print(self.algo.graph)
            else:
                self.canvas.create_line(x, y, x_old, y_old)
            self.canvas.old_coords = None
            self.movement = None

    def draw_line_move(self, event):
        if self.movement:
            self.canvas.delete(self.movement)
        x, y = event.x, event.y
        if self.canvas.old_coords:
            x1, y1 = self.canvas.old_coords
            self.movement = self.canvas.create_line(x, y, x1, y1)


if __name__ == '__main__':
    DrawGraph()
