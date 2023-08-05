import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weekly Timetable")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Add timetable grid
        self.create_timetable()

        # Add event button
        self.add_event_btn = QPushButton("Add Event")
        self.add_event_btn.clicked.connect(self.add_event)  # Connect to your function to add events
        self.layout.addWidget(self.add_event_btn)

    def create_timetable(self):
        self.timetable = QTableWidget(7, 11)  # Assuming 7 days a week, 24 hours a day
        self.timetable.setHorizontalHeaderLabels(['9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00'])
        self.timetable.setVerticalHeaderLabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        
        self.timetable.cellDoubleClicked.connect(self.delete_event)
        self.layout.addWidget(self.timetable)

    def add_event(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Add Event")
        
        layout = QVBoxLayout()
        
        self.day_dropdown = QComboBox()
        self.day_dropdown.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        
        self.start_time_dropdown = QComboBox()
        self.start_time_dropdown.addItems(['9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00'])
        
        self.end_time_dropdown = QComboBox()
        self.end_time_dropdown.addItems(['9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00'])
        
        self.event_name_input = QLineEdit()
        
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.confirm_add_event)
        
        layout.addWidget(QLabel("Select Day:"))
        layout.addWidget(self.day_dropdown)
        layout.addWidget(QLabel("Start Time:"))
        layout.addWidget(self.start_time_dropdown)
        layout.addWidget(QLabel("End Time:"))
        layout.addWidget(self.end_time_dropdown)
        layout.addWidget(QLabel("Event Name:"))
        layout.addWidget(self.event_name_input)
        layout.addWidget(self.add_btn)
        
        self.dialog.setLayout(layout)
        self.dialog.exec_()


    def confirm_add_event(self):
        day = self.day_dropdown.currentIndex()
        start_time = self.start_time_dropdown.currentIndex()
        end_time = self.end_time_dropdown.currentIndex()
        event_name = self.event_name_input.text().strip()

        if not event_name:
            QMessageBox.warning(self, "Input Error", "Please enter a valid event name!")
            return

        if start_time >= end_time:
            QMessageBox.warning(self, "Input Error", "Start time should be before end time!")
            return

        for hour in range(start_time, end_time):
            self.timetable.setItem(day, hour, QTableWidgetItem(event_name))
            
        self.dialog.close()


    def delete_event(self, row, column):
        item = self.timetable.item(row, column)
        if item and item.text():
            reply = QMessageBox.question(self, 'Delete Event', f"Do you want to delete the event '{item.text()}'?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.timetable.takeItem(row, column)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open(".\styles.qss", "r") as f:
        app.setStyleSheet(f.read())

    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
