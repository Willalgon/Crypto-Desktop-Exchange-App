from PyQt5.QtWidgets import (
    QMainWindow, QMessageBox, QHeaderView,
    QTableWidgetItem, QDialog, QFormLayout,
    QLineEdit, QComboBox, QDialogButtonBox, QPushButton
)
from PyQt5 import uic
from PyQt5.QtCore import Qt
Form, Window = uic.loadUiType("src/vista/ui/Administrador.ui")


class Administrador(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None
        self._inyectar_boton_backup()
        self._conectar_senales()
        self._construir_tabla()

    def _inyectar_boton_backup(self):
        self.btn_backup = QPushButton("💾  Copia de seguridad")
        self.btn_backup.setCursor(Qt.PointingHandCursor)
        self.btn_backup.setStyleSheet("""
            QPushButton#btn_backup {
                background: transparent;
                color: rgba(255, 255, 255, 0.45);
                font-size: 12px;
                font-weight: 500;
                letter-spacing: 0.2px;
                border: none;
                border-radius: 10px;
                padding: 10px 14px 10px 14px;
                text-align: left;
            }
            QPushButton#btn_backup:hover {
                background: rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.80);
            }
            QPushButton#btn_backup:pressed {
                background: rgba(255, 107, 0, 0.10);
                color: #FF8C2A;
            }
        """)
        self.btn_backup.setObjectName("btn_backup")
        sidebar_layout = self.sidebar.layout()
        count = sidebar_layout.count()
        sidebar_layout.insertWidget(count - 3, self.btn_backup)

    def _conectar_senales(self):
        self.btn_nav_usuarios.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btn_nav_activos.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.btn_nav_eventos.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btn_nav_salir.clicked.connect(self._on_cerrar_sesion)
        self.btn_eliminar_usuario.clicked.connect(self._on_eliminar_usuario)
        self.btn_editar_usuario.clicked.connect(self._on_editar_usuario)
        self.btn_retirar_activo.clicked.connect(self._on_retirar_activo)
        self.btn_lanzar_evento.clicked.connect(self._on_lanzar_evento)
        self.input_buscar_usuario.hide()
        self.input_buscar_activo.hide()

        self.btn_backup.clicked.connect(self._hacer_backup)


    def _construir_tabla(self):
        self.tabla_usuarios.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_usuarios.setColumnHidden(0, True)  # oculta id_usuario
        self.tabla_activos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_activos.setColumnHidden(0, True)  # oculta id_activo


    def cargar_usuarios(self, usuarios):
        self.tabla_usuarios.setRowCount(0)
        for vo in usuarios:
            if not vo.activo:
                continue
            fila = self.tabla_usuarios.rowCount()
            self.tabla_usuarios.insertRow(fila)
            self.tabla_usuarios.setItem(fila, 0, QTableWidgetItem(str(vo.id_usuario)))
            self.tabla_usuarios.setItem(fila, 1, QTableWidgetItem(vo.dni       or ""))
            self.tabla_usuarios.setItem(fila, 2, QTableWidgetItem(vo.nombre    or ""))
            self.tabla_usuarios.setItem(fila, 3, QTableWidgetItem(vo.apellidos or ""))
            self.tabla_usuarios.setItem(fila, 4, QTableWidgetItem(vo.email     or ""))
            self.tabla_usuarios.setItem(fila, 5, QTableWidgetItem(vo.rol       or ""))

    def cargar_activos(self, activos):
        """Recibe lista de ActivoVO y rellena la tabla."""
        self.tabla_activos.setRowCount(0)
        for vo in activos:
            fila = self.tabla_activos.rowCount()
            self.tabla_activos.insertRow(fila)
            self.tabla_activos.setItem(fila, 0, QTableWidgetItem(str(vo.id_activo)))
            self.tabla_activos.setItem(fila, 1, QTableWidgetItem(vo.nombre  or ""))
            self.tabla_activos.setItem(fila, 2, QTableWidgetItem(vo.simbolo or ""))
            self.tabla_activos.setItem(fila, 3, QTableWidgetItem(str(vo.precio_actual)))


    def _on_eliminar_usuario(self):
        fila = self.tabla_usuarios.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Aviso", "Selecciona un usuario de la tabla primero.")
            return
        email  = self.tabla_usuarios.item(fila, 4).text()
        nombre = self.tabla_usuarios.item(fila, 2).text()
        resp = QMessageBox.question(
            self, "Confirmar Baja",
            f"¿Desactivar la cuenta de {nombre} ({email})?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if resp == QMessageBox.Yes:
            self._controlador.admin_desactivar_usuario(email)

    def _on_editar_usuario(self):
        fila = self.tabla_usuarios.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Aviso", "Selecciona un usuario de la tabla primero.")
            return
        from src.modelo.vo.UsuarioVO import UsuarioVO
        vo = UsuarioVO(
            id_usuario=int(self.tabla_usuarios.item(fila, 0).text()),
            dni=self.tabla_usuarios.item(fila, 1).text(),
            nombre=self.tabla_usuarios.item(fila, 2).text(),
            apellidos=self.tabla_usuarios.item(fila, 3).text(),
            email=self.tabla_usuarios.item(fila, 4).text(),
            rol=self.tabla_usuarios.item(fila, 5).text(),
        )
        dialogo = _DialogoEditarUsuario(vo, self)
        if dialogo.exec_() == QDialog.Accepted:
            self._controlador.admin_editar_usuario(dialogo.get_vo())


    def _on_retirar_activo(self):
        fila = self.tabla_activos.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Aviso", "Selecciona un activo de la tabla.")
            return
        id_activo = self.tabla_activos.item(fila, 0).text()
        nombre    = self.tabla_activos.item(fila, 1).text()
        resp = QMessageBox.question(
            self, "Confirmar Retirada",
            f"¿Retirar '{nombre}' del mercado?\n"
            "Esta acción eliminará el activo de la base de datos.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if resp == QMessageBox.Yes:
            self._controlador.admin_retirar_activo(id_activo)


    def _on_lanzar_evento(self):
        nombre_evento = self.combo_evento.currentText()
        descripcion = self.input_desc_evento.toPlainText().strip()
        if not descripcion:
            QMessageBox.warning(self, "Aviso", "Debes redactar una descripción para el evento.")
            return
        resp = QMessageBox.warning(
            self, "¡Alerta de Volatilidad!",
            f"¿Estás seguro de lanzar '{nombre_evento}'?\n"
            "Esto alterará inmediatamente los precios de todos los activos.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if resp == QMessageBox.Yes:
            self._controlador.admin_lanzar_evento(nombre_evento, descripcion)
            self.input_desc_evento.clear()

    def _hacer_backup(self):
        if self._controlador:
            self._controlador.hacer_backup()

    def mostrar_backup_ok(self, ruta: str):
        QMessageBox.information(
            self,
            "Copia de seguridad",
            f"Backup generado correctamente:\n{ruta}"
        )

    def _on_cerrar_sesion(self):
        if self._controlador:
            self._controlador.cerrarSesion()

    def mostrar_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)

    def mostrar_aviso_ultimo_admin(self):
        QMessageBox.warning(
            self, "Operación no permitida",
            "No puedes desactivar al único administrador del sistema.\n"
            "Crea otro administrador antes de realizar esta acción.",
        )

    def mostrar_aviso_operaciones_pendientes(self):
        QMessageBox.warning(
            self, "Operaciones pendientes",
            "Existen traders con posiciones abiertas en este activo.\n"
            "Cierra o liquida esas posiciones antes de retirarlo.",
        )

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref):
        self._controlador = ref

class _DialogoEditarUsuario(QDialog):
    ROLES = ["TRADER", "ANALISTA", "ADMIN"]

    def __init__(self, usuario_vo, parent=None):
        super().__init__(parent)
        self._vo = usuario_vo
        self.setWindowTitle(f"Editar usuario — {usuario_vo.email}")
        self._build_ui()

    def _build_ui(self):
        layout = QFormLayout(self)
        self.inp_nombre    = QLineEdit(self._vo.nombre    or "")
        self.inp_apellidos = QLineEdit(self._vo.apellidos or "")
        self.combo_rol     = QComboBox()
        self.combo_rol.addItems(self.ROLES)
        idx = self.combo_rol.findText(self._vo.rol or "TRADER")
        if idx >= 0:
            self.combo_rol.setCurrentIndex(idx)
        layout.addRow("Nombre:",    self.inp_nombre)
        layout.addRow("Apellidos:", self.inp_apellidos)
        layout.addRow("Rol:",       self.combo_rol)
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        layout.addRow(botones)

    def get_vo(self):
        from src.modelo.vo.UsuarioVO import UsuarioVO
        return UsuarioVO(
            id_usuario=self._vo.id_usuario,
            dni=self._vo.dni,
            nombre=self.inp_nombre.text().strip(),
            apellidos=self.inp_apellidos.text().strip(),
            email=self._vo.email,
            rol=self.combo_rol.currentText(),
            activo=self._vo.activo,
        )