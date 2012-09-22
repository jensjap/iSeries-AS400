import time#, pdb

def getValidDay():
    ''' This function will ask the user for a day to process and validate it '''

    isGood = 0
    while not isGood:
        date = input('Date (mm/dd/yyyy): ')
        try:
            d_validDate = time.strptime(date, '%m/%d/%Y')
            d_validDate
            isGood = 1
            return d_validDate.tm_mon, d_validDate.tm_mday, d_validDate.tm_year
        except ValueError:
            print('Invalid date! Try again')
            isGood = 0
