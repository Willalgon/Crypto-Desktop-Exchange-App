class UsuarioVo:
    def __init__(self, dni, nombre, primer_apellido, segundo_apellido, email):
        self.__dni = dni
        self.__nombre = nombre
        self.__primerapellido = primer_apellido
        self.__segundoapellido = segundo_apellido
        self._email = email

        @property
        def dni(self):
            return self.__dni
        