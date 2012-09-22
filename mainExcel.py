import sys, datetime, os, inspect

os.chdir( ( os.path.split(sys.argv[0])[0] ) )
print (os.getcwd())

# add lib folder to sys.path list so modules can be imported from that directory
sys.path.append('lib/')

from BuildDaysOpenData import BuildDaysOpenData
from GetOfficeInfo     import GetOfficeInfo
from updateOrthdt      import updateOrthdt
from ExcelBuilder      import ExcelBuilder
from getValidDay       import getValidDay
from Email             import Email

s_holidays             = 'input/holidays.csv'
s_orthdtBKUP           = 'output/%s_orthdt.csv' % ( datetime.datetime.now().strftime("%Y-%m-%d") )
s_lotusNotesExport     = '//someserver/somefolder/orthodt.csv'
s_update = 'output/update.htm'

# set d_kwargs dictionary. optionally exclude custdt.csv
d_kwargs             = {}
s_excelFile          = 'D:\\scripts\\development\\5-daysOpen\\output\\update.xlsx'
d_kwargs['s_orthdt'] = 'input/orthdt.csv'
d_kwargs['s_gendt']  = 'input/gendt.csv'
d_kwargs['s_custdt'] = 'input/custdt.csv'

b_useCustList = True
b_debug       = True

try:
    if sys.argv[1] == 'manual':
        i_month, i_day, i_year = getValidDay()
except IndexError:
    i_month, i_day, i_year = datetime.datetime.now().month, \
                             datetime.datetime.now().day, \
                             datetime.datetime.now().year

# update orthdt.csv and test file:
a_errorsUpdateOrthdt = updateOrthdt(s_lotusNotesExport,
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

with ExcelBuilder(d_office, s_excelFile, i_month, i_day, i_year) as xlBuilder:
    pass

try:
    with open(s_update, 'r') as file:
        s_html = file.read()
except IOError as e:
    print (e)

a_recipients = ['jjap@domain.com']
    
mail = Email()
for i in a_recipients:
    mail.sendEmail_html(i, s_html)

s_emailMsg = str(a_errorsUpdateOrthdt)
a_recipients = ['jjap@domain.com']
for i in a_recipients:
    mail.sendEmail_html(i, s_emailMsg)
