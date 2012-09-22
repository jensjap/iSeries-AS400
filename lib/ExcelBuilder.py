import calendar, os
import win32com.client as win32
from win32com.client import constants as c

class ExcelBuilder:
    ''' Class will build excel spreadsheet for operations to use. The spread-
sheet will have update information for all offices
'''

    def __init__(self, d_office, s_excelFile, i_month, i_day, i_year):
        print ('init')

        self.d_office    = d_office
        
        self.s_excelFile = str(s_excelFile)

        self.i_month = i_month
        self.i_day   = i_day
        self.i_year  = i_year

        self.a_errors = []
        
        self.xl = win32.gencache.EnsureDispatch('Excel.Application')
        self.xl.Visible = False
        self.xl.DisplayAlerts = False

    def __enter__(self):
        print ('enter')
        try:
            self.wb = self.xl.Workbooks.Open(self.s_excelFile)
            print ('update.xlsx found')
        except Exception:
            self.wb = self.xl.Workbooks.Add()
            print ('update.xlsx not found. Creating new one')
            
        self.buildWorkbook()

    def buildWorkbook(self):
        
        row = 3
        
        self.ws1 = self.wb.Worksheets(1)
        self.ws1.Name = calendar.month_name[self.i_month] + '-' + str(self.i_year)

        self.ws1.Cells(1,1).Value = 'Office Number'
        self.ws1.Cells(1,2).Value = 'Office Code'
        self.ws1.Cells(1,3).Value = 'daysOpen MTD'
        self.ws1.Cells(1,4).Value = 'daysOpen Total'
        self.ws1.Cells(1,5).Value = calendar.month_name[self.i_month] + '-' + str(self.i_year)
        
        for i in range(1, 32):
            self.ws1.Cells(1, 5+i).Value = str(i)

        for i in sorted(self.d_office):
            self.ws1.Cells(row, 1).Value = self.d_office[i].i_officeNbr
            self.ws1.Cells(row, 2).Value = self.d_office[i].s_officeCode
            self.ws1.Cells(row, 3).Value = self.d_office[i].i_openDaysCountMTD
            self.ws1.Cells(row, 4).Value = self.d_office[i].i_openDaysCount

            # clear row
            for j in range(1, 32):
                self.ws1.Cells(row, 5+j).Value = ''
                self.ws1.Cells(row, 5+j).Font.Color = -2 # this sets font to white
                self.ws1.Cells(row, 5+j).Font.Bold  = False

            # insert days open MTD
            for k in range(0, self.d_office[i].i_openDaysCountMTD):
                day = self.d_office[i].a_openDaysListMTD[k]
                self.ws1.Cells(row, 5+day).Value = day
                self.ws1.Cells(row, 5+day).Font.Color = -4165632#-11489280(green)
                self.ws1.Cells(row, 5+day).Font.Bold  = True

            # insert days closed MTD
            for l in range(0, self.d_office[i].i_remainingOpenDaysCountMTD):
                day = self.d_office[i].a_remainingOpenDaysListMTD[l]
                self.ws1.Cells(row, 5+day).Value = day
                self.ws1.Cells(row, 5+day).Font.Color = -16776961
                self.ws1.Cells(row, 5+day).Font.Bold  = True

            row += 1

        # format worksheet
        self.ws1.Cells(1,5).NumberFormat = "MMM-yyyy"
        
        self.ws1.Range("A:D").HorizontalAlignment = win32.constants.xlCenter
        
        self.ws1.Range("A:AJ").Borders(c.xlEdgeLeft).LineStyle = c.xlContinuous
        self.ws1.Range("A:AJ").Borders(c.xlEdgeLeft).ColorIndex = 0
        self.ws1.Range("A:AJ").Borders(c.xlEdgeLeft).TintAndShade = 0
        self.ws1.Range("A:AJ").Borders(c.xlEdgeLeft).Weight = c.xlThin

        self.ws1.Range("A:AJ").Borders(c.xlEdgeTop).LineStyle = c.xlContinuous
        self.ws1.Range("A:AJ").Borders(c.xlEdgeTop).ColorIndex = 0
        self.ws1.Range("A:AJ").Borders(c.xlEdgeTop).TintAndShade = 0
        self.ws1.Range("A:AJ").Borders(c.xlEdgeTop).Weight = c.xlThin

        self.ws1.Range("A:AJ").Borders(c.xlEdgeBottom).LineStyle = c.xlContinuous
        self.ws1.Range("A:AJ").Borders(c.xlEdgeBottom).ColorIndex = 0
        self.ws1.Range("A:AJ").Borders(c.xlEdgeBottom).TintAndShade = 0
        self.ws1.Range("A:AJ").Borders(c.xlEdgeBottom).Weight = c.xlThin

        self.ws1.Range("A:AJ").Borders(c.xlEdgeRight).LineStyle = c.xlContinuous
        self.ws1.Range("A:AJ").Borders(c.xlEdgeRight).ColorIndex = 0
        self.ws1.Range("A:AJ").Borders(c.xlEdgeRight).TintAndShade = 0
        self.ws1.Range("A:AJ").Borders(c.xlEdgeRight).Weight = c.xlThin

        self.ws1.Range("A:AJ").Borders(c.xlInsideVertical).LineStyle = c.xlContinuous
        self.ws1.Range("A:AJ").Borders(c.xlInsideVertical).ColorIndex = 0
        self.ws1.Range("A:AJ").Borders(c.xlInsideVertical).TintAndShade = 0
        self.ws1.Range("A:AJ").Borders(c.xlInsideVertical).Weight = c.xlThin

        self.ws1.Range("A:AJ").Borders(c.xlInsideHorizontal).LineStyle = c.xlContinuous
        self.ws1.Range("A:AJ").Borders(c.xlInsideHorizontal).ColorIndex = 0
        self.ws1.Range("A:AJ").Borders(c.xlInsideHorizontal).TintAndShade = 0
        self.ws1.Range("A:AJ").Borders(c.xlInsideHorizontal).Weight = c.xlThin
        
        self.ws1.Columns.AutoFit()

        self.wb.Close(True, self.s_excelFile)

        self.ws1 = None
        self.wb  = None
        self.xl.Quit()
        self.xl.Application.Quit()
        self.xl  = None

    def __exit__(self, type, value, traceback):
        print ('exit')

        # save workbook
##        self.wb.SaveAs(self.s_excelFile)

##        # clean up
##        # close Excel
##        self.xl.Quit()
##        self.xl.Visible = 0
##        self.xl = None
       
        print ('Excel book saved')


