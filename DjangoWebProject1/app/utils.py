from datetime import datetime, date
import calendar

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def rangedate(self):
    """ return first and last day of the current month if nothing is selected """
    currentyear = date.today().year
    currentmonth = date.today().month
    if 'startdate' in self.request.GET and self.request.GET['startdate']:
        startdate = self.request.GET['startdate']
    else:
        startdate = date(currentyear, currentmonth, 1)
    if 'enddate' in self.request.GET and self.request.GET['enddate']:
        enddate = self.request.GET['enddate']
    else:
        enddate = date(currentyear, currentmonth, calendar.monthrange(currentyear,currentmonth)[1])
    return (startdate, enddate)

def firstDayCurrentmonth():
    currentyear = date.today().year
    currentmonth = date.today().month
    return date(currentyear, currentmonth, 1)

def lastDayCurrentmonth():
    currentyear = date.today().year
    currentmonth = date.today().month
    return date(currentyear, currentmonth, calendar.monthrange(currentyear,currentmonth)[1])