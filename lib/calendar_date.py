from datetime import date


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