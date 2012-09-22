import csv

def getOfficeCodes(s_datafile, b_debug=False):

    d_officeCodes = {}

    try:
        with open (s_datafile) as f1:
            rawReader = csv.reader(f1, delimiter=',')
            for i in rawReader:
                try:
                    officeNbr  = int( i[0][0:3] )
                    officeCode = str( i[0][3:6] )
                    d_officeCodes[officeNbr] = officeCode
                except ValueError as e:
                    if b_debug:
                        print (e)
    except IOError as e:
        print (e)
    return d_officeCodes
