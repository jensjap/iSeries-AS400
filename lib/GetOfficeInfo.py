import calendar

class GetOfficeInfo:
    ''' class will build an office object. Object will have the following
attributes:

- Number of days the office is open
- Number of days the office is closed
- List of days the office is open
- List of days the office is closed
- 


'''

    def __init__(self,
                 i_officeNbr,
                 i_month,
                 i_day,
                 i_year,
                 b_debug,
                 d_daysOpenAll,
                 d_officeNbrToCode):

        self.i_officeNbr = int (i_officeNbr)
        self.__i_month   = int (i_month)
        self.__i_day     = int (i_day)
        self.__i_year    = int (i_year)

        self.__b_debug = b_debug

        self.__d_daysOpenAll     = d_daysOpenAll
        self.__d_officeNbrToCode = d_officeNbrToCode

        self.a_openDaysList      = []
        self.a_openDaysListMTD   = []
        self.a_closedDaysList    = []
        self.a_closedDaysListMTD = []

        self.i_openDaysCount               = 0
        self.i_closedDaysCount             = 0
        self.i_openDaysCountMTD            = 0
        self.i_closedDaysCountMTD          = 0
        self.i_remainingOpenDaysCountMTD   = 0
        self.i_remainingClosedDaysCountMTD = 0

        self.__getOpenDaysList()
        self.__getClosedDaysList()
        self.__getOpenDaysCount()
        self.__getClosedDaysCount()
        
        self.a_openDaysListMTD, self.i_openDaysCountMTD                       = self.__getDaysCount(self.a_openDaysList, self.__i_day)
        self.a_closedDaysListMTD, self.i_closedDaysCountMTD                   = self.__getDaysCount(self.a_closedDaysList, self.__i_day)
        self.a_remainingOpenDaysListMTD, self.i_remainingOpenDaysCountMTD     = self.__getRemainingDaysCount(self.a_openDaysList, self.__i_day)
        self.a_remainingClosedDaysListMTD, self.i_remainingClosedDaysCountMTD = self.__getRemainingDaysCount(self.a_closedDaysList, self.__i_day)
        
        self.__getOfficeCode()

    def changeDay(self, day):
        ''' Stay within the same month and year only '''
        try:
            self.__i_day = int (day)
        except ValueError as e:
            print (e)
            
        self.__getOpenDaysList()
        self.__getClosedDaysList()
        self.__getOpenDaysCount()
        self.__getClosedDaysCount()
        
        self.a_openDaysListMTD, self.i_openDaysCountMTD                       = self.__getDaysCount(self.a_openDaysList, self.__i_day)
        self.a_closedDaysListMTD, self.i_closedDaysCountMTD                   = self.__getDaysCount(self.a_closedDaysList, self.__i_day)
        self.a_remainingOpenDaysListMTD, self.i_remainingOpenDaysCountMTD     = self.__getRemainingDaysCount(self.a_openDaysList, self.__i_day)
        self.a_remainingClosedDaysListMTD, self.i_remainingClosedDaysCountMTD = self.__getRemainingDaysCount(self.a_closedDaysList, self.__i_day)

    def __getDaysCount(self, a_daysList, i_day):
        a_daysListMTD = [ day for day in a_daysList if int(day) <= int(i_day) ]
##        print (a_daysListMTD)
        return a_daysListMTD, len( a_daysListMTD )

    def __getRemainingDaysCount(self, a_daysList, i_day):
        a_remainingDaysListMTD = [ day for day in a_daysList if int(day) > int(i_day) ]
        return a_remainingDaysListMTD, len( a_remainingDaysListMTD )

    def __getOpenDaysList(self):
        self.a_openDaysList = self.__d_daysOpenAll[self.i_officeNbr]
        
    def __getClosedDaysList(self):
        for day in range ( 1, calendar.monthrange(self.__i_year, self.__i_month)[1] + 1 ):
            if not day in self.a_openDaysList:
                self.a_closedDaysList.append(day)

    def __getOfficeCode(self):
        self.s_officeCode = self.__d_officeNbrToCode[self.i_officeNbr]

    def __getOpenDaysCount(self):
        self.i_openDaysCount = len(self.a_openDaysList)

    def __getClosedDaysCount(self):
        self.i_closedDaysCount = len(self.a_closedDaysList)

    def getDay(self):
        return self.__i_day
