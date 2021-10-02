from datetime import date, timedelta
from dateutil.easter import easter

weekday_names = ["monday", "tuesday", "wednesday",
                 "thursday", "friday", "saturday", "sunday"]
month_names = ["january", "february", "march", "april", "may", "june",
               "july", "august", "september", "october", "november", "december"]


class CalendarGenerator:
    def __init__(self, start: date, end: date, connection):
        self.start = start
        self.end = end
        self.connection = connection

    def get_start_date(self):
        return self.start

    def get_end_date(self):
        return self.end

    def setup_table(self):
        create_statement = """
        CREATE TABLE calendar (
            dt DATE NOT NULL PRIMARY KEY,
            year SMALLINT NULL,
            month tinyint NULL,
            day tinyint NULL,
            dayInWeek tinyint NULL,
            monthName VARCHAR(9) NULL,
            dayName VARCHAR(9) NULL,
            weekNumber tinyint NULL,
            isWeekday BINARY(1) NULL,
            isHoliday BINARY(1) NULL,
            holidayDesc VARCHAR(32) NULL
        )"""
        self.connection.execute(create_statement)

    def populate_defaults(self):
        days = (self.end - self.start).days - 1
        for i in range(days):
            dt = self.start + timedelta(days=i)
            insert_statement = """
                INSERT INTO calendar (
                    dt, 
                    year, 
                    month, 
                    day, 
                    dayInWeek, 
                    monthName, 
                    dayName, 
                    weekNumber, 
                    isWeekDay, 
                    isHoliday
                ) VALUES (
                   '{dt}', {year}, {month}, {day}, {dayInWeek}, '{monthName}', '{dayName}', {weekNumber}, {isWeekDay}, {isHoliday}
                )
            """.format(
                dt=dt,
                year=dt.year,
                month=dt.month,
                day=dt.day,
                dayInWeek=dt.isoweekday(),
                monthName=month_names[dt.month - 1],
                dayName=weekday_names[dt.isoweekday() - 1],
                weekNumber=dt.isocalendar()[1],
                isWeekDay=(1 if dt.isoweekday() < 6 else 0),
                isHoliday=0
            )
            self.connection.execute(insert_statement)

    def populate_holidays(self):
        years = int((self.end - self.start).days / 365)

        for i in range(years):
            d = self.start + timedelta(days=(i * 365))

            # Easter related holidays
            easter_sunday = easter(d.year)
            ash_wednesday = easter_sunday - timedelta(days=46)
            palm_sunday = easter_sunday - timedelta(weeks=1)
            maundy_thursday = easter_sunday - timedelta(days=3)
            good_friday = easter_sunday - timedelta(days=2)
            holy_saturday = easter_sunday - timedelta(days=1)
            easter_monday = easter_sunday + timedelta(days=1)
            ascension_day = easter_sunday + timedelta(days=39)
            pentecoast_sunday = easter_sunday + timedelta(days=49)
            whit_monday = easter_sunday + timedelta(days=50)

            self.update_holiday_date(ash_wednesday, "ash wednesday")
            self.update_holiday_date(palm_sunday, "palm sunday")
            self.update_holiday_date(maundy_thursday, "maundy thursday")
            self.update_holiday_date(good_friday, "good friday")
            self.update_holiday_date(holy_saturday, "easter saturday")
            self.update_holiday_date(easter_sunday, "easter sunday")
            self.update_holiday_date(easter_monday, "easter monday")
            self.update_holiday_date(ascension_day, "ascension day")
            self.update_holiday_date(pentecoast_sunday, "pentecost sunday")
            self.update_holiday_date(whit_monday, "pentecost monday")


            # Christmas holidays
            christmas_eve = date(d.year, 12, 24)
            christmas_day = date(d.year, 12, 25)
            boxing_day = date(d.year, 12, 26)

            self.update_holiday_date(christmas_eve, "christmas eve")
            self.update_holiday_date(christmas_day, "christmas day")
            self.update_holiday_date(boxing_day, "christmas 2. day")

    def update_holiday_date(self, dt: date, name: str):
        update_statement = '''
            UPDATE 'calendar' 
            SET     isHoliday = 1, 
                    holidayName = '{name}'
            WHERE   dt = '{date}'
        '''.format(
            date=str(dt),
            name=name
        )
        self.connection.execute(update_statement)
