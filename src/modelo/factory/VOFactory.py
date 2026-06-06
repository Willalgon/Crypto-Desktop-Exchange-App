from src.modelo.vo.ActivoVO import ActivoVO
from src.modelo.vo.UsuarioVO import UsuarioVO

class VOFactory:
    @staticmethod
    def crear_vo(tipo, **kwargs):
        if tipo == "usuario":
            return UsuarioVO(**kwargs)
        elif tipo == "activo":
            return ActivoVO(**kwargs)
        return None