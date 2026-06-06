from PyQt5.QtWidgets import QMainWindow, QMessageBox, QHeaderView, QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

Form, Window = uic.loadUiType("./src/vista/ui/Trader.ui")

class Trader(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None
        self.tabla_mercado.setColumnCount(5)
        self.tabla_mercado.setColumnHidden(0, True)
        self.tabla_mercado.setColumnHidden(4, True)
        self.tabla_mercado.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._conectar_senales()
        self.setWindowState(Qt.WindowMaximized)
        self.canvas_grafico = None
        # Timer para avisos urgentes (CU12)
        self._timer_avisos = QTimer()
        self._timer_avisos.timeout.connect(self._check_avisos_urgentes)
        self._timer_avisos.start(10000)

    def _conectar_senales(self):
        self.btn_consultar_criptomonedas.clicked.connect(self._consultar_criptomonedas)
        self.tabla_mercado.doubleClicked.connect(self._ver_detalles)
        self.btn_logout.clicked.connect(self._on_logout)
        self.btn_mercado.clicked.connect(self._on_ver_mercado)
        self.btn_cartera.clicked.connect(self._on_ver_cartera)
        self.btn_noticias.clicked.connect(self._on_ver_noticias)
        self.tabla_datos.itemDoubleClicked.connect(self._on_tabla_doble_click)

    def _consultar_criptomonedas(self):
        if self._controlador:
            return self._controlador.consultar_criptomonedas()

    def _ver_detalles(self):
        fila = self.tabla_mercado.currentRow()
        if fila < 0:
            return
        id_activo   = int(self.tabla_mercado.item(fila, 0).text())
        nombre      = self.tabla_mercado.item(fila, 1).text()
        simbolo     = self.tabla_mercado.item(fila, 2).text()
        descripcion = self.tabla_mercado.item(fila, 4).text()
        if self._controlador:
            self._controlador.ver_detalles_activo(id_activo, nombre, simbolo, descripcion)

    def mostrar_error(self, mensaje: str = "Error al cargar el mercado. Inténtelo de nuevo."):
        QMessageBox.warning(self, "Error", mensaje)

    def actualizar_nombre(self, nombre_completo: str):
        # Actualiza el label del topbar con el nombre del trader
        self.lbl_nombre_trader.setText(nombre_completo)

    def actualizar_saldo(self, saldo_fiat: float, patrimonio_total: float):
        # Actualiza los labels de saldo y patrimonio
        self.lbl_saldo_fiat.setText(f"${saldo_fiat:,.2f}")
        self.lbl_patrimonio.setText(f"${patrimonio_total:,.2f}")

    def cargar_mercado(self, activos: list):
        self.tabla_mercado.setRowCount(len(activos))
        for i, a in enumerate(activos):
            self.tabla_mercado.setItem(i, 0, QTableWidgetItem(str(a.id_activo)))
            self.tabla_mercado.setItem(i, 1, QTableWidgetItem(a.nombre))
            self.tabla_mercado.setItem(i, 2, QTableWidgetItem(a.simbolo))
            self.tabla_mercado.setItem(i, 3, QTableWidgetItem(f"${a.precio_actual:,.2f}"))
            self.tabla_mercado.setItem(i, 4, QTableWidgetItem(a.descripcion_especial or ""))

    def cargar_historial(self, operaciones: list):
        self.tabla_historial.setRowCount(len(operaciones))
        for i, op in enumerate(operaciones):
            self.tabla_historial.setItem(i, 0, QTableWidgetItem(str(op["fecha_hora"])))
            self.tabla_historial.setItem(i, 1, QTableWidgetItem(op["operacion"]))
            self.tabla_historial.setItem(i, 2, QTableWidgetItem(op["simbolo"]))
            self.tabla_historial.setItem(i, 3, QTableWidgetItem(f"{float(op['cantidad']):,.8f}"))
            self.tabla_historial.setItem(i, 4, QTableWidgetItem(f"${float(op['precio_ejecucion']):,.2f}"))
            self.tabla_historial.setItem(i, 5, QTableWidgetItem(f"${float(op['total_fiat']):,.2f}"))

    def mostrar_exito_operacion(self, mensaje: str):
        QMessageBox.information(self, "Operación exitosa", mensaje)

    # ── Navegación ────────────────────────────────────────────────────────────────

    def _on_logout(self):
        if self._controlador:
            self._controlador.cerrarSesion()

    def _on_ver_mercado(self):
        if self._controlador:
            self._controlador.solicitarMercado()

    def _on_ver_cartera(self):
        if self._controlador:
            self._controlador.solicitarEstadoCarteraTrader()

    def _on_ver_noticias(self):
        if self._controlador:
            self._limpiar_espacio_central()
            self._controlador.solicitarNoticias()

    # ── CU9: Cartera ──────────────────────────────────────────────────────────────

    def refrescar_cartera(self, carteraVO, lista_posiciones):
        if carteraVO is None:
            return
        self._limpiar_espacio_central()
        self.lbl_bienvenida.setText(
            f"MI CARTERA  ·  "
            f"Fiat: ${carteraVO.saldo_fiat:,.2f}  |  "
            f"Cripto: ${carteraVO.valor_activos:,.2f}  |  "
            f"Total: ${carteraVO.patrimonio_total:,.2f}"
        )
        self.tabla_datos.setColumnCount(5)
        self.tabla_datos.setHorizontalHeaderLabels(
            ["SÍMBOLO", "CANTIDAD", "PRECIO MEDIO", "PnL (€)", "ROI (%)"]
        )
        self.tabla_datos.setRowCount(len(lista_posiciones))
        for fila, pos in enumerate(lista_posiciones):
            color = Qt.green if pos.pnl >= 0 else Qt.red
            items = [
                QTableWidgetItem(pos.simbolo),
                QTableWidgetItem(f"{pos.cantidad:,.8f}"),
                QTableWidgetItem(f"${pos.precio_medio_compra:,.2f}"),
                QTableWidgetItem(f"${pos.pnl:,.2f}"),
                QTableWidgetItem(f"{pos.roi:.2f}%"),
            ]
            for col, item in enumerate(items):
                if col in (3, 4):
                    item.setForeground(color)
                self.tabla_datos.setItem(fila, col, item)

        etiquetas = ["Liquidez (Fiat)"]
        valores = [float(carteraVO.saldo_fiat)]
        for pos in lista_posiciones:
            etiquetas.append(pos.simbolo)
            valores.append(float(pos.precio_actual) * float(pos.cantidad))

        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)
        colores = ["#FF6A00", "#00E676", "#00B0FF", "#D500F9", "#FFEA00", "#FF1744"]
        wedges, texts, autotexts = ax.pie(
            valores, labels=etiquetas, autopct="%1.1f%%", startangle=90,
            colors=colores, pctdistance=0.75,
            wedgeprops={"width": 0.4, "edgecolor": "#0F0F16", "linewidth": 2},
        )
        for t in texts:
            t.set_color("white");
            t.set_fontsize(10);
            t.set_fontweight("bold")
        for at in autotexts:
            at.set_color("black");
            at.set_fontsize(9);
            at.set_fontweight("bold")
        titulo_plot = ax.set_title("DISTRIBUCIÓN DEL PORTFOLIO", pad=20)
        titulo_plot.set_color("#FF8C00")
        titulo_plot.set_fontsize(12)
        titulo_plot.set_fontweight("bold")
        ax.axis("equal")

        self.canvas_grafico = FigureCanvas(fig)
        self.canvas_grafico.setStyleSheet("background-color: transparent;")
        self.content.addWidget(self.canvas_grafico)

    # ── CU10: Noticias ────────────────────────────────────────────────────────────

    def refrescar_noticias(self, lista_noticias):
        self.lbl_bienvenida.setText("NOTICIAS E INFORMES  ·  MERCADO")
        self.tabla_datos.setColumnCount(2)
        self.tabla_datos.setHorizontalHeaderLabels(["FECHA", "TÍTULO DEL INFORME"])
        self.tabla_datos.setRowCount(len(lista_noticias))
        self.tabla_datos.setColumnWidth(0, 150)
        self.tabla_datos.horizontalHeader().setStretchLastSection(True)
        for fila, noti in enumerate(lista_noticias):
            fecha, titulo, cuerpo, es_aviso = noti
            item_fecha = QTableWidgetItem(str(fecha))
            item_titulo = QTableWidgetItem(str(titulo))
            item_titulo.setData(Qt.UserRole, cuerpo)
            if es_aviso:
                item_titulo.setForeground(Qt.red)
            self.tabla_datos.setItem(fila, 0, item_fecha)
            self.tabla_datos.setItem(fila, 1, item_titulo)

    def _on_tabla_doble_click(self, item):
        if "NOTICIAS" in self.lbl_bienvenida.text():
            fila = item.row()
            titulo = self.tabla_datos.item(fila, 1).text()
            cuerpo = self.tabla_datos.item(fila, 1).data(Qt.UserRole)
            QMessageBox.information(self, titulo, cuerpo)

    # ── CU4: Mercado (versión Vigue para tabla_datos) ─────────────────────────────

    def refrescar_mercado(self, lista_activos):
        self.lbl_bienvenida.setText("MERCADO ACTUAL  ·  LISTADO DE ACTIVOS")
        self.tabla_datos.setColumnCount(4)
        self.tabla_datos.setHorizontalHeaderLabels(
            ["SÍMBOLO", "ACTIVO DIGITAL", "PRECIO (FIAT)", "TIPO"]
        )
        self.tabla_datos.setRowCount(len(lista_activos))
        for fila, act in enumerate(lista_activos):
            tipo = "Cripto" if act.es_cripto else "Digital"
            self.tabla_datos.setItem(fila, 0, QTableWidgetItem(act.simbolo))
            self.tabla_datos.setItem(fila, 1, QTableWidgetItem(act.nombre))
            self.tabla_datos.setItem(fila, 2, QTableWidgetItem(f"${act.precio_actual:,.2f}"))
            self.tabla_datos.setItem(fila, 3, QTableWidgetItem(tipo))

    # ── CU12: Avisos urgentes ─────────────────────────────────────────────────────

    def _check_avisos_urgentes(self):
        if not self._controlador:
            return
        aviso = self._controlador.solicitarAvisoUrgente()
        if aviso:
            ultimo = getattr(self, "_ultimo_aviso_mostrado", None)
            if ultimo != aviso.titulo:
                QMessageBox.warning(self, f"⚠ Alerta: {aviso.titulo}", aviso.cuerpo)
                self._ultimo_aviso_mostrado = aviso.titulo

    # ── Utilidades ────────────────────────────────────────────────────────────────

    def mostrar_mensaje(self, titulo: str, mensaje: str):
        QMessageBox.information(self, titulo, mensaje)

    def _limpiar_espacio_central(self):
        if self.canvas_grafico is not None:
            self.content.removeWidget(self.canvas_grafico)
            self.canvas_grafico.deleteLater()
            self.canvas_grafico = None

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref):
        self._controlador = ref