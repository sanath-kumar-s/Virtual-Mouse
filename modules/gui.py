from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QApplication)
from PySide6.QtCore import Qt, QTimer, Signal, Slot, QPoint
from PySide6.QtGui import QFont, QColor, QPalette, QImage, QPixmap
import numpy as np
import cv2

class StatusDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hand Gesture Controller - Dashboard")
        self.setFixedSize(400, 500)
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        self.title_label = QLabel("SYSTEM STATUS")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Status Cards
        self.gesture_card = self.create_status_card("Current Gesture", "NONE")
        self.state_card = self.create_status_card("System State", "IDLE")
        
        layout.addWidget(self.gesture_card['frame'])
        layout.addWidget(self.state_card['frame'])

        # Stats Grid
        stats_layout = QHBoxLayout()
        self.fps_label = self.create_stat_label("FPS", "0")
        self.latency_label = self.create_stat_label("Latency", "0ms")
        
        stats_layout.addWidget(self.fps_label['frame'])
        stats_layout.addWidget(self.latency_label['frame'])
        layout.addLayout(stats_layout)

        # Info Section
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_layout = QVBoxLayout(info_frame)
        
        instructions = [
            "• Index Tip: Mouse Move",
            "• Pinch: Click/Drag",
            "• Two Fingers Up: Scrolling",
            "• Palm Center: Movement Focus"
        ]
        
        for text in instructions:
            lbl = QLabel(text)
            lbl.setObjectName("infoLabel")
            info_layout.addWidget(lbl)
            
        layout.addWidget(info_frame)
        layout.addStretch()

    def create_status_card(self, title, value):
        frame = QFrame()
        frame.setObjectName("statusCard")
        layout = QVBoxLayout(frame)
        
        title_lbl = QLabel(title.upper())
        title_lbl.setObjectName("cardTitle")
        
        val_lbl = QLabel(value)
        val_lbl.setObjectName("cardValue")
        val_lbl.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title_lbl)
        layout.addWidget(val_lbl)
        
        return {'frame': frame, 'value': val_lbl}

    def create_stat_label(self, title, value):
        frame = QFrame()
        frame.setObjectName("statCard")
        layout = QVBoxLayout(frame)
        
        title_lbl = QLabel(title)
        title_lbl.setObjectName("statTitle")
        
        val_lbl = QLabel(value)
        val_lbl.setObjectName("statValue")
        val_lbl.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title_lbl)
        layout.addWidget(val_lbl)
        
        return {'frame': frame, 'value': val_lbl}

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0F172A;
            }
            #title_label {
                color: #38BDF8;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QLabel {
                color: #F8FAFC;
                font-family: 'Segoe UI', sans-serif;
            }
            #statusCard {
                background-color: #1E293B;
                border-radius: 15px;
                border: 1px solid #334155;
            }
            #cardTitle {
                color: #94A3B8;
                font-size: 12px;
                font-weight: bold;
            }
            #cardValue {
                color: #38BDF8;
                font-size: 32px;
                font-weight: bold;
                padding: 10px;
            }
            #statCard {
                background-color: #1E293B;
                border-radius: 12px;
                border: 1px solid #334155;
            }
            #statTitle {
                color: #94A3B8;
                font-size: 11px;
            }
            #statValue {
                color: #F8FAFC;
                font-size: 18px;
                font-weight: bold;
            }
            #infoFrame {
                background-color: rgba(56, 189, 248, 0.1);
                border-radius: 10px;
                padding: 10px;
            }
            #infoLabel {
                color: #BAE6FD;
                font-size: 13px;
            }
        """)

    @Slot(str, str, int, float)
    def update_status(self, gesture, state, fps, latency):
        self.gesture_card['value'].setText(gesture)
        self.state_card['value'].setText(state)
        self.fps_label['value'].setText(str(int(fps)))
        self.latency_label['value'].setText(f"{int(latency)}ms")
        
        # Color state based on activity
        if state == "CLICKING" or state == "DRAGGING":
            self.state_card['value'].setStyleSheet("color: #F43F5E;") # Red
        elif state == "SCROLLING":
            self.state_card['value'].setStyleSheet("color: #D946EF;") # Purple
        elif state == "IDLE":
            self.state_card['value'].setStyleSheet("color: #94A3B8;") # Slate
        else:
            self.state_card['value'].setStyleSheet("color: #38BDF8;") # Blue

class RigWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hand Skeleton")
        self.setFixedSize(640, 480)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.img_label)
        self.setCentralWidget(self.central_widget)
        
        self.setStyleSheet("background-color: rgba(0, 0, 0, 180); border-radius: 20px;")
        
    @Slot(np.ndarray)
    def update_image(self, cv_img):
        try:
            h, w, ch = cv_img.shape
            bytes_per_line = ch * w
            # Use .copy() to ensure the image data is owned by QImage and not deleted by GC
            qt_img = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_BGR888).copy()
            self.img_label.setPixmap(QPixmap.fromImage(qt_img))
        except Exception as e:
            print(f"[GUI ERROR] Failed to update image: {e}")
    
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
