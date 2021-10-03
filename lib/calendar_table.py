import atexit
from datetime import date
from sqlite3 import Connection, Row

from lib.calendar_date import CalendarDate


class CalendarTable:
    def __init__(self, connection: Connection):
        atexit.register(self.close)
        connection.row_factory = Row
        self.cursor = connection.cursor()

    def get(self, day: date) -> CalendarDate:
        select_statement = """
            SELECT  dt, 
                    year, 
                    month, 
                    day, 
                    dayInWeek, 
                    monthName, 
                    dayName, 
                    weekNumber, 
                    isWeekDay, 
                    isHoliday,
                    holidayName
            FROM calendar 
            WHERE dt = '{dt}'
        """.format(dt=day)
        result = self.cursor.execute(select_statement).fetchone()
        return CalendarDate.parse(result)

    def close(self):
        with self.cursor:
            self.cursor.close()

