# calculator.py
import sys
import ctypes
import json
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox,
    QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Load C shared library
try:
    if sys.platform == "win32":
        lib = ctypes.CDLL("./math_ops.dll")
    else:
        lib = ctypes.CDLL("./math_ops.so")
except OSError as e:
    QMessageBox.critical(None, "Error", f"Could not load C library: {e}")
    sys.exit(1)

# Define argument and return types for C functions
for func_name in ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp']:
    getattr(lib, f"c_{func_name}").argtypes = [ctypes.c_double]
    getattr(lib, f"c_{func_name}").restype = ctypes.c_double

lib.c_pow.argtypes = [ctypes.c_double, ctypes.c_double]
lib.c_pow.restype = ctypes.c_double


class ScientificCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.current_input = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont("Arial", 16))
        layout.addWidget(self.display)

        # Button grid
        buttons = QGridLayout()
        button_names = [
            ['(', ')', 'C', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', 'sqrt'],
            ['sin', 'cos', 'tan', '^'],
            ['log', 'exp', 'pi', 'Ans']
        ]

        positions = [(i, j) for i in range(7) for j in range(4)]
        self.buttons = {}

        for pos, name in zip(positions, [item for row in button_names for item in row]):
            button = QPushButton(name)
            button.setFont(QFont("Arial", 12))
            button.clicked.connect(lambda _, x=name: self.button_click(x))
            buttons.addWidget(button, *pos)
            self.buttons[name] = button

        layout.addLayout(buttons)
        self.setLayout(layout)

    def button_click(self, key):
        if key == 'C':
            self.current_input = ""
            self.display.setText("0")
        elif key == '=':
            try:
                result = self.evaluate_expression(self.current_input)
                self.current_input = str(result)
                self.display.setText(str(result))
            except Exception as e:
                self.display.setText("Error")
                self.current_input = ""
        elif key == 'sqrt':
            try:
                val = float(self.current_input)
                result = lib.c_sqrt(val)
                self.current_input = str(result)
                self.display.setText(str(result))
            except:
                self.display.setText("Error")
        elif key in ['sin', 'cos', 'tan', 'log', 'exp']:
            try:
                val = float(self.current_input)
                func = getattr(lib, f"c_{key}")
                result = func(val)
                self.current_input = str(result)
                self.display.setText(str(result))
            except:
                self.display.setText("Error")
        elif key == 'pi':
            self.current_input += str(3.141592653589793)
            self.display.setText(self.current_input)
        elif key == 'Ans':
            pass  # Could store last answer
        else:
            self.current_input += key
            self.display.setText(self.current_input)

    def evaluate_expression(self, expr):
        # Safely evaluate expression with power support
        expr = expr.replace('^', '**')
        try:
            return eval(expr, {"__builtins__": {}, "lib": lib}, {})
        except:
            raise ValueError("Invalid expression")


class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.rates = {}
        self.init_ui()
        self.fetch_rates()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Currency Converter")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        # From
        from_layout = QHBoxLayout()
        from_layout.addWidget(QLabel("From:"))
        self.from_combo = QComboBox()
        self.from_combo.addItems(["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "INR"])
        from_layout.addWidget(self.from_combo)
        layout.addLayout(from_layout)

        # To
        to_layout = QHBoxLayout()
        to_layout.addWidget(QLabel("To:"))
        self.to_combo = QComboBox()
        self.to_combo.addItems(["EUR", "USD", "GBP", "JPY", "CAD", "AUD", "INR"])
        to_layout.addWidget(self.to_combo)
        layout.addLayout(to_layout)

        # Amount
        amount_layout = QHBoxLayout()
        amount_layout.addWidget(QLabel("Amount:"))
        self.amount_input = QLineEdit("1.0")
        self.amount_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        amount_layout.addWidget(self.amount_input)
        layout.addLayout(amount_layout)

        # Convert button
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.convert)
        layout.addWidget(self.convert_btn)

        # Result
        self.result_label = QLabel("Result: ")
        self.result_label.setFont(QFont("Arial", 14))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

        # Last updated
        self.status = QLabel("Fetching exchange rates...")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet("color: gray;")
        layout.addWidget(self.status)

        self.setLayout(layout)

    def fetch_rates(self):
        try:
            # Use a free API (get your free key at exchangerate-api.com)
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url, timeout=5)
            data = response.json()
            self.rates = data['rates']
            self.status.setText(f"Rates updated: {data['date']}")
        except Exception as e:
            self.status.setText("Failed to fetch rates.")
            QMessageBox.warning(self, "Network Error", f"Could not fetch exchange rates: {e}")

    def convert(self):
        if not self.rates:
            self.status.setText("Rates not loaded yet.")
            return

        try:
            amount = float(self.amount_input.text())
            from_curr = self.from_combo.currentText()
            to_curr = self.to_combo.currentText()

            # Convert via USD as base
            if from_curr != "USD":
                amount_usd = amount / self.rates[from_curr]
            else:
                amount_usd = amount

            result = amount_usd * self.rates[to_curr]
            self.result_label.setText(f"Result: {result:,.4f} {to_curr}")
        except Exception as e:
            self.result_label.setText("Error")
            QMessageBox.critical(self, "Error", f"Conversion failed: {e}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scientific Calculator with Currency Converter")
        self.setGeometry(100, 100, 400, 600)

        tabs = QTabWidget()
        tabs.addTab(ScientificCalculator(), "Calculator")
        tabs.addTab(CurrencyConverter(), "Currency")

        self.setCentralWidget(tabs)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
