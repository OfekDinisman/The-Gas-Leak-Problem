import logging

def CreateLog(fileName):
    # Set up logging
    log = fileName
    logging.basicConfig(filename=log,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    logging.info('Start: %s' % log)