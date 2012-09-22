import csv

def getHolidays(i_month, i_year, s_holidays):

    a_holidays = []
    a_errors   = []

    try:
        with open(s_holidays, 'r') as s_holiday:
            o_holidays = csv.reader (s_holiday, delimiter=',')
            for i in o_holidays:
                try:
                    if int(i[0]) == i_year:
                        if int(i[1]) == i_month:
                            a_holidays.append(int( i[2]) )
                except ValueError as e:
                    a_errors.append(e)
    except IOError as e:
        a_errors.append(e)
    return a_holidays, a_errors
