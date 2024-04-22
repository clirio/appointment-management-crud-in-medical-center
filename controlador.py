"""
Archivo controlador.py del modelo MVC
"""

from tkinter import Tk
import vista
import observador


class Controller:
    def __init__(self, root_w):
        """
        Constructor de la clase Controller
        :param root_w:  objeto que se instancia con la clase Panel.
        """
        # creo atributos de instancia para la ventana y la instancia de panel
        self.root = root_w
        self.objeto_vista = vista.Panel(self.root)  # creo un objeto de panel.
        self.el_observador = observador.ConcreteObserverA(self.objeto_vista.objeto_base)


if __name__ == "__main__":

    # de aca para abajo solo no pueden ver el codigo,
    # los que usen el codigo (los terceros)
    root = Tk()
    mi_app = Controller(root)
    mi_app.objeto_vista.mostrar()

    # aca se lanza la ventana... creo un objeto llamado mi_app
    root.mainloop()
