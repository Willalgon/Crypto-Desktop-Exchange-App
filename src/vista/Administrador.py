
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QHeaderView, QTableWidgetItem
from PyQt5 import uic

Form, Window = uic.loadUiType("src/vista/ui/Administrador.ui")


class Administrador(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None
        self.tabla_usuarios.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_usuarios.setColumnHidden(0, True)

        # Conectar el botón
        self.btn_eliminar_usuario.clicked.connect(self._on_eliminar_usuario)
        self.tabla_activos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_activos.setColumnHidden(0, True)  # Ocultamos el ID
        self.btn_retirar_activo.clicked.connect(self._on_retirar_activo)
        self.btn_lanzar_evento.clicked.connect(self._on_lanzar_evento)


    def setControlador(self, controlador):
        self._controlador = controlador

    def cargar_usuarios(self, usuarios):
        self.tabla_usuarios.setRowCount(0)
        for row_idx, usr in enumerate(usuarios):
            if usr[6] == True or usr[6] == 1:
                self.tabla_usuarios.insertRow(self.tabla_usuarios.rowCount())
                ultima_fila = self.tabla_usuarios.rowCount() - 1

                for col_idx in range(6):
                    item = QTableWidgetItem(str(usr[col_idx]))
                    self.tabla_usuarios.setItem(ultima_fila, col_idx, item)

    def _on_eliminar_usuario(self):
        fila = self.tabla_usuarios.currentRow()
        if fila >= 0:
            email = self.tabla_usuarios.item(fila, 4).text()
            nombre = self.tabla_usuarios.item(fila, 2).text()

            respuesta = QMessageBox.question(self, "Confirmar Baja",
                                             f"¿Estás seguro de que quieres desactivar la cuenta de {nombre} ({email})?",
                                             QMessageBox.Yes | QMessageBox.No)

            if respuesta == QMessageBox.Yes:
                self._controlador.admin_desactivar_usuario(email)
        else:
            QMessageBox.warning(self, "Aviso", "Por favor, selecciona un usuario de la tabla primero.")

    def cargar_activos(self, activos):
        self.tabla_activos.setRowCount(0)
        for row_idx, act in enumerate(activos):
            if act[4] == True or act[4] == 1:
                self.tabla_activos.insertRow(self.tabla_activos.rowCount())
                ultima_fila = self.tabla_activos.rowCount() - 1
                for col_idx in range(4):
                    item = QTableWidgetItem(str(act[col_idx]))
                    self.tabla_activos.setItem(ultima_fila, col_idx, item)

    def _on_retirar_activo(self):
        fila = self.tabla_activos.currentRow()
        if fila >= 0:
            id_activo = self.tabla_activos.item(fila, 0).text()
            nombre = self.tabla_activos.item(fila, 1).text()
            respuesta = QMessageBox.question(self, "Confirmar Retirada",
                                             f"¿Estás seguro de que quieres retirar {nombre} del mercado?",
                                             QMessageBox.Yes | QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                self._controlador.admin_retirar_activo(id_activo)
        else:
            QMessageBox.warning(self, "Aviso", "Selecciona un activo de la tabla.")

    def _on_lanzar_evento(self):
        nombre_evento = self.combo_eventos.currentText()
        descripcion = self.txt_descripcion_evento.toPlainText().strip()

        if not descripcion:
            QMessageBox.warning(self, "Aviso", "Debes redactar una descripción o noticia para el evento.")
            return

        respuesta = QMessageBox.warning(self, "¡Alerta de Volatilidad!",
                                        f"¿Estás seguro de lanzar un {nombre_evento}? \nEsto alterará inmediatamente los precios de todas las criptomonedas y del oro.",
                                        QMessageBox.Yes | QMessageBox.No)

        if respuesta == QMessageBox.Yes:
            self._controlador.admin_lanzar_evento(nombre_evento, descripcion)
            self.txt_descripcion_evento.clear()

    def _on_cerrar_sesion(self):
        if self._controlador:
            self._controlador.cerrarSesion()