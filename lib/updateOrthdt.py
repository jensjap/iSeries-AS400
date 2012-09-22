import shutil, os.path, time

def updateOrthdt(s_lotusNotesExport, s_orthdt, s_orthdtBKUP):

    a_errors = []
    
    try:
        shutil.copy2 (s_orthdt, s_orthdtBKUP)
    except IOError as e:
        a_errors.append( str(e) )

    try:
        shutil.copy2 (s_lotusNotesExport, s_orthdt)
    except IOError as e:
        a_errors.append( str(e) )

    try:
        f_orthdtAge = ( time.time() - os.path.getmtime(s_orthdt) ) / 3600
        msg = 'orthdt.csv is %0.2f hour(s) old' % (f_orthdtAge)
        if f_orthdtAge > 48:
            a_errors.append('WARNING: ' + msg)
##            input('WARNING: ' + msg + '. Press <enter> to continue')
    except WindowsError as e:
        a_errors.append( str(e) )

    return a_errors
