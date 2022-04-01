import random
from time import sleep
from tkinter import Tk, Frame, BOTH, YES, Button, OptionMenu, StringVar, FIRST
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
        self.relx_oval = None
        self.rely_oval = None
        self.canvas.bind('<ButtonPress>', self.draw)
        self.canvas.bind('<ButtonRelease>', self.draw)
        self.canvas.bind('<Motion>', self.draw_line_move)
        self.create_buttons()
        self.root.mainloop()

    def update_oval_relative(self):
        self.relx_oval = self.root.winfo_width() / 80
        self.rely_oval = self.root.winfo_height() / 50


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
        start_draw = Button(self.frame, text="- Start Draw -", borderwidth=0, font=("Helvetica", 13),
                            command=lambda: self.change_prem(start_draw))
        start_draw.place(relheight=0.0450, relwidth=0.135, relx=0.45, rely=0.5)
        Button(self.frame, text='Clear', borderwidth=0, font=("Helvetica", 13),
               command=self.clear_button).place(relheight=0.0450, relwidth=0.135, relx=0.9, rely=0.95)
        Button(self.frame, text='Center', borderwidth=0, font=("Helvetica", 13),
               command=lambda: self.draw_from_event(center_node=self.algo.centerPoint()[0], color='red')) \
            .place(relheight=0.0450, relwidth=0.135, relx=0.15, rely=0.05)
        Button(self.frame, text='MST Kruskal', borderwidth=0, font=("Helvetica", 13),
               command=lambda: self.draw_from_event(color='red', colored=self.algo.kruskal_MST())) \
            .place(relheight=0.0450, relwidth=0.135, relx=0.75, rely=0.05)
        Button(self.frame, text='Connect all Nodes', borderwidth=0, font=("Helvetica", 13),
               command=self.auto_clique) \
            .place(relheight=0.0450, relwidth=0.205, relx=0.30, rely=0.02)
        # datatype of menu text
        # clicked = StringVar()
        # clicked.set("Choose an Algorithm")
        # options = [
        #     "MST Kruskal",
        #     "Dijkstra",
        #     "Center",
        #     "TSP",
        # ]
        # drop = OptionMenu(self.frame, clicked, *options)
        # drop.place(relheight=0.05, relwidth=0.2, relx=0.0, rely=0.0)
        # drop["menu"].configure(borderwidth=0, font=("Helvetica", 13))

    def clear_button(self):
        self.canvas.delete("all")
        self.algo.get_graph().clear_graph()

    def auto_clique(self):
        # self.algo.get_graph().connect_all()
        self.algo.convex_hull()
        self.draw_from_event()

    def draw(self, event):
        if not self.permission: return
        x, y = event.x, event.y
        if int(event.type) == 4:  # mouse clicked
            self.canvas.old_coords = x, y

        elif int(event.type) == 5:  # mouse released
            if not self.canvas.old_coords:
                return
            x_old, y_old = self.canvas.old_coords
            self.update_oval_relative()
            if x_old + 10 > x > x_old - 10 and y_old + 10 > y > y_old - 10:
                self.canvas.create_oval(x, y, x + self.relx_oval, y + self.rely_oval, fill='black')
                self.canvas.create_text(x + 6, y - 12, text=str(self.algo.get_graph().MC),
                                        fill='black', font=("Helvetica", 13))
                self.algo.get_graph().add_node(self.algo.get_graph().MC, (x, y))
            elif self.line_valid_check((x, y), (x_old, y_old)):
                self.canvas.create_line(x, y, x_old, y_old, arrow=FIRST)
                node_id1 = self.algo.get_graph().find_node_by_pos((x_old, y_old))
                node_id2 = self.algo.get_graph().find_node_by_pos((x, y))
                self.algo.get_graph().add_edge(node_id1, node_id2, random.uniform(0.5, 10.5))
            if self.movement:
                self.canvas.delete(self.movement)
            self.canvas.old_coords = None
            self.movement = None

    def draw_line_move(self, event):
        if not self.permission: return
        if self.movement:
            self.canvas.delete(self.movement)
        x, y = event.x, event.y
        if self.canvas.old_coords:
            x1, y1 = self.canvas.old_coords
            self.movement = self.canvas.create_line(x, y, x1, y1, arrow=FIRST)

    def line_valid_check(self, pos1, pos2):
        check_pos1 = check_pos2 = False
        range_ = 15
        for node_id, node in self.algo.get_graph().get_all_v().items():
            if node.pos[0] - range_ < pos1[0] < node.pos[0] + range_ and \
                    node.pos[1] - range_ < pos1[1] < node.pos[1] + range_:
                check_pos1 = True
            if node.pos[0] - range_ < pos2[0] < node.pos[0] + range_ and \
                    node.pos[1] - range_ < pos2[1] < node.pos[1] + range_:
                check_pos2 = True
            if check_pos1 and check_pos2: break

        return check_pos1 and check_pos2

    def draw_from_event(self, color=None, center_node=None, colored: List[tuple] = None):
        self.canvas.delete("all")
        self.update_oval_relative()
        for id, node in self.algo.get_graph().get_all_v().items():
            self.canvas.create_text(node.pos[0] + 6, node.pos[1] - 12, text=str(id), fill='black',
                                    font=("Helvetica", 13))

            if id == center_node:
                self.canvas.create_oval(node.pos[0], node.pos[1], node.pos[0] + self.rely_oval,
                                        node.pos[1] + self.relx_oval, fill=color)
            else:
                self.canvas.create_oval(node.pos[0], node.pos[1], node.pos[0] + self.relx_oval
                                        , node.pos[1] + self.rely_oval, fill='black')

        for (id, other_id) in self.algo.get_graph().get_all_e().keys():
            node = self.algo.get_graph().nodes[id]
            other_node = self.algo.get_graph().nodes[other_id]
            self.canvas.update()
            sleep(1)
            if colored:
                if (id, other_id) in colored or (other_id, id) in colored:
                    self.canvas.create_line(node.pos[0] + 6, node.pos[1] + 6, other_node.pos[0] + 6,
                                            other_node.pos[1] + 6
                                            , fill=color, arrow=FIRST)
                else:
                    self.canvas.create_line(node.pos[0] + 6, node.pos[1] + 6, other_node.pos[0] + 6,
                                            other_node.pos[1] + 6, arrow=FIRST)
            else:
                self.canvas.create_line(node.pos[0] + 6, node.pos[1] + 6, other_node.pos[0] + 6,
                                        other_node.pos[1] + 6, arrow=FIRST)


if __name__ == '__main__':
    DrawGraph()
