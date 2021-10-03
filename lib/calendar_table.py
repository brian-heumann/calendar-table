import atexit
from datetime import date
from sqlite3 import Connection, Cursor, Row


class CalendarDate:
    @classmethod
    def parse(cls, row):
        return CalendarDate(
            dt=date.fromisoformat(row['dt']),
            year=row['year'],
            month=row['month'],
            day=row['day'],
            day_in_week= row['dayInWeek'],
            month_name= row['monthName'],
            day_name=row['dayName'],
            week_number=row['weekNumber'],
            is_weekday=row['isWeekDay'],
            is_holiday=row['isHoliday'],
            holiday_name=row['holidayName']
        )

    def __init__(self,
                 dt: date,
                 year: int,
                 month: int,
                 day: int,
                 day_in_week: int,
                 month_name: str,
                 day_name: str,
                 week_number: int,
                 is_weekday: bool,
                 is_holiday: bool,
                 holiday_name: str
                 ):
        self.dt = dt
        self.year = year
        self.month = month
        self.day = day
        self.day_in_week = day_in_week
        self.month_name = month_name
        self.day_name = day_name
        self.week_number = week_number
        self.is_weekday = is_weekday
        self.is_holiday = is_holiday
        self.holiday_name = holiday_name


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
        self.cursor.close()
