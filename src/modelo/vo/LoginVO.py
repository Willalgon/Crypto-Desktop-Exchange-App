class LoginVO:
    def __init__(self, email, contrasena):
        self.__email = email
        self.__contrasena = contrasena

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, v):
        self.__email = v

    @property
    def contrasena(self):
        return self.__contrasena

    @contrasena.setter
    def contrasena(self, v):
        self.__contrasena = v