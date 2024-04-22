from tkinter import N, W, S, Label, Entry, StringVar, Button
from tkinter import ttk
import subprocess
import os
import threading
import sys
from pathlib import Path

elproceso = ""


class VentanaServer:
    ### Ventana App Server

    def __init__(self, window):
        self.e_desafio = window
        self.e_desafio.title("Servidor App Turnera")
        self.e_desafio.configure(background="Green")

        self.raiz = Path(__file__).resolve().parent
        self.ruta_server = os.path.join(self.raiz, "src", "servidor",
                                        "udp_server_t.py")

        self.boton_en = Button(
            self.e_desafio,
            text="Encender Server",
            command=lambda: self.conexion(),
            background="light green",
            font=("", 10),
        )
        self.boton_en.grid(row=0, column=0)

        self.boton_ap = Button(
            self.e_desafio,
            text="Apagar Server",
            command=lambda: self.apagar(),
            background="light green",
            font=("", 10),
        )
        self.boton_ap.grid(row=0, column=1)

    def conexion(self, ):
        """
        Conexión del servidor
        """
        if elproceso != "":
            elproceso.kill()
            threading.Thread(target=self.encender, args=(True, ),
                             daemon=True).start()
        else:
            threading.Thread(target=self.encender, args=(True, ),
                             daemon=True).start()

    def encender(self, arg):
        """
        Método para el encendido del servidor
        """
        path = self.ruta_server
        if arg is True:
            global elproceso
            elproceso = subprocess.Popen([sys.executable, path])
            elproceso.communicate()
            print("El servidor se ha encendido")
        else:
            print("")

    def apagar(self, ):
        """
        Método para el apagado del servidor
        """
        global elproceso
        if elproceso != "":
            elproceso.kill()
            print("El servidor se ha apagado")
