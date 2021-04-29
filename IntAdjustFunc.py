def logline(logfile,logline):
    with open(logfile, 'a+') as f:
        f.write(logline)