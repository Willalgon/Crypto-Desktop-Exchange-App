class LoginVO:
    def __init__(self,email,contrasena):
        self.__email=email
        self.__contrasena=contrasena
        
    @property
    def email(self):
        return self.__email

    @property
    def contrasena(self):
        return self.__contrasena

    