from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QHeaderView,
                             QTableWidgetItem, QPushButton)
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

Form, Window = uic.loadUiType("./src/vista/ui/Trader.ui")


class Trader(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._controlador = None
        self._canvas_cartera = None
        self._ultimo_aviso_mostrado = None
        self._avisos_mostrados = set()

        self._configurar_tablas()
        self._inyectar_boton_ayuda() 
        self._conectar_senales()

        # Timer avisos urgentes cada 10 s
        self._timer_avisos = QTimer()
        self._timer_avisos.timeout.connect(self._check_avisos_urgentes)
        self._timer_avisos.start(10000)

        

  
    # ── Configuración inicial de tablas ──────────────────────────────────────

    def _configurar_tablas(self):
        # Tabla mercado: col 0 = id_activo (oculta)
        self.tabla_mercado.setColumnCount(5)
        self.tabla_mercado.setHorizontalHeaderLabels(
            ["ID", "ACTIVO", "SÍMBOLO", "PRECIO ACTUAL", "TIPO"]
        )
        self.tabla_mercado.setColumnHidden(0, True)
        self.tabla_mercado.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_mercado.verticalHeader().setVisible(False)

        # Tabla posiciones
        self.tabla_posiciones.setColumnCount(6)
        self.tabla_posiciones.setHorizontalHeaderLabels(
            ["ACTIVO", "SÍMBOLO", "CANTIDAD", "PRECIO MEDIO", "VALOR ACTUAL", "P&L"]
        )
        self.tabla_posiciones.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_posiciones.verticalHeader().setVisible(False)

        # Tabla noticias
        self.tabla_noticias.setColumnCount(4)
        self.tabla_noticias.setHorizontalHeaderLabels(
            ["FECHA", "TÍTULO", "TIPO", "ANALISTA"]
        )
        self.tabla_noticias.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_noticias.verticalHeader().setVisible(False)

        # Tabla historial operaciones
        self.tabla_historial.setColumnCount(6)
        self.tabla_historial.setHorizontalHeaderLabels(
            ["FECHA", "ACTIVO", "TIPO", "CANTIDAD", "PRECIO UNIT.", "TOTAL"]
        )
        self.tabla_historial.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_historial.verticalHeader().setVisible(False)

    # ── Conexión de señales ──────────────────────────────────────────────────

    def _conectar_senales(self):
        # Nav sidebar → cambiar página del stacked
        self.btn_nav_mercado.clicked.connect(self._mostrar_mercado)
        self.btn_nav_cartera.clicked.connect(self._mostrar_cartera)
        self.btn_nav_noticias.clicked.connect(self._mostrar_noticias)
        self.btn_nav_historial.clicked.connect(self._mostrar_historial)
        self.btn_nav_salir.clicked.connect(self._on_logout)
        self.btn_ayuda.clicked.connect(self._abrir_ayuda)

        # Acciones en page_mercado
        self.btn_ver_detalles.clicked.connect(self._ver_detalles_activo)
        self.btn_comprar.clicked.connect(lambda: self._ejecutar_operacion("COMPRA"))
        self.btn_vender.clicked.connect(lambda: self._ejecutar_operacion("VENTA"))

        # Doble clic en tabla mercado → rellena el combo de operación
        self.tabla_mercado.doubleClicked.connect(self._seleccionar_activo_desde_tabla)

        # Doble clic en noticias → leer noticia completa
        self.tabla_noticias.doubleClicked.connect(self._leer_noticia)

    # ── Navegación (stacked) ─────────────────────────────────────────────────

    def _inyectar_boton_ayuda(self):
        self.btn_ayuda = QPushButton("❓ Ayuda", self)
        self.btn_ayuda.setCursor(Qt.PointingHandCursor)
        self.btn_ayuda.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 8px 12px;
                font-size: 11px;
            }
            QPushButton:hover { background: rgba(255, 107, 0, 0.2); color: #FF8C2A; }
        """)
    
        self.topbar.layout().insertWidget(2, self.btn_ayuda)


    def _abrir_ayuda(self):
        from src.vista.Ayuda import Ayuda
        ventana_ayuda = Ayuda(self)
        ventana_ayuda.exec_()

    def _mostrar_mercado(self):
        self.stacked_trader.setCurrentIndex(0)
        self.lbl_topbar_breadcrumb_active.setText("Mercado")
        if self._controlador:
            self._controlador.solicitarMercado()

    def _mostrar_cartera(self):
        self.stacked_trader.setCurrentIndex(1)
        self.lbl_topbar_breadcrumb_active.setText("Mi Cartera")
        if self._controlador:
            self._controlador.solicitarEstadoCarteraTrader()

    def _mostrar_noticias(self):
        self.stacked_trader.setCurrentIndex(2)
        self.lbl_topbar_breadcrumb_active.setText("Noticias")
        if self._controlador:
            self._controlador.solicitarNoticias()

    def _mostrar_historial(self):
        self.stacked_trader.setCurrentIndex(3)
        self.lbl_topbar_breadcrumb_active.setText("Historial")
        if self._controlador:
            self._controlador.cargar_historial_trader()

    def _on_logout(self):
        if self._controlador:
            self._controlador.cerrarSesion()

    # ── Mercado ──────────────────────────────────────────────────────────────

    def cargar_mercado(self, activos: list):
        self.tabla_mercado.setRowCount(len(activos))
        for i, a in enumerate(activos):
            tipo = "Cripto" if a.es_cripto else "Digital"
            self.tabla_mercado.setItem(i, 0, QTableWidgetItem(str(a.id_activo)))
            self.tabla_mercado.setItem(i, 1, QTableWidgetItem(a.nombre))
            self.tabla_mercado.setItem(i, 2, QTableWidgetItem(a.simbolo))
            self.tabla_mercado.setItem(i, 3, QTableWidgetItem(f"${a.precio_actual:,.2f}"))
            self.tabla_mercado.setItem(i, 4, QTableWidgetItem(tipo))
        # Sincronizar combo de operación con los activos cargados
        self._sync_combo_activo(activos)

    # igual que cargar_mercado — alias usado por solicitarMercado
    def refrescar_mercado(self, activos: list):
        self.cargar_mercado(activos)

    def _sync_combo_activo(self, activos: list):
        self.combo_activo.clear()
        for a in activos:
            self.combo_activo.addItem(f"{a.simbolo} — {a.nombre}", userData=a.id_activo)

    def _seleccionar_activo_desde_tabla(self):
        """Doble clic en tabla_mercado → selecciona ese activo en el combo."""
        fila = self.tabla_mercado.currentRow()
        if fila < 0:
            return
        id_activo = int(self.tabla_mercado.item(fila, 0).text())
        for idx in range(self.combo_activo.count()):
            if self.combo_activo.itemData(idx) == id_activo:
                self.combo_activo.setCurrentIndex(idx)
                break

    def _ver_detalles_activo(self):
        fila = self.tabla_mercado.currentRow()
        if fila < 0:
            QMessageBox.information(self, "Selección", "Selecciona un activo de la tabla.")
            return
        id_activo   = int(self.tabla_mercado.item(fila, 0).text())
        nombre      = self.tabla_mercado.item(fila, 1).text()
        simbolo     = self.tabla_mercado.item(fila, 2).text()
        descripcion = ""  # col 4 oculta no disponible directamente
        if self._controlador:
            self._controlador.ver_detalles_activo(id_activo, nombre, simbolo, descripcion)

    # ── Operación (compra / venta) ───────────────────────────────────────────

    def _ejecutar_operacion(self, tipo: str):
        if not self._controlador:
            return
        id_activo = self.combo_activo.currentData()
        if id_activo is None:
            QMessageBox.warning(self, "Error", "Selecciona un activo.")
            return
        cantidad = self.input_cantidad.value()
        self._controlador.trader_realizar_operacion(id_activo, tipo, cantidad)

    # ── Saldo / KPIs ─────────────────────────────────────────────────────────

    def actualizar_nombre(self, nombre_completo: str):
        self.lbl_user_name.setText(nombre_completo)

    def actualizar_saldo(self, saldo_fiat: float, patrimonio_total: float):
        self.lbl_kpi_saldo.setText(f"${saldo_fiat:,.2f}")
        self.lbl_kpi_patrimonio.setText(f"${patrimonio_total:,.2f}")

    def mostrar_exito_operacion(self, mensaje: str):
        QMessageBox.information(self, "Operación ejecutada", mensaje)

    # ── Cartera / Posiciones ─────────────────────────────────────────────────

    def refrescar_cartera(self, carteraVO, lista_posiciones: list):
        if carteraVO is None:
            return
        # Actualizar KPIs
        self.actualizar_saldo(
            float(carteraVO.saldo_fiat),
            float(carteraVO.patrimonio_total),
        )
        # Llenar tabla posiciones
        self.tabla_posiciones.setRowCount(len(lista_posiciones))
        for i, pos in enumerate(lista_posiciones):
            pnl = float(pos.pnl) if hasattr(pos, "pnl") else 0.0
            roi = float(pos.roi) if hasattr(pos, "roi") else 0.0
            color = QColor("#34C759") if pnl >= 0 else QColor("#FF3B30")
            items = [
                QTableWidgetItem(pos.activo   if hasattr(pos, "activo")   else ""),
                QTableWidgetItem(pos.simbolo  if hasattr(pos, "simbolo")  else ""),
                QTableWidgetItem(f"{float(pos.cantidad):,.8f}"),
                QTableWidgetItem(f"${float(pos.precio_medio_compra):,.2f}"),
                QTableWidgetItem(f"${float(pos.precio_actual) * float(pos.cantidad):,.2f}"),
                QTableWidgetItem(f"${pnl:,.2f}  ({roi:.2f}%)"),
            ]
            for col, item in enumerate(items):
                if col == 5:
                    item.setForeground(color)
                self.tabla_posiciones.setItem(i, col, item)

        self._dibujar_grafico_cartera(lista_posiciones)



    def _dibujar_grafico_cartera(self, lista_posiciones):
        # 1. Preparar datos
        posiciones_validas = [p for p in lista_posiciones if float(p.cantidad) > 0]
        nombres = [p.simbolo for p in posiciones_validas]
        valores = [float(p.cantidad) * float(p.precio_actual) for p in posiciones_validas]
        
        if not valores: return

        # 2. Configurar estética oscura (Dark Matter)
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        fig.patch.set_facecolor('#18181B')  # Color Surface-2 de tu app
        ax.set_facecolor('#18181B')

        # 3. Colores personalizados (CryptoOrange y derivados)
        colores = ['#FF6B00', '#FF8C2A', '#FFB347', '#E0A890']
        
        # 4. Crear el anillo (Donut Chart)
        # 'wedgeprops' con 'width' crea el efecto de anillo
        wedges, texts, autotexts = ax.pie(
            valores, labels=nombres, autopct='%1.1f%%', 
            startangle=90, colors=colores,
            wedgeprops={'width': 0.4, 'edgecolor': '#18181B', 'linewidth': 3}
        )

        # 5. Estilo de texto
        plt.setp(texts, size=10, color=(1, 1, 1, 0.7))
        plt.setp(autotexts, size=10, weight="bold", color="white")

        # 6. Integración en Qt
        canvas = FigureCanvas(fig)
        canvas.setStyleSheet("background-color:transparent;") # Asegura transparencia
        
        if self._canvas_cartera:
            self.page_cartera.layout().removeWidget(self._canvas_cartera)
            self._canvas_cartera.deleteLater()
            
        self.page_cartera.layout().addWidget(canvas)
        self._canvas_cartera = canvas

    # ── Noticias ─────────────────────────────────────────────────────────────

    def refrescar_noticias(self, lista_noticias: list):
        self.tabla_noticias.setRowCount(len(lista_noticias))
        for i, n in enumerate(lista_noticias):
            # n puede ser tupla (fecha, titulo, cuerpo, es_aviso) o NoticiaVO
            if isinstance(n, (list, tuple)):
                fecha, titulo, cuerpo, es_aviso = n[0], n[1], n[2], n[3]
                analista = n[4] if len(n) > 4 else ""
            else:
                fecha    = str(n.fecha_publicacion)
                titulo   = n.titulo
                cuerpo   = n.cuerpo
                es_aviso = n.es_aviso
                analista = ""

            tipo_item  = QTableWidgetItem("⚡ AVISO" if es_aviso else "Noticia")
            titulo_item = QTableWidgetItem(titulo)
            titulo_item.setData(Qt.UserRole, cuerpo)   # cuerpo en UserRole

            if es_aviso:
                naranja = QColor("#FF6B00")
                for item in (tipo_item, titulo_item):
                    item.setForeground(naranja)

            self.tabla_noticias.setItem(i, 0, QTableWidgetItem(str(fecha)))
            self.tabla_noticias.setItem(i, 1, titulo_item)
            self.tabla_noticias.setItem(i, 2, tipo_item)
            self.tabla_noticias.setItem(i, 3, QTableWidgetItem(analista))

    def _leer_noticia(self):
        fila = self.tabla_noticias.currentRow()
        if fila < 0:
            return
        titulo_item = self.tabla_noticias.item(fila, 1)
        titulo = titulo_item.text()
        cuerpo = titulo_item.data(Qt.UserRole) or ""
        QMessageBox.information(self, titulo, cuerpo)

    # ── Historial operaciones ─────────────────────────────────────────────────

    def cargar_historial(self, operaciones: list):
        self.tabla_historial.setRowCount(len(operaciones))
        for i, op in enumerate(operaciones):
            # op puede ser dict o VO
            if isinstance(op, dict):
                fecha    = str(op.get("fecha_hora", ""))
                activo   = op.get("simbolo", "")
                tipo     = op.get("operacion", op.get("tipo", ""))
                cantidad = float(op.get("cantidad", 0))
                precio   = float(op.get("precio_ejecucion", 0))
                total    = float(op.get("total_fiat", 0))
            else:
                fecha    = str(op.fecha_hora)
                activo   = op.simbolo
                tipo     = op.tipo
                cantidad = float(op.cantidad)
                precio   = float(op.precio_ejecucion)
                total    = float(op.total_fiat)

            color = QColor("#34C759") if tipo == "COMPRA" else QColor("#FF3B30")
            tipo_item = QTableWidgetItem(tipo)
            tipo_item.setForeground(color)

            self.tabla_historial.setItem(i, 0, QTableWidgetItem(fecha))
            self.tabla_historial.setItem(i, 1, QTableWidgetItem(activo))
            self.tabla_historial.setItem(i, 2, tipo_item)
            self.tabla_historial.setItem(i, 3, QTableWidgetItem(f"{cantidad:,.8f}"))
            self.tabla_historial.setItem(i, 4, QTableWidgetItem(f"${precio:,.2f}"))
            self.tabla_historial.setItem(i, 5, QTableWidgetItem(f"${total:,.2f}"))

    # ── Avisos urgentes (CU12) ────────────────────────────────────────────────

    def _check_avisos_urgentes(self):
        if not self._controlador:
            return

        aviso = self._controlador.solicitarAvisoUrgente()
        if aviso and aviso.titulo not in self._avisos_mostrados:
            QMessageBox.warning(self, aviso.titulo, aviso.cuerpo)
            self._avisos_mostrados.add(aviso.titulo)
            return

        evento = self._controlador.solicitarUltimoEvento()
        if evento and evento.nombre_evento not in self._avisos_mostrados:
            QMessageBox.warning(
                self,
                evento.nombre_evento,
                evento.descripcion or "Se ha producido un evento de mercado."
            )
            self._avisos_mostrados.add(evento.nombre_evento)
            self._controlador.solicitarMercado()

    def _dibujar_grafico_cartera(self, lista_posiciones: list):
        posiciones_validas = [p for p in lista_posiciones if float(p.cantidad) > 0]
        nombres = [p.simbolo for p in posiciones_validas]
        valores = [float(p.cantidad) * float(p.precio_actual) for p in posiciones_validas]

        if not valores:
            return

        plt.rcParams.update({"font.family": "sans-serif"})
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor("#0D0D0F")
        ax.set_facecolor("#0D0D0F")

        colores = [
            "#FF6B00", "#FFFFFF", "#FF9A45",
            "#B0B0B0", "#FFD199", "#787878",
            "#CC4400", "#D4D4D4",
        ]

        total = sum(valores)

        wedges, *_ = ax.pie(
            valores,
            labels=None,
            autopct=None,  # sin porcentajes encima
            startangle=90,
            colors=colores[:len(valores)],
            wedgeprops={"width": 0.35, "edgecolor": "#0D0D0F", "linewidth": 2},
        )

        # Leyenda con símbolo + valor + porcentaje
        ax.legend(
            wedges,
            [f"{n}  ${v:,.0f}  ({v / total * 100:.1f}%)" for n, v in zip(nombres, valores)],
            loc="center left",
            bbox_to_anchor=(1.0, 0.5),
            frameon=False,
            fontsize=8,
            labelcolor="white",
        )

        # Texto central
        ax.text(0, 0.1, "TOTAL", ha="center", va="center",
                fontsize=7, color=(1, 1, 1, 0.4))
        ax.text(0, -0.15, f"${total:,.0f}", ha="center", va="center",
                fontsize=10, weight="bold", color=(1, 1, 1, 1))

        fig.subplots_adjust(left=0.05, right=0.62, top=0.95, bottom=0.05)

        canvas = FigureCanvas(fig)
        canvas.setStyleSheet("background-color: transparent;")

        layout = self.page_cartera.layout()
        if self._canvas_cartera:
            layout.removeWidget(self._canvas_cartera)
            self._canvas_cartera.deleteLater()
            plt.close("all")

        layout.addWidget(canvas)
        self._canvas_cartera = canvas

    def refrescar_cartera(self, carteraVO, lista_posiciones: list):
        if carteraVO is None:
            return

        self.actualizar_saldo(
            float(carteraVO.saldo_fiat),
            float(carteraVO.patrimonio_total),
        )
        self.tabla_posiciones.setRowCount(len(lista_posiciones))
        for i, pos in enumerate(lista_posiciones):
            pnl = float(pos.pnl) if hasattr(pos, "pnl") else 0.0
            roi = float(pos.roi) if hasattr(pos, "roi") else 0.0
            color = QColor("#34C759") if pnl >= 0 else QColor("#FF3B30")
            items = [
                QTableWidgetItem(pos.activo if hasattr(pos, "activo") else ""),
                QTableWidgetItem(pos.simbolo if hasattr(pos, "simbolo") else ""),
                QTableWidgetItem(f"{float(pos.cantidad):,.8f}"),
                QTableWidgetItem(f"${float(pos.precio_medio_compra):,.2f}"),
                QTableWidgetItem(f"${float(pos.precio_actual) * float(pos.cantidad):,.2f}"),
                QTableWidgetItem(f"${pnl:,.2f}  ({roi:.2f}%)"),
            ]
            for col, item in enumerate(items):
                if col == 5:
                    item.setForeground(color)
                self.tabla_posiciones.setItem(i, col, item)
        self._dibujar_grafico_cartera(lista_posiciones)

    def _refrescar_datos_trader(self):
        cartera = self.__modelo.obtener_cartera(self.__usuario_actual.id_usuario)
        if cartera:
            self.__vista_principal.actualizar_saldo(
                saldo_fiat=cartera.saldo_fiat,
                patrimonio_total=cartera.patrimonio_total,
            )
        operaciones = self.__modelo.obtener_historial_operaciones(self.__usuario_actual.id_usuario)
        self.__vista_principal.cargar_historial(operaciones)

        # ← AÑADIR ESTO para que el gráfico se redibuje tras compra/venta
        posiciones = self.__modelo.obtenerPosiciones(self.__usuario_actual.id_usuario)
        self.__vista_principal.refrescar_cartera(cartera, posiciones)

    # ── Utilidades ────────────────────────────────────────────────────────────

    def mostrar_error(self, mensaje: str):
        QMessageBox.warning(self, "Error", mensaje)

    def mostrar_mensaje(self, titulo: str, mensaje: str):
        QMessageBox.information(self, titulo, mensaje)

    # ── Propiedad controlador ─────────────────────────────────────────────────

    @property
    def controlador(self):
        return self._controlador

    @controlador.setter
    def controlador(self, ref):
        self._controlador = ref


