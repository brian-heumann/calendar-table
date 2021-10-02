import argparse, os
import sqlite3
from datetime import date

from lib.calendar_generator import CalendarGenerator


def main(database, start, end):
    print("Removing any existing old database by the name", database)
    os.remove(database)
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    print("Start generating the calendar from", start, "till", end, "in file", database)
    calendar_generator = CalendarGenerator(start, end, cursor)
    calendar_generator.setup_table()
    print("Populating the default dates ...")
    calendar_generator.populate_defaults()
    print("Populating the holidays ...")
    calendar_generator.populate_holidays()
    connection.close()
    print("Done")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate a sqlite database with a calendar table")
    parser.add_argument('--database', required=True,  help='name for generated sqlite database file')
    parser.add_argument('--start', required=True,  help='start date of the calendar table')
    parser.add_argument('--end', required=True, help='end date of the calendar table')
    args = parser.parse_args()
    main(args.database, date.fromisoformat(args.start), date.fromisoformat(args.end))
