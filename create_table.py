from datetime import date, datetime, timedelta
from dateutil.easter import easter
import sqlite3

connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()

# Constants
#
weekday_names = ["monday", "tuesday", "wednesday",
                 "thursday", "friday", "saturday", "sunday"]
month_names = ["january", "february", "march", "april", "may", "june",
               "july", "august", "september", "october", "november", "december"]

# Helper functions
#


def get_weekday(isoweekday: int) -> str:
    return weekday_names[isoweekday-1]


def get_monthname(month: int) -> str:
    return month_names[month - 1]


def get_quarter(month: int) -> int:
    return int(month/3) + 1


def is_weekday(isoweekday: int) -> int:
    if isoweekday < 6:
        return 1
    else:
        return 0


def get_week_number(dt: date) -> int:
    return dt.isocalendar()[1]


# Populate the dt fields
#
start_date = date(2020, 12, 19)
end_date = date(2050, 12, 31)
day_num = (end_date - start_date).days + 1

for i in range(day_num):
    d = start_date + timedelta(days=i)

    sql_insert_statement = '''
        INSERT INTO calendar_table (dt, y, m, d, dw, monthName, dayName, w, q, isWeekday, isHoliday) VALUES ("{dt}", {year}, {month}, {day}, {dw}, "{monthName}", "{dayName}", {w}, {q}, {isWeekday}, {isHoliday} );
        '''.format(
        dt=str(d),
        year=d.year,
        month=d.month,
        day=d.day,
        dw=d.isoweekday(),
        monthName=get_monthname(d.month),
        dayName=get_weekday(d.isoweekday()),
        w=get_week_number(d),
        q=get_quarter(d.month),
        isWeekday=is_weekday(d.isoweekday()),
        isHoliday=0
    )
    # print(sql_insert_statement)
    # cursor.execute(sql_insert_statement)

# connection.commit()


def update_holiday_date(dt: datetime, name: str):
    sql_update_statement = '''
        UPDATE 'calendar_table' 
        SET     isHoliday = 1, 
                holidayName = '{holidayName}'
        WHERE   dt = {date}
    '''.format(
        date=str(dt),
        holidayName=name
    )
    print(sql_update_statement)
    res = cursor.execute(sql_update_statement)
    print(res.fetchone())


# Determine easter for each year in [start_date, end_date]
#
years_num = int((end_date - start_date).days/365)+1

for i in range(years_num):
    d = start_date + timedelta(days=(i*365))

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

    update_holiday_date(ash_wednesday, "ash wednesday")
    update_holiday_date(maundy_thursday, "maundy thursday")
    update_holiday_date(good_friday, "good friday")
    update_holiday_date(holy_saturday, "easter saturday")
    update_holiday_date(easter_sunday, "easter sunday")
    update_holiday_date(easter_monday, "easter monday")
    update_holiday_date(ascension_day, "ascencsion day")
    update_holiday_date(pentecoast_sunday, "pentecost sunday")
    update_holiday_date(whit_monday, "pentecost monday")

    # Christmas holidays
    christmas_eve = date(d.year, 12, 24)
    christmas_day = date(d.year, 12, 25)
    boxing_day = date(d.year, 12, 26)

    update_holiday_date(christmas_eve, "christmas eve")
    update_holiday_date(christmas_day, "christmas day")
    update_holiday_date(boxing_day, "christmas 2. day")

    # print("--------- {0} --------".format(str(d.year)))
    # print("Aschermittwoch: {0}".format(str(ash_wednesday)))
    # print("Palmsonntag:    {0}".format(str(palm_sunday)))
    # print("Gründonnerstag: {0}".format(str(maundy_thursday)))
    # print("Karfreitag:     {0}".format(str(good_friday)))
    # print("Ostersonntag:   {0}".format(str(easter_sunday)))
    # print("Ostermontag:    {0}".format(str(easter_monday)))
    # print("Himmelfahrt:    {0}".format(str(ascension_day)))
    # print("Pfingstsonntag:  {0}".format(str(pentecoast_sunday)))
    # print("Pfingstmontag:  {0}".format(str(whit_monday)))
    # print("Heiligabend:    {0}".format(str(christmas_eve)))
    # print("1. Weihnachtstag:{0}".format(str(christmas_day)))
    # print("2. Weihnachtstag:{0}".format(str(boxing_day)))


# Finally close the connection to the database
#
connection.commit()
connection.close()
