class RegistroVO:
    def __init__(self, dni, nombre, primer_apellido, segundo_apellido, email, contrasena, rol='TRADER', id_usuario=None):
        self.__id_usuario = id_usuario
        self.__dni = dni
        self.__nombre = nombre
        self.__primer_apellido = primer_apellido
        self.__segundo_apellido = segundo_apellido
        self.__email = email
        self.__contrasena = contrasena
        self.__rol = rol

    @property
    def id_usuario(self):
        return self.__id_usuario

    @id_usuario.setter
    def id_usuario(self, v):
        self.__id_usuario = v

    @property
    def dni(self):
        return self.__dni

    @dni.setter
    def dni(self, v):
        self.__dni = v

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, v):
        self.__nombre = v

    @property
    def primer_apellido(self):
        return self.__primer_apellido

    @primer_apellido.setter
    def primer_apellido(self, v):
        self.__primer_apellido = v

    @property
    def segundo_apellido(self):
        return self.__segundo_apellido

    @segundo_apellido.setter
    def segundo_apellido(self, v):
        self.__segundo_apellido = v

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, v):
        self.__email = v

    @property
    def rol(self):
        return self.__rol

    @rol.setter
    def rol(self, v):
        self.__rol = v

    @property
    def contrasena(self):
        return self.__contrasena

    @contrasena.setter
    def contrasena(self, v):
        self.__contrasena = v