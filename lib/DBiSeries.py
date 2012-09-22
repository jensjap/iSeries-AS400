import adodbapi as dbi
import sys

class DBiSeries:
    ''' build an iSeries database connection and update tables

'''

    def __init__(self, cpname, dbname, uname, pwd):
        ''' load instance variables '''
        
        print ('Building connector')
        self._computername = cpname
        self._databasename = dbname
        self._username     = uname
        self._password     = pwd

        self.a_errors    = []
        self.a_dbResults = []

        self.i_sqlUpdateCount = 0

    def __enter__(self):
        return self

    def buildConnector(self):
        ''' Build the DB connector and cursor '''

        # construct connection string
        constr = "Provider=IBMDA400; DATA SOURCE=%s;\
DEFAULT COLLECTION=%s; \
User ID=%s; Password=%s" % (self._computername,
                            self._databasename,
                            self._username,
                            self._password)

        # Open Database Connection
        try:
            self.db = dbi.connect(constr)
            self.c  = self.db.cursor()
            return True
        except Exception as e:
            msg = 'shit something terrible happened:'
            self.a_errors.append(msg + str(e))
            return False

    def resetNORTHDT(self):
        ''' this method completely reset the N.TABLE table.
All offices will have 0 days open out of 0 days in the month
'''
        s_sqlTableReset = """UPDATE DATABASE_NAME."N.TABLE" SET \
"CURR_OPEN_DAYS_R"=0, "TOTAL_OPEN_DAYS_R"=0"""
        self.c.execute(s_sqlTableReset)

    def updateSFLASH(self,
                     i_month,
                     i_year,
                     i_workDays,
                     i_workDaysMTD,
                     s_weekDay):
        ''' the DATABASE."TABLE" file stores information such as the month,
year, total work days this month, work days MTD, and week day by name
'''

        try:
            # build query to test that only 1 row returns
            s_testQuery = """SELECT * FROM DATABASE_NAME."S.TABLE" WHERE F00001 = \
'FA' AND K00001='999999'"""
            self.c.execute(s_testQuery)

            # if only 1 row returns then we execute the update
            if int(self.c.rowcount) == 1:
                qry = """UPDATE DATABASE_NAME."S.TABLE" SET F00002='   %s%s%s%s%s' \
WHERE F00001='FA' AND K00001='999999'""" % ( str.zfill(str(i_month), 2),
                                             str.zfill(str(i_year)[-2:], 2),
                                             str.zfill(str(i_workDays), 2),
                                             str.zfill(str(i_workDaysMTD), 2),
                                             s_weekDay )
                self.c.execute(qry)
                msg = qry + ". Affected row(s): " + str(self.c.rowcount)
                self.a_dbResults.append(msg)
                if not int(self.c.rowcount) == 1:
                    err = 'ERROR: DATABASE_NAME."S.TABLE" did not affect only 1 row. \
Affected row(s): ' + str(self.c.rowcount)
                    self.a_errors.append(err)
            else:
                msg = 'ERROR: Test query did not return 1 row. Update \
aborted. Query: ' + s_testQuery
                self.a_errors.append(msg)
        except Exception as e:
            msg = 'ERROR: Failure to update DATABASE_NAME."S.TABLE": ' + str(e)
            self.a_errors.append(msg)

    def updateNORTHDT(self, i_officeNbr, i_daysTotal, i_daysMTD, b_isManual):
        s_testQuery = 'SELECT * FROM DATABASE_NAME."N.TABLE" WHERE \
"OFFICE_NUMBER"=%s' % ( str.zfill(str(i_officeNbr), 3) )
        self.c.execute(s_testQuery)
        
        if int(self.c.rowcount) == 1:
            s_qry = """UPDATE DATABASE_NAME."N.TABLE" SET \
"CURR_OPEN_DAYS_R"=%s, "TOTAL_OPEN_DAYS_R"=%s WHERE \
"OFFICE_NUMBER"=%s""" % ( str.zfill(str(i_daysMTD), 2),
                          str.zfill(str(i_daysTotal), 2),
                          str.zfill(str(i_officeNbr), 3) )
            self.c.execute(s_qry)
            msg = s_qry + ". Affected row(s): " + str(self.c.rowcount)
            self.a_dbResults.append(msg)
            self.i_sqlUpdateCount += 1
            if not int(self.c.rowcount) == 1:
                err = 'ERROR: DATABASE_NAME."N.TABLE" did not affect only 1 row. \
Affected row(s): ' + str(self.c.rowcount)
                self.a_errors.append(err)
        elif int(self.c.rowcount) == 0:
            # if no office was found then call addOffice() method, provided this is a manual run
            if b_isManual:
                self.addOffice(i_officeNbr, i_daysMTD, i_daysTotal)
        else:
            msg = 'ERROR: Test query did not return 1 row. Update \
aborted. Affected row(s): %s. Query: %s' % (str(self.c.rowcount), s_testQuery)
            self.a_errors.append(msg)

    def addOffice(self, i_officeNbr, i_daysMTD, i_daysTotal):
        s_sql = """Insert into DATABASE_NAME."N.TABLE" \
(OFFICE_NUMBER, CURR_OPEN_DAYS_R, TOTAL_OPEN_DAYS_R, CURR_OPEN_DAYS_S, TOTAL_OPEN_DAYS_S, FILLER) \
VALUES(%s, %s, %s, 0, 0, ' ')""" % ( str.zfill(str(i_officeNbr), 3),
                                     str.zfill(str(i_daysMTD), 2),
                                     str.zfill(str(i_daysTotal), 2) )
        msg = '\n Office %s is missing.\nDo you wish to add the missing office with the \
following statement? SQL:\n%s' % (str(i_officeNbr), s_sql)
        print (msg)
        s_response = input ("Type 'yes' and press <enter> to execute the sql statement: ")
        if s_response.upper() == 'YES':
            self.c.execute(s_sql)
            if int(self.c.rowcount) == 1:
                msg = 'Office %s was successfully added with %s days \
open out of a total of %s days' % (str(i_officeNbr),
                                   str(i_daysMTD),
                                   str(i_daysTotal))
                self.i_sqlUpdateCount += 1
            else:
                msg = 'Failed to add the office'
            print (msg)
            self.a_dbResults.append(msg)
        else:
            msg = 'You chose not to add the office. Program is resuming...'
            print (msg)
            self.a_dbResults.append(msg)
            
    def getDbResults(self):
        return self.a_dbResults

    def getErrors(self):
        return self.a_errors

    def __exit__(self, type, value, traceback):
        try:
            self.db.close()
        except AttributeError as e:
            self.a_errors.append(e)
        finally:
            print ('closing db connector...i\'ve been exited...goodbye cruel world')
        try:
            self.db.close()
        except Exception as e:
            msg = 'db.close() was tested and returned positive with the \
following error message when trying to close a second time: ' + str(e)
            self.a_dbResults.append(msg)
