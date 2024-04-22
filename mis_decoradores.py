from datetime import datetime
import logging


# def logger(dato):
#     loggeo = open("log.txt", "a")
#     loggeo.write(str(dato))
#     loggeo.write(": ")
#     loggeo.write(format(datetime.now().strftime("%Y-%m-%d %H:%M")))
#     loggeo.write("\n")
#     loggeo.close()
#     print(f"\nSe ejecuto {logger.__name__} > {str(dato)}")


def logger(dato):
    logging.basicConfig(
        filename="log.txt", level=logging.INFO, format="%(asctime)s %(message)s"
    )
    logging.info(f"\nSe ejecuto {logger.__name__} - Clase {str(dato)}")


# Registro general por funcion ejecutada
def registro_funcion(f):
    def interno(*args, **kwargs):
        print("Registro de programa nuevo:", datetime.now())
        f(*args, **kwargs)
        print("Se ejecuto %s " % f.__name__)

    return interno


# Inicio App
def inicio_app(f):
    def interno(*args, **kwargs):
        logger(f.__name__)
        print("Inicio de APP", datetime.now())
        f(*args, **kwargs)
        print("Se ejecuto %s " % f.__name__)

    return interno


# Registro para alta
def registro_alta(f):
    def interno(*args, **kwargs):
        logger(f.__name__)
        print("ALTA de registro de programa nuevo:", datetime.now())
        f(*args, **kwargs)
        print("Se ejecuto %s " % f.__name__)

    return interno


# Registro para baja
def registro_baja(f):
    def interno(*args, **kwargs):
        logger(f.__name__)
        print("BAJA de registro de programa nuevo:", datetime.now())
        f(*args, **kwargs)
        print("Se ejecuto %s " % f.__name__)

    return interno


# Registro para modificaciona
def registro_modificar(f):
    def interno(*args, **kwargs):
        logger(f.__name__)
        print("MODIFICACION de registro de programa nuevo:", datetime.now())
        f(*args, **kwargs)
        print("Se ejecuto %s " % f.__name__)

    return interno
