import os
import unittest
from datetime import date
from unittest import TestCase
import sqlite3

from lib.calendar_generator import CalendarGenerator
from lib.calendar_table import CalendarTable


class TestCalendarTable(TestCase):
    _database_file_name = ':memory:'

    @classmethod
    def setUpClass(cls) -> None:
        start = date(2020, 1, 1)
        end = date(2050, 12, 31)
        cls._connection = sqlite3.connect(cls._database_file_name)
        cursor = cls._connection.cursor()

        calendar_generator = CalendarGenerator(start, end, cursor)
        calendar_generator.setup_table()
        calendar_generator.populate_defaults()
        calendar_generator.populate_holidays()

        cursor.close()
        cls._connection.commit()

    def setUp(self) -> None:
        self.calendar_table = CalendarTable(self._connection)

    def test_easter_holidays(self):
        # arrange
        easters = [
            date(2020, 4, 12),
            date(2021, 4, 4),
            date(2022, 4, 17),
            date(2023, 4, 9),
            date(2024, 3, 31),
            date(2025, 4, 20),
            date(2026, 4, 5),
            date(2027, 3, 28),
            date(2028, 4, 16),
            date(2029, 4, 1),
            date(2030, 4, 21),
        ]

        # act
        for easter in easters:
            calendar_date = self.calendar_table.get(easter)
            self.assertTrue(calendar_date.is_holiday)
            self.assertEqual(calendar_date.holiday_name, 'easter sunday')

    def test_maundy_thursday(self):
        # arrange
        maundy_thursdays = [
            date(2022, 4, 14)
        ]

        # act // assert
        for day in maundy_thursdays:
            calendar_date = self.calendar_table.get(day)
            self.assertTrue(calendar_date.is_holiday)
            self.assertEqual(calendar_date.holiday_name, 'maundy thursday')


    @classmethod
    def tearDownClass(cls) -> None:
        # clean up
       # cls._connection.close
        pass


if __name__ == '__main__':
    unittest.main()
