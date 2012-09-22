import datetime, os

def writeLog(s, logName, timestamp=True):
    """ writes to log file within a folder with today's date
        if timestamp is set to true then each entry inside the log
        will have a time stamp """

    now = datetime.datetime.now()

    folder = "logs/" + now.strftime("%Y-%m-%d")
    if not os.path.exists(folder):
        os.makedirs(folder)
    log = open(folder + "/" + str(logName), 'a')
    if timestamp:
        s = now.strftime("%Y-%m-%d %H:%M:%S = ") + s
        log.write(s + '\n')
    else:
        log.write(s + '\n')
    log.close()
