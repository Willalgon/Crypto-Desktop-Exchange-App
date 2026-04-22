class RegistroVo:
    def __init__(self,nombre,primerapellido,segundoapellido, mail, dni, contrasena):
        self.__nombre=nombre
        self.__primerapellido=primerapellido
        self.__segundoapellido=segundoapellido
        self.__mail=mail
        self.__dni=dni
        self.__contrasena=contrasena

    @property
    def nombre(self):
        return self.__nombre

    @property
    def primerapellido(self):
        return self.__primerapellido

    @property
    def segundoapellido(self):
        return self.__segundoapellido

    @property
    def mail(self):
        return self.__mail

    @property
    def dni(self):
        return self.__dni

    @property
    def contrasena(self):
        return self.__contrasena