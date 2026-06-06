from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


# ── Paleta ────────────────────────────────────────────────────────────────────
BG         = "#000000"
SURFACE    = "#0D0D10"
CARD_BG    = "#0E0E14"
ACCENT     = "#FF6B00"
ACCENT2    = "#FF8C2A"
ACCENT_DIM = "#FF6B0022"
WHITE_92   = "#EBEBEB"
WHITE_55   = "#8C8C8C"
WHITE_30   = "#4D4D4D"
WHITE_06   = "#0F0F0F"
BORDER     = "rgba(255,255,255,0.08)"


class DetalleActivo(QDialog):

    def __init__(self, nombre, simbolo, descripcion, historial, parent=None):
        super().__init__(parent)
        self.__nombre      = nombre
        self.__simbolo     = simbolo
        self.__descripcion = descripcion
        self.__historial   = historial  # [(precio, fecha_hora), ...]

        self.setWindowTitle(f"{simbolo} — Detalle")
        self.setMinimumSize(780, 560)
        self.setModal(True)
        self._aplicar_estilo_base()
        self._construir_ui()

    # ── Estilo global del diálogo ─────────────────────────────────────────────

    def _aplicar_estilo_base(self):
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {BG};
                font-family: 'Helvetica Neue', 'Segoe UI Variable', Arial, sans-serif;
            }}
            QFrame#card {{
                background: qradialgradient(
                    cx:0.50, cy:0.35, radius:0.80,
                    stop:0.00 rgba(22,22,30,255),
                    stop:0.60 rgba(14,14,20,255),
                    stop:1.00 rgba(8,8,13,255)
                );
                border-top:    1px solid rgba(255,255,255,0.12);
                border-left:   1px solid rgba(255,255,255,0.07);
                border-right:  1px solid rgba(255,255,255,0.05);
                border-bottom: 1px solid rgba(255,255,255,0.04);
                border-radius: 20px;
            }}
            QFrame#accentLine {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0.00 rgba(255,107,0,0),
                    stop:0.30 rgba(255,107,0,140),
                    stop:0.50 rgba(255,160,0,255),
                    stop:0.70 rgba(255,107,0,140),
                    stop:1.00 rgba(255,107,0,0)
                );
                min-height: 1px;
                max-height: 1px;
                border: none;
                border-radius: 0px;
            }}
            QLabel#eyebrow {{
                color: {ACCENT};
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 2.2px;
            }}
            QLabel#titulo {{
                color: {WHITE_92};
                font-size: 17px;
                font-weight: 700;
                letter-spacing: -0.3px;
            }}
            QLabel#simboloBadge {{
                color: {ACCENT};
                background-color: rgba(255,107,0,0.10);
                border: 1px solid rgba(255,107,0,0.25);
                border-radius: 6px;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1.5px;
                padding: 3px 10px;
            }}
            QLabel#descripcion {{
                color: {WHITE_55};
                font-size: 11px;
            }}
            QLabel#precioActual {{
                color: {WHITE_92};
                font-size: 22px;
                font-weight: 700;
                letter-spacing: -0.5px;
            }}
            QLabel#precioLabel {{
                color: rgba(255,140,0,0.65);
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 2px;
            }}
            QLabel#sinDatos {{
                color: {WHITE_30};
                font-size: 12px;
            }}
            QPushButton#btnCerrar {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FF5E00, stop:0.5 #FF8000, stop:1 #FF5200
                );
                color: #000000;
                font-weight: 800;
                font-size: 11px;
                letter-spacing: 2.5px;
                border-radius: 11px;
                border-top:    1px solid rgba(255,200,100,160);
                border-left:   1px solid rgba(255,200,100,80);
                border-right:  1px solid rgba(180,80,0,80);
                border-bottom: 1px solid rgba(160,60,0,120);
                min-height: 40px;
                padding: 0 28px;
            }}
            QPushButton#btnCerrar:hover {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FF7520, stop:0.5 #FFA040, stop:1 #FF6A18
                );
            }}
            QPushButton#btnCerrar:pressed {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #D94E00, stop:0.5 #E06A00, stop:1 #D04400
                );
                padding-top: 1px;
            }}
        """)

    # ── UI ────────────────────────────────────────────────────────────────────

    def _construir_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(0)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        # Accent line top
        accent = QFrame()
        accent.setObjectName("accentLine")
        card_layout.addWidget(accent)

        # Inner content
        inner = QVBoxLayout()
        inner.setContentsMargins(28, 24, 28, 28)
        inner.setSpacing(0)

        # ── Header ────────────────────────────────────────────────────────────
        header_row = QHBoxLayout()
        header_row.setSpacing(10)

        left_header = QVBoxLayout()
        left_header.setSpacing(4)

        eyebrow = QLabel("DETALLE DE ACTIVO")
        eyebrow.setObjectName("eyebrow")

        titulo_row = QHBoxLayout()
        titulo_row.setSpacing(10)
        titulo_row.setAlignment(Qt.AlignVCenter)

        lbl_titulo = QLabel(self.__nombre)
        lbl_titulo.setObjectName("titulo")

        lbl_simbolo = QLabel(self.__simbolo)
        lbl_simbolo.setObjectName("simboloBadge")
        lbl_simbolo.setAlignment(Qt.AlignCenter)

        titulo_row.addWidget(lbl_titulo)
        titulo_row.addWidget(lbl_simbolo)
        titulo_row.addStretch()

        lbl_desc = QLabel(self.__descripcion or "Sin descripción disponible")
        lbl_desc.setObjectName("descripcion")
        lbl_desc.setWordWrap(True)

        left_header.addWidget(eyebrow)
        left_header.addSpacing(4)
        left_header.addLayout(titulo_row)
        left_header.addSpacing(3)
        left_header.addWidget(lbl_desc)

        # Precio actual (esquina derecha)
        right_header = QVBoxLayout()
        right_header.setAlignment(Qt.AlignTop | Qt.AlignRight)
        right_header.setSpacing(2)

        lbl_precio_label = QLabel("PRECIO ACTUAL")
        lbl_precio_label.setObjectName("precioLabel")
        lbl_precio_label.setAlignment(Qt.AlignRight)

        precio_actual = self.__historial[-1][0] if self.__historial else 0.0
        lbl_precio = QLabel(f"${precio_actual:,.2f}")
        lbl_precio.setObjectName("precioActual")
        lbl_precio.setAlignment(Qt.AlignRight)

        right_header.addWidget(lbl_precio_label)
        right_header.addWidget(lbl_precio)

        header_row.addLayout(left_header, stretch=3)
        header_row.addLayout(right_header, stretch=1)

        inner.addLayout(header_row)
        inner.addSpacing(20)

        # ── Separador ─────────────────────────────────────────────────────────
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: rgba(255,255,255,0.05); max-height: 1px; border: none;")
        inner.addWidget(sep)
        inner.addSpacing(20)

        # ── Gráfico ───────────────────────────────────────────────────────────
        lbl_chart_label = QLabel("HISTORIAL DE PRECIOS")
        lbl_chart_label.setObjectName("precioLabel")
        inner.addWidget(lbl_chart_label)
        inner.addSpacing(8)

        if self.__historial and len(self.__historial) > 1:
            canvas = self._crear_grafico()
            inner.addWidget(canvas)
        else:
            lbl_sin = QLabel("Sin suficientes datos históricos para mostrar el gráfico.")
            lbl_sin.setObjectName("sinDatos")
            lbl_sin.setAlignment(Qt.AlignCenter)
            inner.addWidget(lbl_sin)

        inner.addSpacing(20)

        # ── Botón cerrar ──────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_cerrar = QPushButton("CERRAR")
        btn_cerrar.setObjectName("btnCerrar")
        btn_cerrar.setCursor(Qt.PointingHandCursor)
        btn_cerrar.clicked.connect(self.accept)
        btn_row.addWidget(btn_cerrar)
        inner.addLayout(btn_row)

        card_layout.addLayout(inner)
        root.addWidget(card)

    # ── Gráfico matplotlib ────────────────────────────────────────────────────

    def _crear_grafico(self):
        precios = [p for p, _ in self.__historial]
        etiquetas = [str(f)[:16] if f else f"T{i+1}" for i, (_, f) in enumerate(self.__historial)]

        # Simplificar etiquetas del eje X si hay muchos puntos
        n = len(etiquetas)
        paso = max(1, n // 6)
        indices = list(range(n))

        fig = Figure(figsize=(7, 2.8), dpi=100, facecolor=BG)
        ax = fig.add_subplot(111, facecolor=BG)

        # Área bajo la curva con degradado naranja
        ax.fill_between(indices, precios,
                        alpha=0.18,
                        color=ACCENT,
                        linewidth=0)

        # Línea principal
        ax.plot(indices, precios,
                color=ACCENT,
                linewidth=2,
                solid_capstyle="round",
                zorder=3)

        # Punto del precio más reciente
        ax.scatter([indices[-1]], [precios[-1]],
                   color=ACCENT2, s=50, zorder=5, linewidths=0)

        # Línea de precio mínimo (referencia)
        precio_min = min(precios)
        precio_max = max(precios)
        ax.axhline(y=precio_min,
                   color=WHITE_30,
                   linewidth=0.5,
                   linestyle="--",
                   alpha=0.4)

        # Ejes y grid
        ax.set_xlim(-0.5, n - 0.5)
        margen = (precio_max - precio_min) * 0.15 if precio_max != precio_min else precio_min * 0.1
        ax.set_ylim(precio_min - margen, precio_max + margen)

        ax.grid(axis="y",
                color=WHITE_30,
                linewidth=0.4,
                alpha=0.25,
                linestyle="-")
        ax.grid(axis="x", visible=False)

        # Ticks eje X
        tick_indices = indices[::paso]
        tick_labels  = [etiquetas[i] for i in tick_indices]
        ax.set_xticks(tick_indices)
        ax.set_xticklabels(tick_labels,
                           rotation=20,
                           ha="right",
                           fontsize=7,
                           color=WHITE_55)

        # Ticks eje Y
        ax.yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, _: f"${x:,.2f}")
        )
        ax.tick_params(axis="y", colors=WHITE_55, labelsize=8)
        ax.tick_params(axis="both", length=0)

        # Spines
        for spine in ax.spines.values():
            spine.set_visible(False)

        fig.tight_layout(pad=0.5)

        canvas = FigureCanvas(fig)
        canvas.setStyleSheet(f"background-color: {BG}; border: none;")
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        canvas.setFixedHeight(280)
        return canvas