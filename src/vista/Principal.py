from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
Form, Window = uic.loadUiType("./src/vista/ui/VentanaPrincipal.ui")

class VentanaPrincipal(QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowState(Qt.WindowMaximized)
        self._controlador = None
        # Conexiones de botones del Trader
        self.btn_logout.clicked.connect(self.on_logout_click)
        self.btn_mercado.clicked.connect(self.on_ver_mercado_click)
        self.btn_cartera.clicked.connect(self.on_ver_cartera_click)
        self.btn_noticias.clicked.connect(self.on_ver_noticias_click)

        self.timer_avisos=QTimer()
        self.timer_avisos.timeout.connect(self.check_avisos_urgentes)
        self.timer_avisos.start(10000)

    def check_avisos_urgentes(self):
        aviso=self.controlador.solicitarAvisoUrgente()
        if aviso:
            if not hasattr(self, 'ultimo_aviso_mostrado') or self.ultimo_aviso_mostrado!=titulo:
                QMessageBox.warning(self, f"Alerta: {titulo}", aviso.cuerpo)
                self.ultimo_aviso_mostrado=aviso.titulo

    def on_ver_mercado_click(self):
        if self.controlador:
            self.controlador.solicitarListaClientes() # Usamos la misma función para pedir los datos a la lógica

    def refrescar_tabla(self, lista_datos):
        # Limpia y rellena la tabla con los datos del simulacro
        self.tabla_datos.setRowCount(len(lista_datos))
        for fila, dato in enumerate(lista_datos):
            self.tabla_datos.setItem(fila, 0, QTableWidgetItem(str(dato['id'])))
            self.tabla_datos.setItem(fila, 1, QTableWidgetItem(dato['estado']))
            self.tabla_datos.setItem(fila, 2, QTableWidgetItem(dato['fecha']))
            self.tabla_datos.setItem(fila, 3, QTableWidgetItem(dato['perf']))

    def on_logout_click(self):
        if self.controlador: self.controlador.cerrarSesion()


    def refrescar_cartera(self, carteraVO, lista_posiciones):
        if carteraVO is None:
            return
        
        self.limpiar_espacio_central()
        texto_cartera = f"MI CARTERA | Fiat: {carteraVO.saldo_fiat} € | Cripto: {carteraVO.valor_activos} € | Total: {carteraVO.patrimonio_total} €"
        self.lbl_bienvenida.setText(texto_cartera)
        
        self.tabla_datos.setColumnCount(5)
        self.tabla_datos.setHorizontalHeaderLabels(["Símbolo", "Cantidad", "Precio Medio", "PnL (€)", "ROI (%)"])
        self.tabla_datos.setRowCount(len(lista_posiciones))
        
        for fila, pos in enumerate(lista_posiciones):
            self.tabla_datos.setItem(fila, 0, QTableWidgetItem(str(pos.simbolo)))
            self.tabla_datos.setItem(fila, 1, QTableWidgetItem(str(pos.cantidad)))
            self.tabla_datos.setItem(fila, 2, QTableWidgetItem(str(pos.precio_medio_compra)))
            
            item_pnl = QTableWidgetItem(str(pos.pnl))
            item_roi = QTableWidgetItem(f"{pos.roi} %")
            color = Qt.green if float(pos.pnl) >= 0 else Qt.red
            item_pnl.setForeground(color)
            item_roi.setForeground(color)
            
            self.tabla_datos.setItem(fila, 3, item_pnl)
            self.tabla_datos.setItem(fila, 4, item_roi)

        

        etiquetas = ['Liquidez (Fiat)']
        valores = [float(carteraVO.saldo_fiat)]
        
        for pos in lista_posiciones:
            etiquetas.append(pos.simbolo)
            valor_actual = (float(pos.precio_medio_compra) * float(pos.cantidad)) + float(pos.pnl)
            valores.append(valor_actual)

        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)
        colores_neon=['#FF6A00', '#00E676', '#00B0FF', '#D500F9', '#FFEA00', '#FF1744']
        # Dibujar un Gráfico de Anillo (Donut Chart)
        wedges, texts, autotexts = ax.pie(
            valores, 
            labels=etiquetas, 
            autopct='%1.1f%%', 
            startangle=90, 
            colors=colores_neon,
            pctdistance=0.75, # Acerca los porcentajes a la línea de color
            wedgeprops={'width': 0.4, 'edgecolor': '#0F0F16', 'linewidth': 2} # El "width" vacía el centro
        )

        # 3. Dar formato a los textos para que se lean sobre fondo oscuro
        for text in texts:
            text.set_color('white')  # Nombre de las monedas en blanco
            text.set_fontsize(10)
            text.set_fontweight('bold')
            
        for autotext in autotexts:
            autotext.set_color('black') # Porcentajes en negro para contrastar con los colores neón
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')

        # 4. Título con la tipografía y color de tu interfaz
        titulo = plt.title("DISTRIBUCIÓN DEL PORTFOLIO", pad=20)
        titulo.set_color('#FF8C00') # Naranja
        titulo.set_fontsize(12)
        titulo.set_fontweight('bold')
        titulo.set_family('sans-serif')

        # Para que sea un círculo perfecto
        ax.axis('equal') 

        # Incrustar el gráfico
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        self.canvas_grafico = FigureCanvas(fig)
        
        # Truco final: Hacer que el widget de PyQt5 también sea transparente
        self.canvas_grafico.setStyleSheet("background-color: transparent;")
        self.content.addWidget(self.canvas_grafico)
            

    def on_ver_cartera_click(self):
        if self.controlador:
            self.controlador.solicitarEstadoCarteraTrader()

    def refrescar_noticias(self,lista_noticias):
        self.lbl_bienvenida.setText("NOTICIAS E INFORMES · MERCADO")
        
        # Configurar la tabla para Noticias (2 columnas)
        self.tabla_datos.setColumnCount(2)
        self.tabla_datos.setHorizontalHeaderLabels(["FECHA", "TÍTULO DEL INFORME"])
        self.tabla_datos.setRowCount(len(lista_noticias))
        
        # Estética de columnas
        self.tabla_datos.setColumnWidth(0, 150)
        self.tabla_datos.horizontalHeader().setStretchLastSection(True)
        
        # Rellenar filas
        for fila, noti in enumerate(lista_noticias):
            fecha, titulo, cuerpo, es_aviso = noti
            
            item_fecha = QTableWidgetItem(str(fecha))
            item_titulo = QTableWidgetItem(str(titulo))
            
            # Guardamos el cuerpo en el UserRole para poder leerlo luego (OCULTA)
            item_titulo.setData(Qt.UserRole, cuerpo)
            
            # Si es aviso urgente, estilo especial en rojo neón
            if es_aviso:
                item_titulo.setForeground(Qt.red)
            
            self.tabla_datos.setItem(fila, 0, item_fecha)
            self.tabla_datos.setItem(fila, 1, item_titulo)
        
    def limpiar_espacio_central(self):
        if hasattr(self, 'canvas_grafico') and self.canvas_grafico is not None:
            self.content.removeWidget(self.canvas_grafico)
            self.canvas_grafico.deleteLater()
            self.canvas_grafico = None
        
        if hasattr(self, 'tabla_noticias') and self.tabla_noticias is not None:
            self.content.removeWidget(self.tabla_noticias)
            self.tabla_noticias.deleteLater()
            self.tabla_noticias = None


    def mostrar_mensaje(self,titulo,mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def on_tabla_doble_click(self, item):
        if "NOTICIAS" in self.lbl_bienvenida.text():
            fila = item.row()
            titulo = self.tabla_datos.item(fila, 1).text()
            cuerpo = self.tabla_datos.item(fila, 1).data(Qt.UserRole)
            
            QMessageBox.information(self, titulo, cuerpo)

    
    def refrescar_mercado(self,lista_activos):
        self.lbl_bienvenida.setText("MERCADO ACTUAL | LISTADO DE ACTIVOS")
        self.tabla_datos.setColumnCount(4)
        self.tabla_datos.setHorizontalHeaderLabels(["SÍMBOLO", "ACTIVO DIGITAL", "PRECIO (FIAT)", "TIPO"])
        self.tabla_datos.setRowCount(len(lista_activos))
        
        for fila, act in enumerate(lista_activos):
            self.tabla_datos.setItem(fila, 0, QTableWidgetItem(str(act.simbolo)))
            self.tabla_datos.setItem(fila, 1, QTableWidgetItem(str(act.nombre)))
            self.tabla_datos.setItem(fila, 2, QTableWidgetItem(f"{float(act.precio):.2f} €"))
            self.tabla_datos.setItem(fila, 3, QTableWidgetItem(str(act.tipo)))


    def on_ver_noticias_click(self):
        if self.controlador:
            self.limpiar_espacio_central()
            self.controlador.solicitarNoticias()
    @property
    def controlador(self): return self._controlador
    
    @controlador.setter
    def controlador(self, val): self._controlador = val


    