def consolidateDaysOpenList(d_daysOpenOrth, d_daysOpenGen, d_daysOpenCust):
    ''' function will remove entries in d_daysOpenOrth and d_daysOpenGen
if they appear in d_daysOpenCust and then replace the content in the
respective dictionaries with the content in d_daysOpenCust
'''

    d_daysOpenAll = dict ( list(d_daysOpenGen.items()) +
                           list(d_daysOpenOrth.items()) +
                           list(d_daysOpenCust.items()) )        
    return d_daysOpenAll
