import sys
import os
import psutil
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget, QListWidget, QListWidgetItem, QSizePolicy,
    QStatusBar, QMessageBox, QFileDialog, QListView, QLineEdit, QCheckBox, QInputDialog
)
from PyQt6.QtGui import QFont, QColor, QPalette, QPainter, QBrush
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF

class PongGame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        self.paddle_w, self.paddle_h = 12, 80
        self.ball_size = 16
        self.reset_game()
        self.timer.start(16)

    def reset_game(self):
        self.width_, self.height_ = 600, 400
        self.paddle1_y = self.paddle2_y = (self.height_ - self.paddle_h) // 2
        self.ball_x = self.width_ // 2
        self.ball_y = self.height_ // 2
        self.ball_dx = 4
        self.ball_dy = 4
        self.score1 = 0
        self.score2 = 0
        self.setMinimumSize(self.width_, self.height_)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#101820"))
        # Draw paddles
        painter.setBrush(QBrush(QColor("#39FF14")))
        painter.drawRect(20, self.paddle1_y, self.paddle_w, self.paddle_h)
        painter.drawRect(self.width_ - 20 - self.paddle_w, self.paddle2_y, self.paddle_w, self.paddle_h)
        # Draw ball
        painter.drawEllipse(QRectF(self.ball_x, self.ball_y, self.ball_size, self.ball_size))
        # Draw score
        font = QFont("Consolas", 18, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(self.width_ // 2 - 40, 40, f"{self.score1}  |  {self.score2}")

    def game_loop(self):
        # Move ball
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        # Ball collision with top/bottom
        if self.ball_y <= 0 or self.ball_y + self.ball_size >= self.height_:
            self.ball_dy *= -1
        # Ball collision with paddles
        if (self.ball_x <= 32 and self.paddle1_y <= self.ball_y <= self.paddle1_y + self.paddle_h):
            self.ball_dx *= -1
        elif (self.ball_x + self.ball_size >= self.width_ - 32 and self.paddle2_y <= self.ball_y <= self.paddle2_y + self.paddle_h):
            self.ball_dx *= -1
        # Ball out of bounds
        if self.ball_x < 0:
            self.score2 += 1
            self.ball_x, self.ball_y = self.width_ // 2, self.height_ // 2
            self.ball_dx = abs(self.ball_dx)
        elif self.ball_x > self.width_:
            self.score1 += 1
            self.ball_x, self.ball_y = self.width_ // 2, self.height_ // 2
            self.ball_dx = -abs(self.ball_dx)
        # Simple AI for right paddle
        if self.ball_y > self.paddle2_y + self.paddle_h // 2:
            self.paddle2_y = min(self.height_ - self.paddle_h, self.paddle2_y + 4)
        elif self.ball_y < self.paddle2_y + self.paddle_h // 2:
            self.paddle2_y = max(0, self.paddle2_y - 4)
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_W:
            self.paddle1_y = max(0, self.paddle1_y - 16)
        elif event.key() == Qt.Key.Key_S:
            self.paddle1_y = min(self.height_ - self.paddle_h, self.paddle1_y + 16)
        elif event.key() == Qt.Key.Key_R:
            self.reset_game()
        self.update()

class TaskListPanel(QWidget):
    """
    A versatile, easy-to-use, and maintainable task list panel.
    Users can add, remove, and mark tasks as complete.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.title = QLabel("Task List / To-Do")
        self.title.setFont(QFont("Consolas", 18, QFont.Weight.Bold))
        self.title.setStyleSheet("color: #39FF14;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Add a new task and press Enter...")
        self.input_line.returnPressed.connect(self.add_task)
        self.layout.addWidget(self.input_line)

        self.task_list = QListWidget()
        self.task_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.layout.addWidget(self.task_list)

        btn_layout = QHBoxLayout()
        self.remove_btn = QPushButton("Remove Selected")
        self.remove_btn.clicked.connect(self.remove_task)
        self.complete_btn = QPushButton("Toggle Complete")
        self.complete_btn.clicked.connect(self.toggle_complete)
        btn_layout.addWidget(self.remove_btn)
        btn_layout.addWidget(self.complete_btn)
        self.layout.addLayout(btn_layout)

        self.setStyleSheet("""
            QLineEdit { color: #39FF14; background: #181c20; border: 1px solid #39FF14; }
            QListWidget { background: #181c20; color: #39FF14; }
            QPushButton { background: #101820; border: 1px solid #39FF14; color: #39FF14; }
            QPushButton:hover { background: #222; }
        """)

    def add_task(self):
        text = self.input_line.text().strip()
        if text:
            item = QListWidgetItem(text)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.task_list.addItem(item)
            self.input_line.clear()

    def remove_task(self):
        row = self.task_list.currentRow()
        if row >= 0:
            self.task_list.takeItem(row)

    def toggle_complete(self):
        item = self.task_list.currentItem()
        if item:
            if item.checkState() == Qt.CheckState.Checked:
                item.setCheckState(Qt.CheckState.Unchecked)
            else:
                item.setCheckState(Qt.CheckState.Checked)

class MinerScannerPanel(QWidget):
    """
    Scans running processes for common Bitcoin miner signatures.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.title = QLabel("Bitcoin Miner Scanner")
        self.title.setFont(QFont("Consolas", 18, QFont.Weight.Bold))
        self.title.setStyleSheet("color: #39FF14;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        self.result_label = QLabel("Press 'Scan Now' to check for suspicious miner activity.")
        self.result_label.setFont(QFont("Consolas", 12))
        self.result_label.setStyleSheet("color: #39FF14;")
        self.layout.addWidget(self.result_label)

        self.scan_btn = QPushButton("Scan Now")
        self.scan_btn.clicked.connect(self.scan_miners)
        self.layout.addWidget(self.scan_btn)

        self.details = QLabel("")
        self.details.setFont(QFont("Consolas", 10))
        self.details.setStyleSheet("color: #39FF14;")
        self.details.setWordWrap(True)
        self.layout.addWidget(self.details)
        self.layout.addStretch()

    def scan_miners(self):
        miner_keywords = [
            "xmrig", "cgminer", "cpuminer", "minerd", "nicehash", "ethminer", "bfgminer",
            "cryptonight", "miner", "bitcoin", "btc", "eth", "monero"
        ]
        found = []
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            try:
                pname = (proc.info['name'] or "").lower()
                pexe = (proc.info['exe'] or "").lower()
                pcmd = " ".join(proc.info['cmdline']).lower() if proc.info['cmdline'] else ""
                for kw in miner_keywords:
                    if kw in pname or kw in pexe or kw in pcmd:
                        found.append(f"PID {proc.info['pid']}: {proc.info['name']}")
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        if found:
            self.result_label.setText("⚠️ Potential miner processes detected!")
            self.details.setText("\n".join(found))
        else:
            self.result_label.setText("✅ No common Bitcoin miner processes found.")
            self.details.setText("")

class EchoTraceMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EchoTrace – Windows Security")
        self.setMinimumSize(1000, 650)
        self.setStyleSheet("""
            QMainWindow { background-color: #101820; }
            QLabel, QPushButton, QListWidget, QListWidgetItem {
                color: #39FF14;
                font-family: 'Consolas', 'Fira Mono', 'Cascadia Code', monospace;
            }
            QPushButton {
                background-color: #101820;
                border: 1px solid #39FF14;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #222;
            }
            QListWidget {
                background: #181c20;
                border: none;
            }
            QListWidget::item:selected {
                background: #39FF14;
                color: #101820;
            }
        """)
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        # Sidebar navigation
        self.nav_list = QListWidget()
        self.nav_list.setFixedWidth(220)
        self.nav_list.setSpacing(4)
        nav_items = [
            "Dashboard",
            "Account Discovery",
            "Saved Data Audit",
            "Malware Scanner",
            "Bitcoin Miner Scanner",
            "Autorun Viewer",
            "Snapshot System",
            "Change Tracker",
            "Live Alerts",
            "Export Report",
            "Pong Game",
            "Task List",
            "Settings",
            "Help/About"
        ]
        for item in nav_items:
            QListWidgetItem(item, self.nav_list)
        self.nav_list.setCurrentRow(0)
        self.nav_list.currentRowChanged.connect(self.switch_panel)
        self.nav_list.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.nav_list.setToolTip("Use Up/Down arrows to navigate. Enter to select.")

        # Main content area
        self.stack = QStackedWidget()
        self.stack.addWidget(self.dashboard_panel())
        self.stack.addWidget(self.placeholder_panel("Account Discovery"))
        self.stack.addWidget(self.placeholder_panel("Saved Data Audit"))
        self.stack.addWidget(self.placeholder_panel("Malware Scanner"))
        self.stack.addWidget(MinerScannerPanel())
        self.stack.addWidget(self.placeholder_panel("Autorun Viewer"))
        self.stack.addWidget(self.placeholder_panel("Snapshot System"))
        self.stack.addWidget(self.placeholder_panel("Change Tracker"))
        self.stack.addWidget(self.placeholder_panel("Live Alerts"))
        self.stack.addWidget(self.export_report_panel())
        self.stack.addWidget(PongGame())
        self.stack.addWidget(TaskListPanel())
        self.stack.addWidget(self.settings_panel())
        self.stack.addWidget(self.help_panel())

        main_layout.addWidget(self.nav_list)
        main_layout.addWidget(self.stack)
        self.setCentralWidget(main_widget)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Welcome to EchoTrace! Use the sidebar to navigate.")

        # Keyboard shortcuts
        self.shortcut_actions()

    def shortcut_actions(self):
        # Keyboard shortcuts for navigation
        self.nav_list.setFocus()
        self.nav_list.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.nav_list and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                self.switch_panel(self.nav_list.currentRow())
                return True
        return super().eventFilter(obj, event)

    def dashboard_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        # Cool EchoTrace logo
        logo = QLabel("EchoTrace")
        try:
            logo_font = QFont("Orbitron", 36, QFont.Weight.Bold)
            if not logo_font.exactMatch():
                raise Exception()
        except Exception:
            logo_font = QFont("Consolas", 36, QFont.Weight.Bold)
        logo.setFont(logo_font)
        logo.setStyleSheet("color: #39FF14; letter-spacing: 2px;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = QLabel("Modern Windows Security Dashboard")
        subtitle.setFont(QFont("Consolas", 16))
        subtitle.setStyleSheet("color: #39FF14;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)
        layout.addWidget(subtitle)
        layout.addSpacing(30)
        # Quick feature summary
        features = [
            "• Account Discovery",
            "• Saved Data Audit",
            "• Malware Scanner",
            "• Bitcoin Miner Scanner",
            "• Autorun Viewer",
            "• Snapshot System",
            "• Change Tracker",
            "• Live Alerts",
            "• Export Security Report",
            "• Play Pong Game!",
            "• Manage Task List!"
        ]
        for feat in features:
            lbl = QLabel(feat)
            lbl.setFont(QFont("Consolas", 14))
            lbl.setStyleSheet("color: #39FF14;")
            layout.addWidget(lbl)
        layout.addSpacing(20)
        # Export button
        export_btn = QPushButton("Export Security Report")
        export_btn.clicked.connect(self.export_report)
        layout.addWidget(export_btn)
        layout.addStretch()
        return panel

    def placeholder_panel(self, title):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        label = QLabel(f"{title}\n\n(Feature coming soon!)")
        label.setFont(QFont("Consolas", 18, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #39FF14;")
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        return panel

    def export_report_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        label = QLabel("Export Security Report")
        label.setFont(QFont("Consolas", 18, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #39FF14;")
        layout.addWidget(label)
        export_btn = QPushButton("Export Now")
        export_btn.clicked.connect(self.export_report)
        layout.addWidget(export_btn)
        layout.addStretch()
        return panel

    def export_report(self):
        # Placeholder: Export a dummy report
        fname, _ = QFileDialog.getSaveFileName(self, "Export Security Report", "echotrace_report.txt", "Text Files (*.txt)")
        if fname:
            with open(fname, "w") as f:
                f.write("EchoTrace Security Report\n========================\n\n")
                f.write("This is a placeholder report.\n")
            self.status.showMessage(f"Report exported to {fname}", 5000)
        else:
            self.status.showMessage("Export cancelled.", 3000)

    def settings_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        label = QLabel("Settings\n\n(Dark/Light theme, Accessibility, etc.)")
        label.setFont(QFont("Consolas", 16))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #39FF14;")
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        return panel

    def help_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        label = QLabel("EchoTrace Help & About")
        label.setFont(QFont("Consolas", 18, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #39FF14;")
        about = QLabel(
            "Created by Jonathan Ehlinger 2025\n"
            "A modern, lightweight, and interactive desktop app built with Python and PyQt6.\n"
            "Analyze, visualize, and manage your Windows 11 system’s security state — in real time.\n\n"
            "Navigate with keyboard or mouse. Try the Pong Game and Task List for fun!"
        )
        about.setFont(QFont("Consolas", 12))
        about.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about.setStyleSheet("color: #39FF14;")
        layout.addWidget(label)
        layout.addWidget(about)
        layout.addStretch()
        return panel

    def switch_panel(self, index):
        self.stack.setCurrentIndex(index)
        nav_name = self.nav_list.item(index).text()
        self.status.showMessage(f"Switched to: {nav_name}", 3000)
        # Show About dialog if Help/About selected
        if nav_name == "Help/About":
            QMessageBox.information(self, "About EchoTrace", 
                "EchoTrace\n\nCreated by Jonathan Ehlinger 2025\n\n"
                "A modern, lightweight, and interactive desktop app built with Python and PyQt6.\n"
                "Analyze, visualize, and manage your Windows 11 system’s security state — in real time.\n\n"
                "Enjoy the Pong Game and Task List in the sidebar!"
            )

def main():
    app = QApplication(sys.argv)
    # Remove or update the following line for PyQt6 6.9+ compatibility
    # app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    window = EchoTraceMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
