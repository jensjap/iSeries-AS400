import calendar
from getHolidays import getHolidays

def getWorkDays(i_month, i_day, i_year, s_holidays):
    ''' calculate the number of work days in the month and MTD '''

    a_workDays    = []
    a_workDaysMTD = []

    a_holidays, a_errors = getHolidays(i_month, i_year, s_holidays)

    for day in range( 1, calendar.monthrange(i_year, i_month)[1] + 1 ):
        if not calendar.weekday(i_year, i_month, day) == 6:
            if not day in a_holidays:
                a_workDays.append(day)

    a_workDaysMTD = [ day for day in a_workDays if int(day) <= int(i_day) ]

    s_weekDay = calendar.day_name[calendar.weekday(i_year,
                                                   i_month,
                                                   a_workDaysMTD[-1])].upper()

    return a_workDays, a_workDaysMTD, s_weekDay
