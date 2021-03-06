import datetime
import logging
import pathlib
import signal
import codecs
import pickle
import time
import zmq
import sys
import re

from slickrpc import Proxy
from slickrpc import exc

from eccgw_email import sendEmail
from eccgw_tweet import sendTweet

import settings

eccoin = Proxy('http://%s:%s@%s'%(settings.rpc_user, settings.rpc_pass, settings.rpc_address))

################################################################################

def handle(protocolID = '', message = ''):

    if (protocolID == '255') and re.match('\S+ \S+', message): 

        handleFaucet(message)

    elif re.match('%.+', message):

        handleEcho(message)

    elif re.match('@\S+ .+', message):

        handleTweet(message)

    elif re.match('\S+@\S+ .+', message):

        handleEmail(message)

    else:

    	logging.info('No syntax handler found')

################################################################################

faucetFileNameAddresses = 'faucet/addresses.dat'
faucetFileNameNodes     = 'faucet/nodes.dat'

faucetAddresses = []
faucetNodes     = []

############################################################

def loadListFile(filePath = ''):

    nullList = []

    if not pathlib.Path(filePath).is_file():

        with open(filePath, 'wb') as f:

            pickle.dump(nullList, f)

            f.close()

            return nullList

    else:

        with open(filePath, 'rb') as f:

            return pickle.load(f)

############################################################

def loadFaucetFiles():

    global faucetAddresses
    global faucetNodes

    faucetAddresses = loadListFile(faucetFileNameAddresses)
    faucetNodes     = loadListFile(faucetFileNameNodes)

############################################################

def saveListFile(list = [], filePath = ''):

    with open(filePath, 'wb') as f:

        pickle.dump(list, f)

        f.close()

############################################################

def saveFaucetFiles():

    saveListFile(faucetAddresses, faucetFileNameAddresses)
    saveListFile(faucetNodes,     faucetFileNameNodes)

################################################################################

def handleFaucet(message = ''):

    logging.info('Handle Faucet - %s' % message)

    match = re.match('E[a-zA-Z0-9]{33}', message)

    # Check 1 - correct syntax

    if not match:

        logging.warning('Handle Faucet - SYNTAX ERROR')

        return

    eccAddress = match.group(0)
    routingTag = message[match.end()+1:]

    logging.info('Faucet visited for address %s by node %s' % (eccAddress, routingTag))

    # Check 2 - valid address syntax (this check could be stronger by checking valid address encoding)

    if (len(eccAddress) != 34) or (eccAddress[0] != 'E'):

        logging.warning('Faucet visited for invalid address syntax %s' % eccAddress)

        return

    # Check 3 - valid routing tag syntax (this check could be stronger by checking valid Base64 encoding)

    if (len(routingTag) != 88) or (routingTag[-1] != '='):

        logging.warning('Faucet visited by node with invalid routing tag syntax %s' % routingTag)

        return

    # Check 4 - current route to node

    try:

        isRoute = eccoin.haveroute(routingTag)

    except exc.RpcInvalidAddressOrKey:

        logging.warning('Faucet visited by node with invalid base64 encoding')

        return

    if not isRoute:

        logging.warning('Faucet visited by node with no current route %s' % routingTag)

        return

    # Check 5 - both node and address have not visited faucet before

    if eccAddress in faucetAddresses:

        logging.warning('Faucet previously visited for address %s' % eccAddress)

        return

    if routingTag in faucetNodes:

        logging.warning('Faucet previously visited by node %s' % routingTag)

        return

    # Check 6 - faucet payout rate limit

    # ***** TODO *****

    balance = eccoin.getbalance()

    # Check 7 - sufficient faucet balance - block and/or flag as appropriate

    if (float(balance) < settings.faucet_threshold):

        logging.warning('Faucet balance %s below threshold %f - payouts blocked' % (balance, settings.faucet_threshold))

        sendTweet('@eccgw', 'ECC Faucet balance %s is below threshold %f - payouts blocked' % (balance, settings.faucet_threshold))

        return

    if (float(balance) < settings.faucet_warning):

        logging.warning('Faucet balance %s starting to get low - please refill' % (balance))

        sendTweet('@eccgw', 'ECC Faucet balance %s is starting to get low - please refill soon' % (balance))

    # All checks passed - process payment

    try:

        txid = eccoin.sendtoaddress(eccAddress, str(settings.faucet_payout), "faucet")

    except exc.RpcWalletUnlockNeeded:

        logging.warning('Wallet unlock required')

    else:

        logging.info('Faucet payout %f sent to %s txid %s' % (settings.faucet_payout, eccAddress, txid))

        sendTweet('@eccgw', 'ECC Faucet payout %f sent to %s txid %s remaining balance %s' % (settings.faucet_payout, eccAddress, txid, balance))
        
        faucetAddresses.append(eccAddress)

        faucetNodes.append(routingTag)

        saveFaucetFiles()

################################################################################

def handleEcho(message = ''):

    logging.info('Handle Echo - %s' % message)

    match = re.match('%[a-zA-Z0-9+/=]{88}', message)

    # Check 1 - correct syntax

    if not match:

        logging.warning('Handle Echo - SYNTAX ERROR')

        return

    routingTag  = match.group(0)[1:]
    content     = message[match.end()+1:]

    # Check 2 - valid routing tag syntax (this check could be stronger by checking valid Base64 encoding)

    if (len(routingTag) != 88) or (routingTag[-1] != '='):

        logging.warning('Echo requested by node with invalid routing tag syntax %s' % routingTag)

        return

    # Check 3 - current route to node

    try:

        isRoute = eccoin.haveroute(routingTag)

    except exc.RpcInvalidAddressOrKey:

        logging.warning('Echo requested by node with invalid base64 encoding')

        return

    if not isRoute:

        logging.warning('Echo requested by node with no current route %s' % routingTag)

        return

    logging.info('Sending echo to %s' % routingTag)

    eccoin.sendpacket(routingTag, 1, 1, content)

################################################################################

def handleTweet(message = ''):

    logging.info('Handle Tweet - %s' % message)

    match = re.match('@[a-zA-Z0-9-_]+', message)

    if not match:

        logging.warning('Handle Tweet - SYNTAX ERROR')

        return

    handle  = match.group(0)
    content = message[match.end()+1:]

    logging.info('Sending tweet to %s' % handle)

    sendTweet(handle, content)

################################################################################

def handleEmail(message = ''):

    logging.info('Handle Email - %s' % message)

    match = re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', message)

    if not match:

        logging.warning('Handle Email - SYNTAX ERROR')

        return

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
						filemode = 'a',
						level    = logging.INFO,
						format   = '%(asctime)s - %(levelname)s : %(message)s',
						datefmt  = '%d/%m/%Y %H:%M:%S')

    logging.info('STARTUP')

    signal.signal(signal.SIGINT,  terminate)  # keyboard interrupt ^C
    signal.signal(signal.SIGTERM, terminate)  # kill [default -15]

    loadFaucetFiles()

    context    = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect('tcp://%s'%settings.zmq_address)
    subscriber.setsockopt(zmq.SUBSCRIBE, b'')

    while True:

        [address, contents] = subscriber.recv_multipart()

        if address.decode() == 'packet':

            protocolID = contents.decode()[1:]

            logging.info('Notification for Protocol ID %s' % protocolID)

            eccbuffer = eccoin.getbuffer(int(protocolID))

            for packet in eccbuffer.values():

                message = codecs.decode(packet, 'hex').decode()

                logging.info('Received message - %s' % message)

                handle(protocolID, message)

    subscriber.close()
    context.term()

    logging.info('SHUTDOWN')

################################################################################

if __name__ == "__main__":

    main()

################################################################################
