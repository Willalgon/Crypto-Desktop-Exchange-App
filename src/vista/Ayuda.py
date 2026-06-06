from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QLineEdit, QTextEdit, QSplitter
from PyQt5.QtCore import Qt

class Ayuda(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayuda y Soporte — CryptoLearning")
        self.resize(800, 600)
        self.setStyleSheet("background-color: #111113; color: white;")
        
        layout = QVBoxLayout(self)
        
        # Buscador
        self.buscador = QLineEdit()
        self.buscador.setPlaceholderText("🔍 Buscar en la ayuda...")
        self.buscador.textChanged.connect(self._filtrar_ayuda)
        layout.addWidget(self.buscador)
        
        splitter = QSplitter(Qt.Horizontal)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Índice"])
        self.texto_ayuda = QTextEdit()
        self.texto_ayuda.setReadOnly(True)
        
        splitter.addWidget(self.tree)
        splitter.addWidget(self.texto_ayuda)
        splitter.setStretchFactor(1, 2)
        layout.addWidget(splitter)
        
        self._cargar_contenido()
        self.tree.itemClicked.connect(self._mostrar_contenido)

    def _cargar_contenido(self):
        self.items = {
            "Inicio": "Bienvenido a CryptoLearning. Aquí puedes gestionar tu cartera.",
            "Trading": "En la sección de Mercado puedes ver activos y realizar compras/ventas.",
            "Mi Cartera": "Visualiza tus posiciones, el gráfico de distribución y tu P&L.",
            "Noticias": "Noticias publicadas por analistas para guiar tus decisiones."
        }
        for titulo in self.items:
            item = QTreeWidgetItem(self.tree)
            item.setText(0, titulo)

    def _mostrar_contenido(self, item):
        titulo = item.text(0)
        self.texto_ayuda.setPlainText(self.items.get(titulo, "Sin ayuda."))

    def _filtrar_ayuda(self, texto):
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            item.setHidden(texto.lower() not in item.text(0).lower())