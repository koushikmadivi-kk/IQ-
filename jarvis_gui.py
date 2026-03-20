from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel

from PyQt6.QtGui import QFont, QPainter, QColor, QPen
import math
import sys
import threading
import time

# Import your existing Jarvis functions
from main import listen, speak, ask_gpt, execute_local_commands, remember, recall

# ---------------- HUD ANIMATION ----------------
class JarvisHUD(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(800, 600)
        self.setWindowTitle("JARVIS HUD")
        self.setStyleSheet("background-color: black;")

        self.angle1 = 0
        self.angle2 = 0

        self.label = QLabel("J.A.R.V.I.S", self)
        self.label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        self.label.setStyleSheet("color: cyan;")
        self.label.adjustSize()

        timer = QTimer(self)
        timer.timeout.connect(self.animate)
        timer.start(30)

    def animate(self):
        self.angle1 = (self.angle1 + 3) % 360
        self.angle2 = (self.angle2 - 2) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2

        size = min(w, h) * 0.7
        radius = size / 2

        self.label.move(int(cx - self.label.width()/2), int(cy - 12))

        glow = QColor(0, 255, 255, 200)
        faint = QColor(0, 255, 255, 120)

        # Outer Neon Ring
        pen = QPen(glow, 3)
        painter.setPen(pen)
        painter.drawEllipse(int(cx-radius), int(cy-radius), int(size), int(size))

        # Mid Segmented Ring (rotating)
        painter.setPen(QPen(glow, 4))
        for i in range(20):
            angle = (self.angle1 + i*18) * 16
            painter.drawArc(int(cx-radius*0.8), int(cy-radius*0.8),
                            int(size*0.8), int(size*0.8),
                            angle, 10*16)

        # Inner Faint Ring
        painter.setPen(QPen(faint, 2))
        painter.drawEllipse(int(cx-radius*0.6), int(cy-radius*0.6),
                            int(size*0.6), int(size*0.6))

        # Tiny Rotating Dashes
        painter.setPen(QPen(glow, 3))
        for i in range(30):
            angle = math.radians(self.angle2 + i*12)
            x1 = cx + radius*0.45 * math.cos(angle)
            y1 = cy + radius*0.45 * math.sin(angle)
            x2 = cx + radius*0.5 * math.cos(angle)
            y2 = cy + radius*0.5 * math.sin(angle)
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        # Central Small Ring
        painter.setPen(QPen(glow, 3))
        painter.drawEllipse(int(cx-radius*0.3), int(cy-radius*0.3),
                            int(size*0.3), int(size*0.3))




# ---------------- JARVIS GUI ----------------
class JarvisGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis AI")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #0f0f0f; color: #00ffcc;")

        # Layout
        layout = QVBoxLayout()

        # Console area
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 12))
        self.console.setStyleSheet("""
    background-color: rgba(0, 0, 0, 150);  /* semi-transparent black */
    color: #00ffcc;                        /* neon green/teal text */
    border-radius: 10px;
""")

        layout.addWidget(self.console)

        # Speak button
        self.listen_button = QPushButton("🎙 Speak")
        self.listen_button.setFont(QFont("Consolas", 14))
        self.listen_button.setStyleSheet("""
    QPushButton {
        background-color: #1c1c1c;
        color: #00ffcc;
        border-radius: 10px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #00ffcc;
        color: #1c1c1c;
        border: 1px solid #00ffcc;
        box-shadow: 0 0 15px #00ffcc;
    }
""")

        # Run listen_command in a thread to avoid freezing GUI
        self.listen_button.clicked.connect(lambda: threading.Thread(target=self.listen_command).start())
        layout.addWidget(self.listen_button)

        self.setLayout(layout)

        # Add HUD animation behind everything
        self.hud = JarvisHUD(self)
        self.hud.setGeometry(0, 0, self.width(), self.height())
        self.hud.show()
        self.hud.lower()
        # keeps it on top of console/buttons
        # keep it behind console & button
        self.hud.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.hud.setStyleSheet("background: transparent;")
        self.hud.raise_()  # keep it on top


        # Initial message
        self.type_text("Jarvis: System online. How can I assist you?")
        threading.Thread(target=lambda: speak("System online. How can I assist you?")).start()
    def type_text(self, text):
        self.console.clear()              # Clear current console
        self.text_to_show = text          # Store the full text
        self.current_index = 0            # Start at the first character
        self.timer = QTimer()             # Create a timer
        self.timer.timeout.connect(self._update_text)  # call _update_text each tick
        self.timer.start(50)              # 50ms per character (adjust speed)
    
    def _update_text(self):
         if self.current_index < len(self.text_to_show):
            self.console.insertPlainText(self.text_to_show[self.current_index])
            self.current_index += 1
         else:
             self.timer.stop()    
    # ---------------- HUD RESIZE ----------------
    def _resize_hud(self, event):
        self.hud.setGeometry(0, 0, self.width(), self.height())
        QWidget.resizeEvent(self, event)

    # ---------------- LISTEN COMMAND ----------------
    def listen_command(self):
        threading.Thread(target=self._process_command).start()
    def resizeEvent(self, event):
    # Make the HUD fill the whole window
        self.hud.setGeometry(0, 0, self.width(), self.height())
    
    # Call the default PyQt resize behavior (very important)
        super().resizeEvent(event)

    

    def _process_command(self):
        self.console.append("Listening...")

        # Step 1: get voice input
        command = listen()
        if not command:
            return
        self.console.append(f"User: {command}")

        # Step 2: local commands
        if execute_local_commands(command):
            return

       # Step 3: memory commands
        if "remember my name is" in command:
            name = command.replace("remember my name is", "").strip()
            remember("name", name)
            self.type_text(f"Jarvis: Okay, I will remember your name is {name}.")
            threading.Thread(target=lambda: speak(f"Okay, I will remember your name is {name}")).start()
            return

        if "what is my name" in command:
            name = recall("name")
            if name:
                self.type_text(f"Jarvis: Your name is {name}.")
                threading.Thread(target=lambda: speak(f"Your name is {name}")).start()
            else:
                self.type_text("Jarvis: I don't know your name yet.")
                threading.Thread(target=lambda: speak("I don't know your name yet.")).start()
            return
        

        # Step 4: fallback to GPT
        self.type_text("Jarvis is thinking...")
        response = ask_gpt(command)
        for frame in ["|", "/", "-", "\\"]:
            self.type_text(f"Thinking {frame}")
            time.sleep(0.1)
        self.type_text(f"Jarvis: {response}")
        threading.Thread(target=lambda: speak(response)).start()


# ---------------- RUN ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JarvisGUI()
    window.show()
    sys.exit(app.exec())
