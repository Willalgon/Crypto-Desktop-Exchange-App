# modelo/vo/RegistroVO.py
class RegistroVO:
    def __init__(self, dni, nombre, primer_apellido, segundo_apellido, email, contrasena):
        self.__dni = dni
        self.__nombre = nombre
        self.__primer_apellido = primer_apellido
        self.__segundo_apellido = segundo_apellido
        self.__email = email
        self.__rol = 'TRADER'
        self.__contrasena = contrasena

    @property
    def dni(self):
        return self.__dni

    @property
    def nombre(self):
        return self.__nombre

    @property
    def primer_apellido(self):
        return self.__primer_apellido

    @property
    def segundo_apellido(self):
        return self.__segundo_apellido

    @property
    def email(self):
        return self.__email

    @property
    def rol(self):
        return self.__rol

    @property
    def contrasena(self):
        return self.__contrasena