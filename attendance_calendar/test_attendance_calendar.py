import unittest
import json
import os
from datetime import datetime
from PySide6.QtCore import QDate
from PySide6.QtWidgets import QApplication
import sys
import date_attendance_main
from date_attendance_main import AttendanceCalendar

class TestAttendanceCalendar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create the QApplication instance"""
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication(sys.argv)
    def setUp(self):
        """Set up test environment before each test"""
        self.test_json = "test_attendance.json"
        # Save original json file path
        self.original_json = date_attendance_main.CLASS_JSON_FILE
        date_attendance_main.CLASS_JSON_FILE = self.test_json
        # Create a test json with a start_date to avoid interactive dialogs
        from datetime import datetime
        with open(self.test_json, "w", encoding="utf-8") as f:
            json.dump({"start_date": datetime.now().strftime("%Y-%m-%d")}, f)
        self.calendar = AttendanceCalendar()

    def tearDown(self):
        """Clean up after each test"""
        # Restore original json file path
        date_attendance_main.CLASS_JSON_FILE = self.original_json
        # Remove test json file if it exists
        if os.path.exists(self.test_json):
            os.remove(self.test_json)

    def test_initial_load_empty(self):
        """Test that a new calendar starts empty"""
        # With the new StartDateDialog behavior we expect a start_date to be set
        self.assertIn("start_date", self.calendar.attendance)

    def test_save_and_load_data(self):
        """Test saving and loading attendance data"""
        # Set a test date
        test_date = "2025-11-05"
        test_status = "Karlsruhe"
        
        # Save data
        self.calendar.attendance[test_date] = test_status
        self.calendar.save_data()

        # Create new calendar instance to load data
        new_calendar = AttendanceCalendar()
        self.assertEqual(new_calendar.attendance.get(test_date), test_status)

    def test_set_status_for_date(self):
        """Test setting status for a specific date"""
        # Create a valid date
        test_date = QDate(2025, 11, 5)
        self.calendar.calendar.setSelectedDate(test_date)
        self.calendar.combo.setCurrentText("Homeoffice")
        
        # Set status
        self.calendar.set_status_for_selected_date()
        
        # Check if status was saved
        date_str = test_date.toString("yyyy-MM-dd")
        self.assertEqual(self.calendar.attendance.get(date_str), "Homeoffice")

    def test_status_colors(self):
        """Test that all status options have corresponding colors"""
        for status in AttendanceCalendar.STATUS_OPTIONS:
            self.assertIn(status, AttendanceCalendar.STATUS_COLORS)

    def test_monthly_statistics(self):
        """Test monthly statistics calculation"""
        # Set up some test data for the current month
        now = datetime.now()
        current_month = f"{now.year}-{now.month:02d}"
        
        # Add some test entries
        test_data = {
            f"{current_month}-01": "Karlsruhe",
            f"{current_month}-02": "Homeoffice",
            f"{current_month}-03": "Karlsruhe"
        }
        # Ensure start_date is set and earlier than the test entries
        self.calendar.attendance = {"start_date": f"{now.year}-{now.month:02d}-01", **test_data}
        
        # Update statistics
        self.calendar.update_stats_label()
        
        # Check if stats label contains the expected percentages
        stats_text = self.calendar.stats_label.text()
        self.assertIn("Karlsruhe: 67%", stats_text)
        self.assertIn("Homeoffice: 33%", stats_text)

if __name__ == '__main__':
    unittest.main()