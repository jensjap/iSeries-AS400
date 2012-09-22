import csv, calendar, sys

# add lib folder to sys.path list so modules can be imported from that directory
sys.path.append('lib/')

from consolidateDaysOpenList import consolidateDaysOpenList
from getHolidays             import getHolidays

class BuildDaysOpenData:
    """ class will build a data object. Object will have the following
attributes:

- Dictionary of OfficeNbr:[list of days the office is open]
- Dictionary of OfficeNbr:'OfficeCode'
- Dictionary of 'OfficeCode':OfficeNbr
- List of Holidays for the given month

"""

    def __init__(self,
                 i_month,
                 i_day,
                 i_year,
                 s_holidays,
                 b_debug=False,
                 b_useCustList=True,
                 **kwargs):

        self.s_holidays = s_holidays

        self.i_failCount = 0

        self.b_debug       = b_debug
        self.b_useCustList = b_useCustList

        self.i_day   = int(i_day)
        self.i_month = int(i_month)
        self.i_year  = int(i_year)

        self.d_kwargs          = kwargs
        self.d_officeNbrToCode = {}
        self.d_officeCodeToNbr = {}
        
        self.buildDataArray()

    def buildDataArray(self):
        """

        """

        self.d_daysOpenOrth  = {}
        self.d_daysOpenGen   = {}
        self.d_daysOpenCust  = {}
        self.d_daysClosedGen = {}
        self.d_daysOpenAll   = {}

        self.a_errors = []

        self.a_holidays, self.a_errorsHolidays = getHolidays(self.i_month,
                                                             self.i_year,
                                                             self.s_holidays)

        self.a_errors = self.a_errors + self.a_errorsHolidays

        # build ortho days
        try:
            with open (self.d_kwargs['s_orthdt']) as f:
                rawReader = csv.reader(f, delimiter=',')
                for i in rawReader:
                    try:
                        i_officeNbr  = int ( i[0][0:3] )
                        s_officeCode = str ( i[0][3:6] )
                        __i_month    = int ( i[1][0:2] )
                        __i_day      = int ( i[1][3:5] )
                        __i_year     = int ( i[1][6:10] )
                        self.d_officeNbrToCode[i_officeNbr]  = s_officeCode
                        self.d_officeCodeToNbr[s_officeCode] = i_officeNbr
                        if __i_year == self.i_year:
                            if __i_month == self.i_month:
                                if i_officeNbr in self.d_daysOpenOrth:
                                    self.d_daysOpenOrth[i_officeNbr].append(__i_day)
                                else:
                                    self.d_daysOpenOrth[i_officeNbr] = [__i_day]
                    except ValueError as e:
                        self.a_errors.append(e)
        except IOError as e:
            self.a_errors.append(e)
            input('ERROR: ' + str(e) + '. Press <enter> to continue')

        # build general office closures
        try:
            with open (self.d_kwargs['s_gendt']) as f:
                rawReader = csv.reader(f, delimiter=',')
                for i in rawReader:
                    try:
                        i_officeNbr  = int ( i[0][0:3] )
                        s_officeCode = str ( i[0][3:6] )
                        a_dayClosed  = i[1:]
                        self.d_officeNbrToCode[i_officeNbr]  = s_officeCode
                        self.d_officeCodeToNbr[s_officeCode] = i_officeNbr
                        if i_officeNbr in self.d_daysClosedGen:
                            msg = 'WARNING: Duplicate entry for office %s found in gendt.csv.\
 There should be only one row for every office' % (i_officeNbr)
                            self.a_errors.append(msg)
                        else:
                            try:
                                self.d_daysClosedGen[i_officeNbr] = []
                                for j in a_dayClosed:
                                    self.d_daysClosedGen[i_officeNbr].append( int (j) )
                            except ValueError as e:
                                self.a_errors.append(e)
                    except ValueError as e:
                        self.a_errors.append(e)
        except IOError as e:
            self.a_errors.append(e)
            input('ERROR: ' + str(e) + '. Press <enter> to continue')

        # build general days
        for i in self.d_daysClosedGen:
            self.d_daysOpenGen[i] = []
            for day in range( 1, calendar.monthrange(self.i_year, self.i_month)[1] + 1 ):
                if not calendar.weekday(self.i_year, self.i_month, day) in self.d_daysClosedGen[i]:
                    if not calendar.weekday(self.i_year, self.i_month, day) == 6:
                        if not day in self.a_holidays:
                            self.d_daysOpenGen[i].append(day)

        # build custom days
        try:
            with open (self.d_kwargs['s_custdt']) as f:
                rawReader = csv.reader(f, delimiter=',')
                for i in rawReader:
                    try:
                        i_officeNbr  = int ( i[0][0:3] )
                        s_officeCode = str ( i[0][3:6] )
                        __i_month    = int ( i[1][0:2] )
                        __i_day      = int ( i[1][3:5] )
                        __i_year     = int ( i[1][6:10] )
                        self.d_officeNbrToCode[i_officeNbr]  = s_officeCode
                        self.d_officeCodeToNbr[s_officeCode] = i_officeNbr
                        if __i_year == self.i_year:
                            if __i_month == self.i_month:
                                if i_officeNbr in self.d_daysOpenCust:
                                    self.d_daysOpenCust[i_officeNbr].append(__i_day)
                                else:
                                    self.d_daysOpenCust[i_officeNbr] = [__i_day]
                    except ValueError as e:
                        self.a_errors.append(e)
        except IOError as e:
            self.a_errors.append(e)
            input('ERROR: ' + str(e) + '. Press <enter> to continue')

        # if custom list is to be excluded, then empty the custom dictionary before consolidating
        if not self.b_useCustList:
            self.d_daysOpenCust = {}
        self.d_daysOpenAll = consolidateDaysOpenList(self.d_daysOpenOrth,
                                                     self.d_daysOpenGen,
                                                     self.d_daysOpenCust)

    def changeDate(self, month, day, year):
        '''

'''
        self.i_day   = int(day)
        self.i_month = int(month)
        self.i_year  = int(year)

        self.buildDataArray()
