"""
Archivo modelo.py del modelo MVC
"""
import re
from tkinter import messagebox
import win32com.client as client
from tkinter.colorchooser import askcolor
from peewee import CharField
from peewee import SqliteDatabase
from peewee import Model
import webbrowser
import os
from mis_decoradores import registro_funcion
from mis_decoradores import registro_alta
from mis_decoradores import registro_baja
from mis_decoradores import registro_modificar
from observador import Sujeto

OPTIONS = [
    "ALERGIA",
    "ALERGIA E INMUNOLOGIA",
    "CARDIOLOGIA",
    "CARDIOLOGIA INFANTIL",
    "CIRUGIA PLASTICA Y EPARADORA",
    "CIRUGIA TORACICA",
    "CIRUGIA GENERAL",
    "CIRUGIA CARDIOVASCULAR",
    "CIRUGIA NFANTIL",
    "CLINICA MEDICA: Medicina Interna",
    "DERMATOLOGIA",
    "DIAGNOSTICO POR IMAGENES",
    "ENDOCRINOLOGIA",
    "INFECTOLOGIA PEDIÁTRICA",
    "GASTROENTEROLOGIA",
    "GENETICA MEDICA",
    "GERIATRIA Y GERONTOLOGIA",
    "GINECOLOGIA",
    "MEDICINA LEGAL",
    "MEDICINA DEL TRABAJO",
    "MEDICINA GENERAL / FAMILIAR",
    "NEONATOLOGIA",
    "NEUMONOLOGIA",
    "NEUROCIRUGIA",
    "NEUROLOGIA",
    "NEUROLOGIA INFANTIL",
    "NUTRICION",
    "OBSTETRICIA",
    "OFTALMOLOGIA",
    "ONCOLOGIA (Clínica)",
    "OTORRINOLARINGOLOGIA",
    "PEDIATRIA (Clínica Pediátrica)",
    "PSIQUIATRIA",
    "PSIQUIATRIA INFANTO JUVENIL",
    "RADIOTERAPIA (Terapia Radiante)",
    "SALUD PUBLICA",
    "TERAPIA INTENSIVA",
    "TISIONEUMONOLOGIA",
    "TOCOGINECOLOGIA",
]

db = SqliteDatabase("midbpacientesORM.db")


class BaseModel(Model):
    class Meta:
        database = db


class Lista(BaseModel):
    nombre = CharField()
    apellido = CharField()
    dni = CharField()
    telefono = CharField()
    correo = CharField()
    especialidad = CharField()
    fecha = CharField()
    horario = CharField()


try:
    db.connect()
    db.create_tables([Lista])
except:
    print("Hubo un error")
finally:
    print("Terminó el Try-Except")


class Abmc(Sujeto):

    # Defino una funcion para actualizar el treeview
    def actualizar_treeview(self, mitreview):
        """
        Metodo para la actualizacion del treeview

        :param mitreview: objeto tipo treeview

        """
        records = (
            mitreview.get_children()
        )  # El método get_children devuelve una lista de IDs de los items,
        # uno para cada "hijo".
        for element in records:  # Esto vacio el treeview
            mitreview.delete(element)

        for fila in Lista.select():
            mitreview.insert(
                "",
                0,
                text=fila.id,
                values=(
                    fila.nombre,
                    fila.apellido,
                    fila.dni,
                    fila.telefono,
                    fila.correo,
                    fila.especialidad,
                    fila.fecha,
                    fila.horario,
                ),
            )
        print("Actualizar OK")

    # Defino una funcion guardar para hacer el alta en sqlite3

    @registro_funcion
    @registro_alta
    def alta_sqlite3(
        self,
        nombre,
        apellido,
        dni,
        telefono,
        correo,
        especialidad,
        fecha,
        horario,
        tree,
    ):
        """

        Metodo de Alta de dB SQLite3

        :param nombre: argumento del nombre de la persona que toma el turno

        :param apeliido: argumento del apellido de la persona que toma el turno

        :param dni: argumento del dni de la persona que toma el turno

        :param telefono: argumento del telefono de la persona que toma el turno

        :param correo: argumento del correo electronico de la persona que toma el turno

        :param especialidad: argumento del especialidad seleccionada del turno

        :param fecha: argumento de la fecha seleccionada del turno

        :param horario: argumento del horario seleccionada del turno

        :param tree: argumento del base de datos empleada

        """
        if self.check_mail(correo) is True and self.blank_dni(dni) is True:
            lista = Lista()
            lista.nombre = nombre
            lista.apellido = apellido
            lista.dni = dni
            lista.telefono = telefono
            lista.correo = correo
            lista.especialidad = especialidad
            lista.fecha = fecha
            lista.horario = horario
            lista.tree = tree
            lista.save()
            self.actualizar_treeview(tree)
            messagebox.showinfo(
                "Alta",
                f"Se dio de alta al paciente {nombre} {apellido} con turno para {especialidad} el dia {fecha} con horario {horario}",
            )
            print("Alta OK")
            # Llamo a Notificar de observador.py
            self.notificar(nombre, apellido)

    # Defino una funcion modificar en sqlite3 la fila seleccionada del treeview
    @registro_funcion
    @registro_modificar
    def modificar_sqlite3(
        self,
        arg_nombre,
        arg_apellido,
        arg_dni,
        arg_telefono,
        arg_correo,
        arg_especialidad,
        arg_fecha,
        arg_horario,
        tree,
        arg_seleccion,
    ):
        """

        Metodo de Modificar de dB SQLite3

        :param arg_nombre: nombre de la persona que toma el turno

        :param arg_apeliido: apellido de la persona que toma el turno

        :param arg_dni: dni de la persona que toma el turno

        :param arg_telefono: telefono de la persona que toma el turno

        :param arg_correo: correo electronico de la persona que toma el turno

        :param arg_especialidad: especialidad seleccionada del turno

        :param arg_fecha: fecha seleccionada del turno

        :param arg_horario: horario seleccionada del turno

        :param tree: base de datos empleada

        :param arg_seleccion: seleccion dentro del tree de la fila a modificar

        """
        if self.check_mail(arg_correo) is True:
            tree_id = tree.item(arg_seleccion)["text"]
            modificar = Lista.update(
                nombre=arg_nombre,
                apellido=arg_apellido,
                dni=arg_dni,
                telefono=arg_telefono,
                correo=arg_correo,
                especialidad=arg_especialidad,
                fecha=arg_fecha,
                horario=arg_horario,
            ).where(Lista.id == tree_id)
            modificar.execute()
            self.actualizar_treeview(tree)
            messagebox.showinfo(
                "Alta",
                f"Se modifico los datos del paciente {arg_nombre} {arg_apellido} con turno para {arg_nombre} el dia {arg_nombre} con horario {arg_nombre}",
            )
            print("Modificacion OK")

    # Defino funcion p/eliminar en sqlite3 la fila seleccionada del treeview
    @registro_funcion
    @registro_baja
    def baja_sqlite3(self, seleccion, tree):
        """

        Metodo de Baja de dB SQLite3

        :param seleccion: argumento de la seleccion de la fila a borrar

        :param tree: argumento de la base de datos empleada

        """
        eliminadas = []
        for x in seleccion:
            eliminadas.append(x)
            tree_id = (tree.item(x)["text"],)
            borrar = Lista.get(Lista.id == tree_id)
            borrar.delete_instance()
        self.actualizar_treeview(tree)
        messagebox.showinfo(
            "Eliminar",
            f"Se elminaron {len(eliminadas)} línea(s) de la base de datos",
            icon="warning",
        )
        print("Eliminacion OK")

    # Defino una funcion consultar por DNI
    def consultar_dni(self, arg_dni):
        """

        Metodo de consulta en base a la seleccion del DNI

        :param arg_dni: argumento que selecciona el DNI a consultar

        """
        check_dni = Lista.select(Lista).where(Lista.dni == arg_dni)
        # print(check_dni)
        # print(len(check_dni))
        if arg_dni == "":
            messagebox.showinfo("Error", "No hay DNI ingresado", icon="warning")
        elif len(check_dni) == 0:
            messagebox.showinfo("Error", "El DNI ingresado no existe", icon="warning")
        else:
            consulta = Lista.select(
                Lista.especialidad,
                Lista.fecha,
                Lista.horario,
            ).where(Lista.dni == arg_dni)
            keys = ["Especialidad: ", "Fecha: ", "Horario: "]
            turnos = {}
            # print(consulta)
            # print(len(consulta))
            # for c in consulta:
            #     print(c.especialidad)
            #     print(c.fecha)
            #     print(c.horario)
            for i in range(len(consulta)):
                for c in consulta:
                    turnos[i + 1] = [
                        keys[0] + c.especialidad,
                        keys[1] + c.fecha,
                        keys[2] + c.horario,
                    ]
            print(turnos)
            [print(key, ":", value) for key, value in turnos.items()]
            messagebox.showinfo(
                "Consulta de Turno",
                f"El paciente tiene los siguientes turnos:\n{turnos}",
            )

    # Funcion borrar textos
    def limpiar(
        self,
        nombre_e,
        apellido_e,
        dni_e,
        tel_e,
        correo_e,
        var_especialidades,
        var_cal,
        var_horarios,
    ):
        """

        Metodo para "limpiar" los campos

        :param nombre_e: argumento para limpiar el campo nombre

        :param apeliido_e: argumento para limpiar el campo apellido

        :param dni_e: argumento para limpiar el dni

        :param tel_e: argumento para limpiar el telefono

        :param correo_e: argumento para limpiar el correo electronico

        :param var_especialidades: argumento para limpiar el especialidad

        :param var_cal: argumento para limpiar la fecha

        :param var_horarios: argumento para limpiar el horario

        """
        for entry in nombre_e, apellido_e, dni_e, tel_e, correo_e:
            entry.delete(0, "end")
        var_especialidades.set("ALERGIA")
        var_cal.selection_set("1/1/2022")
        var_horarios.set("00:00")
        print("Limpiar OK")

    # Defino la funcion para mandar mail por oulook (no se otra forma)
    def email(self, seleccion, tree):
        """
        Metodo para el envio del turno via correo electronico

        :param seleccion: argumento de la seleccion del turno a enviar

        :param tree: argumento de la base de datos

        """

        tree_id = (tree.item(seleccion)["text"],)
        consulta = Lista.select(
            Lista.id,
            Lista.nombre,
            Lista.apellido,
            Lista.correo,
            Lista.especialidad,
            Lista.fecha,
            Lista.horario,
        ).where(Lista.id == tree_id)

        datos_px = []
        for c in consulta:
            datos_px.append(c.nombre)
            datos_px.append(c.apellido)
            datos_px.append(c.correo)
            datos_px.append(c.especialidad)
            datos_px.append(c.fecha)
            datos_px.append(c.horario)

        outlook = client.Dispatch("Outlook.Application")
        message = outlook.CreateItem(0)
        message.Subject = f"Turno para {datos_px[0]} {datos_px[1]}"
        message.To = datos_px[2]
        message.Body = f"""Estimado {datos_px[0]} {datos_px[1]},
        Su turno para la especialidad {datos_px[3]} corresponde al día {datos_px[4]} a la hora {datos_px[5]}.
        Atte
        Coordinación"""
        message.Display()
        print("Mail OK")

    # Funcion de cambiar de color
    def cambiar_color(self, root):
        """
        Metodo para cambiar el color del fondo de la aplicacion

        :param root: argumento del color seleccionado

        """
        color_fondo = askcolor(
            color="#00ff00", title="Seleccione su color de fondo para la aplicación"
        )
        root.configure(bg=color_fondo[1])
        print("Cambiar Color OK")

    # Defino una funcion p/borrar el entry del mail cuando ingresamos al entry
    def entry_delete(self, e):
        """
        Metodo para borrar el entry del mail cuando ingresamos al entry

        :param e: argumento para borrar el entry
        """
        e.widget.delete(0, "end")

    # Funcion de completar los entries y dropdowns c/la selección del treeview
    def completar(
        self,
        seleccion,
        nombre_e,
        apellido_e,
        dni_e,
        tel_e,
        correo_e,
        var_especialidades,
        var_cal,
        var_horarios,
        tree,
    ):
        """
        Metodo para completar los entries y dropdowns con la selección del trewview

        :param seleccion: argumento de la seleccion de la fila

        :param nombre_e: argumento para completar el campo nombre

        :param apeliido_e: argumento para completar el campo apellido

        :param dni_e: argumento para completar el campo dni

        :param tel_e: argumento para completar el campo telefono

        :param correo_e: argumento para completar el campo correo electronico

        :param var_especialidades: argumento para completar el campo especialidad

        :param var_cal: argumento para completar el campo fecha

        :param var_horarios: argumento para completar el campo horario

        :param tree: argumento de la base de datos


        """
        try:
            # print(tree.item(seleccion))
            entries = [nombre_e, apellido_e, dni_e, tel_e, correo_e]
            for x in range(len(entries)):
                entries[x].delete(0, "end")
                entries[x].insert(0, tree.item(seleccion)["values"][x])
            var_especialidades.set(tree.item(seleccion)["values"][5])
            var_cal.selection_set(tree.item(seleccion)["values"][6])
            var_horarios.set(tree.item(seleccion)["values"][7])
            print("Completar OK")
        except IndexError:
            messagebox.showinfo(
                "Error",
                "No seleccionó ninguna línea",
            )

    # Regex para el mail
    def check_mail(self, email):
        """
        Metodo Regex para verificacion del campo de correo electronico

        :param email: argumento para chequeo del campo correo electronico
        """
        regex_mail = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(regex_mail, email):
            return True
        else:
            messagebox.showinfo(
                "ERROR",
                "Email no valido",
                icon="warning",
            )
        print("Check Mail OK")

    def blank_dni(self, dni):
        """
        Metodo de verificacion del campo DNI

        :param dni: argumento del dni enviado para verificar que no este vacio

        """
        if dni != "":
            return True
        else:
            messagebox.showinfo(
                "ERROR",
                "DNI no puede estar vacío",
                icon="warning",
            )

    # Defino una funcion para hora y minuto
    def hora_min(
        self,
    ):
        """
        Metodo para establecer la hora y minutos de la base de datos

        """
        min = ["00", 15, 30, 45]
        hhmm = []
        for h in range(0, 25):
            for m in min:
                if h < 10:
                    hhmm.append("0" + str(h) + ":" + str(m))
                else:
                    hhmm.append(str(h) + ":" + str(m))
        return hhmm

    def abrir_manual(
        self,
    ):
        """
        Metodo para abrir manual de Sphinx

        """
        webbrowser.open(
            os.path.dirname(os.path.abspath(__file__)) + "\docs\_build\html\index.html"
        )
