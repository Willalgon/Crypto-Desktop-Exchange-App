class UsuarioVO:
    def __init__(self, id_usuario=None, dni=None, nombre=None,
                 apellidos=None, email=None, rol=None, activo=None):
        self.__id_usuario = id_usuario
        self.__dni = dni
        self.__nombre = nombre
        self.__apellidos = apellidos
        self.__email = email
        self.__rol = rol
        if activo is not None:
            self.__activo = bool(activo)
        else:
            self.__activo = None

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
    def apellidos(self):
        return self.__apellidos

    @apellidos.setter
    def apellidos(self, v):
        self.__apellidos = v

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
    def activo(self):
        return self.__activo

    @activo.setter
    def activo(self, v):
        self.__activo = bool(v) if v is not None else None

    def __repr__(self):
        return (f"UsuarioVO(id={self.__id_usuario}, email={self.__email}, "
                f"rol={self.__rol}, activo={self.__activo})")