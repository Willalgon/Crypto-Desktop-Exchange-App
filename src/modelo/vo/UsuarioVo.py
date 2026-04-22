class UsuarioVo:
    def __init__(self,dni,nombre,primer_apellido,segundo_apellido,email):
        self.__dni=dni
        self.__nombre=nombre
        self.__primerapellido=primer_apellido
        self.__segundoapellido=segundo_apellido
        self.__email=email

    @property
    def dni(self):
        return self.__dni

    @property
    def nombre(self):
        return self.__nombre

    @property
    def email(self):
        return self.__email

    @property
    def primerapellido(self):
        return self.__primerapellido

    @property
    def segundoapellido(self):
        return self.__segundoapellido