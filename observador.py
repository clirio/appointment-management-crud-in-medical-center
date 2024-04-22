class Sujeto:

    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def quitar(self, obj):
        self.observadores.remove(obj)

    def notificar(self, *args):
        for observador in self.observadores:
            observador.update(args)
        print(
            f"imprimo lista de observadores {self.observadores}"
        )  # no funciona no se como hacerlo


class Observador:
    def update(self):
        raise NotImplementedError("Delegación de actualización")


class ConcreteObserverA(
    Sujeto
):  # Acá heradaba de Observador y lo cambié a Sujeto, no se si está bien.
    def __init__(self, obj):
        self.observado_a = obj
        self.observado_a.agregar(self)

    def update(self, *args):
        print("Actualización dentro de ObservadorConcretoA")
        print("Aquí están los parámetros:")
        P = ("Nombre", "Apellido")  # prompts
        print(*("".join(f"{p}: {v}\n" for p, v in zip(P, t)) for t in args), sep="\n")
