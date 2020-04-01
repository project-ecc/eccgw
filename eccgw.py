import datetime
import logging
import signal
import codecs
import time
import zmq
import sys
import re

from slickrpc import Proxy

from eccgw_email import sendEmail

################################################################################

def handle(message = ''):

    if re.match('@ .+', message):

        handleEcho(message)

    elif re.match('@\S+ .+', message):

        handleTwitter(message)

    elif re.match('\S+@\S+ .+', message):

        handleEmail(message)

    else:

    	logging.info('No syntax handler found')

################################################################################

def handleEcho(message = ''):

    logging.info('Handle Echo - %s' % message)

################################################################################

def handleTwitter(message = ''):

    logging.info('Handle Twitter - %s' % message)

################################################################################

def handleEmail(message = ''):

    logging.info('Handle Email - %s' % message)

    match = re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', message)

    address = match.group(0)
    content = message[match.end()+1:]

    logging.info('Sending email to %s' % address)

    sendEmail(address, content)

################################################################################

def handleWeb():

    pass

################################################################################

def terminate(signalNumber, frame):

    logging.info('%s received - terminating' % signal.Signals(signalNumber).name)

    sys.exit()

################################################################################
### Main program ###############################################################
################################################################################

def main():

    logging.basicConfig(filename = 'log/{:%Y-%m-%d}.log'.format(datetime.datetime.now()),
						filemode = 'w',
						level    = logging.INFO,
						format   = '%(asctime)s - %(levelname)s : %(message)s',
						datefmt  = '%d/%m/%Y %H:%M:%S')

    logging.info('STARTUP')

    signal.signal(signal.SIGINT,  terminate)  # keyboard interrupt ^C
    signal.signal(signal.SIGTERM, terminate)  # kill [default -15]

    context    = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect('tcp://127.0.0.1:28001')
    subscriber.setsockopt(zmq.SUBSCRIBE, b'')

    eccoin = Proxy('http://%s:%s@127.0.0.1:19119'%('eccoinrpc', 'ecc123-OK-Maybeitneedstobemorecomplex'))

    while True:

        [address, contents] = subscriber.recv_multipart()

        if address.decode() == 'packet':

            protocolID = contents.decode()[1:]

            logging.info('Notification for Protocol ID %s' % protocolID)

            eccbuffer = eccoin.getbuffer(int(protocolID))

            for packet in eccbuffer.values():

                message = codecs.decode(packet, 'hex').decode()

                logging.info('Received message - %s' % message)

                handle(message)

    subscriber.close()
    context.term()

    logging.info('SHUTDOWN')

################################################################################

if __name__ == "__main__":

    main()

################################################################################
