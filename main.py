import sys, os, datetime

# add lib folder to sys.path list so modules can be imported from that directory
sys.path.append('lib/')

from BuildDaysOpenData import BuildDaysOpenData
from GetOfficeInfo     import GetOfficeInfo
from updateOrthdt      import updateOrthdt
from getValidDay       import getValidDay
from getWorkDays       import getWorkDays
from DBiSeries         import DBiSeries
from writeLog          import writeLog
from Email             import *

o_report = Email()

a_errors = []

b_debug       = False
b_useCustList = True
b_isManual    = False

d_orthOffices  = {}
d_genOffices   = {}
d_custOffices  = {}
d_kwargs       = {}

s_log              = 'main.log'
s_holidays         = 'input/holidays.csv'
s_orthdtBKUP       = 'output/%s_orthdt.csv' % ( datetime.datetime.now().strftime("%Y-%m-%d") )
s_lotusNotesExport = '//someserver/somefolder/orthodt.csv'

s_cpname           = 'SERVERNAME'
s_dbname           = 'DBNAME'
s_uname            = 'USERNAME'
s_pwd              = 'PASSWORD'

# set d_kwargs dictionary. optionally exclude custdt.csv
d_kwargs['s_orthdt'] = 'input/orthdt.csv'
d_kwargs['s_gendt']  = 'input/gendt.csv'
d_kwargs['s_custdt'] = 'input/custdt.csv'

# check if program was called with any parameters
try:
    if sys.argv[1] == 'manual':
        b_isManual = True
        os.system('cls' if os.name=='nt' else 'clear')
        print ('\nATTENTION: If you need to add any offices to the \
.\input\custdt.csv file then do so now and save it before continuing\n')
        
        i_month, i_day, i_year = getValidDay()
        if i_month == 1:
            print ('ATTENTION: \n*** Remember to set holiday.csv for the new year! ***')
            input ('Quickly, there\'s still time. When you are done, hit <enter> to continue')
    elif sys.argv[1] == 'debug':
        b_isManual = True
        i_month, i_day, i_year = datetime.datetime.now().month, \
                                 datetime.datetime.now().day, \
                                 datetime.datetime.now().year
        b_debug = True
except:
    i_month, i_day, i_year = datetime.datetime.now().month, \
                             datetime.datetime.now().day, \
                             datetime.datetime.now().year

# update orthdt.csv and test file:
a_errorsUpdate = updateOrthdt(s_lotusNotesExport,
                                    d_kwargs['s_orthdt'],
                                    s_orthdtBKUP)

# build daysOpen data. this object has a changeDate() method
o_data = BuildDaysOpenData(i_month,
                           i_day,
                           i_year,
                           s_holidays,
                           b_debug,
                           b_useCustList,
                           **d_kwargs)

# build office objects
d_office = {}

for i in o_data.d_daysOpenAll:
    d_office[i] = GetOfficeInfo(i,
                                i_month,
                                i_day,
                                i_year,
                                b_debug,
                                o_data.d_daysOpenAll,
                                o_data.d_officeNbrToCode)

# get work days this month - total and MTD
a_workDays, a_workDaysMTD, s_weekDay = getWorkDays(i_month,
                                                   i_day, i_year,
                                                   s_holidays)

# update iSeries tables
with DBiSeries(s_cpname,
               s_dbname,
               s_uname,
               s_pwd) as iSeries:
    b_connected = iSeries.buildConnector()

    if b_connected:
        # if this is a manual run then give the option to zero out all offices
        if b_isManual:
            print ('''
If this is a new month, then you might want to reset the DB_TABLE table. \n\
This is in order to prevent custom days entries made last month from spilling \
over into the new month''')
            s_response = input ("Would you like to zero out all entries? \nEnter \
'Y' or 'Yes' to do so. Any other response including a blank entry \nwill \
result in leaving the tables as it is: ")
            if s_response.upper() in ['YES', 'Y']:
                iSeries.resetNORTHDT()
                print ('I am wiping the TABLE table clean...I\'m not touching \
the specialty days though')
                a_errors.append('TABLE was reset')
        
        iSeries.updateTABLE(i_month,
                             i_year,
                             len(a_workDays),
                             len(a_workDaysMTD),
                             s_weekDay)
        for office in sorted(d_office):
            iSeries.UPDATE(d_office[office].i_officeNbr,
                                  len( d_office[office].a_openDaysList ),
                                  d_office[office].i_openDaysCountMTD, b_isManual)

    a_errorsDB  = iSeries.getErrors()
    a_dbResults = iSeries.getDbResults()


# collect errors
a_errors = a_errorsUpdate + a_errors + o_data.a_errors + a_errorsDB

# print results for debugging
if b_debug:

    for key, value in sorted (o_data.d_daysOpenAll.items() ):
        print (key, value)

    print ('List of Holidays:', o_data.a_holidays)
    if a_errors:
        for i in a_errors:
            print ('Debugging:', i)
    if b_useCustList: print ('Custom list was used')
    else: print ('Use custom list was set to False')

    print (a_workDays)
    print (a_workDaysMTD)
    print (s_weekDay)
    print (a_dbResults)
    print (iSeries.i_sqlUpdateCount)

s_reportBody = 'Number of SQL updates: %s\n' % (iSeries.i_sqlUpdateCount)
s_reportBody = s_reportBody + \
               'List of holidays this month: %s\n' % (o_data.a_holidays)
for line in a_errors + a_dbResults:
    s_reportBody = s_reportBody + str(line) + '\n'

o_report.sendEmail( 'jjap@domain.com', s_reportBody )
