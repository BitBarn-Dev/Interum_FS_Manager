from PySide2.QtWidgets import QDialog, QVBoxLayout, QPushButton

class PublisherBase(QDialog):
    def __init__(self, parent=None):
        super(PublisherBase, self).__init__(parent)
        self.setWindowTitle("Publisher")
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)  # Ensure layout is set correctly

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
