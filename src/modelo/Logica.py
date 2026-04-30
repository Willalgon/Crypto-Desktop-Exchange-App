from src.modelo.vo.UsuarioVo import UsuarioVo

class Logica:
    def hacerLogin(self, loginVO):
        # Si el usuario es admin, saltamos el DAO y entramos directo
        if loginVO.nombre == "admin":
            return UsuarioVo("12345678A", "Admin", "The Brain", "System", "admin@brain.com")
        return None

    def hacerRegistro(self, registroVO):
        # Simplemente decimos que sí a todo para que no explote
        print(f"DEBUG: Registro recibido correctamente en la lógica")
        return True

    def obtenerDatosSimulados(self):
        # Datos extraídos del Apéndice 4.1 de tu ERS
        return [
            {'id': 'BTC', 'estado': 'Bitcoin', 'fecha': '$65,000', 'perf': 'Store Value'},
            {'id': 'ETH', 'estado': 'Ethereum', 'fecha': '$3,500', 'perf': 'Smart contracts'},
            {'id': 'GOLD', 'estado': 'Oro Digital', 'fecha': '$2,000', 'perf': 'Refugio'},
            {'id': 'SOL', 'estado': 'Solana', 'fecha': '$150', 'perf': 'High Speed'}
        ]