import unittest
from unittest import TestCase
from datetime import date
from unittest.mock import Mock

from lib.calendar_generator import CalendarGenerator


class TestCalendarGenerator(TestCase):
    def test_has_start_and_end_dates(self):
        # arrange
        start = date(2020, 1, 1)
        end = date(2020, 12, 31)
        calendar = CalendarGenerator(start=start, end=end, connection=None)
        # act/assert start date
        calendar_start = calendar.get_start_date()
        self.assertEqual(start, calendar_start)
        # act/assert end date
        calendar_end = calendar.get_end_date()
        self.assertEqual(end, calendar_end)

    def test_setup_table(self):
        # arrange
        mock_connection = Mock()
        mock_connection.execute = Mock(return_value=None)
        calendar = CalendarGenerator(
            start=date(2020, 1, 1),
            end=date(2020, 12, 31),
            connection=mock_connection)
        # act
        calendar.setup_table()
        # assert
        mock_connection.execute.assert_called()

    def test_populate_defaults(self):
        # arrange
        start = date(2020, 1, 1)
        end = date(2020, 12, 31)
        days = (end-start).days - 1
        mock_connection = Mock()
        mock_connection.execute = Mock(return_value=None)
        calendar = CalendarGenerator(
            start=date(2020, 1, 1),
            end=date(2020, 12, 31),
            connection=mock_connection)
        # act
        calendar.populate_defaults()
        # assert
        self.assertEquals(mock_connection.execute.call_count, days)

    def test_populate_holidays(self):
        # arrange
        start = date(2020, 1, 1)
        end = date(2020, 12, 31)

        mock_connection = Mock()
        mock_connection.execute = Mock(return_value=None)
        calendar = CalendarGenerator(start=start, end=end, connection=mock_connection)
        # act
        calendar.populate_holidays()
        # assert
        self.assertEquals(mock_connection.execute.call_count, 14)


if __name__ == '__main__':
    unittest.main()
