"""
Archivo vista.py del modelo MVC
"""

from tkinter import Label
from tkinter import StringVar
from tkinter import Entry
from tkinter import Button
from tkinter import OptionMenu
from tkinter import ttk
from tkcalendar import Calendar
import modelo
import controlador
import os
from PIL import Image, ImageTk
from mis_decoradores import inicio_app


class Panel:
    @inicio_app
    def __init__(self, window):
        """

        Constructor de la clase Panel

        param window:  parametro de entrada para la creacion de la "ventana" de la app

        """
        self.objeto_base = modelo.Abmc()
        # root.geometry("800x600")
        self.root = window
        self.root.title("Turnera v1.0")
        # Cambio del ícono de la App
        self.root.iconbitmap(
            os.path.dirname(os.path.abspath(__file__)) + "\img\Turnera icono3.ico"
        )
        # Definicion de variables para icono de botones
        self.icono_original = Image.open(
            os.path.dirname(os.path.abspath(__file__)) + "\img\manual.jfif"
        )
        self.icono_modificado = self.icono_original.resize((20, 20))
        self.icono_mostrar = ImageTk.PhotoImage(self.icono_modificado)

        # Definicion de variables de entrada
        self.var_apellido = StringVar()
        self.var_nombre = StringVar()
        self.var_dni = StringVar()
        self.var_tel = StringVar()
        self.var_correo = StringVar()

        # Los labels y cajas de las entradas
        self.nombre_l = Label(self.root, text="Nombre", font=("", 12))
        self.nombre_l.grid(row=0, column=0, sticky="w")
        self.apellido_l = Label(self.root, text="Apellido", font=("", 12))
        self.apellido_l.grid(row=1, column=0, sticky="w")
        self.dni_l = Label(self.root, text="D.N.I.", font=("", 12))
        self.dni_l.grid(row=2, column=0, sticky="w")
        self.tel_l = Label(self.root, text="Telefono", font=("", 12))
        self.tel_l.grid(row=3, column=0, sticky="w")
        self.correo_l = Label(self.root, text="Correo", font=("", 12))
        self.correo_l.grid(row=4, column=0, sticky="w")
        self.especial_l = Label(self.root, text="Especialidad", font=("", 12))
        self.especial_l.grid(row=5, column=0, sticky="w")

        self.nombre_e = Entry(self.root, textvariable=self.var_nombre)
        self.nombre_e.grid(row=0, column=1, sticky="w")
        self.apellido_e = Entry(self.root, textvariable=self.var_apellido)
        self.apellido_e.grid(row=1, column=1, sticky="w")
        self.dni_e = Entry(self.root, textvariable=self.var_dni)
        self.dni_e.grid(row=2, column=1, sticky="w")
        self.tel_e = Entry(self.root, textvariable=self.var_tel)
        self.tel_e.grid(row=3, column=1, sticky="w")
        self.correo_e = Entry(self.root, textvariable=self.var_correo)
        self.correo_e.grid(row=4, column=1, sticky="w")
        self.correo_e.insert(0, "ejemplo@ejemplo.com")
        self.correo_e.bind("<FocusIn>", self.objeto_base.entry_delete)
        self.correo_e.config(fg="grey", font=("", 8))

        # *********************************** Especialidades
        self.var_especialidades = StringVar(self.root)  # Variable de especialidades
        # Dropdown
        self.var_especialidades.set(modelo.OPTIONS[0])
        self.dropdown = OptionMenu(self.root, self.var_especialidades, *modelo.OPTIONS)
        self.dropdown.grid(row=5, column=1, sticky="w")
        self.dropdown.config(font=("", 14))

        # *********************************** Calendario
        self.fecha_l = Label(self.root, text="Fecha", font=("", 12))
        self.fecha_l.grid(row=0, rowspan=5, column=3, sticky="w")
        # Calendario
        self.var_cal = Calendar(self.root, selectmode="day")
        self.var_cal.grid(row=0, rowspan=5, column=4, sticky="w")

        # *********************************** Horarios

        self.horario_l = Label(self.root, text="Horario", font=("", 12))
        self.horario_l.grid(row=5, column=3, sticky="w")
        # Dropdown
        self.var_horarios = StringVar(self.root)
        self.var_horarios.set(self.objeto_base.hora_min()[0])
        self.dropdown = OptionMenu(
            self.root, self.var_horarios, *self.objeto_base.hora_min()
        )
        self.dropdown.grid(row=5, column=4, sticky="we")
        self.dropdown.config(font=("", 14))

        # *********************************** Tree
        self.tree = ttk.Treeview(self.root)
        # Columnas
        self.tree["columns"] = (
            "col1",
            "col2",
            "col3",
            "col4",
            "col5",
            "col6",
            "col7",
            "col8",
        )
        self.tree.column(
            "#0", width=80, minwidth=80, anchor="w"
        )  # es la primera columna
        self.tree.column("col1", width=80, minwidth=80, anchor="w")
        self.tree.column("col2", width=80, minwidth=80, anchor="w")
        self.tree.column("col3", width=80, minwidth=80, anchor="w")
        self.tree.column("col4", width=80, minwidth=80, anchor="w")
        self.tree.column("col5", width=80, minwidth=80, anchor="w")
        self.tree.column("col6", width=80, minwidth=80, anchor="w")
        self.tree.column("col7", width=80, minwidth=80, anchor="w")
        self.tree.column("col8", width=80, minwidth=80, anchor="w")
        # Headings
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Nombre")
        self.tree.heading("col2", text="Apellido")
        self.tree.heading("col3", text="DNI")
        self.tree.heading("col4", text="Teléfono")
        self.tree.heading("col5", text="Email")
        self.tree.heading("col6", text="Especialidad")
        self.tree.heading("col7", text="Fecha")
        self.tree.heading("col8", text="Horario")
        # Saco el treeview por pantalla
        self.tree.grid(column=0, row=16, columnspan=9)
        # self.objeto_base.mostrar_al_iniciar(self.tree)

        # *********************************** Scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=16, column=9, sticky="ns")

        # **************************** BOTONES
        # ABMC
        self.alta_b = Button(
            self.root,
            text="Alta",
            command=lambda: self.objeto_base.alta_sqlite3(
                self.var_nombre.get(),
                self.var_apellido.get(),
                self.var_dni.get(),
                self.var_tel.get(),
                self.var_correo.get(),
                self.var_especialidades.get(),
                self.var_cal.get_date(),
                self.var_horarios.get(),
                self.tree,
            ),  # tambien mando el tree para que se me actualice
            bg="light green",
            fg="black",
            width=10,
            font=("", 12),
        )
        self.alta_b.grid(row=0, column=7, sticky="")
        # tomo .get() a una funcion del mismo bucle, tengo que mandarla como lambda

        self.modificar_b = Button(
            self.root,
            text="Modificar",
            command=lambda: self.objeto_base.modificar_sqlite3(
                self.var_nombre.get(),
                self.var_apellido.get(),
                self.var_dni.get(),
                self.var_tel.get(),
                self.var_correo.get(),
                self.var_especialidades.get(),
                self.var_cal.get_date(),
                self.var_horarios.get(),
                self.tree,
                self.tree.focus(),
            ),  # tambien mando el tree para que se me actualice
            bg="light blue",
            fg="black",
            width=10,
            font=("", 12),
        )
        self.modificar_b.grid(row=1, column=7, sticky="")

        self.baja_b = Button(
            self.root,
            text="Eliminar",
            command=lambda: self.objeto_base.baja_sqlite3(
                self.tree.selection(), self.tree
            ),
            bg="red",
            fg="black",
            width=10,
            font=("", 12),
        )
        self.baja_b.grid(row=2, column=7, sticky="")

        self.consultar_b = Button(
            self.root,
            text="Consultar",
            command=lambda: self.objeto_base.consultar_dni(self.var_dni.get()),
            bg="light yellow",
            fg="black",
            width=10,
            font=("", 12),
        )
        self.consultar_b.grid(row=3, column=7, sticky="")

        self.limpiar_b = Button(
            self.root,
            text="Limpiar",
            command=lambda: self.objeto_base.limpiar(
                self.nombre_e,
                self.apellido_e,
                self.dni_e,
                self.tel_e,
                self.correo_e,
                self.var_especialidades,
                self.var_cal,
                self.var_horarios,
            ),
            bg="brown",
            fg="black",
            width=10,
            font=("", 12),
        )
        self.limpiar_b.grid(row=4, column=7, sticky="")

        self.email_b = Button(
            self.root,
            text="Enviar correo",
            command=lambda: self.objeto_base.email(
                self.tree.selection(),
                self.tree,
            ),
            bg="dark grey",
            fg="black",
            width=10,
            font=("", 12),
        )
        self.email_b.grid(row=5, column=7, sticky="")

        self.color_b = Button(
            self.root,
            text="Color Fondo",
            command=lambda: self.objeto_base.cambiar_color(self.root),
            bg="white",
            fg="black",
            width=10,
            font=("", 12),
        )
        self.color_b.grid(row=6, column=7, sticky="")

        self.completar_b = Button(
            self.root,
            text="Cargar valores",
            command=lambda: self.objeto_base.completar(
                self.tree.selection(),
                self.nombre_e,
                self.apellido_e,
                self.dni_e,
                self.tel_e,
                self.correo_e,
                self.var_especialidades,
                self.var_cal,
                self.var_horarios,
                self.tree,
            ),
            bg="violet",
            fg="black",
            width=20,
            font=("", 12),
        )
        self.completar_b.grid(row=6, columnspan=2, column=0, sticky="")

        self.manual = Button(
            self.root,
            text="",
            command=lambda: self.objeto_base.abrir_manual(),
            bg="white",
            fg="black",
            width=20,
            font=("", 12),
            image=self.icono_mostrar,
        )
        self.manual.grid(row=0, column=9, sticky="")

    def mostrar(
        self,
    ):
        """
        Metodo de mostrar que llama al objeto actualizar_treeview
        """
        self.objeto_base.actualizar_treeview(self.tree)
