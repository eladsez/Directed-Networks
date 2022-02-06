import random
from tkinter import Tk, Frame, BOTH, YES, Button
from typing import List

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
        self.permission = False
        self.root.bind('<ButtonPress>', self.draw)
        self.root.bind('<ButtonRelease>', self.draw)
        self.root.bind('<Motion>', self.draw_line_move)
        self.create_buttons()
        self.root.mainloop()

    def change_prem(self, start_draw: Button):
        if self.permission:
            start_draw['text'] = '- Start Draw -'
            self.permission = False
        else:
            start_draw.place(relheight=0.0450, relwidth=0.135, relx=0.45, rely=0.07)
            start_draw['text'] = '- Stop Draw -'
            self.canvas.old_coords = None
            self.movement = None
            self.permission = True

    def create_buttons(self):
        start_draw = Button(self.canvas, text="- Start Draw -", borderwidth=0, font=("Helvetica", 13),
                            command=lambda: self.change_prem(start_draw))
        start_draw.place(relheight=0.0450, relwidth=0.135, relx=0.45, rely=0.5)
        Button(self.canvas, text='Clear', borderwidth=0, font=("Helvetica", 13),
               command=self.clear_button).place(relheight=0.0450, relwidth=0.135, relx=0.45, rely=0.02)
        Button(self.canvas, text='Center', borderwidth=0, font=("Helvetica", 13),
               command=lambda: self.draw_from_event(center_node=self.algo.centerPoint()[0])) \
            .place(relheight=0.0450, relwidth=0.135, relx=0.15, rely=0.05)
        Button(self.canvas, text='Shortest Path', borderwidth=0, font=("Helvetica", 13)) \
            .place(relheight=0.0450, relwidth=0.135, relx=0.75, rely=0.05)

    def clear_button(self):
        print(self.algo.graph)
        self.canvas.delete("all")
        self.algo.get_graph().clear_graph()

    def draw(self, event):
        if not self.permission: return
        x, y = event.x, event.y
        if int(event.type) == 4:  # mouse clicked
            self.canvas.old_coords = x, y

        elif int(event.type) == 5:  # mouse released
            if not self.canvas.old_coords:
                return
            x_old, y_old = self.canvas.old_coords

            if x_old + 5 > x > x_old - 5 and y_old + 5 > y > y_old - 5:
                self.canvas.create_oval(x, y, x + 12, y + 12, fill='black')
                self.canvas.create_text(x + 6, y - 12, text=str(self.algo.get_graph().MC), fill='black', font=("Helvetica", 13))
                self.algo.get_graph().add_node(self.algo.get_graph().MC, (x, y))
            else:
                self.canvas.create_line(x, y, x_old, y_old)
                node_id1 = self.algo.get_graph().find_node_by_pos((x_old, y_old))
                node_id2 = self.algo.get_graph().find_node_by_pos((x, y))
                self.algo.get_graph().add_edge(node_id1, node_id2, random.uniform(10.5, 75.5))
            self.canvas.old_coords = None
            self.movement = None

    def draw_line_move(self, event):
        if not self.permission: return
        if self.movement:
            self.canvas.delete(self.movement)
        x, y = event.x, event.y
        if self.canvas.old_coords:
            x1, y1 = self.canvas.old_coords
            self.movement = self.canvas.create_line(x, y, x1, y1)

    def draw_from_event(self, color=None, center_node=None, colored: List[tuple] = None):
        self.canvas.delete("all")
        for id, node in self.algo.get_graph().get_all_v().items():
            self.canvas.create_text(node.pos[0] + 6, node.pos[1] - 12, text=str(id), fill='black', font=("Helvetica", 13))
            if id == center_node:
                self.canvas.create_oval(node.pos[0], node.pos[1], node.pos[0] + 12, node.pos[1] + 12, fill='red')
            else:
                self.canvas.create_oval(node.pos[0], node.pos[1], node.pos[0] + 12, node.pos[1] + 12, fill='black')
            for other_id, w in self.algo.get_graph().all_out_edges_of_node(id).items():
                other_node = self.algo.get_graph().nodes[other_id]
                self.canvas.create_line(node.pos[0] + 6, node.pos[1] + 6, other_node.pos[0] + 6, other_node.pos[1] + 6)


if __name__ == '__main__':
    DrawGraph()
