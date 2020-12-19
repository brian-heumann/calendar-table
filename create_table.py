from datetime import date, datetime, timedelta 
import sqlite3

connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()

# Constants
weekday_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
month_names = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

def get_weekday(isoweekday: int) -> str:
    return weekday_names[isoweekday-1]

def get_monthname(month: int) -> str:
    return month_names[month -1]

def get_quarter(month: int)  -> int: 
    return int(month/3) + 1

def is_weekday(isoweekday: int) -> int :
    if isoweekday < 6 :
        return 1
    else:
        return 0

def get_week_number(dt:date) -> int:
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
        dt = str(d), 
        year = d.year, 
        month= d.month, 
        day = d.day, 
        dw = d.isoweekday(), 
        monthName = get_monthname(d.month), 
        dayName = get_weekday(d.isoweekday()),
        w = get_week_number(d),
        q=get_quarter(d.month),
        isWeekday=is_weekday(d.isoweekday()),
        isHoliday=0
    )
    print(sql_insert_statement)
    cursor.execute(sql_insert_statement)

connection.commit()


# Finally close the connection to the database
#
connection.close()