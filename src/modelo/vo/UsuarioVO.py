class UsuarioVO:
    def __init__(self, id_usuario=None, dni=None, nombre=None,
                 apellidos=None, email=None, rol=None, activo=None):
        self.__id_usuario = id_usuario
        self.__dni        = dni
        self.__nombre     = nombre
        self.__apellidos  = apellidos
        self.__email      = email
        self.__rol        = rol
        if activo is not None:
            self.__activo = bool(activo)
        else:
            self.__activo = None

    @property
    def id_usuario(self): return self.__id_usuario
    @property
    def dni(self):        return self.__dni
    @property
    def nombre(self):     return self.__nombre
    @property
    def apellidos(self):  return self.__apellidos
    @property
    def email(self):      return self.__email
    @property
    def rol(self):        return self.__rol
    @property
    def activo(self):     return self.__activo

    @nombre.setter
    def nombre(self, v):    self.__nombre = v
    @apellidos.setter
    def apellidos(self, v): self.__apellidos = v
    @rol.setter
    def rol(self, v):       self.__rol = v
    @activo.setter
    def activo(self, v):    self.__activo = bool(v)

    def __repr__(self):
        return (f"UsuarioVO(id={self.__id_usuario}, email={self.__email}, "
                f"rol={self.__rol}, activo={self.__activo})")