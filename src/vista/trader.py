# src/vista/VentanaTrader.py
# ─────────────────────────────────────────────────────────────────────────────
# CAPA VISTA — CryptoLearning · Ventana del Trader
# Responsabilidad: mostrar datos y capturar eventos de UI.
# Patrón MVC: la Vista NO llama al Modelo directamente; delega al Controlador.
# ─────────────────────────────────────────────────────────────────────────────

import os
from PyQt6.QtWidgets import (
    QMainWindow, QTableWidgetItem, QMessageBox, QHeaderView
)
from PyQt6.QtGui  import QColor, QFont
from PyQt6.QtCore import Qt
from PyQt6 import uic


class VentanaTrader(QMainWindow):
    """
    Vista principal del Trader.
    Contiene:
      · Tabla de mercado   (tabla_mercado)    → CU4 / CU6
      · Panel de operación (spin_cantidad,
                            btn_comprar,
                            btn_vender)       → CU6 / CU7 / CU8
      · Tabla de historial (tabla_historial)  → CU8 / CU9
    """

    # Ruta al .ui (ajusta si tu estructura de carpetas es diferente)
    _UI_PATH = os.path.join(os.path.dirname(__file__), "VentanaTrader.ui")

    def __init__(self):
        super().__init__()
        uic.loadUi(self._UI_PATH, self)

        # Referencia al controlador — se asigna desde fuera (ControladorPrincipal)
        self.controlador = None

        # Estado interno: activo seleccionado en la tabla de mercado
        self._activo_seleccionado = None   # dict {id_activo, nombre, simbolo, precio_actual}

        self._configurar_tablas()
        self._conectar_signals()

    # ─────────────────────────────────────────────────────────────────────────
    # Configuración inicial
    # ─────────────────────────────────────────────────────────────────────────

    def _configurar_tablas(self):
        """Ajusta columnas de las dos tablas para que se estiren correctamente."""
        # Mercado
        hm = self.tabla_mercado.horizontalHeader()
        hm.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        hm.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hm.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_mercado.setEditTriggers(
            self.tabla_mercado.EditTrigger.NoEditTriggers
        )
        self.tabla_mercado.setSelectionBehavior(
            self.tabla_mercado.SelectionBehavior.SelectRows
        )

        # Historial
        hh = self.tabla_historial.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.tabla_historial.setEditTriggers(
            self.tabla_historial.EditTrigger.NoEditTriggers
        )

    def _conectar_signals(self):
        """Conecta los eventos de UI a los métodos de esta Vista o del Controlador."""
        # Selección en la tabla de mercado → actualiza el panel de operación
        self.tabla_mercado.itemSelectionChanged.connect(self._on_activo_seleccionado)

        # Cambio de cantidad → recalcula el total estimado (sin BD, solo UI)
        self.spin_cantidad.valueChanged.connect(self._actualizar_total_estimado)

        # Botones COMPRAR / VENDER → delegan al Controlador
        self.btn_comprar.clicked.connect(self._on_comprar)
        self.btn_vender.clicked.connect(self._on_vender)

        # Cerrar sesión
        self.btn_cerrar_sesion.clicked.connect(self._on_cerrar_sesion)

    # ─────────────────────────────────────────────────────────────────────────
    # Handlers de UI (privados — solo la Vista los llama)
    # ─────────────────────────────────────────────────────────────────────────

    def _on_activo_seleccionado(self):
        """Cuando el usuario hace clic en una fila de la tabla de mercado."""
        filas = self.tabla_mercado.selectedItems()
        if not filas:
            return

        fila = self.tabla_mercado.currentRow()
        # Recuperamos el dict del activo guardado en la UserRole de la celda 0
        item = self.tabla_mercado.item(fila, 0)
        if not item:
            return

        activo = item.data(Qt.ItemDataRole.UserRole)
        if not activo:
            return

        self._activo_seleccionado = activo
        self.lbl_activo_sel.setText(f"{activo['nombre']}  ·  {activo['simbolo']}")
        self.lbl_precio_actual.setText(f"${float(activo['precio_actual']):,.2f}")
        self.lbl_activo_desc.setText(activo.get("descripcion_especial") or "")
        self._actualizar_total_estimado()

    def _actualizar_total_estimado(self):
        """Recalcula el coste/retorno estimado sin tocar la BD."""
        if not self._activo_seleccionado:
            self.lbl_total_valor.setText("—")
            return
        precio   = float(self._activo_seleccionado["precio_actual"])
        cantidad = self.spin_cantidad.value()
        total    = precio * cantidad
        self.lbl_total_valor.setText(f"${total:,.2f}")

    def _on_comprar(self):
        if not self._activo_seleccionado:
            self.mostrar_aviso("Selecciona un activo del mercado primero.")
            return
        if self.controlador:
            self.controlador.trader_realizar_operacion(
                id_activo=self._activo_seleccionado["id_activo"],
                tipo="COMPRA",
                cantidad=self.spin_cantidad.value(),
            )

    def _on_vender(self):
        if not self._activo_seleccionado:
            self.mostrar_aviso("Selecciona un activo del mercado primero.")
            return
        if self.controlador:
            self.controlador.trader_realizar_operacion(
                id_activo=self._activo_seleccionado["id_activo"],
                tipo="VENTA",
                cantidad=self.spin_cantidad.value(),
            )

    def _on_cerrar_sesion(self):
        if self.controlador:
            self.controlador.cerrarSesion()

    # ─────────────────────────────────────────────────────────────────────────
    # Métodos públicos — llamados desde el Controlador
    # ─────────────────────────────────────────────────────────────────────────

    def cargar_mercado(self, activos: list[dict]):
        """
        Rellena la tabla de mercado.
        activos: lista de dicts {id_activo, nombre, simbolo, precio_actual, descripcion_especial}
        """
        self.tabla_mercado.setRowCount(0)
        for activo in activos:
            fila = self.tabla_mercado.rowCount()
            self.tabla_mercado.insertRow(fila)

            # Columna 0: Nombre — guarda el dict completo en UserRole
            item_nombre = QTableWidgetItem(activo["nombre"])
            item_nombre.setData(Qt.ItemDataRole.UserRole, activo)
            self.tabla_mercado.setItem(fila, 0, item_nombre)

            # Columna 1: Símbolo
            item_sym = QTableWidgetItem(activo["simbolo"])
            item_sym.setForeground(QColor("#666680"))
            self.tabla_mercado.setItem(fila, 1, item_sym)

            # Columna 2: Precio
            precio_str = f"${float(activo['precio_actual']):,.2f}"
            item_precio = QTableWidgetItem(precio_str)
            item_precio.setForeground(QColor("#FFFFFF"))
            self.tabla_mercado.setItem(fila, 2, item_precio)

    def actualizar_saldo(self, saldo_fiat: float, patrimonio_total: float):
        """Actualiza el banner superior con el saldo actual del trader."""
        self.lbl_saldo_valor.setText(f"${saldo_fiat:,.2f}")
        self.lbl_patrimonio_valor.setText(f"${patrimonio_total:,.2f}")

    def actualizar_nombre(self, nombre: str):
        """Muestra el nombre del trader en el topbar y el avatar."""
        self.lbl_bienvenida.setText(f"Hola, {nombre}")
        iniciales = "".join(p[0].upper() for p in nombre.split()[:2])
        self.lbl_avatar.setText(iniciales or "TR")

    def cargar_historial(self, operaciones: list[dict]):
        """
        Rellena la tabla de historial. CU8.
        operaciones: lista de dicts {fecha_hora, operacion, simbolo,
                                     cantidad, precio_ejecucion, total_fiat}
        """
        self.tabla_historial.setRowCount(0)
        for op in operaciones:
            fila = self.tabla_historial.rowCount()
            self.tabla_historial.insertRow(fila)

            # Fecha
            fecha_str = str(op["fecha_hora"])[:16]   # "YYYY-MM-DD HH:MM"
            self.tabla_historial.setItem(fila, 0, QTableWidgetItem(fecha_str))

            # Tipo (COMPRA=verde / VENTA=rojo)
            tipo_item = QTableWidgetItem(op["operacion"])
            color = QColor("#00C851") if op["operacion"] == "COMPRA" else QColor("#FF3B30")
            tipo_item.setForeground(color)
            font = QFont()
            font.setBold(True)
            tipo_item.setFont(font)
            self.tabla_historial.setItem(fila, 1, tipo_item)

            # Activo
            self.tabla_historial.setItem(fila, 2, QTableWidgetItem(op["simbolo"]))

            # Cantidad
            cant_str = f"{float(op['cantidad']):.8f}".rstrip("0").rstrip(".")
            self.tabla_historial.setItem(fila, 3, QTableWidgetItem(cant_str))

            # Total
            total_str = f"${float(op['total_fiat']):,.2f}"
            self.tabla_historial.setItem(fila, 4, QTableWidgetItem(total_str))

    def mostrar_exito_operacion(self, mensaje: str):
        """Muestra un diálogo de éxito tras ejecutar CU6."""
        QMessageBox.information(self, "Operación ejecutada", mensaje)

    def mostrar_error(self, mensaje: str):
        """Muestra un diálogo de error (saldo insuficiente, etc.)."""
        QMessageBox.warning(self, "Error", mensaje)

    def mostrar_aviso(self, mensaje: str):
        """Aviso informativo (activo no seleccionado, etc.)."""
        QMessageBox.information(self, "Aviso", mensaje)