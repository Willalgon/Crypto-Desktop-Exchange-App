from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt, QDateTime
from PyQt5 import uic

Form, Window = uic.loadUiType("src/vista/ui/Analista.ui")
class Analista(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None
        self._usuario = None
        self._configurar_tabla()
        self._conectar_senales()

    def _configurar_tabla(self):
        self.tabla_noticias.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tabla_noticias.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla_noticias.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tabla_noticias.verticalHeader().setVisible(False)
        self.tabla_noticias.setWordWrap(False)

    def _conectar_senales(self):
        self.btn_publicar.clicked.connect(self._on_publicar)
        self.btn_limpiar.clicked.connect(self._limpiar_formulario)
        self.btn_nav_noticias.clicked.connect(self._scroll_to_form)
        self.btn_nav_historial.clicked.connect(self._scroll_to_hist)
        self.btn_nav_salir.clicked.connect(self._on_cerrar_sesion)

    def _on_publicar(self):
        titulo = self.input_titulo.text().strip()
        cuerpo = self.input_cuerpo.toPlainText().strip()
        es_aviso = self.chk_aviso.isChecked()
        if not titulo:
            self._mostrar_error("Tiene que incluir un título")
            return
        if not cuerpo:
            self._mostrar_error("El contenido no puede estar vacío")
            return
        if self._controlador:
            self._controlador.publicarNoticia(titulo, cuerpo, es_aviso)

    def _limpiar_formulario(self):
        self.input_titulo.clear()
        self.input_cuerpo.clear()
        self.chk_aviso.setChecked(False)
        self.input_titulo.setFocus() # Para ubicarnos en el titulo de nuevo (comodidad)

    def _on_cerrar_sesion(self):
        if self.controlador:
            self._controlador.cerrarSesion()

    def _scroll_to_form(self):
        self.input_titulo.setFocus()

    def _scroll_to_hist(self):
        if self._controlador:
            self._controlador.cargarHistorial()  # ← pide los datos al controlador
        self.tabla_noticias.setFocus()

    def mostrarExitoPublicacion(self, titulo, es_aviso):
        if es_aviso:
            tipo = "AVISO"
        else:
            tipo = "NO_AVISO"
        fecha = QDateTime.currentDateTime().toString("dd/MM/yyyy  hh:mm")
        self._anadir_fila_tabla(fecha, titulo, tipo)
        self._limpiar_formulario()
        self._mostrar_info(f"Noticia publicada correctamente.\n\nTítulo: {titulo}")

    def _anadir_fila_tabla(self, fecha, titulo, tipo):
        fila = self.tabla_noticias.rowCount() # devuelve el numero de filas de la tabla
        self.tabla_noticias.insertRow(fila) # insertar fila en la última posición

        item_fecha = QTableWidgetItem(fecha)
        item_fecha.setForeground(Qt.white)
        item_fecha.setTextAlignment(Qt.AlignCenter)

        item_titulo = QTableWidgetItem(titulo)
        item_titulo.setForeground(Qt.white)

        item_tipo = QTableWidgetItem(tipo)
        item_tipo.setTextAlignment(Qt.AlignCenter)

        if tipo == "AVISO":
            from PyQt5.QtGui import QColor
            item_tipo.setForeground(QColor("#FF6A00"))
        else:
            from PyQt5.QtGui import QColor
            item_tipo.setForeground(QColor(180, 180, 180))

        self.tabla_noticias.setItem(fila, 0, item_fecha)
        self.tabla_noticias.setItem(fila, 1, item_titulo)
        self.tabla_noticias.setItem(fila, 2, item_tipo)
        self.tabla_noticias.scrollToBottom()

    def cargarHistorial(self, noticias):
        self.tabla_noticias.setRowCount(0)
        for fecha, titulo, es_aviso in noticias:
            if es_aviso:
                tipo = "AVISO"
            else:
                tipo = "NO_AVISO"
            self._anadir_fila_tabla(fecha, titulo, tipo)

    def setNombreUsuario(self, email):
        self.lbl_header_usuario.setText(email)

    def mostrar_error(self, aviso):
        self._mostrar_error(aviso)

    def _mostrar_error(self, aviso):
        QMessageBox.warning(self, "Error", aviso)

    def _mostrar_info(self, msg):
        QMessageBox.information(self, "Publicado", msg)

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref):
        self._controlador = ref

