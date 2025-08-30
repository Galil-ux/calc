# 🔬 Scientific Calculator with Currency Converter

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![C](https://img.shields.io/badge/C-GCC%2FMinGW-orange?logo=c)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green?logo=qt)
![License](https://img.shields.io/badge/License-MIT-purple)

A high-performance **scientific calculator** powered by **C** for math operations and **Python** for GUI and real-time **currency conversion**. Built with **PyQt6** for a sleek, functional interface.

✨ Features:
- ✅ **C-accelerated** scientific functions (`sin`, `cos`, `log`, `sqrt`, etc.)
- 💱 **Live currency conversion** using real exchange rates
- 🖼️ **Modern GUI** with tabbed interface
- 🔌 Seamless **C-Python integration** via `ctypes`

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Galil-ux/scientific-calculator.git
cd scientific-calculator

🛠️ Prerequisites
Before running, ensure you have:

Python 3.8 or higher → python.org
A C compiler:
Linux/macOS: gcc (install via sudo apt install build-essential or xcode-select --install)
Windows: MinGW-w64 or TDM-GCC
Internet connection (for currency exchange rates)

📦 Install Dependencies
bash
1. pip install PyQt6 requests
💡 Tip: Use a virtual environment! 

bash
1. python -m venv venv
2. source venv/bin/activate    # Linux/macOS
3.# or
4. venv\Scripts\activate       # Windows
🔧 Compile the C Extension
This project uses C for fast math operations. You must compile math_ops.c into a shared library.

On Linux/macOS:
bash
1. gcc -fPIC -shared -o math_ops.so math_ops.c -lm
On Windows (MinGW):
bash
1. gcc -shared -o math_ops.dll math_ops.c -lm
✅ This creates:

math_ops.so (Linux/macOS)
math_ops.dll (Windows)
⚠️ Make sure the compiled file is in the same directory as calculator.py. 

▶️ Run the Application
bash
1. python calculator.py
🎉 The app will launch with two tabs:

Scientific Calculator – C-powered math
Currency Converter – Real-time rates from exchangerate-api.com
 

💱 Currency Converter
Select From and To currencies
Enter an amount
Click Convert
🌐 Uses free API: https://api.exchangerate-api.com/v4/latest/USD
🔁 Rates update on app startup

📄 License
MIT © Galil-ux
See LICENSE for details.
