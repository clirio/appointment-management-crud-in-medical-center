#Controlador Server

import vista_server
from tkinter import Tk


class Controller_server:
    # Lanza al app del server``

    def __init__(self, root_w):
        self.root = root_w
        self.objeto_vista = vista_server.VentanaServer(self.root)


if __name__ == "__main__":
    root = Tk()
    mi_app = Controller_server(root)
    root.mainloop()
