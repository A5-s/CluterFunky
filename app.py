import ctypes
import os
import shutil
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
from datetime import datetime

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

excluded_files = ['pagefile.sys', 'hiberfil.sys', 'DumpStack.log.tmp']

def log_movement(logfile_path, files_moved):
    with open(logfile_path, 'a') as log_file:
        timestamp = datetime.now().strftime("--(%m/%d/%y/%H:%M) ")
        log_file.write(timestamp + ', '.join(files_moved) + '\n')

def organize_files():
    source_dir = 'D:/'
    destination_dir = 'D:/Unorganized'

    log_folder = os.path.join(destination_dir, 'Logs')
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file_path = os.path.join(log_folder, 'Log.txt')

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    files_moved = []

    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)

        if os.path.isdir(item_path) or item in excluded_files or item.startswith('.') or item.startswith('$'):
            continue

        file_ext = os.path.splitext(item)[1][1:] or 'Unknown'
        subfolder_name = f"Unorganized ({file_ext}) files"
        subfolder = os.path.join(destination_dir, subfolder_name)

        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        dst_path = os.path.join(subfolder, item)
        try:
            shutil.move(item_path, dst_path)
            files_moved.append(item)
        except PermissionError:
            print(f"One or more files skipped, admin permissions were not granted: {item}")
        except Exception as e:
            print(f"Error moving {item}: {e}")

    if files_moved:
        log_movement(log_file_path, files_moved)

class FileOrganizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Organizer')
        self.setGeometry(500, 200, 400, 200)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()

        self.label = QLabel("Click the button to organize files")
        self.label.setFont(QFont('Arial', 12))
        self.label.setStyleSheet("margin-bottom: 20px;")
        layout.addWidget(self.label)

        self.organize_button = QPushButton('Organize Files')
        self.organize_button.setFont(QFont('Arial', 11))
        self.organize_button.setStyleSheet("background-color: #1f1f1f; color: white; padding: 10px 20px; border: none; border-radius: 5px;")
        self.organize_button.clicked.connect(self.organize_files)

        layout.addWidget(self.organize_button)
        self.setLayout(layout)

    def organize_files(self):
        organize_files()
        self.label.setText("Selected files were successfully organized.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec_())
